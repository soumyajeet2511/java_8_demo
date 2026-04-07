package org.example.repository;

import org.example.model.Payment;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public class PaymentRepository {

    private List<Payment> payments = new ArrayList<>();

    public PaymentRepository() {
        payments.add(new Payment(1, 1, 1000, "SUCCESS"));
        payments.add(new Payment(2, 1, 500, "FAILED"));
        payments.add(new Payment(3, 2, 2000, "SUCCESS"));
    }

    public List<Payment> findAll() {
        return payments;
    }

    public List<Payment> findByUserId(int userId) {
        List<Payment> result = new ArrayList<>();
        for (Payment p : payments) {
            if (p.getUserId() == userId) {
                result.add(p);
            }
        }
        return result;
    }
}
