import logging
from typing import Any, Dict, Optional


class BaseAPI:
    """DB금융투자 API의 기본 클래스"""

    def __init__(self, app_key: str, app_secret_key: str, log_level=logging.INFO):
        self._setup_logging(log_level)

        from .oauth import OAuth

        self.auth = OAuth(appkey=app_key, appsecretkey=app_secret_key)
        self.logger.info("DB증권 API SDK가 초기화되었습니다.")

        try:
            self.auth.get_token()
            self.logger.info(f"토큰 발급 성공 (만료: {self.auth.expire_in})")
        except Exception as e:
            self.logger.error(f"토큰 발급 실패: {str(e)}")

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

    def close(self):
        """세션 종료"""
        try:
            self.auth.revoke_token()
            self.logger.info("DB증권 API 세션이 종료되었습니다.")
        except Exception as e:
            self.logger.error(f"세션 종료 중 오류 발생: {str(e)}")


class DomesticAPI(BaseAPI):
    """국내 주식 API"""

    def __init__(self, app_key: str, app_secret_key: str, log_level=logging.INFO):
        super().__init__(app_key, app_secret_key, log_level)
        self._trading_service = None
        self._quote_service = None
        self._chart_service = None

    def _get_trading_service(self):
        if self._trading_service is None:
            from .service.trading import DomesticTradingService

            self._trading_service = DomesticTradingService(auth=self.auth)
        return self._trading_service

    def _get_quote_service(self):
        if self._quote_service is None:
            from .service.quote import DomesticQuoteService

            self._quote_service = DomesticQuoteService(auth=self.auth)
        return self._quote_service

    def _get_chart_service(self):
        if self._chart_service is None:
            from .service.chart import DomesticChartService

            self._chart_service = DomesticChartService(auth=self.auth)
        return self._chart_service

    def buy(
        self,
        stock_code: str,
        quantity: int,
        price: float,
        price_type: str = "00",  # 지정가(00)
        credit_type: str = "000",  # 보통
        loan_date: str = "00000000",  # 일반주문
        order_condition: str = "0",  # 없음
    ) -> Dict[str, Any]:
        """국내 주식 매수 주문"""
        from .data.domestic.request import DomesticOrderRequest

        order_request = DomesticOrderRequest(
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            order_type="2",  # 매수
            price_type=price_type,
            credit_type=credit_type,
            loan_date=loan_date,
            order_condition=order_condition,
        )

        service = self._get_trading_service()
        return service.place_order(order_request)

    def sell(
        self,
        stock_code: str,
        quantity: int,
        price: float,
        price_type: str = "00",  # 지정가(00)
        credit_type: str = "000",  # 보통
        loan_date: str = "00000000",  # 일반주문
        order_condition: str = "0",  # 없음
    ) -> Dict[str, Any]:
        """국내 주식 매도 주문"""
        from .data.domestic.request import DomesticOrderRequest

        order_request = DomesticOrderRequest(
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            order_type="1",  # 매도
            price_type=price_type,
            credit_type=credit_type,
            loan_date=loan_date,
            order_condition=order_condition,
        )

        service = self._get_trading_service()
        return service.place_order(order_request)

    def cancel(self, order_no: int, stock_code: str, quantity: int) -> Dict[str, Any]:
        """국내 주식 주문 취소"""
        from .data.domestic.request import DomesticCancelOrderRequest

        cancel_request = DomesticCancelOrderRequest(
            original_order_no=order_no, stock_code=stock_code, quantity=quantity
        )

        service = self._get_trading_service()
        return service.cancel_order(cancel_request)

    def get_transaction_history(
        self,
        execution_status: str = "0",  # 체결여부 (0:전체, 1:체결, 2:미체결)
        order_type: str = "0",  # 매매구분 (0:전체, 1:매도, 2:매수)
        stock_type: str = "0",  # 종목구분 (0:전체)
        query_type: str = "0",  # 조회구분 (0:전체, 1:ELW, 2:ELW제외)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 거래 내역 조회"""
        from .data.domestic.request import DomesticTransactionHistoryRequest

        request = DomesticTransactionHistoryRequest(
            exec_yn=execution_status,
            bns_tp_code=order_type,
            isu_tp_code=stock_type,
            qry_tp=query_type,
        )

        service = self._get_trading_service()
        return service.get_transaction_history(
            request, cont_yn=cont_yn, cont_key=cont_key
        )

    def get_stock_balance(
        self,
        query_type: str = "0",  # 조회구분코드 (0:전체, 1:비상장제외, 2:비상장,코넥스,kotc 제외)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 잔고 조회"""
        from .data.domestic.request import DomesticBalanceRequest

        request = DomesticBalanceRequest(qry_tp_code=query_type)

        service = self._get_trading_service()
        return service.get_balance(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_deposit(self, cont_yn: str = "N", cont_key: str = None):
        """국내 예수금 조회"""
        service = self._get_trading_service()
        return service.get_deposit(cont_yn=cont_yn, cont_key=cont_key)

    def get_able_order_quantity(
        self,
        stock_code: str,
        price: float,
        order_type: str = "2",  # 매매구분 (1:매도, 2:매수)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주문 가능 수량 조회"""
        from .data.domestic.request import DomesticAbleOrderQuantityRequest

        request = DomesticAbleOrderQuantityRequest(
            stock_code=stock_code, price=price, bns_tp_code=order_type
        )

        service = self._get_trading_service()
        return service.get_able_order_quantity(
            request, cont_yn=cont_yn, cont_key=cont_key
        )

    # ===== 시세 관련 메소드 =====

    def get_stock_tickers(
        self,
        market_code: str = "J",  # 시장분류코드 (J:주식, E:ETF, EN:ETN)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 티커 조회"""
        from .data.domestic.request import DomesticQuoteRequest

        request = DomesticQuoteRequest(market_type=market_code)

        service = self._get_quote_service()
        return service.get_stock_tickers(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_stock_price(
        self,
        stock_code: str,
        market_code: str = "J",  # 시장분류코드 (J:주식, E:ETF, EN:ETN)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 시세 조회"""
        from .data.domestic.request import DomesticQuoteRequest

        request = DomesticQuoteRequest(market_type=market_code, stock_code=stock_code)

        service = self._get_quote_service()
        return service.get_stock_price(request, cont_yn=cont_yn, cont_key=cont_key)

    # ===== 차트 관련 메소드 =====

    def get_minute_chart(
        self,
        stock_code: str,
        start_date: str,
        time_interval: str = "60",  # 시간 간격 (60:1분, 300:5분, 600:10분 등)
        market_code: str = "J",  # 시장분류코드 (J:주식)
        adjust_price_yn: str = "0",  # 수정주가 사용 여부 (0:사용, 1:미사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 분봉 차트 조회"""
        from .data.domestic.request import DomesticMinuteChartRequest

        request = DomesticMinuteChartRequest(
            market_type=market_code,
            adjust_price_yn=adjust_price_yn,
            stock_code=stock_code,
            start_date=start_date,
            time_interval=time_interval,
        )

        service = self._get_chart_service()
        return service.get_minute_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_daily_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "J",  # 시장분류코드 (J:주식)
        adjust_price_yn: str = "0",  # 수정주가 사용 여부 (0:사용, 1:미사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 일봉 차트 조회"""
        from .data.domestic.request import DomesticDailyChartRequest

        request = DomesticDailyChartRequest(
            market_type=market_code,
            adjust_price_yn=adjust_price_yn,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
        )

        service = self._get_chart_service()
        return service.get_daily_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_weekly_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "J",  # 시장분류코드 (J:주식)
        adjust_price_yn: str = "0",  # 수정주가 사용 여부 (0:사용, 1:미사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 주봉 차트 조회"""
        from .data.domestic.request import DomesticWeeklyChartRequest

        request = DomesticWeeklyChartRequest(
            market_type=market_code,
            adjust_price_yn=adjust_price_yn,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            period="W",  # 주봉
        )

        service = self._get_chart_service()
        return service.get_weekly_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_monthly_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "J",  # 시장분류코드 (J:주식)
        adjust_price_yn: str = "0",  # 수정주가 사용 여부 (0:사용, 1:미사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 월봉 차트 조회"""
        from .data.domestic.request import DomesticMonthlyChartRequest

        request = DomesticMonthlyChartRequest(
            market_type=market_code,
            adjust_price_yn=adjust_price_yn,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            period="M",  # 월봉
        )

        service = self._get_chart_service()
        return service.get_monthly_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_yearly_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "J",  # 시장분류코드 (J:주식)
        adjust_price_yn: str = "0",  # 수정주가 사용 여부 (0:사용, 1:미사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """국내 주식 년봉 차트 조회"""
        from .data.domestic.request import DomesticWeeklyChartRequest

        request = DomesticWeeklyChartRequest(
            market_type=market_code,
            adjust_price_yn=adjust_price_yn,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            period="Y",  # 년봉
        )

        service = self._get_chart_service()
        return service.get_yearly_chart(request, cont_yn=cont_yn, cont_key=cont_key)


class OverseasAPI(BaseAPI):
    """해외 주식 API"""

    def __init__(self, app_key: str, app_secret_key: str, log_level=logging.INFO):
        super().__init__(app_key, app_secret_key, log_level)
        self._trading_service = None
        self._quote_service = None
        self._chart_service = None

    def _get_trading_service(self):
        if self._trading_service is None:
            from .service.trading import OverseasTradingService

            self._trading_service = OverseasTradingService(auth=self.auth)
        return self._trading_service

    def _get_quote_service(self):
        if self._quote_service is None:
            from .service.quote import OverseasQuoteService

            self._quote_service = OverseasQuoteService(auth=self.auth)
        return self._quote_service

    def _get_chart_service(self):
        if self._chart_service is None:
            from .service.chart import OverseasChartService

            self._chart_service = OverseasChartService(auth=self.auth)
        return self._chart_service

    # ===== 매매 관련 메소드 =====

    def buy(
        self,
        stock_code: str,
        quantity: int,
        price: float,
        price_type: str = "1",  # 지정가
        order_condition: str = "1",  # 일반
        trade_type: str = "0",  # 주문
        original_order_no: int = 0,  # 신규주문
    ) -> Dict[str, Any]:
        """해외 주식 매수 주문"""
        from .data.overseas.request import OverseasOrderRequest

        order_request = OverseasOrderRequest(
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            order_type="2",  # 매수
            price_type=price_type,
            order_condition=order_condition,
            trade_type=trade_type,
            original_order_no=original_order_no,
        )

        service = self._get_trading_service()
        return service.place_order(order_request)

    def sell(
        self,
        stock_code: str,
        quantity: int,
        price: float,
        price_type: str = "1",  # 지정가
        order_condition: str = "1",  # 일반
        trade_type: str = "0",  # 주문
        original_order_no: int = 0,  # 신규주문
    ) -> Dict[str, Any]:
        """해외 주식 매도 주문"""
        from .data.overseas.request import OverseasOrderRequest

        order_request = OverseasOrderRequest(
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            order_type="1",  # 매도
            price_type=price_type,
            order_condition=order_condition,
            trade_type=trade_type,
            original_order_no=original_order_no,
        )

        service = self._get_trading_service()
        return service.place_order(order_request)

    def cancel(self, order_no: int, stock_code: str, quantity: int) -> Dict[str, Any]:
        """해외 주식 주문 취소"""
        from .data.overseas.request import OverseasCancelOrderRequest

        cancel_request = OverseasCancelOrderRequest(
            original_order_no=order_no, stock_code=stock_code, quantity=quantity
        )

        service = self._get_trading_service()
        return service.cancel_order(cancel_request)

    def get_transaction_history(
        self,
        start_date: str = "",  # 조회시작일자 (YYYYMMDD)
        end_date: str = "",  # 조회종료일자 (YYYYMMDD)
        stock_code: str = "",  # 해외주식종목번호 (빈값은 전체 종목)
        order_type: str = "0",  # 해외주식매매구분코드 (0:전체, 1:매도, 2:매수)
        execution_status: str = "0",  # 주문체결구분코드 (0:전체, 1:체결, 2:미체결)
        sort_type: str = "0",  # 정렬구분코드 (0:역순, 1:정순)
        query_type: str = "0",  # 조회구분코드 (0:합산별, 1:건별)
        online_yn: str = "0",  # 온라인여부 (0:전체, Y:온라인, N:오프라인)
        opposite_order_yn: str = "0",  # 반대매매주문여부 (0:전체, Y:반대매매, N:일반주문)
        won_fcurr_type: str = "1",  # 원화외화구분코드 (1:원화, 2:외화)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 거래 내역 조회"""
        from .data.overseas.request import OverseasTransactionHistoryRequest

        # 해외 거래내역 조회는 날짜 지정이 없으면 당일로 설정
        if not qry_srt_dt and not qry_end_dt:
            from datetime import datetime

            today = datetime.now().strftime("%Y%m%d")
            qry_srt_dt = today
            qry_end_dt = today

        request = OverseasTransactionHistoryRequest(
            start_date=start_date,
            end_date=end_date,
            stock_code=stock_code,
            order_type=order_type,
            execution_status=execution_status,
            sort_type=sort_type,
            query_type=query_type,
            online_yn=online_yn,
            opposite_order_yn=opposite_order_yn,
            won_fcurr_type=won_fcurr_type,
        )

        service = self._get_trading_service()
        return service.get_transaction_history(
            request, cont_yn=cont_yn, cont_key=cont_key
        )

    def get_stock_balance(
        self,
        balance_type: str = "2",  # 처리구분코드 (1:외화잔고, 2:주식잔고상세, 3:주식잔고(국가별), 9:당일실현손익)
        cmsn_type: str = "2",  # 수수료구분코드 (0:전부 미포함, 1:매수제비용만 포함, 2:매수제비용+매도제비용)
        won_fcurr_type: str = "2",  # 원화외화구분코드 (1:원화, 2:외화)
        decimal_balance_type: str = "0",  # 소수점잔고구분코드 (0:전체, 1:일반, 2:소수점)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 잔고 조회"""
        from .data.overseas.request import OverseasBalanceRequest

        request = OverseasBalanceRequest(
            balance_type=balance_type,
            cmsn_type=cmsn_type,
            won_fcurr_type=won_fcurr_type,
            decimal_balance_type=decimal_balance_type,
        )

        service = self._get_trading_service()
        return service.get_balance(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_deposit(self, cont_yn: str = "N", cont_key: str = None):
        """해외 예수금 조회"""
        service = self._get_trading_service()
        return service.get_deposit(cont_yn=cont_yn, cont_key=cont_key)

    def get_able_order_quantity(
        self,
        stock_code: str,
        price: float,
        trx_type: str = "2",  # 처리구분코드 (1:매도, 2:매수)
        won_fcurr_type: str = "2",  # 원화외화구분코드 (1:원화, 2:외화)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주문 가능 수량 조회"""
        from .data.overseas.request import OverseasAbleOrderQuantityRequest

        request = OverseasAbleOrderQuantityRequest(
            stock_code=stock_code,
            price=price,
            order_type=trx_type,
            won_fcurr_type=won_fcurr_type,
        )

        service = self._get_trading_service()
        return service.get_able_order_quantity(
            request, cont_yn=cont_yn, cont_key=cont_key
        )

    # ===== 시세 관련 메소드 =====

    def get_stock_tickers(
        self,
        market_code: str = "NY",  # 시장 코드 (NY:뉴욕, NA:나스닥, AM:아멕스)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 티커 조회"""
        from .data.overseas.request import OverseasStockTickersRequest

        request = OverseasStockTickersRequest(market_code=market_code)

        service = self._get_quote_service()
        return service.get_stock_tickers(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_stock_price(
        self,
        stock_code: str,
        market_code: str = "FY",  # 시장 코드 (FY:뉴욕, FN:나스닥, FA:아멕스)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 시세 조회"""
        from .data.overseas.request import OverseasQuoteRequest

        request = OverseasQuoteRequest(market_code=market_code, stock_code=stock_code)

        service = self._get_quote_service()
        return service.get_stock_price(request, cont_yn=cont_yn, cont_key=cont_key)

    # ===== 차트 관련 메소드 =====

    def get_minute_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        time_interval: str = "60",  # 시간 간격 (60:1분, 300:5분, 600:10분 등)
        market_code: str = "FY",  # 시장 코드 (FY:뉴욕, FN:나스닥, FA:아멕스)
        adjust_price_yn: str = "1",  # 수정주가 사용 여부 (0:미사용, 1:사용)
        period_specified: str = "Y",  # 기간지정여부코드 (Y:기간지정, N:기간미지정)
        hour_class_code: str = "0",  # 입력시간구분코드 (항상 "0" 입력)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 분봉 차트 조회"""
        from .data.overseas.request import OverseasMinuteChartRequest

        request = OverseasMinuteChartRequest(
            market_type=market_code,
            adjust_price_yn=adjust_price_yn,
            period_specified=period_specified,
            hour_class_code=hour_class_code,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            chart_interval_code=time_interval,
        )

        service = self._get_chart_service()
        return service.get_minute_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_daily_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "FY",  # 시장 코드 (FY:뉴욕, FN:나스닥, FA:아멕스)
        adjust_price_yn: str = "1",  # 수정주가 사용 여부 (0:미사용, 1:사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 일봉 차트 조회"""
        from .data.overseas.request import OverseasDailyChartRequest

        request = OverseasDailyChartRequest(
            adjust_price_yn=adjust_price_yn,
            market_type=market_code,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
        )

        service = self._get_chart_service()
        return service.get_daily_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_weekly_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "FY",  # 시장 코드 (FY:뉴욕, FN:나스닥, FA:아멕스)
        use_adjust_price: str = "1",  # 수정주가 사용 여부 (0:미사용, 1:사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 주봉 차트 조회"""
        from .data.overseas.request import OverseasWeeklyChartRequest

        request = OverseasWeeklyChartRequest(
            market_type=market_code,
            use_adjust_price=use_adjust_price,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            period_div_code="W",  # 주봉
        )

        service = self._get_chart_service()
        return service.get_weekly_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_monthly_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "FY",  # 시장 코드 (FY:뉴욕, FN:나스닥, FA:아멕스)
        use_adjust_price: str = "1",  # 수정주가 사용 여부 (0:미사용, 1:사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 월봉 차트 조회"""
        from .data.overseas.request import OverseasWeeklyChartRequest

        request = OverseasWeeklyChartRequest(
            market_type=market_code,
            use_adjust_price=use_adjust_price,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            period_div_code="M",  # 월봉
        )

        service = self._get_chart_service()
        return service.get_monthly_chart(request, cont_yn=cont_yn, cont_key=cont_key)

    def get_yearly_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        market_code: str = "FY",  # 시장 코드 (FY:뉴욕, FN:나스닥, FA:아멕스)
        use_adjust_price: str = "1",  # 수정주가 사용 여부 (0:미사용, 1:사용)
        cont_yn: str = "N",
        cont_key: str = None,
    ) -> Dict[str, Any]:
        """해외 주식 년봉 차트 조회"""
        from .data.overseas.request import OverseasWeeklyChartRequest

        request = OverseasWeeklyChartRequest(
            market_type=market_code,
            use_adjust_price=use_adjust_price,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            period_div_code="Y",  # 년봉
        )

        service = self._get_chart_service()
        return service.get_yearly_chart(request, cont_yn=cont_yn, cont_key=cont_key)
