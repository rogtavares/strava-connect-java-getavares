package com.getavares.strava;

import com.google.gson.Gson;

public class GsonExample {
    public static void main(String[] args) {
        Gson gson = new Gson();

        // JSON vindo da API Strava
        String json = "{\"firstname\":\"Rogério\",\"lastname\":\"Tavares\"}";

        // Converte JSON em objeto Java
        Athlete athlete = gson.fromJson(json, Athlete.class);
        System.out.println(athlete.firstname); // Rogério

        // Converte objeto Java em JSON
        String novoJson = gson.toJson(athlete);
        System.out.println(novoJson);
    }

    static class Athlete {
        String firstname;
        String lastname;
    }
}
