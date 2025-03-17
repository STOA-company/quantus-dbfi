from abc import ABC, abstractmethod
from typing import Dict, Any


class IOrderService(ABC):
    @abstractmethod
    def place_order(self, order_request, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def cancel_order(self, cancel_request, **kwargs) -> Dict[str, Any]:
        pass


class IInquiryService(ABC):
    @abstractmethod
    def get_transaction_history(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_able_order_quantity(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_balance(
        self, request, cont_yn="N", cont_key=None, **kwargs
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_deposit(self, cont_yn="N", cont_key=None, **kwargs) -> Dict[str, Any]:
        pass


class ITradingService(IOrderService, IInquiryService):
    @property
    @abstractmethod
    def order_service(self) -> IOrderService:
        pass

    @property
    @abstractmethod
    def inquiry_service(self) -> IInquiryService:
        pass
