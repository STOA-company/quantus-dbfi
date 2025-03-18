from typing import Any, Dict

from dbfi.data.domestic.request import *
from dbfi.data.overseas.request import *
from dbfi.service.common.base import BaseService
from dbfi.service.common.interfaces import IQuoteService


class DomesticQuoteService(BaseService, IQuoteService):
    def get_stock_tickers(
        self, request: QuoteRequest, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/quote/kr-stock/inquiry/stock-ticker"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_stock_price(
        self, request: QuoteRequest, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/quote/kr-stock/inquiry/price"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_order_book(
        self, request: QuoteRequest, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/quote/kr-stock/inquiry/orderbook"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )


class OverseasQuoteService(BaseService, IQuoteService):
    def get_stock_tickers(
        self, request: OverseasStockTickersRequest, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/quote/overseas-stock/inquiry/stock-ticker"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_stock_price(
        self, request: OverseasQuoteRequest, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/quote/overseas-stock/inquiry/price"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )

    def get_order_book(
        self, request: OverseasQuoteRequest, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        endpoint = "/api/v1/quote/overseas-stock/inquiry/orderbook"
        data = request.to_request_data()
        return self._request(
            "POST", endpoint, data=data, cont_yn=cont_yn, cont_key=cont_key, **kwargs
        )
