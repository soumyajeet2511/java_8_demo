package org.example.util;

import sun.misc.BASE64Encoder;

public class TestFails {

    public static void main(String[] args) {
        BASE64Encoder encoder = new BASE64Encoder();
        String encoded = encoder.encode("hello".getBytes());
        System.out.println("Base64: " + encoded);
    }
}