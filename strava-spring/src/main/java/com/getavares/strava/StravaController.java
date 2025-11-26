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

    // Simple token store persisted to strava-spring/tokens.json
    private Map<String, Object> tokenStore = loadTokenStore();

    public StravaController() {
        System.out.println("\n\n========================================");
        System.out.println("✅ StravaController LOADED!");
        System.out.println("Endpoints: /, /authorize, /callback, /activities/export");
        System.out.println("========================================\n\n");
    }

    @GetMapping("/")
    public String home() {
        return "Strava API is running! Access /authorize to start OAuth flow.";
    }

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
    tokenStore.put("expires_at", Instant.ofEpochSecond(json.path("expires_at").asLong()).toString());
    saveTokenStore();

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
        // Map to cleaned JSON
        JsonNode arr = mapper.readTree(resp.body());
        // Build cleaned array
        return mapper.writeValueAsString(mapActivities(arr));
    }

    private void saveTokenStore() {
        try {
            mapper.writerWithDefaultPrettyPrinter().writeValue(new java.io.File("strava-spring/tokens.json"), tokenStore);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> loadTokenStore() {
        try {
            java.io.File f = new java.io.File("strava-spring/tokens.json");
            if (f.exists()) {
                return mapper.readValue(f, Map.class);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return new HashMap<>();
    }

    private JsonNode mapActivities(JsonNode arr) {
        // Create a new ArrayNode with cleaned fields
        com.fasterxml.jackson.databind.node.ArrayNode out = mapper.createArrayNode();
        if (arr.isArray()) {
            for (JsonNode a : arr) {
                com.fasterxml.jackson.databind.node.ObjectNode node = mapper.createObjectNode();
                node.put("id", a.path("id").asLong());
                node.put("name", a.path("name").asText(null));
                node.put("type", a.path("type").asText(null));
                node.put("distance", a.path("distance").asDouble(0.0));
                node.put("moving_time", a.path("moving_time").asInt(0));
                node.put("start_date", a.path("start_date").asText(null));
                // start lat/lng
                if (a.has("start_latlng") && a.path("start_latlng").isArray() && a.path("start_latlng").size() >= 2) {
                    node.putArray("start_latlng").add(a.path("start_latlng").get(0).asDouble()).add(a.path("start_latlng").get(1).asDouble());
                }
                out.add(node);
            }
        }
        return out;
    }
}
