package com.getavares.strava;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.io.entity.StringEntity;

public class StravaService {
    private final String clientId;
    private final String clientSecret;
    private final String redirectUri;
    private final Gson gson = new Gson();

    public StravaService(String clientId, String clientSecret, String redirectUri) {
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.redirectUri = redirectUri;
    }

    public String getAuthorizationUrl() {
        return String.format("https://www.strava.com/oauth/authorize?client_id=%s&response_type=code&redirect_uri=%s&scope=read,activity:read_all",
                clientId, redirectUri);
    }

    public String exchangeCodeForToken(String code) {
        try (CloseableHttpClient client = HttpClients.createDefault()) {
            HttpPost post = new HttpPost("https://www.strava.com/oauth/token");
            String json = String.format("{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"code\":\"%s\",\"grant_type\":\"authorization_code\"}",
                    clientId, clientSecret, code);
            post.setEntity(new StringEntity(json));
            post.setHeader("Content-Type", "application/json");

            try (CloseableHttpResponse response = client.execute(post)) {
                String body = EntityUtils.toString(response.getEntity());
                JsonObject obj = gson.fromJson(body, JsonObject.class);
                return obj.get("access_token").getAsString();
            }
        } catch (Exception e) {
            System.err.println("Erro ao trocar código por token: " + e.getMessage());
            return null;
        }
    }

    public void getAthleteInfo(String accessToken) {
        try (CloseableHttpClient client = HttpClients.createDefault()) {
            HttpGet get = new HttpGet("https://www.strava.com/api/v3/athlete");
            get.setHeader("Authorization", "Bearer " + accessToken);

            try (CloseableHttpResponse response = client.execute(get)) {
                String body = EntityUtils.toString(response.getEntity());
                System.out.println("\n📊 Informações do Atleta:\n" + body);
            }
        } catch (Exception e) {
            System.err.println("Erro ao buscar informações do atleta: " + e.getMessage());
        }
    }

    public void getAthleteActivities(String accessToken) {
        try (CloseableHttpClient client = HttpClients.createDefault()) {
            HttpGet get = new HttpGet("https://www.strava.com/api/v3/athlete/activities?per_page=5");
            get.setHeader("Authorization", "Bearer " + accessToken);

            try (CloseableHttpResponse response = client.execute(get)) {
                String body = EntityUtils.toString(response.getEntity());
                System.out.println("\n🏃 Atividades Recentes:\n" + body);
            }
        } catch (Exception e) {
            System.err.println("Erro ao buscar atividades: " + e.getMessage());
        }
    }
}
