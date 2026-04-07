package com.example.service;

import org.example.repository.PaymentRepository;
import org.example.service.PaymentService;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PaymentServiceTest {

    private PaymentService service =
            new PaymentService(new PaymentRepository());

    @Test
    void testGetAllPayments() {
        assertFalse(service.getAllPayments().isEmpty());
    }

    @Test
    void testGetSuccessfulPayments() {
        assertTrue(service.getSuccessfulPayments(1).size() > 0);
    }

    @Test
    void testTotalAmount() {
        double total = service.getTotalSuccessAmount(1);
        assertTrue(total > 0);
    }

    @Test
    void testNoPayments() {
        assertEquals(0, service.getTotalSuccessAmount(999));
    }
}