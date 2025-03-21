import pandas as pd

class EconomicModel:
    def __init__(self, user_count=2000):
        self.user_count = user_count
        self.price_tiers = {
            '至尊级': 1000,
            '史诗级': 160,
            '传说级': 80,
            '稀有级': 50,
            '普通级': 20
        }
        
    def calculate_monthly(self, params):
        """单月经济模型计算"""
        # 繁殖收益计算
        offspring = {
            '普通级': 12,
            '稀有级': 9,
            '传说级': 6,
            '史诗级': 3
        }
        
        # 道具消耗计算
        props_cost = (
            params['姻缘丹'] * 5 +
            params['饲料'] * 5 +
            params['仙草'] * 15
        )
        
        # 收益计算
        revenue = sum(
            count * self.price_tiers[tier] * (1 - params['放生率'])
            for tier, count in offspring.items()
        )
        
        # 平台收益
        platform_income = (
            params['至尊数量'] * self.price_tiers['至尊级'] +
            params['至尊数量'] * props_cost +
            revenue * 0.03  # 交易手续费
        )
        
        # 用户净收益
        user_net = revenue * (1 - 0.03) - (
            params['至尊数量'] * self.price_tiers['至尊级'] +
            params['至尊数量'] * props_cost
        )
        
        return {
            '平台收益': platform_income,
            '用户净收益': user_net,
            '市场流通量': sum(offspring.values()) * (1 - params['放生率'])
        }
