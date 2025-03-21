# economic_model.py
import pandas as pd

def calculate_single_breeding(
    breeding_cycle=30,
    release_rate=0.7,
    item_prices={"姻缘丹":5, "饲料":5, "仙草":15},
    market_prices={"普通":20, "稀有":50, "传说":80, "史诗":160},
    transaction_fee=0.03,
    supreme_price=1000
):
    """严格遵循文档产量规则，保留参数调节能力"""
    # 固定后代产量（文档第1章）
    fixed_offspring = {
        "普通": 12 * (breeding_cycle / 30),  # 周期比例调整
        "稀有": 9 * (breeding_cycle / 30),
        "传说": 6 * (breeding_cycle / 30),
        "史诗": 3 * (breeding_cycle / 30)
    }
    
    # 道具成本计算（文档第1章公式）
    item_cost = (
        30 * item_prices["姻缘丹"] +  # 姻缘丹30颗
        37 * item_prices["饲料"] +    # 饲料37份
        2 * item_prices["仙草"]      # 仙草2份
    )
    
    # 后代销售额计算（使用实际市场价格）
    total_sales = sum(
        count * market_prices[level]
        for level, count in fixed_offspring.items()
    )
    
    # 精确成本计算
    transaction_cost = total_sales * transaction_fee
    net_profit = total_sales - supreme_price - item_cost - transaction_cost
    
    return {
        "单只总成本": supreme_price + item_cost,
        "单只销售额": total_sales,
        "单只净收益": net_profit,
        "交易手续费": transaction_cost,
        "后代分布": fixed_offspring
    }

def calculate_phase_data(supreme_count=300, **kwargs):
    single = calculate_single_breeding(**kwargs)
    
    # 总量计算
    total_sales = single["单只销售额"] * supreme_count
    total_cost = single["单只总成本"] * supreme_count
    total_fee = total_sales * kwargs["transaction_fee"]
    
    # 健康度指标（文档第4章）
    health_metrics = {
        "market_digestion": 0.7,
        "user_retention": 0.75,
        "inflation_rate": 0.0
    }
    
    return pd.DataFrame([{
        "至尊数量": supreme_count,
        "总销售额": total_sales,
        "至尊总成本": total_cost,
        "交易手续费": total_fee,
        "用户净收益": total_sales - total_cost - total_fee,
        "平台总收益": total_cost + total_fee,
        "市场消化率": health_metrics["market_digestion"],
        "用户留存率": health_metrics["user_retention"],
        **{f"{k}后代": v*supreme_count for k,v in single["后代分布"].items()}
    }])
