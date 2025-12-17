# CSV Profiling Report

Generated: 2025-12-17T09:09:21

## Summary

- **Rows:** 20
- **Columns:** 10

## Columns

| Column | Type | Missing | Unique |
|--------|------|--------:|-------:|
| order_id | number | 0 | 20 |
| customer_name | text | 3 | 9 |
| city | text | 4 | 9 |
| item_name | text | 2 | 6 |
| quantity | number | 0 | 3 |
| unit_price_sar | number | 5 | 6 |
| total_amount_sar | number | 3 | 12 |
| payment_method | text | 3 | 3 |
| order_status | text | 1 | 2 |
| order_date | text | 4 | 14 |

## Detailed Statistics

### order_id

- **Type:** number
- **Missing values:** 0
- **Unique values:** 20
- **Min:** 1.0
- **Max:** 20.0
- **Mean:** 10.50

### customer_name

- **Type:** text
- **Missing values:** 3
- **Unique values:** 9
- **Top values:**
  - Khalid Al Zahrani: 6
  - Abdullah Al Anazi: 2
  - Fahad Al Qahtani: 2

### city

- **Type:** text
- **Missing values:** 4
- **Unique values:** 9
- **Top values:**
  - Abha: 5
  - Qassim: 2
  - Riyadh: 2

### item_name

- **Type:** text
- **Missing values:** 2
- **Unique values:** 6
- **Top values:**
  - Laptop: 5
  - Keyboard: 4
  - Monitor: 3

### quantity

- **Type:** number
- **Missing values:** 0
- **Unique values:** 3
- **Min:** 1.0
- **Max:** 3.0
- **Mean:** 1.75

### unit_price_sar

- **Type:** number
- **Missing values:** 5
- **Unique values:** 6
- **Min:** 300.0
- **Max:** 3500.0
- **Mean:** 2093.33

### total_amount_sar

- **Type:** number
- **Missing values:** 3
- **Unique values:** 12
- **Min:** 300.0
- **Max:** 10500.0
- **Mean:** 3564.71

### payment_method

- **Type:** text
- **Missing values:** 3
- **Unique values:** 3
- **Top values:**
  - mada: 6
  - apple_pay: 6
  - credit_card: 5

### order_status

- **Type:** text
- **Missing values:** 1
- **Unique values:** 2
- **Top values:**
  - pending: 11
  - completed: 8

### order_date

- **Type:** text
- **Missing values:** 4
- **Unique values:** 14
- **Top values:**
  - 2025-04-27: 2
  - 2025-09-01: 2
  - 2025-11-25: 1
