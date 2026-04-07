package org.example.controller;


import org.example.dto.OrderDTO;
import org.example.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    @Autowired
    private OrderService service;

    @GetMapping
    public List<OrderDTO> getAll() {
        return service.getAllOrders();
    }

    @GetMapping("/user/{userId}")
    public List<OrderDTO> getByUser(@PathVariable int userId) {
        return service.getOrdersByUser(userId);
    }
}
