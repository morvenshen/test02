# economic_model.py
import pandas as pd

class EconomicModel:
    @staticmethod
    def calculate_phase(supreme_count=300, phase_month=1):
        """
        严格遵循参考数值表的计算规则
        :param supreme_count: 至尊级投放量
        :param phase_month: 当前阶段月份(1-6)
        :return: 包含完整经济数据的DataFrame
        """
        # 阶段参数校验
        if phase_month < 1 or phase_month > 6:
            raise ValueError("阶段月份必须在1-6之间")

        # 基础参数（来自文档第1章）
        BASE_PRODUCTION = {
            "普通": 12, "稀有": 9, "传说": 6, "史诗": 3  # 固定产量
        }
        ITEM_COST_PER = 365  # 固定道具成本
        
        # 阶段参数（来自文档第2章）
        phase_params = {
            1: {"release": 300, "dynamic_price": 55},
            2: {"release": 100, "dynamic_price": 55},
            3: {"release": 30, "dynamic_price": 55},
            6: {"release": 30, "dynamic_price": 55}
        }
        params = phase_params.get(phase_month, phase_params[6])

        # 核心计算（来自文档第2章首月经济测算）
        total_offspring = sum(BASE_PRODUCTION.values()) * supreme_count
        total_sales = total_offspring * params["dynamic_price"]
        
        # 成本计算
        supreme_cost = 1000 * supreme_count
        item_cost = ITEM_COST_PER * supreme_count
        transaction_fee = total_sales * 0.03
        
        # 收益计算
        platform_income = supreme_cost + item_cost + transaction_fee
        user_profit = total_sales - (supreme_cost + item_cost + transaction_fee)
        
        # 健康度指标（来自文档第4章）
        health_metrics = {
            "market_digestion": 0.7,
            "inflation_rate": 0.0,
            "user_retention": [0.75, 0.78, 0.82, 0.85][min(phase_month-1, 3)]
        }

        return pd.DataFrame([{
            "阶段月份": phase_month,
            "至尊投放量": supreme_count,
            "后代总产量": total_offspring,
            "动态定价": params["dynamic_price"],
            "平台总收益": platform_income,
            "用户净收益": user_profit,
            "市场消化率": health_metrics["market_digestion"],
            "用户留存率": health_metrics["user_retention"],
            "至尊级成本": supreme_cost,
            "道具总成本": item_cost,
            "交易手续费": transaction_fee
        }])
