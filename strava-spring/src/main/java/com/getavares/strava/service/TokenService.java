package com.getavares.strava.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.getavares.strava.exception.TokenRefreshException;
import com.getavares.strava.exception.TokenExpiredException;
import com.getavares.strava.exception.InvalidConfigurationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.File;
import java.io.IOException;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

/**
 * Serviço responsável pelo gerenciamento de tokens OAuth 2.0 da Strava
 * Implementa:
 * - Persistência em arquivo (tokens.json)
 * - Refresh automático de tokens
 * - Validação de expiração
 * - Sincronização segura
 */
@Service
public class TokenService {
    private static final Logger logger = LoggerFactory.getLogger(TokenService.class);
    private static final String TOKENS_FILE = "tokens.json";
    private static final int BUFFER_SECONDS = 300; // Refresh 5 min antes de expirar

    @Value("${strava.client-id}")
    private String clientId;

    @Value("${strava.client-secret}")
    private String clientSecret;

    @Value("${strava.redirect-uri}")
    private String redirectUri;

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public TokenService(RestTemplate restTemplate, ObjectMapper objectMapper) {
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
    }

    /**
     * Salva tokens no arquivo tokens.json
     */
    public void saveTokens(String accessToken, String refreshToken, long expiresAt) {
        try {
            Map<String, Object> tokens = new HashMap<>();
            tokens.put("access_token", accessToken);
            tokens.put("refresh_token", refreshToken);
            tokens.put("expires_at", expiresAt);
            tokens.put("expires_in", expiresAt - System.currentTimeMillis() / 1000);
            tokens.put("token_type", "Bearer");
            tokens.put("saved_at", System.currentTimeMillis() / 1000);

            objectMapper.writeValue(new File(TOKENS_FILE), tokens);
            logger.info("Tokens salvos com sucesso. Expira em: {}", formatExpiration(expiresAt));
        } catch (IOException e) {
            logger.error("Erro ao salvar tokens", e);
            throw new TokenRefreshException("Erro ao salvar tokens", e);
        }
    }

    /**
     * Lê tokens do arquivo tokens.json
     */
    public Map<String, Object> readTokens() {
        try {
            File file = new File(TOKENS_FILE);
            if (!file.exists()) {
                logger.warn("Arquivo tokens.json não encontrado");
                return null;
            }

            return objectMapper.readValue(file, Map.class);
        } catch (IOException e) {
            logger.error("Erro ao ler tokens", e);
            return null;
        }
    }

    /**
     * Obtém o access token, fazendo refresh se necessário
     */
    public String getAccessToken() {
        Map<String, Object> tokens = readTokens();
        if (tokens == null) {
            throw new TokenRefreshException("Nenhum token salvo. Execute autorização primeiro.");
        }

        long expiresAt = ((Number) tokens.get("expires_at")).longValue();
        long nowSeconds = System.currentTimeMillis() / 1000;

        if (isTokenExpired(expiresAt)) {
            logger.info("Token expirado. Fazendo refresh...");
            refreshToken((String) tokens.get("refresh_token"));
            tokens = readTokens();
        }

        return (String) tokens.get("access_token");
    }

    /**
     * Faz refresh do token usando o refresh token
     */
    public void refreshToken(String refreshToken) {
        try {
            Map<String, String> request = new HashMap<>();
            request.put("client_id", clientId);
            request.put("client_secret", clientSecret);
            request.put("grant_type", "refresh_token");
            request.put("refresh_token", refreshToken);

            String url = "https://www.strava.com/oauth/token";
            Map<String, Object> response = restTemplate.postForObject(url, request, Map.class);

            if (response == null || !response.containsKey("access_token")) {
                throw new TokenRefreshException("Resposta inválida do servidor", refreshToken);
            }

            String newAccessToken = (String) response.get("access_token");
            String newRefreshToken = (String) response.getOrDefault("refresh_token", refreshToken);
            long expiresIn = ((Number) response.get("expires_in")).longValue();
            long newExpiresAt = System.currentTimeMillis() / 1000 + expiresIn;

            saveTokens(newAccessToken, newRefreshToken, newExpiresAt);
            logger.info("Token refreshado com sucesso");
        } catch (Exception e) {
            logger.error("Erro ao fazer refresh do token", e);
            throw new TokenRefreshException("Erro ao fazer refresh do token", refreshToken, e);
        }
    }

    /**
     * Valida se o token está expirado
     */
    public boolean isTokenExpired(long expiresAt) {
        long nowSeconds = System.currentTimeMillis() / 1000;
        return expiresAt < (nowSeconds + BUFFER_SECONDS);
    }

    /**
     * Valida se há tokens salvos
     */
    public boolean hasValidToken() {
        Map<String, Object> tokens = readTokens();
        if (tokens == null || !tokens.containsKey("expires_at")) {
            return false;
        }

        long expiresAt = ((Number) tokens.get("expires_at")).longValue();
        return !isTokenExpired(expiresAt);
    }

    /**
     * Retorna informações sobre o token (apenas para debug)
     */
    public Map<String, Object> getTokenInfo() {
        Map<String, Object> tokens = readTokens();
        if (tokens == null) {
            return null;
        }

        Map<String, Object> info = new HashMap<>();
        long expiresAt = ((Number) tokens.get("expires_at")).longValue();
        long nowSeconds = System.currentTimeMillis() / 1000;

        info.put("token_exists", true);
        info.put("is_expired", isTokenExpired(expiresAt));
        info.put("expires_at", expiresAt);
        info.put("expires_in_seconds", Math.max(0, expiresAt - nowSeconds));
        info.put("expires_in_minutes", Math.max(0, (expiresAt - nowSeconds) / 60));
        info.put("saved_at", tokens.get("saved_at"));

        return info;
    }

    /**
     * Limpa os tokens (logout)
     */
    public void clearTokens() {
        try {
            File file = new File(TOKENS_FILE);
            if (file.exists() && file.delete()) {
                logger.info("Tokens removidos com sucesso");
            }
        } catch (Exception e) {
            logger.error("Erro ao limpar tokens", e);
        }
    }

    private String formatExpiration(long expiresAt) {
        long nowSeconds = System.currentTimeMillis() / 1000;
        long diffSeconds = expiresAt - nowSeconds;

        if (diffSeconds < 0) return "EXPIRADO";
        if (diffSeconds < 60) return diffSeconds + " segundos";
        if (diffSeconds < 3600) return (diffSeconds / 60) + " minutos";
        return (diffSeconds / 3600) + " horas";
    }
}
