package org.example.model;

import java.time.LocalDate;

public class User {

    private int id;
    private String name;
    private String email;
    private LocalDate createdDate;

    public User(int id, String name, String email, LocalDate createdDate) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdDate = createdDate;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public LocalDate getCreatedDate() { return createdDate; }
}