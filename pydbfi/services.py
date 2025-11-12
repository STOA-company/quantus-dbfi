from .main import *
import pandas as pd
from datetime import datetime, timedelta

def get_balance_domestic(dbfi: DBFI):
    region = "domestic"
    domestic_balance = dbfi.get_stock_balance(region=region)
    
    out1_data = []
    if isinstance(domestic_balance, dict) and domestic_balance["rsp_cd"] == "00000":
        balance = domestic_balance["Out"]
        out1_data = domestic_balance["Out1"]
    elif isinstance(domestic_balance, list):
        balance = domestic_balance[0]["Out"]
        for r in domestic_balance:
            if r["rsp_cd"] == "00000":
                out1_data.extend(r["Out1"])
    
    stocks = {}
    for i, r in enumerate(out1_data):
        if r["BalQty0"] > 0:
            try:
                previous_ror = float(dbfi.get_stock_price(region=region, stock_code=r['IsuNo'])["Out"]["PrdyCtrt"])
            except:
                previous_ror = 0
            stocks[i] = {
                "종목코드": r['IsuNo'][1:],
                "종목명": r["IsuNm"],
                "평가손익률": float(r['Ernrat']) * 100,
                "매입금액": r["PchsAmt"],
                "평가금액": r["EvalAmt"],
                "평가손익": r["EvalPnlAmt"],
                "평균단가": round(r["PchsAmt"] / r["BalQty0"], 2) if r["BalQty0"] > 0 else 0,
                "보유수량": r["BalQty0"],
                "현재가": float(r["NowPrc"]),
                "전일대비등락율": previous_ror,
                "country": "KR",
            }

    domestic_deposit = dbfi.get_deposit(region=region)
    deposit = domestic_deposit["Out1"]
    # TODO :: 예외처리 필요
    # if "Out1" in domestic_deposit:
    #     deposit = domestic_deposit["Out1"]
    # else:
    #     # 예외케이스
    #     return dict(
    #         stocks=stocks,
    #         balances=balances,
    #         **domestic_deposit
    #     )
    balances = {
        "예수금": deposit["DpsBalAmt"],
        "익일정산금액": deposit["PrsmptDpsD1"],
        "가수도정산금액": deposit["PrsmptDpsD2"],
        "평가금": balance["DpsastAmt"],
        "평가손익률": round(float(balance["TotErnrat"]) * 2),
        "매입금액합계": balance["TotBuyAmt"],
        "유가평가금액합계": balance["TotEvalAmt"],
        "손익금액합계": balance["TotEvalPnlAmt"],
        "금일매수금액": balance["ThdayBuyAmt"],
        "금일매도금액": balance["ThdaySellAmt"],
        "주문가능현금": balance["Dps2"],
    }
    
    return dict(
        stocks=stocks,
        balances=balances,
        **domestic_deposit
    )
    
def get_balance_overseas(dbfi: DBFI, is_integrated: bool = False):
    region = "overseas"
    
    able_order_quantity = dbfi.get_able_order_quantity(
        region="overseas", 
        stock_code="AAPL",
        order_type="2", # 매수가능금액 조회
        price=1
    )
    
    exec_amts = get_execute_amounts_overseas(dbfi, datetime.now(pytz.timezone('Asia/Seoul')))
    balances = {
        "주문가능현금": float(able_order_quantity["Out"]["AstkOrdAbleAmt0" if is_integrated else "AstkOrdAbleAmt"]),
        "평가손익률": 0,
        "매입금액합계": 0,
        "유가평가금액합계": 0,
        "손익금액합계": 0,
        "금일매수금액": exec_amts["buy_exec_amts"],
        "금일매도금액": exec_amts["sell_exec_amts"],
    }
    
    stocks = {}
    out2_data = []
    overseas_balance = dbfi.get_stock_balance(region=region)
    if isinstance(overseas_balance, dict) and overseas_balance.get("rsp_cd") == "00000":
        out2_data = overseas_balance.get("Out2", [])
    elif isinstance(overseas_balance, list):
        for r in overseas_balance:
            if isinstance(r, dict) and r.get("rsp_cd") == "00000" and r.get("Out2"):
                out2_data.extend(r.get("Out2"))
    
    if out2_data:
        stocks = {
            _: {
                "종목코드": r['SymCode'],
                "종목명": r["AstkHanglIsuNm"],
                "평가손익률": round(float(r['EvalPnlRat']), 2),
                "매입금액": round(float(r["AstkBuyAmt"]), 2),
                "평가금액": round(float(r["AstkEvalAmt"]), 2),
                "평가손익": round(float(r["AstkEvalPnlAmt"]), 2),
                "평균단가": round(float(r["AstkAvrPchsPrc"]), 2),
                "보유수량": int(float(r["AstkExecBaseQty"])),
                "현재가": round(float(r["AstkNowPrc"]), 2),
                "전일대비등락율": round(float(r["AstkUpdnRat"]), 2),
                "country": "US",
            } for _, r in enumerate(out2_data)
        }
        buy_amts, eval_amts, pnl_amts = (
            round(sum(float(r[key]) for r in out2_data), 2)
            for key in ("AstkBuyAmt", "AstkEvalAmt", "AstkEvalPnlAmt")
        )
        balances.update(
            {
                "매입금액합계": buy_amts,
                "유가평가금액합계": eval_amts,
                "손익금액합계": pnl_amts,
                "평가손익률": round((pnl_amts / buy_amts) * 100, 2) if buy_amts > 0 else 0
            }
        )
        
    return dict(
        stocks=stocks,
        balances=balances
    )
    
def get_execute_amounts_overseas(
    dbfi: DBFI,
    trading_datetime: datetime
):
    _trading_datetime = trading_datetime - timedelta(days=1)
    end_date = trading_datetime.strftime("%Y%m%d")
    start_date = _trading_datetime.strftime("%Y%m%d")
    trans_history = dbfi.get_transaction_history("overseas", start_date=start_date, end_date=end_date)
    
    def get_exec_amts(trans_history: dict, buy_exec_amts: float, sell_exec_amts: float):
        if trans_history["rsp_cd"] == "00000":
            # 전일 개장시간과 당일 폐장시간 설정
            start_time = datetime(year=_trading_datetime.year, month=_trading_datetime.month, 
                                day=_trading_datetime.day, hour=22)
            end_time = datetime(year=trading_datetime.year, month=trading_datetime.month, 
                            day=trading_datetime.day, hour=6)
            
            # 거래 내역 직접 순회하며 계산
            for transaction in trans_history["Out"]:
                # 날짜시간 파싱 (AstkExecDttm의 처음 14자리)
                exec_dt_str = transaction["AstkExecDttm"][:14]
                if len(exec_dt_str) == 14:
                    exec_dt = datetime(
                        year=int(exec_dt_str[0:4]),
                        month=int(exec_dt_str[4:6]),
                        day=int(exec_dt_str[6:8]),
                        hour=int(exec_dt_str[8:10]),
                        minute=int(exec_dt_str[10:12]),
                        second=int(exec_dt_str[12:14])
                    )
                    
                    # 시간 범위 내 거래만 필터링
                    if start_time <= exec_dt <= end_time:
                        # 매수(2) 또는 매도(1) 금액 합산
                        if transaction["AstkBnsTpCode"] == "2":  # 매수
                            buy_exec_amts += float(transaction["WonAmt3"])
                        elif transaction["AstkBnsTpCode"] == "1":  # 매도
                            sell_exec_amts += float(transaction["WonAmt3"])
        return buy_exec_amts, sell_exec_amts
            
    buy_exec_amts, sell_exec_amts = 0, 0
    if isinstance(trans_history, list):
        for _trans_history in trans_history:
            buy_exec_amts, sell_exec_amts = get_exec_amts(_trans_history, buy_exec_amts, sell_exec_amts)
    elif isinstance(trans_history, dict):
        buy_exec_amts, sell_exec_amts = get_exec_amts(trans_history, buy_exec_amts, sell_exec_amts)
    
    return dict(
        buy_exec_amts=buy_exec_amts,
        sell_exec_amts=sell_exec_amts,
    )
