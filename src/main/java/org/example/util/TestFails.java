package org.example.util;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import sun.misc.BASE64Encoder;

@Configuration
public class TestFails {

    @Bean
    public static void main(String[] args) {
        BASE64Encoder encoder = new BASE64Encoder();
        String encoded = encoder.encode("hello".getBytes());
        System.out.println("Base64: " + encoded);
    }
}