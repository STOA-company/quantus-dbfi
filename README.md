# DBFI(DB 증권) API

## 설치

```bash
pip install pydbfi
```

## 초기화

```python
from dbfi import DBFI

dbfi = DBFI(app_key="YOUR_APP_KEY", app_secret_key="YOUR_SECRET_KEY")
```

## 주요 기능

### 1. 매수 및 매도

```python
# 국내 주식 매수
result = dbfi.buy(region="domestic", stock_code="005930", quantity=10, price=50000)
print(result)

# 해외 주식 매도
result = dbfi.sell(region="overseas", stock_code="AAPL", quantity=5, price=150.0)
print(result)
```

### 2. 주문 취소

```python
# 국내 주문 취소
result = dbfi.cancel(region="domestic", order_no=12345, stock_code="005930", quantity=10)
print(result)

# 해외 주문 취소
result = dbfi.cancel(region="overseas", order_no=54321, stock_code="AAPL", quantity=5)
print(result)
```

### 3. 거래 내역 조회

```python
# 국내 체결/미체결 내역 조회
result = dbfi.get_transaction_history(region="domestic", execution_status="0")
print(result)

# 해외 체결/미체결 내역 조회
result = dbfi.get_transaction_history(region="overseas")
print(result)
```

### 4. 잔고 및 예수금 조회

```python
# 국내 주식 잔고 조회
result = dbfi.get_stock_balance(region="domestic", query_type="0")
print(result)

# 해외 주식 잔고 조회
result = dbfi.get_stock_balance(region="overseas", balance_type="2")
print(result)

# 국내 예수금 조회
result = dbfi.get_deposit(region="domestic")
print(result)

# 해외 예수금 조회
result = dbfi.get_deposit(region="overseas")
print(result)
```

### 5. 주문 가능 수량 조회

```python
# 국내 주식 주문 가능 수량 조회
result = dbfi.get_able_order_quantity(region="domestic", stock_code="005930", price=50000, order_type="2")
print(result)

# 해외 주식 주문 가능 수량 조회
result = dbfi.get_able_order_quantity(region="overseas", stock_code="AAPL", price=150.0, trx_type="2")
print(result)
```

### 6. 주식 가격 조회

```python
# 국내 주식 현재가 조회
result = dbfi.get_stock_price(region="domestic", stock_code="005930", market_code="J")
print(result)

# 해외 주식 현재가 조회
result = dbfi.get_stock_price(region="overseas", stock_code="AAPL", market_code="FY")
print(result)
```

### 7. 차트 조회
```python
# 국내 분봉 차트 조회
result = dbfi.get_minute_chart(region="domestic", stock_code="005930", start_date="20230101", time_interval="60", market_code="J")
print(result)

# 해외 일봉 차트 조회
result = dbfi.get_daily_chart(region="overseas", stock_code="AAPL", start_date="20230101", end_date="20230131", market_code="FY")
print(result)
```

## 세션 종료

```python
dbfi.close()
```
