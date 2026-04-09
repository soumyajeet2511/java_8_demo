package org.example.service;

import org.springframework.stereotype.Service;
import org.springframework.web.util.HtmlUtils;

@Service
public class VulnerableService {

    // These methods are added for testing the AI migration agent's ability to detect and fix common issues.

    // 4. Null Pointer Risk
    public int getLength(String input) {
        if (input == null) {
            return 0;
        }
        return input.length();
    }
 
    // 5. Sensitive Data Exposure in Logs
    public void logUser(String username, String password) {
        // Do not log sensitive information such as passwords
        System.out.println("User: " + HtmlUtils.htmlEscape(username) + " logged in.");
        // Password is intentionally not logged for security reasons
    }
 
    // 6. Weak Validation
    public boolean isValidEmail(String email) {
        if (email == null || email.isBlank()) {
            return false;
        }
        // Improved email validation using regex
        // Note: This regex is basic and does not cover all valid emails per RFC 5322
        // Sanitize email input to prevent XSS
        String sanitizedEmail = HtmlUtils.htmlEscape(email);
        return sanitizedEmail.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");
    }
 
    // 7. Exception Leakage
    public String process() {
        try {
            int a = 10 / 0;
            return "Success";
        } catch (Exception e) {
            // Do not expose internal error messages
            // Optionally log the exception internally for diagnostics
            // Logger can be used here in production code
            return "An internal error occurred.";
        }
    }
}
