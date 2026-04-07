package org.example.service;

import org.example.dto.PaymentDTO;
import org.example.model.Payment;
import org.example.repository.PaymentRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class PaymentService {

    private final PaymentRepository repository;

    public PaymentService(PaymentRepository repository) {
        this.repository = repository;
    }

    public List<PaymentDTO> getAllPayments() {
        return repository.findAll()
                .stream()
                .map(p -> new PaymentDTO(p.getId(), p.getAmount(), p.getStatus()))
                .collect(Collectors.toList());
    }

    public List<PaymentDTO> getSuccessfulPayments(int userId) {
        return repository.findByUserId(userId)
                .stream()
                .filter(p -> "SUCCESS".equals(p.getStatus()))
                .map(p -> new PaymentDTO(p.getId(), p.getAmount(), p.getStatus()))
                .collect(Collectors.toList());
    }

    public double getTotalSuccessAmount(int userId) {
        return repository.findByUserId(userId)
                .stream()
                .filter(p -> "SUCCESS".equals(p.getStatus()))
                .mapToDouble(Payment::getAmount)
                .sum();
    }
}
