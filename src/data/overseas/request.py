from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any
from src.data.request import *


@dataclass
class OverseasOrderRequest(OrderRequest):
    price_type: str = "1"  # 기본값: 지정가
    order_condition: str = "1"  # 기본값: 일반
    trade_type: str = "0"  # 기본값: 주문
    original_order_no: int = 0  # 기본값: 신규주문

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "AstkIsuNo": self.stock_code,
                "AstkBnsTpCode": self.order_type,
                "AstkOrdprcPtnCode": self.price_type,
                "AstkOrdCndiTpCode": self.order_condition,
                "AstkOrdQty": self.quantity,
                "AstkOrdPrc": self.price,
                "OrdTrdTpCode": self.trade_type,
                "OrgOrdNo": self.original_order_no,
            }
        }


@dataclass
class OverseasCancelOrderRequest(OrderRequest):
    original_order_no: int
    stock_code: str
    quantity: int

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "AstkIsuNo": self.stock_code,
                "AstkBnsTpCode": "1",  # 취소주문시에는 원래 매도/매수 구분과 무관
                "AstkOrdprcPtnCode": "1",  # 지정가
                "AstkOrdCndiTpCode": "1",  # 일반
                "AstkOrdQty": self.quantity,
                "AstkOrdPrc": 0,
                "OrdTrdTpCode": "2",  # 취소주문
                "OrgOrdNo": self.original_order_no,
            }
        }


@dataclass
class OverseasTransactionHistoryRequest(TransactionHistoryRequest):
    qry_srt_dt: str = ""  # 조회시작일자 (YYYYMMDD)
    qry_end_dt: str = ""  # 조회종료일자 (YYYYMMDD)
    astk_isu_no: str = ""  # 해외주식종목번호 (빈값은 전체 종목)
    astk_bns_tp_code: str = "0"  # 해외주식매매구분코드 (0:전체, 1:매도, 2:매수)
    ordxct_tp_code: str = "0"  # 주문체결구분코드 (0:전체, 1:체결, 2:미체결)
    stnln_tp_code: str = "0"  # 정렬구분코드 (0:역순, 1:정순)
    qry_tp_code: str = "0"  # 조회구분코드 (0:합산별, 1:건별)
    online_yn: str = "0"  # 온라인여부 (0:전체, Y:온라인, N:오프라인)
    cvrg_ord_yn: str = "0"  # 반대매매주문여부 (0:전체, Y:반대매매, N:일반주문)
    won_fcurr_tp_code: str = "1"  # 원화외화구분코드 (1:원화, 2:외화)

    def to_request_data(self) -> Dict[str, Any]:
        # 시작일자와 종료일자가 없으면 당일 조회
        if not self.qry_srt_dt and not self.qry_end_dt:
            today = datetime.now().strftime("%Y%m%d")
            self.qry_srt_dt = today
            self.qry_end_dt = today

        return {
            "In": {
                "QrySrtDt": self.qry_srt_dt,
                "QryEndDt": self.qry_end_dt,
                "AstkIsuNo": self.astk_isu_no,
                "AstkBnsTpCode": self.astk_bns_tp_code,
                "OrdxctTpCode": self.ordxct_tp_code,
                "StnlnTpCode": self.stnln_tp_code,
                "QryTpCode": self.qry_tp_code,
                "OnlineYn": self.online_yn,
                "CvrgOrdYn": self.cvrg_ord_yn,
                "WonFcurrTpCode": self.won_fcurr_tp_code,
            }
        }


@dataclass
class OverseasAbleOrderQuantityRequest(AbleOrderQuantityRequest):
    trx_tp_code: str = "1"  # 처리구분코드 ("1:매도, 2:매수")
    stock_code: str = "0"  # 해외주식종목번호
    price: float = 0  # 해외주식주문가
    won_fcurr_tp_code: str = "2"  # 원화외화구분코드 (1:원화, 2:외화)

    def to_request_data(self) -> Dict[str, Any]:
        return {
            "In": {
                "TrxTpCode": self.trx_tp_code,
                "AstkIsuNo": self.stock_code,
                "AstkOrdPrc": self.price,
                "WonFcurrTpCode": self.won_fcurr_tp_code,
            }
        }


@dataclass
class OverseasBalanceRequest(BalanceRequest):
    trx_tp_code: str = (
        "2"  # 처리구분코드 (1:외화잔고, 2:주식잔고상세, 3:주식잔고(국가별), 9:당일실현손익)
    )
    cmsn_tp_code: str = (
        "2"  # 수수료구분코드 (0:전부 미포함, 1:매수제비용만 포함, 2:매수제비용+매도제비용)
    )
    won_fcurr_tp_code: str = "2"  # 원화외화구분코드 (1:원화, 2:외화)
    dpnt_bal_tp_code: str = "0"  # 소수점잔고구분코드 (0:전체, 1:일반, 2:소수점)

    def to_request_data(self) -> Dict[str, Any]:
        """API 요청 데이터 형식으로 변환"""
        return {
            "In": {
                "TrxTpCode": self.trx_tp_code,
                "CmsnTpCode": self.cmsn_tp_code,
                "WonFcurrTpCode": self.won_fcurr_tp_code,
                "DpntBalTpCode": self.dpnt_bal_tp_code,
            }
        }
