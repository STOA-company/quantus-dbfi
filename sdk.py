from typing import Dict, Any, Optional, Literal
import logging


class SDK:
    def __init__(self, app_key: str, app_secret_key: str, log_level=logging.INFO):
        self._setup_logging(log_level)

        from src.oauth import OAuth

        self.auth = OAuth(appkey=app_key, appsecretkey=app_secret_key)
        self.logger.info("DB증권 API SDK가 초기화되었습니다.")

        try:
            self.auth.get_token()
            self.logger.info(f"토큰 발급 성공 (만료: {self.auth.expire_in})")
        except Exception as e:
            self.logger.error(f"토큰 발급 실패: {str(e)}")

        self._services = {}

    def _setup_logging(self, log_level):
        self.logger = logging.getLogger("db-trading-sdk")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(log_level)

    def _get_service(self, market: str):
        if market not in self._services:
            from src.service.trading import (
                DomesticTradingService,
                OverseasTradingService,
            )

            if market == "domestic":
                self._services[market] = DomesticTradingService(auth=self.auth)
            elif market == "overseas":
                self._services[market] = OverseasTradingService(auth=self.auth)
            else:
                raise ValueError(f"지원하지 않는 시장입니다: {market}")

        return self._services[market]

    def buy(
        self,
        stock_code: str,
        quantity: int,
        price: float,
        market: str = "domestic",
        **kwargs,
    ) -> Dict[str, Any]:
        if market == "domestic":
            from src.data.domestic.request import DomesticOrderRequest

            order_request = DomesticOrderRequest(
                stock_code=stock_code,
                quantity=quantity,
                price=price,
                order_type="2",
                **kwargs,
            )
        elif market == "overseas":
            from src.data.overseas.request import OverseasOrderRequest

            order_request = OverseasOrderRequest(
                stock_code=stock_code,
                quantity=quantity,
                price=price,
                order_type="2",
                **kwargs,
            )
        else:
            raise ValueError(f"지원하지 않는 시장입니다: {market}")

        service = self._get_service(market)
        return service.place_order(order_request)

    def sell(
        self,
        stock_code: str,
        quantity: int,
        price: float,
        market: str = "domestic",
        **kwargs,
    ) -> Dict[str, Any]:
        if market == "domestic":
            from src.data.domestic.request import DomesticOrderRequest

            order_request = DomesticOrderRequest(
                stock_code=stock_code,
                quantity=quantity,
                price=price,
                order_type="1",
                **kwargs,
            )
        elif market == "overseas":
            from src.data.overseas.request import OverseasOrderRequest

            order_request = OverseasOrderRequest(
                stock_code=stock_code,
                quantity=quantity,
                price=price,
                order_type="1",
                **kwargs,
            )
        else:
            raise ValueError(f"지원하지 않는 시장입니다: {market}")

        service = self._get_service(market)
        return service.place_order(order_request)

    def cancel(
        self, order_no: int, stock_code: str, quantity: int, market: str = "domestic"
    ) -> Dict[str, Any]:
        if market == "domestic":
            from src.data.domestic.request import DomesticCancelOrderRequest

            cancel_request = DomesticCancelOrderRequest(
                original_order_no=order_no, stock_code=stock_code, quantity=quantity
            )
        elif market == "overseas":
            from src.data.overseas.request import OverseasCancelOrderRequest

            cancel_request = OverseasCancelOrderRequest(
                original_order_no=order_no, stock_code=stock_code, quantity=quantity
            )
        else:
            raise ValueError(f"지원하지 않는 시장입니다: {market}")

        service = self._get_service(market)
        return service.cancel_order(cancel_request)

    def get_transaction_history(
        self, market: str = "domestic", **kwargs
    ) -> Dict[str, Any]:
        """
        거래 내역 조회
        """
        cont_yn = kwargs.pop("cont_yn", "N")
        cont_key = kwargs.pop("cont_key", None)

        if market == "domestic":
            from src.data.domestic.request import DomesticTransactionHistoryRequest

            request = DomesticTransactionHistoryRequest(**kwargs)
        elif market == "overseas":
            from src.data.overseas.request import OverseasTransactionHistoryRequest

            request = OverseasTransactionHistoryRequest(**kwargs)
        else:
            raise ValueError(f"지원하지 않는 시장입니다: {market}")

        service = self._get_service(market)
        return service.get_transaction_history(
            request, cont_yn=cont_yn, cont_key=cont_key
        )

    def get_stock_balance(self, market: str = "domestic", **kwargs) -> Dict[str, Any]:
        """
        주식 잔고 조회
        """
        cont_yn = kwargs.pop("cont_yn", "N")
        cont_key = kwargs.pop("cont_key", None)

        if market == "domestic":
            from src.data.domestic.request import DomesticBalanceRequest

            request = DomesticBalanceRequest(**kwargs)
        elif market == "overseas":
            from src.data.overseas.request import OverseasBalanceRequest

            request = OverseasBalanceRequest(**kwargs)
        else:
            raise ValueError(f"지원하지 않는 시장입니다: {market}")

        service = self._get_service(market)
        return service.get_balance(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_deposit(
        self, market: str = "domestic", cont_yn: str = "N", cont_key: str = None
    ):
        service = self._get_service(market)
        return service.get_deposit(cont_yn=cont_yn, cont_key=cont_key)

    def get_able_order_quantity(
        self,
        stock_code: str,
        price: float,
        order_type: str = "2",
        market: str = "domestic",
        **kwargs,
    ) -> Dict[str, Any]:
        """
        주문 가능 수량 조회
        """
        cont_yn = kwargs.pop("cont_yn", "N")
        cont_key = kwargs.pop("cont_key", None)

        if market == "domestic":
            from src.data.domestic.request import DomesticAbleOrderQuantityRequest

            request = DomesticAbleOrderQuantityRequest(
                stock_code=stock_code, price=price, bns_tp_code=order_type, **kwargs
            )
        elif market == "overseas":
            from src.data.overseas.request import OverseasAbleOrderQuantityRequest

            request = OverseasAbleOrderQuantityRequest(
                stock_code=stock_code, price=price, bns_tp_code=order_type, **kwargs
            )
        else:
            raise ValueError(f"지원하지 않는 시장입니다: {market}")

        service = self._get_service(market)
        return service.get_able_order_quantity(
            request, cont_yn=cont_yn, cont_key=cont_key
        )

    def close(self):
        """
        세션 종료
        """
        try:
            self.auth.revoke_token()
            self.logger.info("DB증권 API 세션이 종료되었습니다.")
        except Exception as e:
            self.logger.error(f"세션 종료 중 오류 발생: {str(e)}")
