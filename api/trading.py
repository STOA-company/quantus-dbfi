from typing import Dict, Any
from abc import ABC, abstractmethod
from oauth import Oauth
from api.base import BaseAPI
from data.request import *
from data.domestic.request import *
from data.overseas.request import *

class TradingAPI(BaseAPI, ABC):
    """
        cont_yn: 연속 거래 여부 (Y/N)
        cont_key: 연속키 값
    """
    
    def __init__(self, auth: Oauth):
        super().__init__(auth=auth)
    
    @abstractmethod
    def place_order(self, order_request: OrderRequest, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def cancel_order(self, cancel_request: OrderRequest, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_transaction_history(
            self, request: TransactionHistoryRequest, 
            cont_yn: str = "N", 
            cont_key: str = None, 
            **kwargs
        ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_balance(
            self, 
            request: BalanceRequest, 
            cont_yn: str = "N", 
            cont_key: str = None, 
            **kwargs
        ) -> Dict[str, Any]:
        pass


class DomesticTradingAPI(TradingAPI):
    
    def place_order(self, order_request: DomesticOrderRequest, **kwargs) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/kr-stock/order"
        data = order_request.to_request_data()
        return self._request("POST", endpoint, data=data, **kwargs)
    
    def cancel_order(self, cancel_request: DomesticCancelOrderRequest, **kwargs) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/kr-stock/order-cancel"
        data = cancel_request.to_request_data()
        return self._request("POST", endpoint, data=data, **kwargs)

    def get_transaction_history(
            self, request: DomesticTransactionHistoryRequest,
            cont_yn: str = "N",
            cont_key: str = None, 
            **kwargs
        ) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/kr-stock/inquiry/transaction-history"
        data = request.to_request_data()
        
        return self._request("POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs)
    
    def get_balance(
            self, 
            request: DomesticBalanceRequest,
            cont_yn: str = "N", 
            cont_key: str = None, 
            **kwargs
        ) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/kr-stock/inquiry/balance"
        data = request.to_request_data()
        
        return self._request("POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs)
    

class OverseasTradingAPI(TradingAPI):
    
    def place_order(self, order_request: OverseasOrderRequest, **kwargs) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/overseas-stock/order"
        data = order_request.to_request_data()
        return self._request("POST", endpoint, data=data, **kwargs)

    
    def cancel_order(self, cancel_request: OverseasCancelOrderRequest, **kwargs) -> Dict[str, Any]:
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
        endpoint = "/api/v1/trading/overseas-stock/inquiry/transaction-history"
        data = request.to_request_data()
        
        return self._request("POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs)

    def get_balance(
            self, 
            request: OverseasBalanceRequest,
            cont_yn: str = "N", 
            cont_key: str = None, 
            **kwargs
        ) -> Dict[str, Any]:
        endpoint = "/api/v1/trading/overseas-stock/inquiry/balance-margin"
        data = request.to_request_data()
        
        return self._request("POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs)
