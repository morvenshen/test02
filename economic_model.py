# economic_model.py
import pandas as pd

def calculate_single_breeding(
    supreme_price=1000,
    release_rate=0.7,
    item_prices={"姻缘丹":5, "饲料":5, "仙草":15},
    offspring_ratios={"普通":0.4, "稀有":0.3, "传说":0.2, "史诗":0.1},
    market_prices={"普通":20, "稀有":50, "传说":80, "史诗":160},
    transaction_fee=0.03
):
    # 计算单只至尊级繁殖数据
    item_costs = {
        "姻缘丹": 30 * item_prices["姻缘丹"],
        "饲料": 37 * item_prices["饲料"],
        "仙草": 2 * item_prices["仙草"]
    }
    total_item_cost = sum(item_costs.values())
    
    # 后代数量计算（基于比例）
    offspring_counts = {
        "普通": int(12 * offspring_ratios["普通"]),
        "稀有": int(9 * offspring_ratios["稀有"]),
        "传说": int(6 * offspring_ratios["传说"]),
        "史诗": int(3 * offspring_ratios["史诗"])
    }
    
    # 实际流通量
    actual_circulation = {
        level: count * (1 - release_rate) for level, count in offspring_counts.items()
    }
    
    # 收益计算
    total_sales = sum(
        actual_circulation[level] * market_prices[level] * (1 - transaction_fee)
        for level in ["普通", "稀有", "传说", "史诗"]
    )
    
    user_net_profit = total_sales - supreme_price - total_item_cost
    platform_income = supreme_price + sum(item_costs.values()) + sum(
        actual_circulation[level] * market_prices[level] * transaction_fee
        for level in ["普通", "稀有", "传说", "史诗"]
    )
    
    return {
        "单只成本": supreme_price + total_item_cost,
        "单只收益": user_net_profit,
        "平台收入": platform_income,
        "市场流通量": actual_circulation,
        "功德值": sum(actual_circulation[level] * market_prices[level] * 0.5 
                  for level in ["普通", "稀有", "传说", "史诗"])
    }

def calculate_phase_data(supreme_count=300, **kwargs):
    single_data = calculate_single_breeding(**kwargs)
    return pd.DataFrame([{
        "平台总收益": single_data["平台收入"] * supreme_count,
        "用户总收益": single_data["单只收益"] * supreme_count,
        "市场总流通量": sum(single_data["市场流通量"].values()) * supreme_count,
        "至尊数量": supreme_count
    }])
