package org.example.model;

import java.time.LocalDate;

public class User {

    private int id;
    private String name;
    private String email;
    private LocalDate createdDate;
    private String password; // Added for vulnerability simulation

    public User(int id, String name, String email, LocalDate createdDate, String password) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdDate = createdDate;
        this.password = password;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public LocalDate getCreatedDate() { return createdDate; }
    public String getPassword() { return password; }

    @Override
    public String toString() {
        // VULNERABILITY: Sensitive Information Leakage
        return "User{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                ", password='" + password + '\'' +
                ", createdDate=" + createdDate +
                '}';
    }
}
