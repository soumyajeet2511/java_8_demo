# Common Java 11 Build Error Patterns

| Error Message Pattern | Probable Cause | Recommended Fix |
|:---|:---|:---|
| `package javax.xml.bind does not exist` | JAXB removed from JDK 11 | Add `jakarta.xml.bind-api` dependency and update imports. |
| `package javax.annotation does not exist` | Common Annotations removed | Add `javax.annotation-api` dependency. |
| `cannot find symbol: class _` | `_` is now a keyword | Rename variable `_` to something like `unused` or `arg`. |
| `package sun.misc does not exist` | Internal API access restricted | Use `java.util.Base64` instead of `sun.misc.BASE64Encoder`. |
| `module not found: ...` | Java Module System issue | Usually happens if `module-info.java` is present but incomplete. |
| `java.lang.NoClassDefFoundError: javax/xml/bind/JAXBException` | JAXB missing at runtime | Ensure dependencies are in the runtime classpath (Maven scope `runtime` or `compile`). |
| `UnsupportedClassVersionError: ... has been compiled by a more recent version` | JDK mismatch | Ensure the compiler and runtime are both using Java 11. |
