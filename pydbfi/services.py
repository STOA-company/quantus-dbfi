from .main import *

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
            "평균단가": round(r["PchsAmt"] / r["BalQty0"], 2),
            "보유수량": r["BalQty0"],
            "현재가": r["NowPrc"],
            "전일대비등락율": float(dbfi.get_stock_price(region=region, stock_code=r['IsuNo'])["Out"]["PrdyCtrt"]),
            "country": "KR",
        } for _, r in enumerate(domestic_balance["Out1"])
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
    
def get_balance_overseas(dbfi: DBFI):
    region = "overseas"
    # overseas_deposit = dbfi.get_deposit(region=region)
    overseas_balance = dbfi.get_stock_balance(region=region)
    
    able_order_quantity = dbfi.get_able_order_quantity(
        region="overseas", 
        stock_code="AAPL",
        price=1
    )
    balances = {"주문가능현금": float(able_order_quantity["Out"]["AstkOrdAbleAmt"])} # 주문가능달러
    
    if not isinstance(overseas_balance, dict) or overseas_balance.get("rsp_cd") != "00000":
        # 보유종목 없음
        stocks = []
        balances["유가평가금액합계"] = 0
    else:
        # TODO :: 보유종목 잔고 체크
        stocks = []
        balances["유가평가금액합계"] = 0
        
    return dict(
        stocks=stocks,
        balances=balances
    )