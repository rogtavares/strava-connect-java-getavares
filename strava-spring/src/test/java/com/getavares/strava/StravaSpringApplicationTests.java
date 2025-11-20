package com.getavares.strava;

import com.getavares.strava.service.TokenService;
import com.getavares.strava.service.StravaService;
import com.getavares.strava.exception.TokenRefreshException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Testes unitários para a aplicação Strava Spring
 * Cobre casos básicos de TokenService e StravaService
 */
@ExtendWith(SpringExtension.class)
@SpringBootTest
@DisplayName("Strava Spring Application Tests")
class StravaSpringApplicationTests {

    @MockBean
    private RestTemplate restTemplate;

    @Autowired
    private TokenService tokenService;

    @Autowired
    private StravaService stravaService;

    @BeforeEach
    void setUp() {
        // Setup do ambiente de teste
    }

    // ============================================================================
    // TESTES DE TOKENSERVICE
    // ============================================================================

    @Test
    @DisplayName("Should check if token is expired")
    void testIsTokenExpired() {
        // Token que expirou há 1 hora
        long expiredTime = System.currentTimeMillis() / 1000 - 3600;
        assertTrue(tokenService.isTokenExpired(expiredTime));

        // Token que expira em 1 hora
        long futureTime = System.currentTimeMillis() / 1000 + 3600;
        assertFalse(tokenService.isTokenExpired(futureTime));
    }

    @Test
    @DisplayName("Should detect no valid token when file does not exist")
    void testHasValidTokenWhenNoFile() {
        assertFalse(tokenService.hasValidToken());
    }

    @Test
    @DisplayName("Should throw exception when trying to refresh token without tokens")
    void testRefreshTokenWithoutSavedTokens() {
        assertThrows(TokenRefreshException.class, () -> {
            tokenService.getAccessToken();
        });
    }

    @Test
    @DisplayName("Should return authorization URL")
    void testGetAuthorizationUrl() {
        String authUrl = stravaService.getAuthorizationUrl();
        assertNotNull(authUrl);
        assertTrue(authUrl.contains("oauth/authorize"));
        assertTrue(authUrl.contains("client_id="));
        assertTrue(authUrl.contains("redirect_uri="));
    }

    // ============================================================================
    // TESTES DE STRAVASERVICE
    // ============================================================================

    @Test
    @DisplayName("Should correctly format authorization URL with proper parameters")
    void testAuthorizationUrlFormat() {
        String authUrl = stravaService.getAuthorizationUrl();
        
        assertTrue(authUrl.contains("client_id="));
        assertTrue(authUrl.contains("response_type=code"));
        assertTrue(authUrl.contains("scope=activity:read_all"));
        assertTrue(authUrl.contains("redirect_uri="));
        assertTrue(authUrl.contains("approval_prompt=force"));
    }

    @Test
    @DisplayName("Should indicate user is not authenticated when no token saved")
    void testIsAuthenticatedWhenNoToken() {
        assertFalse(stravaService.isAuthenticated());
    }

    // ============================================================================
    // TESTES DE INTEGRAÇÃO
    // ============================================================================

    @Test
    @DisplayName("Should have proper beans configured")
    void testBeansConfiguration() {
        assertNotNull(tokenService);
        assertNotNull(stravaService);
        assertNotNull(restTemplate);
    }

    // ============================================================================
    // TESTES DE LÓGICA DE NEGÓCIO
    // ============================================================================

    @Test
    @DisplayName("Should handle token expiration gracefully")
    void testTokenExpirationHandling() {
        // Token que expirou
        long expiredTime = System.currentTimeMillis() / 1000 - 100;
        assertTrue(tokenService.isTokenExpired(expiredTime));

        // Token no buffer (vai expirar em menos de 5 min)
        long bufferTime = System.currentTimeMillis() / 1000 + 100; // +100 seg = < 5 min
        assertTrue(tokenService.isTokenExpired(bufferTime));

        // Token válido por muito tempo
        long validTime = System.currentTimeMillis() / 1000 + 10000; // +10000 seg
        assertFalse(tokenService.isTokenExpired(validTime));
    }

    // ============================================================================
    // TESTS PARA ERRO HANDLING
    // ============================================================================

    @Test
    @DisplayName("Should throw proper exception on token refresh failure")
    void testTokenRefreshExceptionHandling() {
        // TokenService deve lançar TokenRefreshException quando não há token salvo
        assertThrows(
            TokenRefreshException.class,
            () -> tokenService.getAccessToken(),
            "Should throw TokenRefreshException when no tokens are saved"
        );
    }

    @Test
    @DisplayName("Should have proper exception message on token refresh failure")
    void testTokenRefreshExceptionMessage() {
        TokenRefreshException ex = assertThrows(TokenRefreshException.class, () -> {
            tokenService.getAccessToken();
        });

        assertNotNull(ex.getMessage());
        assertTrue(ex.getMessage().length() > 0);
    }

    // ============================================================================
    // SMOKE TESTS
    // ============================================================================

    @Test
    @DisplayName("Application context should load successfully")
    void contextLoads() {
        // Simples test para confirmar que o contexto carrega sem erros
        assertNotNull(stravaService);
        assertNotNull(tokenService);
    }
}
