package org.example.util;


public class PriceUtil {

    public static double applyDiscount(double price) {
        if (price > 1000) {
            return price * 0.9;
        }
        return price;
    }
}
