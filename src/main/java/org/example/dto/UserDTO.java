package org.example.dto;

import java.time.LocalDate;

public class UserDTO {

    private int id;
    private String name;
    private String email;
    private LocalDate createdDate;


    public UserDTO(int id, String name, String email,LocalDate createdDate) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdDate = createdDate;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public String getEmail(){ return email; }
    public LocalDate getCreatedDate(){ return createdDate; }
}