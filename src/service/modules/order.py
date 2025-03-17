from typing import Dict, Any
from src.service.common.base import BaseService
from src.service.common.interfaces import IOrderService
from src.data.domestic.request import *
from src.data.overseas.request import *


class DomesticOrderService(BaseService, IOrderService):
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


class OverseasOrderService(BaseService, IOrderService):
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
