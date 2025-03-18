# PYDBFI - DB증권 API Python SDK

https://openapi.db-fi.com

## 설치

```bash
pip install pydbfi
```

## 사용 방법

### 기본 초기화

```python
from pydbfi import DomesticAPI, OverseasAPI

# 국내 시장 API 초기화
domestic_api = DomesticAPI(app_key="your_app_key", app_secret_key="your_app_secret_key")

# 해외 시장 API 초기화
overseas_api = OverseasAPI(app_key="your_app_key", app_secret_key="your_app_secret_key")
```

## 라이센스

[MIT License](LICENSE)