from typing import Dict, Any
from src.service.common.base import BaseService
from src.service.common.interfaces import IInquiryService
from src.data.domestic.request import *
from src.data.overseas.request import *


class DomesticInquiryService(BaseService, IInquiryService):
    def get_transaction_history(
        self,
        request: DomesticTransactionHistoryRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """국내 주식 거래 내역 조회"""
        endpoint = "/api/v1/trading/kr-stock/inquiry/transaction-history"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_able_order_quantity(
        self,
        request: DomesticAbleOrderQuantityRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """국내 주식 주문 가능 수량 조회"""
        endpoint = "/api/v1/trading/kr-stock/inquiry/able-orderqty"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_balance(
        self,
        request: DomesticBalanceRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """국내 주식 잔고 조회"""
        endpoint = "/api/v1/trading/kr-stock/inquiry/balance"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_deposit(
        self, cont_yn: str = "N", cont_key: str = None, **kwargs
    ) -> Dict[str, Any]:
        """국내 주식 예수금 조회"""
        endpoint = "/api/v1/trading/kr-stock/inquiry/acnt-deposit"
        return self._request(
            "POST", endpoint, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )


class OverseasInquiryService(BaseService, IInquiryService):
    def get_transaction_history(
        self,
        request: OverseasTransactionHistoryRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """해외 주식 거래 내역 조회"""
        endpoint = "/api/v1/trading/overseas-stock/inquiry/transaction-history"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_able_order_quantity(
        self,
        request: OverseasAbleOrderQuantityRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """해외 주식 주문 가능 수량 조회"""
        endpoint = "/api/v1/trading/overseas-stock/inquiry/able-orderqty"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_balance(
        self,
        request: OverseasBalanceRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """해외 주식 잔고 조회"""
        endpoint = "/api/v1/trading/overseas-stock/inquiry/balance-margin"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_deposit(
        self, cont_yn: str = "N", cont_key: str = None, **kwargs
    ) -> Dict[str, Any]:
        """해외 주식 예수금 조회"""
        endpoint = "/api/v1/trading/overseas-stock/inquiry/deposit-detail"
        return self._request(
            "POST", endpoint, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )
