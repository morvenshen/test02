# economic_model.py
import pandas as pd

def calculate_single_breeding(
    supreme_price=1000,
    breeding_cycle=30,
    release_rate=0.7,
    item_prices={"姻缘丹":5, "饲料":5, "仙草":15},
    offspring_ratios={"普通":0.4, "稀有":0.3, "传说":0.2, "史诗":0.1},
    market_prices={"普通":20, "稀有":50, "传说":80, "史诗":160},
    transaction_fee=0.03
):
    # 计算单只至尊级繁殖数据
    item_costs = {
        "姻缘丹": breeding_cycle * item_prices["姻缘丹"],  # 动态计算道具消耗
        "饲料": (breeding_cycle + 7) * item_prices["饲料"],
        "仙草": 2 * item_prices["仙草"]
    }
    total_item_cost = sum(item_costs.values())
    
    # 后代数量计算（基于比例和繁殖周期）
    base_counts = {
        "普通": 12 * (breeding_cycle // 30),
        "稀有": 9 * (breeding_cycle // 30),
        "传说": 6 * (breeding_cycle // 30),
        "史诗": 3 * (breeding_cycle // 30)
    }
    
    offspring_counts = {
        level: int(base_counts[level] * offspring_ratios[level])
        for level in ["普通", "稀有", "传说", "史诗"]
    }
    
    # 实际流通量
    actual_circulation = {
        level: count * (1 - release_rate)
        for level, count in offspring_counts.items()
    }
    
    # 收益计算（用户总收益=单只收益×至尊数量）
    total_sales = sum(
        actual_circulation[level] * market_prices[level] * (1 - transaction_fee)
        for level in ["普通", "稀有", "传说", "史诗"]
    )
    
    user_net_profit = total_sales - 1000 - total_item_cost  # 单只收益扣除1000基础成本
    platform_income = supreme_price + sum(item_costs.values()) + sum(
        actual_circulation[level] * market_prices[level] * transaction_fee
        for level in ["普通", "稀有", "传说", "史诗"]
    )
    
    return {
        "单只成本": 1000 + total_item_cost,  # 固定1000基础成本
        "单只收益": user_net_profit,
        "平台收入": platform_income,
        "市场流通量": actual_circulation,
        "功德值": sum(actual_circulation[level] * market_prices[level] * 0.5 
                  for level in ["普通", "稀有", "传说", "史诗"])
    }

def calculate_phase_data(supreme_count=300, **kwargs):
    single_data = calculate_single_breeding(**kwargs)
    circulation = single_data["市场流通量"]
    return pd.DataFrame([{
        "平台总收益": single_data["平台收入"] * supreme_count,
        "用户总收益": (single_data["单只收益"]) * supreme_count,
        "市场流通量-普通": circulation["普通"] * supreme_count,
        "市场流通量-稀有": circulation["稀有"] * supreme_count,
        "市场流通量-传说": circulation["传说"] * supreme_count,
        "市场流通量-史诗": circulation["史诗"] * supreme_count,
        "繁殖周期(天)": kwargs.get("breeding_cycle", 30),
        "至尊数量": supreme_count
    }])
