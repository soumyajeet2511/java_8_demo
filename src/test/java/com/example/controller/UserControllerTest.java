package com.example.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(
        webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
        classes = org.example.Main.class
)
public class UserControllerTest {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void testGetAllUsers() {
        String response = restTemplate.getForObject(
                "http://localhost:" + port + "/users",
                String.class
        );

        assertNotNull(response);
        assertTrue(response.contains("Mike"));
    }

    @Test
    void testGetUserById() {
        String response = restTemplate.getForObject(
                "http://localhost:" + port + "/users/1",
                String.class
        );

        assertNotNull(response);
        assertTrue(response.contains("Mike"));
    }

    @Test
    void testAddUser() {
        String response = restTemplate.postForObject(
                "http://localhost:" + port + "/users?name=Test&email=test@mail.com",
                null,
                String.class
        );

        assertEquals("User added", response);
    }
}
