package com.getavares.strava.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.getavares.strava.exception.StravaAPIException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.*;

/**
 * Serviço de Strava responsável pela lógica de negócio
 * Implementa:
 * - OAuth 2.0 flow (authorize, callback)
 * - Busca de atividades
 * - Enriquecimento com dados adicionais
 * - Tratamento de erros
 */
@Service
public class StravaService {
    private static final Logger logger = LoggerFactory.getLogger(StravaService.class);
    private static final String STRAVA_API_BASE = "https://www.strava.com/api/v3";
    private static final String OAUTH_BASE = "https://www.strava.com/oauth";
    private static final int REQUEST_TIMEOUT_MS = 10000;

    @Value("${strava.client-id}")
    private String clientId;

    @Value("${strava.client-secret}")
    private String clientSecret;

    @Value("${strava.redirect-uri}")
    private String redirectUri;

    private final RestTemplate restTemplate;
    private final TokenService tokenService;
    private final ObjectMapper objectMapper;

    public StravaService(RestTemplate restTemplate, TokenService tokenService, ObjectMapper objectMapper) {
        this.restTemplate = restTemplate;
        this.tokenService = tokenService;
        this.objectMapper = objectMapper;
    }

    /**
     * Retorna a URL de autorização OAuth
     */
    public String getAuthorizationUrl() {
        String scopes = "activity:read_all";
        return String.format(
            "%s/authorize?client_id=%s&response_type=code&redirect_uri=%s&scope=%s&approval_prompt=force",
            OAUTH_BASE, clientId, redirectUri, scopes
        );
    }

    /**
     * Processa o callback OAuth e salva tokens
     */
    public Map<String, Object> exchangeCodeForToken(String code) {
        try {
            logger.info("Trocando authorization code por token...");

            Map<String, String> request = new HashMap<>();
            request.put("client_id", clientId);
            request.put("client_secret", clientSecret);
            request.put("code", code);
            request.put("grant_type", "authorization_code");

            String url = OAUTH_BASE + "/token";
            Map<String, Object> response = restTemplate.postForObject(url, request, Map.class);

            if (response == null || !response.containsKey("access_token")) {
                throw new StravaAPIException("Resposta inválida do servidor OAuth");
            }

            String accessToken = (String) response.get("access_token");
            String refreshToken = (String) response.get("refresh_token");
            long expiresIn = ((Number) response.getOrDefault("expires_in", 3600)).longValue();
            long expiresAt = System.currentTimeMillis() / 1000 + expiresIn;

            tokenService.saveTokens(accessToken, refreshToken, expiresAt);

            logger.info("Token obtido com sucesso. Atleta: {}", response.get("athlete"));
            return response;

        } catch (RestClientException e) {
            logger.error("Erro ao trocar código por token", e);
            throw new StravaAPIException("Erro ao trocar código por token", e);
        }
    }

    /**
     * Busca as atividades do usuário autenticado
     */
    public List<Map<String, Object>> getActivities() {
        try {
            String accessToken = tokenService.getAccessToken();
            logger.info("Buscando atividades com token: {}...", accessToken.substring(0, 20));

            HttpHeaders headers = new HttpHeaders();
            headers.setBearerAuth(accessToken);
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<String> entity = new HttpEntity<>(headers);
            String url = STRAVA_API_BASE + "/athlete/activities?per_page=30&page=1";

            try {
                ResponseEntity<Object[]> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    entity,
                    Object[].class
                );

                if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                    List<Map<String, Object>> activities = new ArrayList<>();
                    for (Object obj : response.getBody()) {
                        if (obj instanceof Map) {
                            activities.add((Map<String, Object>) obj);
                        }
                    }
                    logger.info("Encontradas {} atividades", activities.size());
                    return activities;
                }
            } catch (Exception e) {
                if (e.getMessage() != null && e.getMessage().contains("401")) {
                    logger.warn("Token expirado. Fazendo refresh...");
                    tokenService.refreshToken((String) tokenService.readTokens().get("refresh_token"));
                    return getActivities(); // Retry com novo token
                }
                throw e;
            }

            return new ArrayList<>();

        } catch (RestClientException e) {
            logger.error("Erro ao buscar atividades", e);
            throw new RuntimeException("Erro ao buscar atividades", e);
        } catch (Exception e) {
            logger.error("Erro inesperado ao buscar atividades", e);
            throw new RuntimeException("Erro inesperado ao buscar atividades", e);
        }
    }

    /**
     * Busca os detalhes de uma atividade específica
     */
    public Map<String, Object> getActivity(long activityId) {
        try {
            String accessToken = tokenService.getAccessToken();

            HttpHeaders headers = new HttpHeaders();
            headers.setBearerAuth(accessToken);
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<String> entity = new HttpEntity<>(headers);
            String url = STRAVA_API_BASE + "/activities/" + activityId;

            ResponseEntity<Map> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                entity,
                Map.class
            );

            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("Atividade {} recuperada com sucesso", activityId);
                return response.getBody();
            }

            return new HashMap<>();

        } catch (RestClientException e) {
            logger.error("Erro ao buscar atividade {}", activityId, e);
            throw new RuntimeException("Erro ao buscar atividade " + activityId, e);
        }
    }

    /**
     * Retorna informações do atleta autenticado
     */
    public Map<String, Object> getAthleteInfo() {
        try {
            String accessToken = tokenService.getAccessToken();

            HttpHeaders headers = new HttpHeaders();
            headers.setBearerAuth(accessToken);
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<String> entity = new HttpEntity<>(headers);
            String url = STRAVA_API_BASE + "/athlete";

            ResponseEntity<Map> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                entity,
                Map.class
            );

            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("Informações do atleta recuperadas");
                return response.getBody();
            }

            return new HashMap<>();

        } catch (RestClientException e) {
            logger.error("Erro ao buscar informações do atleta", e);
            throw new StravaAPIException("Erro ao buscar informações do atleta", e);
        }
    }

    /**
     * Verifica se há um token válido
     */
    public boolean isAuthenticated() {
        return tokenService.hasValidToken();
    }

    /**
     * Faz logout (limpa tokens)
     */
    public void logout() {
        tokenService.clearTokens();
        logger.info("Usuário desconectado com sucesso");
    }

    /**
     * Obtém informações sobre o token (debug)
     */
    public Map<String, Object> getTokenInfo() {
        return tokenService.getTokenInfo();
    }
}
