package com.getavares.strava.exception;

/**
 * Exceção customizada para erros da API Strava
 * Lançada quando a API Strava retorna erro ou está indisponível
 */
public class StravaAPIException extends RuntimeException {
    private final int statusCode;
    private final String apiResponse;

    public StravaAPIException(String message) {
        super(message);
        this.statusCode = 0;
        this.apiResponse = null;
    }

    public StravaAPIException(String message, Throwable cause) {
        super(message, cause);
        this.statusCode = 0;
        this.apiResponse = null;
    }

    public StravaAPIException(String message, int statusCode, String apiResponse) {
        super(message);
        this.statusCode = statusCode;
        this.apiResponse = apiResponse;
    }

    public StravaAPIException(String message, int statusCode, String apiResponse, Throwable cause) {
        super(message, cause);
        this.statusCode = statusCode;
        this.apiResponse = apiResponse;
    }

    public int getStatusCode() {
        return statusCode;
    }

    public String getApiResponse() {
        return apiResponse;
    }
}

/**
 * Exceção customizada para erros de refresh de token
 * Lançada quando não é possível refazer o refresh do token OAuth
 */
class TokenRefreshException extends RuntimeException {
    private final String refreshToken;

    public TokenRefreshException(String message) {
        super(message);
        this.refreshToken = null;
    }

    public TokenRefreshException(String message, Throwable cause) {
        super(message, cause);
        this.refreshToken = null;
    }

    public TokenRefreshException(String message, String refreshToken) {
        super(message);
        this.refreshToken = refreshToken;
    }

    public TokenRefreshException(String message, String refreshToken, Throwable cause) {
        super(message, cause);
        this.refreshToken = refreshToken;
    }

    public String getRefreshToken() {
        return refreshToken;
    }
}

/**
 * Exceção customizada para erros ao buscar atividades
 * Lançada quando há problema ao recuperar atividades da API Strava
 */
class ActivityFetchException extends RuntimeException {
    private final long athleteId;

    public ActivityFetchException(String message) {
        super(message);
        this.athleteId = 0;
    }

    public ActivityFetchException(String message, Throwable cause) {
        super(message, cause);
        this.athleteId = 0;
    }

    public ActivityFetchException(String message, long athleteId) {
        super(message);
        this.athleteId = athleteId;
    }

    public ActivityFetchException(String message, long athleteId, Throwable cause) {
        super(message, cause);
        this.athleteId = athleteId;
    }

    public long getAthleteId() {
        return athleteId;
    }
}

/**
 * Exceção para quando token está expirado
 */
class TokenExpiredException extends RuntimeException {
    private final long expiresAt;

    public TokenExpiredException(String message, long expiresAt) {
        super(message);
        this.expiresAt = expiresAt;
    }

    public long getExpiresAt() {
        return expiresAt;
    }
}

/**
 * Exceção para configuração inválida
 */
class InvalidConfigurationException extends RuntimeException {
    public InvalidConfigurationException(String message) {
        super(message);
    }

    public InvalidConfigurationException(String message, Throwable cause) {
        super(message, cause);
    }
}
