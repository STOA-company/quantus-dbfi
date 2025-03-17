from dataclasses import dataclass
from typing import Dict, Any
from src.data.request import *


@dataclass
class DomesticOrderRequest(OrderRequest):
    price_type: str = "00"  # 기본값: 지정가
    credit_type: str = "000"  # 기본값: 보통
    loan_date: str = "00000000"  # 기본값: 일반주문
    order_condition: str = "0"  # 기본값: 없음

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
            }
        }


@dataclass
class DomesticCancelOrderRequest(OrderRequest):
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
    exec_yn: str = "0"  # 체결여부 (0:전체, 1:체결, 2:미체결)
    bns_tp_code: str = "0"  # 매매구분 (0:전체, 1:매도, 2:매수)
    isu_tp_code: str = "0"  # 종목구분 (0:전체)
    qry_tp: str = "0"  # 조회구분 (0:전체, 1:ELW, 2:ELW제외)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "ExecYn": self.exec_yn,
                "BnsTpCode": self.bns_tp_code,
                "IsuTpCode": self.isu_tp_code,
                "QryTp": self.qry_tp,
            }
        }


@dataclass
class DomesticAbleOrderQuantityRequest(AbleOrderQuantityRequest):
    bns_tp_code: str = "0"  # 매매구분 (1:매도, 2:매수)
    stock_code: str = "0"  # 종목번호
    price: float = 0  # 주문가

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "BnsTpCode": self.bns_tp_code,
                "IsuNo": self.stock_code,
                "OrdPrc": self.price,
            }
        }


@dataclass
class DomesticBalanceRequest(BalanceRequest):
    qry_tp_code: str = (
        "0"  # 조회구분코드 (0:전체, 1:비상장제외, 2:비상장,코넥스,kotc 제외)
    )

    def to_request_data(self) -> Dict[str, Any]:
        """API 요청 데이터 형식으로 변환"""
        return {"In": {"QryTpCode": self.qry_tp_code}}
