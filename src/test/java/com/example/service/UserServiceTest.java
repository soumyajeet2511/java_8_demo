package com.example.service;

import org.example.dto.UserDTO;
import org.example.repository.UserRepository;
import org.example.service.UserService;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class UserServiceTest {

    private UserRepository repository = new UserRepository();
    private UserService service = new UserService(repository);


    @Test
    void testGetAllUsers() {
        List<UserDTO> users = service.getAllUsers();

        assertNotNull(users);
        assertFalse(users.isEmpty());
    }

    @Test
    void testGetUserById_Valid() {
        UserDTO user = service.getUserById(1);

        assertNotNull(user);
        assertEquals(1, user.getId());
    }

    @Test
    void testGetUserById_Invalid() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            service.getUserById(999);
        });

        assertTrue(ex.getMessage().contains("User not found"));
    }

    @Test
    void testAddUser() {
        service.addUser("TestUser", "test@mail.com");

        List<UserDTO> users = service.getAllUsers();
        assertTrue(users.size() >= 1);
    }
}
