package com.getavares.strava.exception;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Classe para padronizar respostas de erro
 */
public class ErrorResponse {
    private int status;
    private String message;
    private String path;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime timestamp;
    
    private Map<String, String> details;

    public ErrorResponse(int status, String message, String path, LocalDateTime timestamp, Map<String, String> details) {
        this.status = status;
        this.message = message;
        this.path = path;
        this.timestamp = timestamp;
        this.details = details;
    }

    // Getters
    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public Map<String, String> getDetails() {
        return details;
    }

    public void setDetails(Map<String, String> details) {
        this.details = details;
    }
}

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
public class TokenRefreshException extends RuntimeException {
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
public class ActivityFetchException extends RuntimeException {
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
public class TokenExpiredException extends RuntimeException {
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
public class InvalidConfigurationException extends RuntimeException {
    public InvalidConfigurationException(String message) {
        super(message);
    }

    public InvalidConfigurationException(String message, Throwable cause) {
        super(message, cause);
    }
}
