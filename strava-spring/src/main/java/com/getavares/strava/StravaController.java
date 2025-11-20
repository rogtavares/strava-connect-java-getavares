package com.getavares.strava;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

@RestController
public class StravaController {

    private final ObjectMapper mapper = new ObjectMapper();
    private final HttpClient http = HttpClient.newHttpClient();

    // In-memory simple token store (for example purposes)
    private Map<String, Object> tokenStore = new HashMap<>();

    @GetMapping("/authorize")
    public String authorize() {
        String clientId = System.getenv("STRAVA_CLIENT_ID");
        String redirect = System.getenv("STRAVA_REDIRECT_URI");
        String url = String.format("https://www.strava.com/oauth/authorize?client_id=%s&response_type=code&redirect_uri=%s&scope=activity:read_all,profile:read_all&approval_prompt=auto", clientId, redirect);
        return "<html><body><a href=\"" + url + "\">Authorize with Strava</a></body></html>";
    }

    @GetMapping("/callback")
    public String callback(@RequestParam String code) throws IOException, InterruptedException {
        String clientId = System.getenv("STRAVA_CLIENT_ID");
        String clientSecret = System.getenv("STRAVA_CLIENT_SECRET");
        String tokenUrl = "https://www.strava.com/oauth/token";

        String body = String.format("client_id=%s&client_secret=%s&code=%s&grant_type=authorization_code", clientId, clientSecret, code);

        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create(tokenUrl))
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();

        HttpResponse<String> resp = http.send(req, HttpResponse.BodyHandlers.ofString());
        JsonNode json = mapper.readTree(resp.body());
        tokenStore.put("access_token", json.path("access_token").asText());
        tokenStore.put("refresh_token", json.path("refresh_token").asText());
        tokenStore.put("expires_at", Instant.ofEpochSecond(json.path("expires_at").asLong()));

        return "Token armazenado. Você pode acessar /activities/export";
    }

    @GetMapping(value = "/activities/export", produces = MediaType.APPLICATION_JSON_VALUE)
    public String exportActivities() throws IOException, InterruptedException {
        Object token = tokenStore.get("access_token");
        if (token == null) {
            return "{\"error\":\"no_token\"}";
        }

        String url = "https://www.strava.com/api/v3/athlete/activities?per_page=50";
        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Authorization", "Bearer " + token.toString())
                .GET()
                .build();

        HttpResponse<String> resp = http.send(req, HttpResponse.BodyHandlers.ofString());
        // Return raw response for simplicity; in real code map to DTO
        return resp.body();
    }
}
