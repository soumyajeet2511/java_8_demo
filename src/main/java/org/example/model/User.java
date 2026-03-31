package org.example.model;

import java.time.LocalDate;

public class User {

    private int id;
    private String name;
    private LocalDate createdDate;

    public User(int id, String name, LocalDate createdDate) {
        this.id = id;
        this.name = name;
        this.createdDate = createdDate;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public LocalDate getCreatedDate() { return createdDate; }
}