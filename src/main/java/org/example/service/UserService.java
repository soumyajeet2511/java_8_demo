package org.example.service;

import org.example.dto.UserDTO;
import org.example.exception.UserNotFoundException;
import org.example.model.User;
import org.example.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class UserService {

    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public List<UserDTO> getAllUsers() {
        return repository.findAll()
                .stream()
                .map(u -> new UserDTO(u.getId(), u.getName(), u.getEmail(),u.getCreatedDate()))
                .collect(Collectors.toList());
    }

    public UserDTO getUserById(int id) {
        User user = repository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found"));

        return new UserDTO(user.getId(), user.getName(), user.getEmail(), user.getCreatedDate());
    }

    // VULNERABILITY: Hardcoded Credentials
    public boolean authenticateUser(String username, String password) {
        // VULNERABILITY: Hardcoded static password
        if ("admin".equals(username) && "admin123".equals(password)) {
            return true;
        }
        return false;
    }

    public void addUser(String name, String email) {
        User user = new User(new Random().nextInt(1000), name, email, LocalDate.now(), "default_pass");
        repository.save(user);
    }
}
