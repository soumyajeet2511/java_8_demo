package org.example.dto;


public class OrderDTO {
    private int id;
    private String product;

    public OrderDTO(int id, String product) {
        this.id = id;
        this.product = product;
    }

    public int getId() { return id; }
    public String getProduct() { return product; }
}