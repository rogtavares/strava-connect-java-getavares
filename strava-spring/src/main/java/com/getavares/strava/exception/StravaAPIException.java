package com.getavares.strava.exception;

/**
 * Exceção para erros da API Strava
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

    public int getStatusCode() {
        return statusCode;
    }

    public String getApiResponse() {
        return apiResponse;
    }
}
