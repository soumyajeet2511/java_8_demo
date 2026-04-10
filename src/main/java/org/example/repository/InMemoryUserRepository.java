package org.example.repository;

import org.example.model.User;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.*;
import org.springframework.web.util.HtmlUtils;

@Repository
public class InMemoryUserRepository {
    private final Map<Long, User> users = new HashMap<>();
    private long idSequence = 1L;

    public List<User> findAll() {
        // Defensive copy, remains mutable for compatibility
        return List.copyOf(users.values());
    }

    public Optional<User> findById(Long id) {
        if (id == null) return Optional.empty();
        return Optional.ofNullable(users.get(id));
    }

    public void save(String name, String email) {
        long id = idSequence++;
        // Sanitize user input to prevent XSS and handle nulls safely
        String safeName = name == null ? "" : HtmlUtils.htmlEscape(name.strip());
        String safeEmail = email == null ? "" : HtmlUtils.htmlEscape(email.strip());
        User user = new User(Math.toIntExact(id), safeName, safeEmail, LocalDate.now(), null);
        users.put(id, user);
    }

    public void deleteById(Long id) {
        users.remove(id);
    }

    public List<User> findRegisteredAfter(LocalDate date) {
        List<User> result = new ArrayList<>();
        for (User user : users.values()) {
            if (user.getRegistrationDate() != null && user.getRegistrationDate().isAfter(date)) {
                result.add(user);
            }
        }
        return result;
    }
}
