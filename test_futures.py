#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pydbfi import DBFI

def test_domestic_futures_balance():
    """국내 선물옵션 잔고 조회 테스트"""
    
    # API 키 설정
    APP_KEY = "PSWlFD1iMzo8LtA2xfL9PljMgclx9wNQBmyf"
    SECRET_KEY = "tPph3ARVPNcCPx1gagT9zpasKROmPBS9"
    
    try:
        print("=== DB증권 국내 선물옵션 잔고 조회 테스트 ===")
        print(f"APP_KEY: {APP_KEY}")
        print(f"SECRET_KEY: {SECRET_KEY[:10]}...")
        print()
        
        # DBFI 인스턴스 생성
        print("1. DBFI 인스턴스 초기화 중...")
        dbfi = DBFI(app_key=APP_KEY, app_secret_key=SECRET_KEY)
        print("✓ 초기화 완료")
        print()
        
        # 국내 선물옵션 잔고 조회
        print("2. 국내 선물옵션 잔고 조회 중...")
        result = dbfi.get_domestic_futures_balance()
        print("✓ 조회 완료")
        print()
        
        # 결과 출력
        print("3. 조회 결과:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
        
        # 세션 종료
        print("4. 세션 종료 중...")
        dbfi.close()
        print("✓ 세션 종료 완료")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_domestic_futures_balance() 