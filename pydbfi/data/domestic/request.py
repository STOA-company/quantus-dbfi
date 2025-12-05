from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..request import *


@dataclass
class DomesticOrderRequest(OrderRequest):
    price_type: str = "00"  # 기본값: 지정가
    credit_type: str = "000"  # 기본값: 보통
    loan_date: str = "00000000"  # 기본값: 일반주문
    order_condition: str = "0"  # 기본값: 없음
    trc_no: int = 1 # 주문시 거래소 구분용도로 사용 (1 : KRX) ※ 1로 고정하셔서 사용 부탁드립니다. (SOR 주문 구분은 추후 제공 예정)

    def to_request_data(self) -> Dict[str, Any]:
        if not self.stock_code.startswith("A") and len(self.stock_code) == 6:
            isu_no = self.stock_code
        else:
            isu_no = self.stock_code

        return {
            "In": {
                "IsuNo": isu_no,  # 종목번호
                "OrdQty": self.quantity,  # 주문수량
                "OrdPrc": self.price,  # 주문가
                "BnsTpCode": self.order_type,  # 매매구분
                "OrdprcPtnCode": self.price_type,  # 호가유형코드
                "MgntrnCode": self.credit_type,  # 신용거래코드
                "LoanDt": self.loan_date,  # 대출일
                "OrdCndiTpCode": self.order_condition,  # 주문조건
                "TrchNo": self.trc_no, # 트렌치번호
            }
        }


@dataclass
class DomesticCancelOrderRequest:
    original_order_no: int
    stock_code: str
    quantity: int

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "OrgOrdNo": self.original_order_no,
                "IsuNo": self.stock_code,
                "OrdQty": self.quantity,
            }
        }


@dataclass
class DomesticTransactionHistoryRequest(TransactionHistoryRequest):
    execution_status: str = "0"  # 체결여부 (0:전체, 1:체결, 2:미체결)
    order_type: str = "0"  # 매매구분 (0:전체, 1:매도, 2:매수)
    stock_type: str = "0"  # 종목구분 (0:전체)
    query_type: str = "0"  # 조회구분 (0:전체, 1:ELW, 2:ELW제외)
    sor_tp_yn: str = "2" # SOR구분여부 (0 : N, 1 : Y, 2 : 전체)
    trd_mkt_code: str = "0" # 거래시장코드 (0 : 전체, 1 : KRX, 2 : NXT)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "ExecYn": self.execution_status,
                "BnsTpCode": self.order_type,
                "IsuTpCode": self.stock_type,
                "QryTp": self.query_type,
                "TrdMktCode": self.trd_mkt_code,
                "SorTpYn": self.sor_tp_yn,
            }
        }


@dataclass
class DomesticAbleOrderQuantityRequest(AbleOrderQuantityRequest):
    order_type: str = "0"  # 매매구분 (1:매도, 2:매수)
    stock_code: str = "0"  # 종목번호
    price: float = 0  # 주문가

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "BnsTpCode": self.order_type,
                "IsuNo": self.stock_code,
                "OrdPrc": self.price,
            }
        }


@dataclass
class DomesticBalanceRequest(BalanceRequest):
    query_type: str = (
        "0"  # 조회구분코드 (0:전체, 1:비상장제외, 2:비상장,코넥스,kotc 제외)
    )

    def to_request_data(self) -> Dict[str, Any]:
        """API 요청 데이터 형식으로 변환"""
        return {"In": {"QryTpCode": self.query_type}}


@dataclass
class DomesticQuoteRequest(QuoteRequest):
    market_type: str = "UJ"  # 입력 조건 시장 분류 코드 (UJ:주식(통합), NJ:주식(NXT), E:ELW, EN:ETN, U:업종&지수, W:ELW)
    stock_code: Optional[str] = None  # 종목 코드 (업종(U) 선택 시 지수 코드)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "InputCondMrktDivCode": self.market_type,
                "InputIscd1": self.stock_code,
            }
        }


@dataclass
class DomesticMinuteChartRequest(ChartRequest):
    market_type: str = "UJ"  # 입력 조건 시장 분류 코드 (UJ:주식(통합), NJ:주식(NXT), E:ELW, EN:ETN, U:업종&지수, W:ELW)
    adjust_price_yn: str = "0"  # 수정 주가 사용 여부 (0:사용, 1:미사용)
    stock_code: str = "0"  # 종목 코드
    start_date: str = "0"  # 조회일자 (YYYYMMDD)
    time_interval: Optional[str] = None  # 시간 간격 (60*N: N분)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "InputCondMrktDivCode": self.market_type,
                "InputOrgAdjPrc": self.adjust_price_yn,
                "InputIscd1": self.stock_code,
                "InputDate1": self.start_date,
                "InputDivXtick": self.time_interval,
            }
        }


@dataclass
class DomesticDailyChartRequest(ChartRequest):
    market_type: str = "UJ"  # 입력 조건 시장 분류 코드 (UJ:주식(통합), NJ:주식(NXT), E:ELW, EN:ETN, U:업종&지수, W:ELW)
    adjust_price_yn: str = "0"  # 수정 주가 사용 여부 (0:사용, 1:미사용)
    stock_code: str = "0"  # 종목 코드
    start_date: str = "0"  # 조회일자 (YYYYMMDD)
    end_date: str = "0"  # 조회일자 (YYYYMMDD)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "InputCondMrktDivCode": self.market_type,
                "InputOrgAdjPrc": self.adjust_price_yn,
                "InputIscd1": self.stock_code,
                "InputDate1": self.start_date,
                "InputDate2": self.end_date,
            }
        }


@dataclass
class DomesticWeeklyChartRequest(ChartRequest):
    market_type: str = "UJ"  # 입력 조건 시장 분류 코드 (UJ:주식(통합), NJ:주식(NXT), E:ELW, EN:ETN, U:업종&지수, W:ELW)
    adjust_price_yn: str = "0"  # 수정 주가 사용 여부 (0:사용, 1:미사용)
    stock_code: str = "0"  # 종목 코드
    start_date: str = "0"  # 조회일자 (YYYYMMDD)
    end_date: str = "0"  # 조회일자 (YYYYMMDD)
    period: str = "W"  # 주기 (W:주, M:월, Y:년)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "InputCondMrktDivCode": self.market_type,
                "InputOrgAdjPrc": self.adjust_price_yn,
                "InputIscd1": self.stock_code,
                "InputDate1": self.start_date,
                "InputDate2": self.end_date,
                "InputPeriodDivCode": self.period,
            }
        }


@dataclass
class DomesticMonthlyChartRequest(ChartRequest):
    market_type: str = "UJ"  # 입력 조건 시장 분류 코드 (UJ:주식(통합), NJ:주식(NXT), E:ELW, EN:ETN, U:업종&지수, W:ELW)
    adjust_price_yn: str = "0"  # 수정 주가 사용 여부 (0:사용, 1:미사용)
    stock_code: str = "0"  # 종목 코드
    start_date: str = "0"  # 조회일자 (YYYYMMDD)
    end_date: str = "0"  # 조회일자 (YYYYMMDD)
    period: str = "M"  # 주기 (W:주, M:월, Y:년)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "InputCondMrktDivCode": self.market_type,
                "InputOrgAdjPrc": self.adjust_price_yn,
                "InputIscd1": self.stock_code,
                "InputDate1": self.start_date,
                "InputDate2": self.end_date,
                "InputPeriodDivCode": self.period,
            }
        }


@dataclass
class DomesticFuturesBalanceRequest:
    """국내 선물옵션 잔고 조회 요청 데이터 클래스"""
    
    def to_request_data(self) -> Dict[str, Any]:
        """API 요청 데이터 형식으로 변환"""
        return {"In": {}}

@dataclass
class DomesticPostTradingHistoryRequest:
    """
    QyTP : 0:전체, 1:입출금, 2:입출고, 3:매매, 4:이체/대체
    QrySrtDt: 조회시작일자 (YYYYMMDD)
    QryEndDt: 조회종료일자 (YYYYMMDD) , 최대 12개월 (선물 6개월) 까지 조회 가능
    SrtNo: 시작번호 (기본값: 0, 조회구분 "0.전체"인 경우 CMA매매내역 생략시 1 입력)
    IsuNo: 종목번호 ("" : 공백 입력시 전체 종목 조회, "A+종목번호" 입력시 특정 종목 내역 조회)
    """
    QrySrtDt: str  # 필수 매개변수
    QryEndDt: str  # 필수 매개변수
    QryTp: str = "0"  # 기본값 있는 매개변수
    SrtNo: int = 0
    IsuNo: str = ""

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "QryTp": self.QryTp,
                "QrySrtDt": self.QrySrtDt,
                "QryEndDt": self.QryEndDt,
                "SrtNo": self.SrtNo,
                "IsuNo": self.IsuNo,
            }
        }

@dataclass
class DomesticDailyTradeReportRequest:
    """
    IsuNo: 종목번호 ("" : 공백 입력시 전체 종목 조회, "A+종목번호" 입력시 특정 종목 내역 조회)
    BnsDt: 거래일자 (YYYYMMDD)
    """
    isu_no: str = ""
    bns_dt: str = ""

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "IsuNo": self.isu_no,
                "BnsDt": self.bns_dt,
            }
        }