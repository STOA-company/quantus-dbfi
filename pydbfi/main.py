import logging
from .api import *

class DBFI():
    """
    사용 예:
        dbfi = DBFI(app_key="YOUR_APP_KEY", app_secret_key="YOUR_SECRET_KEY")
        
        # 국내 매수 주문 실행
        dbfi.buy(region="domestic", stock_code="005930", quantity=10, price=50000)
        
        # 해외 매수 주문 실행
        dbfi.buy(region="overseas", stock_code="AAPL", quantity=5, price=150.0)
        
        # 국내 선물옵션 잔고 조회
        dbfi.get_domestic_futures_balance()

        # VIP 블랙스완 업데이트
        dbfi.update_vip_blackswans()
        
        # 세션 종료
        dbfi.close()
    """
    def __init__(
        self, 
        app_key: str, 
        app_secret_key: str, 
        log_level=logging.INFO, 
        headers: dict = {}, 
        token: str = None, 
        token_type: str = None,
        expire_in: datetime = None
    ):
        _oauth = OAuth(
            appkey=app_key,
            appsecretkey=app_secret_key,
            headers=headers,
            token=token,
            token_type=token_type,
            expire_in=expire_in,
        )
        self.domestic = DomesticAPI(_oauth, log_level)
        self.overseas = OverseasAPI(_oauth, log_level)
        self.domestic_futures = DomesticFuturesAPI(_oauth, log_level)
    
    def close(self):
        self.domestic.close()
        self.overseas.close()
        self.domestic_futures.close()
    
    def buy(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.buy(**kwargs)
        elif region == 'overseas':
            return self.overseas.buy(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def sell(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.sell(**kwargs)
        elif region == 'overseas':
            return self.overseas.sell(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def cancel(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.cancel(**kwargs)
        elif region == 'overseas':
            return self.overseas.cancel(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_transaction_history(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_transaction_history(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_transaction_history(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def post_trading_history(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.post_trading_history(**kwargs)
        else:
            raise ValueError("region은 'domestic' 여야 합니다.")

    def post_daily_trade_report(self, region: str, **kwargs):
        """국내 주식 일일 거래 보고서 조회
        
        Args:
            region: 지역 ('domestic')
            bns_dt: 거래일자 (YYYYMMDD) - 필수
            **kwargs: isu_no (종목번호), cont_yn, cont_key 등
        """
        region = region.lower()
        if region == 'domestic':
            return self.domestic.post_daily_trade_report(**kwargs)
        else:
            raise ValueError("region은 'domestic' 여야 합니다.")

    
    def get_stock_balance(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_stock_balance(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_stock_balance(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_deposit(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_deposit(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_deposit(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_able_order_quantity(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_able_order_quantity(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_able_order_quantity(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_stock_tickers(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_stock_tickers(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_stock_tickers(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_stock_price(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_stock_price(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_stock_price(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
        
    def get_order_book(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_order_book(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_order_book(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_minute_chart(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_minute_chart(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_minute_chart(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_daily_chart(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_daily_chart(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_daily_chart(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_weekly_chart(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_weekly_chart(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_weekly_chart(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_monthly_chart(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_monthly_chart(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_monthly_chart(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_yearly_chart(self, region: str, **kwargs):
        region = region.lower()
        if region == 'domestic':
            return self.domestic.get_yearly_chart(**kwargs)
        elif region == 'overseas':
            return self.overseas.get_yearly_chart(**kwargs)
        else:
            raise ValueError("region은 'domestic' 또는 'overseas'여야 합니다.")
    
    def get_domestic_futures_balance(self, **kwargs):
        """국내 선물옵션 잔고 조회"""
        return self.domestic_futures.get_futures_balance(**kwargs)

