# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DB증권(DB Securities) 트레이딩 API Python SDK. 국내/해외 주식 매매, 시세 조회, 차트 데이터를 단일 인터페이스로 제공합니다. PyPI 패키지명: `pydbfi`

## Commands

```bash
pip install pydbfi          # PyPI 설치
python setup.py install     # 로컬 설치
```

테스트 프레임워크, 린터, CI/CD 미설정 상태입니다.

## Architecture

```
pydbfi/
├── main.py              # DBFI 메인 클래스 (진입점)
├── api.py               # API 구현 (BaseAPI, DomesticAPI, OverseasAPI, DomesticFuturesAPI)
├── oauth.py             # OAuth 인증
├── oauth_single_tone.py # 싱글톤 OAuth 패턴
├── services.py          # 서비스 레이어 exports
├── data/
│   ├── request.py       # 기본 요청 빌더
│   ├── domestic/request.py   # 국내 주식 요청
│   └── overseas/request.py   # 해외 주식 요청
└── service/
    ├── base.py          # 베이스 서비스
    ├── interfaces.py    # 서비스 인터페이스
    ├── trading.py       # 매매 서비스
    ├── quote.py         # 시세 서비스
    └── chart.py         # 차트 서비스
```

### 사용법

```python
from pydbfi import DBFI

dbfi = DBFI(app_key="YOUR_KEY", app_secret_key="YOUR_SECRET")

# 매매
dbfi.buy(region="domestic", **kwargs)
dbfi.sell(region="overseas", **kwargs)
dbfi.cancel(region="domestic", **kwargs)

# 조회
dbfi.get_stock_balance(region="domestic", **kwargs)
dbfi.get_stock_price(region="domestic", **kwargs)
dbfi.get_daily_chart(region="domestic", **kwargs)

dbfi.close()  # 정리
```

### Rate Limits

| 작업 | 제한 |
|------|------|
| 주문 | 10회/초 |
| 취소 | 3회/초 |
| 조회 | 1~2회/초 (타입별 상이) |

### 지원 리전

- `domestic`: 국내 주식 + 선물/옵션 잔고
- `overseas`: 해외 주식

## Key Dependencies

requests, fake-useragent, tenacity (retry with backoff)
