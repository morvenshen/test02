# economic_model.py
import pandas as pd

def calculate_single_breeding(
    breeding_cycle=30,
    release_rate=0.7,
    item_prices={"姻缘丹":5, "饲料":5, "仙草":15},
    market_prices={"普通":20, "稀有":50, "传说":80, "史诗":160},
    transaction_fee=0.03,
    supreme_price=1000,
    price_multiplier=1.0,  # 新增价格倍率
    item_discount=1.0      # 新增道具折扣
):
    """增加收益优化参数"""
    # 应用价格倍率
    adjusted_prices = {k:v*price_multiplier for k,v in market_prices.items()}
    
    # 固定后代产量
    fixed_offspring = {
        "普通": 12 * (breeding_cycle / 30),
        "稀有": 9 * (breeding_cycle / 30),
        "传说": 6 * (breeding_cycle / 30),
        "史诗": 3 * (breeding_cycle / 30)
    }
    
    # 应用道具折扣
    item_cost = (
        30 * item_prices["姻缘丹"] * item_discount +
        37 * item_prices["饲料"] * item_discount +
        2 * item_prices["仙草"] * item_discount
    )
    
    total_sales = sum(count*adjusted_prices[level] for level, count in fixed_offspring.items())
    transaction_cost = total_sales * transaction_fee
    net_profit = total_sales - supreme_price - item_cost - transaction_cost
    
    return {
        "单只总成本": supreme_price + item_cost,
        "单只销售额": total_sales,
        "单只净收益": net_profit,
        "交易手续费": transaction_cost,
        "后代分布": fixed_offspring,
        "收益率": net_profit / (supreme_price + item_cost)  # 新增收益率指标
    }

def calculate_phase_data(supreme_count=300, **kwargs):
    single = calculate_single_breeding(**kwargs)
    
    total_sales = single["单只销售额"] * supreme_count
    total_cost = single["单只总成本"] * supreme_count
    total_fee = total_sales * kwargs.get("transaction_fee", 0.03)
    
    return pd.DataFrame([{
        "至尊数量": supreme_count,
        "总销售额": total_sales,
        "至尊总成本": total_cost,
        "交易手续费": total_fee,
        "用户净收益": total_sales - total_cost - total_fee,
        "平台总收益": total_cost + total_fee,
        "用户收益率": (total_sales - total_cost - total_fee) / total_cost * 100,  # 新增
        "市场消化率": 0.7,
        "用户留存率": 0.75,
        **{f"{k}后代": v*supreme_count for k,v in single["后代分布"].items()}
    }])
