package org.example.util;

import javax.xml.bind.DatatypeConverter;

public class DataTypeUtil {
    public static void main(String[] args) {
        String hex = "4a617661";
        byte[] bytes = DatatypeConverter.parseHexBinary(hex);

        System.out.println(new String(bytes));
    }
}