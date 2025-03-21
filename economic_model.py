# economic_model.py
import pandas as pd

def calculate_single_breeding(
    breeding_cycle=30,
    release_rate=0.7,
    item_prices={"姻缘丹":5, "饲料":5, "仙草":15},
    offspring_ratios={"普通":0.4, "稀有":0.3, "传说":0.2, "史诗":0.1},
    market_prices={"普通":20, "稀有":50, "传说":80, "史诗":160},
    transaction_fee=0.03,
    supreme_price=1000
):
    # 道具成本计算（精确到浮点数）
    item_costs = {
        "姻缘丹": breeding_cycle * item_prices["姻缘丹"],
        "饲料": (breeding_cycle + 7) * item_prices["饲料"],
        "仙草": 2 * item_prices["仙草"]
    }
    total_item_cost = sum(item_costs.values())
    
    # 后代基础数量计算（保留小数）
    cycle_multiplier = breeding_cycle / 30  # 改用精确比例
    base_counts = {
        "普通": 12 * cycle_multiplier,
        "稀有": 9 * cycle_multiplier,
        "传说": 6 * cycle_multiplier,
        "史诗": 3 * cycle_multiplier
    }
    
    # 实际后代数量（四舍五入代替取整）
    offspring_counts = {
        level: round(base_counts[level] * offspring_ratios[level])
        for level in ["普通", "稀有", "传说", "史诗"]
    }
    
    # 后代总销售额（使用精确计算）
    total_offspring_sales = sum(
        count * market_prices[level]
        for level, count in offspring_counts.items()
    )
    
    # 交易手续费计算
    transaction_fee_total = total_offspring_sales * transaction_fee
    
    # 用户净收益计算（修正公式）
    user_net_profit = total_offspring_sales - (supreme_price + total_item_cost + transaction_fee_total)
    
    return {
        "单只成本": supreme_price + total_item_cost,
        "单只收益": user_net_profit,
        "后代总销售额": total_offspring_sales,
        "交易手续费": transaction_fee_total,
        "总后代数量": sum(offspring_counts.values())
    }

def calculate_phase_data(supreme_count=300, **kwargs):
    single_data = calculate_single_breeding(**kwargs)
    
    # 总费用计算
    supreme_total = kwargs["supreme_price"] * supreme_count
    total_item_cost = (single_data["单只成本"] - kwargs["supreme_price"]) * supreme_count  # 精确道具成本
    
    # 总收益计算
    total_offspring_sales = single_data["后代总销售额"] * supreme_count
    total_fee = total_offspring_sales * kwargs["transaction_fee"]  # 直接计算总手续费
    
    # 用户净收益（最终正确公式）
    user_total_profit = total_offspring_sales - supreme_total - total_item_cost - total_fee
    
    return pd.DataFrame([{
        "至尊级总费用": supreme_total,
        "道具总消耗": total_item_cost,
        "后代总销售额": total_offspring_sales,
        "总交易手续费": total_fee,
        "用户总成本": supreme_total + total_item_cost,
        "购买至尊级用户净收益": user_total_profit,
        "平台总收益": supreme_total + total_item_cost + total_fee,
        # 其他字段保持不变...
    }])
