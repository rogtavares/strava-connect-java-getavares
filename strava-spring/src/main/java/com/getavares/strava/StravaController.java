package com.getavares.strava;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jakarta.annotation.PostConstruct;
import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.HashMap;
import java.util.Map;

@RestController
public class StravaController {

    private final ObjectMapper mapper = new ObjectMapper();
    private final HttpClient http = HttpClient.newHttpClient();

    @Value("${strava.client-id}")
    private String clientId;

    @Value("${strava.client-secret}")
    private String clientSecret;

    @Value("${strava.redirect-uri}")
    private String redirectUri;

    private String tokenFilePath = "strava_tokens.json";
    private Map<String, Object> tokenStore;

    @PostConstruct
    public void init() {
        System.out.println("\n\n========================================");
        System.out.println("✅ StravaController INICIANDO...");
        this.tokenStore = loadTokenStore();
        System.out.println("Status do Token: " + (tokenStore.containsKey("access_token") ? "CARREGADO OK" : "NÃO ENCONTRADO"));
        System.out.println("Endpoints Disponíveis:");
        System.out.println(" - GET / (Home)");
        System.out.println(" - GET /authorize (Login)");
        System.out.println(" - GET /athlete (Perfil)");
        System.out.println(" - GET /activities/export (Lista Simples)");
        System.out.println(" - GET /activities/{id} (Detalhes)");
        System.out.println(" - GET /stats/custom (ATIV.GE TAVARES 2025)");
        System.out.println("========================================\n\n");
    }

    @GetMapping("/")
    public String home() {
        return "Strava API is running! Access /authorize to start OAuth flow.";
    }

    @GetMapping("/authorize")
    public String authorize() {
        String url = String.format("https://www.strava.com/oauth/authorize?client_id=%s&response_type=code&redirect_uri=%s&scope=activity:read_all,profile:read_all&approval_prompt=auto", clientId, redirectUri);
        return "<html><body><a href=\"" + url + "\">Authorize with Strava</a></body></html>";
    }

    @GetMapping("/callback")
    public String callback(@RequestParam String code) {
        try {
            String tokenUrl = "https://www.strava.com/oauth/token";
            String body = String.format("client_id=%s&client_secret=%s&code=%s&grant_type=authorization_code", clientId, clientSecret, code);

            HttpRequest req = HttpRequest.newBuilder()
                    .uri(URI.create(tokenUrl))
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .POST(HttpRequest.BodyPublishers.ofString(body))
                    .build();

            HttpResponse<String> resp = http.send(req, HttpResponse.BodyHandlers.ofString());

            if (resp.statusCode() != 200) {
                return "Error exchanging token: " + resp.body();
            }

            JsonNode json = mapper.readTree(resp.body());
            tokenStore.put("access_token", json.path("access_token").asText());
            tokenStore.put("refresh_token", json.path("refresh_token").asText());
            tokenStore.put("expires_at", Instant.ofEpochSecond(json.path("expires_at").asLong()).toString());
            saveTokenStore();

            return "Token armazenado com sucesso! Você pode acessar /activities/export";
        } catch (Exception e) {
            e.printStackTrace();
            return "Error: " + e.getMessage();
        }
    }

    @GetMapping(value = "/activities/export", produces = MediaType.APPLICATION_JSON_VALUE)
    public String exportActivities() {
        return makeStravaRequest("https://www.strava.com/api/v3/athlete/activities?per_page=50", true);
    }

    @GetMapping(value = "/athlete", produces = MediaType.APPLICATION_JSON_VALUE)
    public String getProfile() {
        return makeStravaRequest("https://www.strava.com/api/v3/athlete", false);
    }

    @GetMapping(value = "/activities/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public String getActivityDetail(@PathVariable Long id) {
        return makeStravaRequest("https://www.strava.com/api/v3/activities/" + id, false);
    }

    // --- ATIV.GE TAVARES 2025 (01/08/2025 a 31/12/2026) ---
    @GetMapping(value = "/stats/custom", produces = MediaType.APPLICATION_JSON_VALUE)
    public String getCustomStats() {
        try {
            Object token = tokenStore.get("access_token");
            if (token == null) {
                tokenStore = loadTokenStore();
                token = tokenStore.get("access_token");
                if (token == null) return "{\"error\":\"no_token\"}";
            }

            // Datas em Timestamp (Epoch)
            long startEpoch = LocalDateTime.of(2025, 8, 1, 0, 0).toEpochSecond(ZoneOffset.UTC);
            long endEpoch = LocalDateTime.of(2026, 12, 31, 23, 59).toEpochSecond(ZoneOffset.UTC);

            double totalDistance = 0;
            long totalMovingTime = 0;
            int totalActivities = 0;
            int page = 1;
            boolean keepFetching = true;

            System.out.println(">>> Iniciando cálculo de estatísticas...");

            while (keepFetching) {
                // Busca 200 atividades por página
                String url = String.format("https://www.strava.com/api/v3/athlete/activities?after=%d&before=%d&page=%d&per_page=200",
                                         startEpoch, endEpoch, page);

                HttpRequest req = HttpRequest.newBuilder()
                        .uri(URI.create(url))
                        .header("Authorization", "Bearer " + token.toString())
                        .GET()
                        .build();

                HttpResponse<String> resp = http.send(req, HttpResponse.BodyHandlers.ofString());

                if (resp.statusCode() != 200) {
                    return "{\"error\":\"api_error\", \"status\": " + resp.statusCode() + "}";
                }

                JsonNode activities = mapper.readTree(resp.body());

                if (activities.isArray() && activities.size() > 0) {
                    System.out.println(">>> Página " + page + ": processando " + activities.size() + " atividades.");
                    for (JsonNode a : activities) {
                        totalDistance += a.path("distance").asDouble(0.0);
                        totalMovingTime += a.path("moving_time").asLong(0);
                        totalActivities++;
                    }
                    page++;
                } else {
                    keepFetching = false; // Acabou
                }
            }

            // Monta o JSON de resposta
            ObjectNode stats = mapper.createObjectNode();
            stats.put("titulo", "ATIV.GE TAVARES 2025"); // <--- MUDANÇA AQUI
            stats.put("total_atividades", totalActivities);
            stats.put("distancia_total_km", Math.round(totalDistance / 1000.0 * 100.0) / 100.0);

            long hours = totalMovingTime / 3600;
            long minutes = (totalMovingTime % 3600) / 60;
            stats.put("tempo_total", String.format("%dh %02dm", hours, minutes));

            if (totalActivities > 0) {
                stats.put("media_km_por_atividade", Math.round((totalDistance / 1000.0 / totalActivities) * 100.0) / 100.0);
            }

            return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(stats);

        } catch (Exception e) {
            e.printStackTrace();
            return "{\"error\":\"internal_error\", \"message\": \"" + e.getMessage() + "\"}";
        }
    }

    private String makeStravaRequest(String url, boolean mapList) {
        try {
            Object token = tokenStore.get("access_token");
            if (token == null) {
                tokenStore = loadTokenStore();
                token = tokenStore.get("access_token");
                if (token == null) return "{\"error\":\"no_token\"}";
            }

            HttpRequest req = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Authorization", "Bearer " + token.toString())
                    .GET()
                    .build();

            HttpResponse<String> resp = http.send(req, HttpResponse.BodyHandlers.ofString());

            if (resp.statusCode() != 200) {
                 return "{\"error\":\"api_error\", \"status\": " + resp.statusCode() + ", \"body\": " + mapper.writeValueAsString(resp.body()) + "}";
            }

            if (mapList) {
                JsonNode arr = mapper.readTree(resp.body());
                return mapper.writeValueAsString(mapActivities(arr));
            } else {
                return resp.body();
            }

        } catch (Exception e) {
            e.printStackTrace();
            return "{\"error\":\"internal_error\", \"message\": \"" + e.getMessage() + "\"}";
        }
    }

    private void saveTokenStore() {
        try {
            mapper.writerWithDefaultPrettyPrinter().writeValue(new File(tokenFilePath), tokenStore);
        } catch (IOException e) {
            System.err.println("Failed to save token store: " + e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> loadTokenStore() {
        try {
            File f1 = new File("strava_tokens.json");
            if (f1.exists()) {
                this.tokenFilePath = "strava_tokens.json";
                return mapper.readValue(f1, Map.class);
            }
            File f2 = new File("../strava_tokens.json");
            if (f2.exists()) {
                this.tokenFilePath = "../strava_tokens.json";
                return mapper.readValue(f2, Map.class);
            }
        } catch (IOException e) {
            System.err.println("Erro ao ler arquivo de token: " + e.getMessage());
        }
        return new HashMap<>();
    }

    private JsonNode mapActivities(JsonNode arr) {
        ArrayNode out = mapper.createArrayNode();
        if (arr.isArray()) {
            for (JsonNode a : arr) {
                ObjectNode node = mapper.createObjectNode();
                node.put("id", a.path("id").asLong());
                node.put("name", a.path("name").asText(null));
                node.put("type", a.path("type").asText(null));
                node.put("distance", a.path("distance").asDouble(0.0));
                node.put("moving_time", a.path("moving_time").asInt(0));
                node.put("start_date", a.path("start_date").asText(null));
                if (a.has("start_latlng") && a.path("start_latlng").isArray() && a.path("start_latlng").size() >= 2) {
                    node.putArray("start_latlng").add(a.path("start_latlng").get(0).asDouble()).add(a.path("start_latlng").get(1).asDouble());
                }
                out.add(node);
            }
        }
        return out;
    }
}
