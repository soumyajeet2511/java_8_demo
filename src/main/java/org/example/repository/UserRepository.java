package org.example.repository;

import org.example.model.User;
import org.springframework.stereotype.Repository;
import org.springframework.web.util.HtmlUtils;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Repository
public class UserRepository {

    private final List<User> users = new ArrayList<>();

    public UserRepository() {
        users.add(new User(1, "Mike", "test1@gmail.com", LocalDate.now(), ""));
        users.add(new User(2, "John", "john@gmail.com", LocalDate.now(), ""));
        users.add(new User(3, "Alice", "alice@gmail.com", LocalDate.now(), ""));
        // Ensure no passwords are stored in memory
    }

    public List<User> findAll() {
        // Return a defensive copy to prevent external modification
        // Remove password field from returned users
        return users.stream()
                .map(user -> new User(
                        user.getId(),
                        user.getName(),
                        user.getEmail(),
                        user.getRegistrationDate() != null ? user.getRegistrationDate() : LocalDate.now(),
                        "" // Do not expose password
                ))
                .collect(Collectors.toList());
    }

    public Optional<User> findById(int id) {
        // Defensive: do not expose password in returned User
        return users.stream()
                .filter(u -> u.getId() == id)
                .findFirst()
                .map(user -> new User(
                        user.getId(),
                        user.getName(),
                        user.getEmail(),
                        user.getRegistrationDate() != null ? user.getRegistrationDate() : LocalDate.now(), // Use actual registration date
                        "" // Do not expose password
                ));
    }

    public void save(User user) {
        // Prevent duplicate users by ID
        if (users.stream().anyMatch(u -> u.getId() == user.getId())) {
            throw new IllegalArgumentException("User with this ID already exists.");
        }
        // Sanitize email to prevent XSS
        String sanitizedEmail = HtmlUtils.htmlEscape(
                user.getEmail() == null || user.getEmail().isBlank() ? "" : user.getEmail().strip()
        );
        // Remove password from being stored in memory for security
        LocalDate registrationDate = user.getRegistrationDate() != null ? user.getRegistrationDate() : LocalDate.now();
        // Do not persist password in memory (set to empty string)
        User sanitizedUser = new User(
                user.getId(),
                user.getName(),
                sanitizedEmail,
                registrationDate,
                ""
        );
        users.add(sanitizedUser);
    }
}
