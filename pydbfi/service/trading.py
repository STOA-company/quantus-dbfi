from ..data.domestic.request import *
from ..data.overseas.request import *
from ..service.common.base import BaseService
from ..service.common.interfaces import ITradingService


class DomesticTradingService(BaseService, ITradingService):
    def place_order(
        self, order_request: DomesticOrderRequest, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/kr-stock/order"
        data = order_request.to_request_data()
        return self._request("POST", endpoint, data=data, **kwargs)

    def cancel_order(
        self, cancel_request: DomesticCancelOrderRequest, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/kr-stock/order-cancel"
        data = cancel_request.to_request_data()
        return self._request("POST", endpoint, data=data, **kwargs)

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

    def post_trading_history(
        self,
        request: DomesticPostTradingHistoryRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """국내 주식 거래 내역 조회"""
        endpoint = "/api/v1/trading/kr-stock/inquiry/trading-history"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        ) 

    def post_daily_trade_report(
        self,
        request: DomesticDailyTradeReportRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """국내 주식 일일 거래 보고서 조회"""
        endpoint = "/api/v1/trading/kr-stock/inquiry/daliy-trade-report"
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


class OverseasTradingService(BaseService, ITradingService):
    def place_order(
        self, order_request: OverseasOrderRequest, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/overseas-stock/order"
        data = order_request.to_request_data()
        return self._request("POST", endpoint, data=data, **kwargs)

    def cancel_order(
        self, cancel_request: OverseasCancelOrderRequest, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/overseas-stock/order"
        data = cancel_request.to_request_data()
        return self._request("POST", endpoint, data=data, **kwargs)

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


class DomesticFuturesTradingService(BaseService, ITradingService):
    def get_balance(
        self,
        request: DomesticFuturesBalanceRequest,
        cont_yn: str = "N",
        cont_key: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """국내 선물옵션 잔고 조회"""
        endpoint = "/api/v1/trading/kr-futureoption/inquiry/balance"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def cancel_order(self, *args, **kwargs):
        raise NotImplementedError("국내 선물옵션 취소 미구현")

    def get_able_order_quantity(self, *args, **kwargs):
        raise NotImplementedError("국내 선물옵션 주문가능수량 미구현")

    def get_deposit(self, *args, **kwargs):
        raise NotImplementedError("국내 선물옵션 예수금 미구현")

    def get_transaction_history(self, *args, **kwargs):
        raise NotImplementedError("국내 선물옵션 거래내역 미구현")

    def place_order(self, *args, **kwargs):
        raise NotImplementedError("국내 선물옵션 주문 미구현")
