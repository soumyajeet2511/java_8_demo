name: java-modernization
description: Apply safe Java 11–21 code improvements without changing behavior.
dependencies:
- global-restrictions

---

# Java Modernization Skill

## Purpose
Enhance code using modern Java features after compatibility migration.

---

## Target
Java 21

---

## Allowed Improvements (SAFE ONLY)

### 1. String Improvements
- trim().isEmpty() → isBlank()
- str != null && !str.isEmpty() → !str.isBlank() (ONLY if null-safety remains unchanged)

---

### 2. Collections

- Arrays.asList(...) → List.of(...)  
  (ONLY if list is NOT modified later)

- new ArrayList<>(Arrays.asList(...)) → new ArrayList<>(List.of(...))

- Collections.emptyList() → List.of()
- Collections.emptyMap() → Map.of()

---

### 3. Map Improvements

- new HashMap<>() + simple put(...) initialization  
  → Map.of(...) (ONLY for small fixed maps)

---

### 4. Optional Improvements

- Optional.ofNullable(x).isPresent() → !Optional.ofNullable(x).isEmpty() (Java 11+)

- Simplify Optional usage ONLY if logic remains identical

---

### 5. Base64 / Encoding

- sun.misc.BASE64Encoder → Base64.getEncoder()
- sun.misc.BASE64Decoder → Base64.getDecoder()

---

### 6. Hex / Binary

- DatatypeConverter.printHexBinary(...) → HexFormat.of().formatHex(...)

---

### 7. File API

- new File(path).exists() → Files.exists(Path.of(path))
- new File(path).delete() → Files.deleteIfExists(Path.of(path))

(ONLY if exception handling behavior remains unchanged)

---

### 8. Stream Improvements (VERY LIMITED)

- Replace simple loops → stream ONLY if:
    - no break/continue
    - no mutation side effects
    - no complex logic

Example:
for (String s : list) {
result.add(s);
}

→

list.forEach(result::add);

---

### 9. Stream Collection Modernization (IMPORTANT)

Replace:

stream().collect(Collectors.toList())

→

stream().toList()

---

#### ⚠️ ONLY IF:

- The resulting list is NOT modified later
- No add(), remove(), clear() operations are used
- No mutable behavior is required

---

#### ✅ Safe Alternative (Preferred if unsure)

Use:

new ArrayList<>(stream().toList())

---

#### ❌ DO NOT CHANGE IF:

- List is modified later
- Mutability is required
- Usage is unclear

---

### 10. instanceof Modernization (Java 16+)

if (obj instanceof String) {
String s = (String) obj;
}

→

if (obj instanceof String s) {
}

---

### 11. Switch Modernization (SAFE ONLY)

- Convert simple switch to switch expression ONLY if:
    - no fall-through logic
    - no side effects

---

### 12. Remove Redundant Code

- Remove unnecessary:
    - redundant null checks (ONLY if guaranteed safe)
    - trivial temporary variables

---

## Forbidden

- Do NOT change business logic
- Do NOT change method signatures
- Do NOT change return types
- Do NOT modify queries
- Do NOT introduce mutability changes unintentionally
- Do NOT refactor complex logic

---

## Strict Safety Rules

Only apply change if:

- Behavior remains EXACTLY the same
- No external dependency impact
- No API contract impact

If unsure → SKIP

---

## Execution

- Scan ALL project files (not only failing ones)
- Apply improvements selectively
- Prefer minimal and localized changes

---

## Validation Rule

- Code must compile successfully
- No new runtime risks introduced
- No behavioral changes

---

## Golden Rule

Prefer SAFETY over modernization

---

## NEXT ACTION

→ STOP (do not trigger build automatically unless explicitly requested)