package org.example.repository;

import org.example.model.Order;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public class OrderRepository {

    private List<Order> orders = new ArrayList<>();

    public OrderRepository() {
        orders.add(new Order(1, 1, "Laptop", 70000));
        orders.add(new Order(2, 1, "Mouse", 500));
        orders.add(new Order(3, 2, "Keyboard", 1500));
    }

    public List<Order> findAll() {
        return orders;
    }

    public List<Order> findByUserId(int userId) {
        List<Order> result = new ArrayList<>();
        for (Order o : orders) {
            if (o.getUserId() == userId) {
                result.add(o);
            }
        }
        return result;
    }
}
