# LLM Context Guide: Constructing `q` Values for News API v3

Use this guide to generate valid and effective `q` parameters for NewsCatcher News API v3. Queries should return precise, relevant news articles by using the supported syntax correctly.

---

## 1. Purpose

You are generating the `q` parameter inside a JSON query for NewsCatcher News API v3. Your job is to create high-precision search strings using:

- Boolean logic
- Exact match
- Grouping
- Proximity queries
- Wildcards

---

## 2. Syntax Rules

- `AND`: both terms must appear  
  `Tesla AND layoffs`

- `OR`: at least one term must appear  
  `strikes OR closures`

- `NOT`: exclude terms  
  `airline NOT "United Airlines"`

- `()`: group expressions and control precedence  
  `(airport OR "freight port") AND strike`

- `"..."`: exact phrase match (must be escaped in JSON)  
  `"climate change"`

- `*`: wildcard for multiple characters  
  `invest*` → investor, investing

- `?`: wildcard for single character  
  `c?t` → cat, cut

- `NEAR("A", "B", distance, in_order?)`: proximity between phrases

---

## 3. JSON Formatting Rules

When writing `q` inside a JSON string:

- Escape internal double quotes using `\"...\"`
- Wrap full query string in standard JSON string syntax

Example:
```json
{ "q": "(\"climate change\" OR \"global warming\") AND policy" }
````

---

## 4. Common Pitfalls

* `q: "climate change"` → parsed as `climate AND change`

* `q: "\"climate change\""` → exact match

* `airport OR port AND strike` → ambiguous

* `(airport OR port) AND strike` → explicit grouping (correct)

---

## 5. Query Templates

**Exact match (escaped):**

```json
"q": "\"John Smith\""
```

**Boolean with grouping:**

```json
"q": "(airline OR airport) AND strike"
```

**Exclusion:**

```json
"q": "Tesla NOT \"Elon Musk\""
```

**Proximity query:**

```json
"q": "NEAR(\"climate change\", \"Paris agreement\", 15)"
```

---

## 6. DOs and DON’Ts

| ✅ DO                                    | ❌ DON’T                      |
| --------------------------------------- | ---------------------------- |
| Use `\"...\"` for exact phrases in JSON | Assume `"A B"` = exact match |
| Use parentheses with `AND` and `OR`     | Mix logic without grouping   |
| Escape quotes inside JSON strings       | Leave quotes unescaped       |
| Use `NEAR(...)` for context             | Overuse `*` or `?`           |

---

## 7. Sample Queries

**Basic:**

```json
{ "q": "\"Tesla\" AND layoffs" }
```

**Complex:**

```json
{
  "q": "(\"airline workers\" OR pilots OR crew) AND (strike OR protest) AND NOT (historical OR ended)"
}
```

**Proximity:**

```json
{
  "q": "NEAR(\"climate change\", \"policy response\", 20)"
}
```
