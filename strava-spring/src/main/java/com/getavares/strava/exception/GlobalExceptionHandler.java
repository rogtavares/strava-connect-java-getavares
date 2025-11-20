package com.getavares.strava.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Gerenciador centralizado de exceções para toda a aplicação
 * Implementa tratamento consistente de erros com respostas padronizadas
 */
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * Trata exceções de validação (MethodArgumentNotValidException)
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationExceptions(
            MethodArgumentNotValidException ex, WebRequest request) {

        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });

        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.BAD_REQUEST.value(),
            "Erro de validação",
            request.getDescription(false).replace("uri=", ""),
            LocalDateTime.now(),
            errors
        );

        logger.warn("Erro de validação: {}", errors);
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    /**
     * Trata exceções específicas da API Strava
     */
    @ExceptionHandler(StravaAPIException.class)
    public ResponseEntity<ErrorResponse> handleStravaAPIException(
            StravaAPIException ex, WebRequest request) {

        Map<String, String> details = new HashMap<>();
        details.put("error", ex.getMessage());
        if (ex.getStatusCode() > 0) {
            details.put("status_code", String.valueOf(ex.getStatusCode()));
        }
        if (ex.getApiResponse() != null) {
            details.put("api_response", ex.getApiResponse());
        }

        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.BAD_GATEWAY.value(),
            "Erro na API Strava",
            request.getDescription(false).replace("uri=", ""),
            LocalDateTime.now(),
            details
        );

        logger.error("Erro Strava API: {}", ex.getMessage(), ex);
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_GATEWAY);
    }

    /**
     * Trata exceções de refresh de token
     */
    @ExceptionHandler(TokenRefreshException.class)
    public ResponseEntity<ErrorResponse> handleTokenRefreshException(
            TokenRefreshException ex, WebRequest request) {

        Map<String, String> details = new HashMap<>();
        details.put("error", ex.getMessage());
        if (ex.getRefreshToken() != null) {
            details.put("refresh_token", "***" + ex.getRefreshToken().substring(Math.max(0, ex.getRefreshToken().length() - 4)));
        }

        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.UNAUTHORIZED.value(),
            "Erro ao fazer refresh do token",
            request.getDescription(false).replace("uri=", ""),
            LocalDateTime.now(),
            details
        );

        logger.error("Erro de refresh de token: {}", ex.getMessage(), ex);
        return new ResponseEntity<>(errorResponse, HttpStatus.UNAUTHORIZED);
    }

    /**
     * Trata exceções ao buscar atividades
     */
    @ExceptionHandler(ActivityFetchException.class)
    public ResponseEntity<ErrorResponse> handleActivityFetchException(
            ActivityFetchException ex, WebRequest request) {

        Map<String, String> details = new HashMap<>();
        details.put("error", ex.getMessage());
        if (ex.getAthleteId() > 0) {
            details.put("athlete_id", String.valueOf(ex.getAthleteId()));
        }

        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "Erro ao buscar atividades",
            request.getDescription(false).replace("uri=", ""),
            LocalDateTime.now(),
            details
        );

        logger.error("Erro ao buscar atividades: {}", ex.getMessage(), ex);
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    /**
     * Trata exceções de token expirado
     */
    @ExceptionHandler(TokenExpiredException.class)
    public ResponseEntity<ErrorResponse> handleTokenExpiredException(
            TokenExpiredException ex, WebRequest request) {

        Map<String, String> details = new HashMap<>();
        details.put("error", ex.getMessage());
        details.put("expires_at", String.valueOf(ex.getExpiresAt()));

        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.UNAUTHORIZED.value(),
            "Token expirado",
            request.getDescription(false).replace("uri=", ""),
            LocalDateTime.now(),
            details
        );

        logger.warn("Token expirado: {}", ex.getMessage());
        return new ResponseEntity<>(errorResponse, HttpStatus.UNAUTHORIZED);
    }

    /**
     * Trata exceções de configuração inválida
     */
    @ExceptionHandler(InvalidConfigurationException.class)
    public ResponseEntity<ErrorResponse> handleInvalidConfigurationException(
            InvalidConfigurationException ex, WebRequest request) {

        Map<String, String> details = new HashMap<>();
        details.put("error", ex.getMessage());

        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "Configuração inválida",
            request.getDescription(false).replace("uri=", ""),
            LocalDateTime.now(),
            details
        );

        logger.error("Erro de configuração: {}", ex.getMessage(), ex);
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    /**
     * Trata todas as outras exceções não mapeadas
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGlobalException(
            Exception ex, WebRequest request) {

        Map<String, String> details = new HashMap<>();
        details.put("error", ex.getMessage());
        details.put("exception_type", ex.getClass().getSimpleName());

        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "Erro interno do servidor",
            request.getDescription(false).replace("uri=", ""),
            LocalDateTime.now(),
            details
        );

        logger.error("Erro não tratado:", ex);
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
