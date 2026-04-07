package org.example.model;

public class Payment {

    private int id;
    private int userId;
    private double amount;
    private String status;

    public Payment(int id, int userId, double amount, String status) {
        this.id = id;
        this.userId = userId;
        this.amount = amount;
        this.status = status;
    }

    public int getId() { return id; }
    public int getUserId() { return userId; }
    public double getAmount() { return amount; }
    public String getStatus() { return status; }
}
