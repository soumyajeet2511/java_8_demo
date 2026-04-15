package org.example.controller;

import org.example.dto.PaymentDTO;
import org.example.service.PaymentService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin("*")
@RequestMapping("/payments")
public class PaymentController {

    private final PaymentService service;

    public PaymentController(PaymentService service) {
        this.service = service;
    }

    @GetMapping
    public List<PaymentDTO> getAll() {
        return service.getAllPayments();
    }

    @GetMapping("/user/{userId}")
    public List<PaymentDTO> getSuccess(@PathVariable int userId) {
        return service.getSuccessfulPayments(userId);
    }

    @GetMapping("/total/{userId}")
    public double getTotal(@PathVariable int userId) {
        return service.getTotalSuccessAmount(userId);
    }
}
