package com.getavares.strava;

import java.util.Scanner;

public class StravaApp {
    public static void main(String[] args) {
        String clientId = System.getenv("STRAVA_CLIENT_ID");
        String clientSecret = System.getenv("STRAVA_CLIENT_SECRET");
        String redirectUri = "http://localhost";

        if (clientId == null || clientSecret == null) {
            System.err.println("❌ Erro: Configure STRAVA_CLIENT_ID e STRAVA_CLIENT_SECRET como variáveis de ambiente.");
            return;
        }

        System.out.println("🚀 Iniciando StravaApp com Client ID: " + clientId);

        StravaService service = new StravaService(clientId, clientSecret, redirectUri);

        String authUrl = service.getAuthorizationUrl();
        System.out.println("Acesse esta URL no navegador:\n" + authUrl);
        System.out.println("\nApós autorizar, copie o código da URL e cole aqui:");

        Scanner scanner = new Scanner(System.in);
        String code = scanner.nextLine().trim();

        String accessToken = service.exchangeCodeForToken(code);
        if (accessToken != null) {
            System.out.println("\n✅ Autenticação bem-sucedida!");
            service.getAthleteInfo(accessToken);
            service.getAthleteActivities(accessToken);
        }
        scanner.close();
    }
}
