package org.example.repository;

import org.example.model.User;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class UserRepository {

    private List<User> users = new ArrayList<>();

    public UserRepository() {
        users.add(new User(1, "Java", LocalDate.now()));
        users.add(new User(2, "Spring", LocalDate.now().minusDays(1)));
    }

    public List<User> findAll() {
        return users;
    }

    public Optional<User> findById(int id) {
        for (User user : users) {   // Java 8 style loop (migration candidate)
            if (user.getId() == id) {
                return Optional.of(user);
            }
        }
        return Optional.empty();
    }

    public void save(User user) {
        users.add(user);
    }
}