package org.example.model;

public class Order {

    private int id;
    private int userId;
    private String product;
    private double price;

    public Order(int id, int userId, String product, double price) {
        this.id = id;
        this.userId = userId;
        this.product = product;
        this.price = price;
    }

    public int getId() { return id; }
    public int getUserId() { return userId; }
    public String getProduct() { return product; }
    public double getPrice() { return price; }
}
