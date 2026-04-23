name: config-fix
description: Fix build configuration issues such as Java version or plugin settings.
dependencies:
  - global-restrictions

---

# Config Fix Skill

## Purpose
Fix configuration issues (pom.xml, properties, YAML).

## Allowed
- Fix Java version config
- Fix plugin versions
- Fix build configs

## Forbidden
- Do NOT modify Java classes
- Do NOT change logic

## Output
Config patch only