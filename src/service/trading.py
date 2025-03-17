from src.oauth import OAuth
from src.service.common.base import BaseService
from src.service.common.interfaces import ITradingService
from src.service.modules.order import *
from src.service.modules.inquiry import *


class DomesticTradingService(BaseService, ITradingService):
    def __init__(self, auth: OAuth):
        super().__init__(auth)
        self._order_service = DomesticOrderService(auth)
        self._inquiry_service = DomesticInquiryService(auth)

    @property
    def order_service(self) -> IOrderService:
        return self._order_service

    @property
    def inquiry_service(self) -> IInquiryService:
        return self._inquiry_service

    def place_order(self, order_request, **kwargs) -> Dict[str, Any]:
        return self.order_service.place_order(order_request, **kwargs)

    def cancel_order(self, cancel_request, **kwargs) -> Dict[str, Any]:
        return self.order_service.cancel_order(cancel_request, **kwargs)

    def get_transaction_history(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        return self.inquiry_service.get_transaction_history(
            request, cont_yn, cont_key, **kwargs
        )

    def get_able_order_quantity(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        return self.inquiry_service.get_able_order_quantity(
            request, cont_yn, cont_key, **kwargs
        )

    def get_balance(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        return self.inquiry_service.get_balance(request, cont_yn, cont_key, **kwargs)

    def get_deposit(self, cont_yn="N", cont_key=None, **kwargs) -> Dict[str, Any]:
        return self.inquiry_service.get_deposit(cont_yn, cont_key, **kwargs)


class OverseasTradingService(BaseService, ITradingService):
    def __init__(self, auth: OAuth):
        super().__init__(auth)
        self._order_service = OverseasOrderService(auth)
        self._inquiry_service = OverseasInquiryService(auth)

    @property
    def order_service(self) -> IOrderService:
        return self._order_service

    @property
    def inquiry_service(self) -> IInquiryService:
        return self._inquiry_service

    def place_order(self, order_request, **kwargs) -> Dict[str, Any]:
        return self.order_service.place_order(order_request, **kwargs)

    def cancel_order(self, cancel_request, **kwargs) -> Dict[str, Any]:
        return self.order_service.cancel_order(cancel_request, **kwargs)

    def get_transaction_history(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        return self.inquiry_service.get_transaction_history(
            request, cont_yn, cont_key, **kwargs
        )

    def get_able_order_quantity(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        return self.inquiry_service.get_able_order_quantity(
            request, cont_yn, cont_key, **kwargs
        )

    def get_balance(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        return self.inquiry_service.get_balance(request, cont_yn, cont_key, **kwargs)

    def get_deposit(self, cont_yn="N", cont_key=None, **kwargs) -> Dict[str, Any]:
        return self.inquiry_service.get_deposit(cont_yn, cont_key, **kwargs)
