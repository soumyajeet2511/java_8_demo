package com.example.service;

import org.example.dto.OrderDTO;
import org.example.repository.OrderRepository;
import org.example.service.OrderService;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class OrderServiceTest {

    private OrderRepository repository = new OrderRepository();
    private OrderService service = new OrderService(repository);

    @Test
    void testGetAllOrders() {
        List<OrderDTO> orders = service.getAllOrders();

        assertNotNull(orders);
        assertFalse(orders.isEmpty());
    }

    @Test
    void testGetOrdersByUser() {
        List<OrderDTO> orders = service.getOrdersByUser(1);

        assertNotNull(orders);
        assertTrue(orders.size() > 0);
    }

    @Test
    void testGetOrdersByUser_NoOrders() {
        List<OrderDTO> orders = service.getOrdersByUser(999);

        assertNotNull(orders);
        assertTrue(orders.isEmpty());
    }
}
