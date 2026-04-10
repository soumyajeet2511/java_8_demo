package org.example.repository;

import org.example.model.User;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.*;

@Repository
public class UserRepository {

    private List<User> users = new ArrayList<>();

    public UserRepository() {
        users.add(new User(1, "Mike", "test1@gmail.com", LocalDate.now(),""));
        users.add(new User(2, "John", "john@gmail.com", LocalDate.now(),""));
        users.add(new User(3, "Alice", "alice@gmail.com", LocalDate.now(),""));
    }

    public List<User> findAll() {
        return users;
    }

    public Optional<User> findById(int id) {
        for (User u : users) {
            if (u.getId() == id) {
                return Optional.of(u);
            }
        }
        return Optional.empty();
    }

    public void save(User user) {
        users.add(user);
    }
}