package org.example.service;

import org.example.dto.OrderDTO;
import org.example.repository.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class OrderService {

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }


    public List<OrderDTO> getAllOrders() {
        return repository.findAll()
                .stream()
                .map(o -> new OrderDTO(o.getId(), o.getProduct()))
                .collect(Collectors.toList());
    }

    public List<OrderDTO> getOrdersByUser(int userId) {
        return repository.findByUserId(userId)
                .stream()
                .map(o -> new OrderDTO(o.getId(), o.getProduct()))
                .collect(Collectors.toList());
    }
}
