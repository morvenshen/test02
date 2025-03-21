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
    # 精确道具成本计算
    item_cost = (
        breeding_cycle * item_prices["姻缘丹"] +
        (breeding_cycle + 7) * item_prices["饲料"] +
        2 * item_prices["仙草"]
    )
    
    # 后代数量计算（精确浮点运算）
    cycle_ratio = breeding_cycle / 30
    base_counts = {
        "普通": 12 * cycle_ratio,
        "稀有": 9 * cycle_ratio,
        "传说": 6 * cycle_ratio,
        "史诗": 3 * cycle_ratio
    }
    
    # 后代数量分配（确保最小数量）
    offspring_counts = {
        level: max(round(base_counts[level] * offspring_ratios[level]), 1)
        for level in ["普通", "稀有", "传说", "史诗"]
    }
    
    # 销售额计算（包含所有后代）
    total_sales = sum(
        count * market_prices[level]
        for level, count in offspring_counts.items()
    )
    
    # 净收益计算（关键修正）
    transaction_cost = total_sales * transaction_fee
    net_profit = total_sales - supreme_price - item_cost - transaction_cost
    
    return {
        "单只总成本": supreme_price + item_cost,
        "单只销售额": total_sales,
        "单只净收益": net_profit,
        "交易手续费": transaction_cost,
        "总后代数": sum(offspring_counts.values())
    }

def calculate_phase_data(supreme_count=300, **kwargs):
    single = calculate_single_breeding(**kwargs)
    
    # 总收益计算（修正量级错误）
    total_sales = single["单只销售额"] * supreme_count
    total_cost = single["单只总成本"] * supreme_count
    
    # 手续费应基于总销售额重新计算（关键修正）
    total_fee = total_sales * kwargs["transaction_fee"]
    
    net_profit = total_sales - total_cost - total_fee
    
    return pd.DataFrame([{
        "至尊总投入": total_cost,
        "后代总销售额": total_sales,
        "总交易手续费": total_fee,
        "购买至尊级用户净收益": net_profit,
        "平台总收益": total_cost + total_fee,
        "单只收益率": net_profit / total_cost * 100,
        "有效后代数量": single["总后代数"] * supreme_count,
    }])
