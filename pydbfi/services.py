from .main import *
import pandas as pd
from datetime import datetime, timedelta

def get_balance_domestic(dbfi: DBFI):
    region = "domestic"
    domestic_deposit = dbfi.get_deposit(region=region)
    domestic_balance = dbfi.get_stock_balance(region=region)

    balance = domestic_balance["Out"]
    stocks = {
        _: {
            "종목코드": r['IsuNo'][1:],
            "종목명": r["IsuNm"],
            "평가손익률": float(r['Ernrat']) * 100,
            "매입금액": r["PchsAmt"],
            "평가금액": r["EvalAmt"],
            "평가손익": r["EvalPnlAmt"],
            "평균단가": round(r["PchsAmt"] / r["BalQty0"], 2) if r["BalQty0"] > 0 else 0,
            "보유수량": r["BalQty0"],
            "현재가": float(r["NowPrc"]),
            "전일대비등락율": float(dbfi.get_stock_price(region=region, stock_code=r['IsuNo'])["Out"]["PrdyCtrt"]),
            "country": "KR",
        } for _, r in enumerate(domestic_balance["Out1"]) if r["BalQty0"] > 0
    }

    deposit = domestic_deposit["Out1"]
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
        balances=balances
    )
    
def get_balance_overseas(dbfi: DBFI, is_integrated: bool = False):
    region = "overseas"
    # overseas_deposit = dbfi.get_deposit(region=region)
    overseas_balance = dbfi.get_stock_balance(region=region)
    
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
    if isinstance(overseas_balance, dict) and overseas_balance.get("rsp_cd") == "00000":
        out2_data = overseas_balance.get("Out2", [])
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
        # balance = overseas_balance.get("Out1", [])
        # if balance:
        #     _balance = balance[0] # TODO :: 국가별 분기 필요
        #     balances.update(
        #         {
        #             "예수금": round(float(_balance["FcurrDps"]), 2),
        #             "익일정산금액": round(float(_balance["AstkOrdAbleAmt"]), 2),
        #             "가수도정산금액": round(float(_balance["AstkMnyoutAbleAmt"]), 2),
        #             "평가금": round(float(_balance["AstkAssetEvalAmt"]), 2),
        #             "평가손익률": round(float(_balance["ErnRat"]), 2),
        #             "유가평가금액합계": round(float(_balance["AstkEvalAmt"]), 2),
        #             "환율": round(float(_balance['Xchrat']), 2),
        #             "평균환율": round(float(_balance['AvrXchrat']), 2),
        #             "매입금액합계": round(sum([float(r["AstkBuyAmt"]) for r in overseas_balance.get("Out2", [])]), 2),
        #             "손익금액합계": round(sum([float(r["AstkEvalPnlAmt"]) for r in overseas_balance.get("Out2", [])]), 2),
                    
        #             # TODO :: 당일 매매금액
        #             # "금일매수금액": 0,
        #             # "금일매도금액": 0,
        #         }
        #     )
        if out2_data:
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
    
    if trans_history["rsp_cd"] != "00000":
        # 조회 실패
        buy_exec_amts, sell_exec_amts = 0, 0
    else:
        df = pd.DataFrame(trans_history["Out"])
        df["exec_dt"] = pd.to_datetime(df["AstkExecDttm"].str[:14])
        exec_df = df[
                (df["exec_dt"]>=datetime(year=_trading_datetime.year, month=_trading_datetime.month, day=_trading_datetime.day, hour=22)) # 전일 개장시간
                & (df["exec_dt"]<=datetime(year=trading_datetime.year, month=trading_datetime.month, day=trading_datetime.day, hour=6)) # 익일 폐장시간
            ]
        buy_exec_amts, sell_exec_amts \
            = exec_df[exec_df["AstkBnsTpCode"]=="2"]["WonAmt3"].sum(), exec_df[exec_df["AstkBnsTpCode"]=="1"]["WonAmt3"].sum() # 원화 환산 체결 금액
            
    return dict(
        buy_exec_amts=buy_exec_amts,
        sell_exec_amts=sell_exec_amts,
    )