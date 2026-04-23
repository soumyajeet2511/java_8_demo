# Dependency and Plugin Rules for Java 11

## 1. Maven Properties
- Ensure the following properties are set to 11:
  ```xml
  <maven.compiler.source>11</maven.compiler.source>
  <maven.compiler.target>11</maven.compiler.target>
  ```
  Or using the newer release property:
  ```xml
  <maven.compiler.release>11</maven.compiler.release>
  ```

## 2. Essential Plugin Upgrades
- **maven-compiler-plugin**: Minimum version `3.8.0` for Java 11 support.
- **maven-surefire-plugin**: Minimum version `2.22.0` or `3.0.0-M3+`.
- **maven-javadoc-plugin**: Minimum version `3.0.1`.

## 3. Replacements for Removed JDK Modules
If the code uses these APIs, add the following dependencies:

### JAXB (Java Architecture for XML Binding)
```xml
<dependency>
    <groupId>javax.xml.bind</groupId>
    <artifactId>jaxb-api</artifactId>
    <version>2.3.1</version>
</dependency>
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>2.3.1</version>
</dependency>
```

### JAF (JavaBeans Activation Framework)
```xml
<dependency>
    <groupId>javax.activation</groupId>
    <artifactId>javax.activation-api</artifactId>
    <version>1.2.0</version>
</dependency>
```

### Common Annotations
```xml
<dependency>
    <groupId>javax.annotation</groupId>
    <artifactId>javax.annotation-api</artifactId>
    <version>1.3.2</version>
</dependency>
```

## 4. Lombok and Bytecode Manipulators
- **Lombok**: Upgrade to at least `1.18.4`.
- **ASM**: Upgrade to at least `7.0`.
- **Mockito**: Upgrade to `2.23.0` or higher.
