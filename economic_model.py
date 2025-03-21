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
    # 计算单只至尊级繁殖数据
    # 道具成本计算
    item_costs = {
        "姻缘丹": breeding_cycle * item_prices["姻缘丹"],
        "饲料": (breeding_cycle + 7) * item_prices["饲料"],
        "仙草": 2 * item_prices["仙草"]
    }
    total_item_cost = sum(item_costs.values())
    
    # 后代基础数量计算
    base_counts = {
        "普通": 12 * (breeding_cycle // 30),
        "稀有": 9 * (breeding_cycle // 30),
        "传说": 6 * (breeding_cycle // 30),
        "史诗": 3 * (breeding_cycle // 30)
    }
    
    # 实际后代数量（考虑繁殖比例）
    offspring_counts = {
        level: int(base_counts[level] * offspring_ratios[level])
        for level in ["普通", "稀有", "传说", "史诗"]
    }
    
    # 市场流通量（考虑放生率）
    actual_circulation = {
        level: count * (1 - release_rate)
        for level, count in offspring_counts.items()
    }
    
    # 后代总销售额（不含手续费）
    total_offspring_sales = sum(
        actual_circulation[level] * market_prices[level]
        for level in ["普通", "稀有", "传说", "史诗"]
    )
    
    # 交易手续费计算
    transaction_fee_total = total_offspring_sales * transaction_fee
    
    # 用户净收益计算
    user_net_profit = (total_offspring_sales - transaction_fee_total) - supreme_price - total_item_cost
    
    return {
        "单只成本": supreme_price + total_item_cost,
        "单只收益": user_net_profit,
        "道具成本": total_item_cost,
        "后代总销售额": total_offspring_sales,
        "交易手续费": transaction_fee_total,
        "市场流通量": actual_circulation,
        "总后代数量": sum(offspring_counts.values())
    }

def calculate_phase_data(supreme_count=300, **kwargs):
    single_data = calculate_single_breeding(**kwargs)
    
    # 至尊级总销售额
    supreme_sales = kwargs.get("supreme_price", 1000) * supreme_count
    
    # 道具总消耗
    total_item_cost = single_data["道具成本"] * supreme_count
    
    # 后代总销售额
    total_offspring_sales = single_data["后代总销售额"] * supreme_count
    
    # 总交易手续费
    total_fee = single_data["交易手续费"] * supreme_count
    
    # 用户总成本
    user_total_cost = (kwargs.get("supreme_price", 1000) + single_data["道具成本"]) * supreme_count + total_fee
    
    # 平台总收益
    platform_profit = supreme_sales + total_item_cost + total_fee
    
    return pd.DataFrame([{
        "新增后代总数": single_data["总后代数量"] * supreme_count,
        "至尊级销售额": supreme_sales,
        "道具总消耗": total_item_cost,
        "总交易手续费": total_fee,
        "平台总收益": platform_profit,
        "后代总销售额": total_offspring_sales,
        "用户总成本": user_total_cost,
        "用户总净收益": (total_offspring_sales - total_fee) - user_total_cost + total_fee,  # 修正计算
        "市场流通量-普通": single_data["市场流通量"]["普通"] * supreme_count,
        "市场流通量-稀有": single_data["市场流通量"]["稀有"] * supreme_count,
        "市场流通量-传说": single_data["市场流通量"]["传说"] * supreme_count,
        "市场流通量-史诗": single_data["市场流通量"]["史诗"] * supreme_count,
        "繁殖周期(天)": kwargs.get("breeding_cycle", 30),
        "至尊数量": supreme_count
    }])
