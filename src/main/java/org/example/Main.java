package org.example;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.text.SimpleDateFormat;
import java.util.*;

@SpringBootApplication
public class Main {

    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
        List<String> users = Arrays.asList("Alice", "Bob", "Charlie");

        // Old loop
        for (String user : users) {
            System.out.println(user);
        }

        //cause of nullPointerException
        String s = null;
        System.out.println(s.length());

        String str = "   ";
        if (str.trim().isEmpty()) { //JAVA 8
            System.out.println("String is empty");
        }

        // Date handling (old API)
        Date date = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        String formattedDate = sdf.format(date);
        System.out.println("Date: " + formattedDate);

        // Optional usage (not used properly)
        Optional<String> optional = Optional.ofNullable(getUser());
        if (optional.isPresent()) {
            System.out.println(optional.get());
        }

        // Stream usage (can be improved)
        List<String> filtered = new ArrayList<>();
        for (String user : users) {
            if (user.startsWith("A")) {
                filtered.add(user);
            }
        }
        System.out.println(filtered);
    }

    public static String getUser() {
        return null;
    }
}