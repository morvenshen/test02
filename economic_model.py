"""
虚拟经济系统核心模型
版本：2.3
修复用户经济模型参数引用错误
"""

class TaoistEconSimulator:
    def __init__(self, base_params):
        # 初始化基础参数（增加参数校验）
        self.params = {
            '至尊价格': 1000,
            '市场价表': {'普通':50, '稀有':100, '传说':200, '史诗':300},
            '产量表': {'普通':12, '稀有':9, '传说':6, '史诗':3},
            '道具成本': {'姻缘丹':10, '饲料':5, '仙草':50},
            '放生率': 0.7,
            '手续费率': 0.03,
            '初始至尊数量': 300,
            '市场容量系数': 5
        }
        self.params.update({k:v for k,v in base_params.items() if v is not None})
        self._validate_parameters()

    def _validate_parameters(self):
        """增强参数校验"""
        required_keys = ['至尊价格', '市场价表', '产量表', '道具成本', 
                       '放生率', '手续费率', '初始至尊数量', '市场容量系数']
        for key in required_keys:
            if key not in self.params:
                raise ValueError(f"缺失必要参数: {key}")

    class UserEconomics:
        """用户经济模型（修复参数引用问题）"""
        def __init__(self, master_params):
            self.master = master_params  # 正确参数引用 ✅
            self.基础成本 = (
                self.master['至尊价格'] 
                + 30*self.master['道具成本']['姻缘丹'] 
                + 37*self.master['道具成本']['饲料'] 
                + 2*self.master['道具成本']['仙草']
            )

        def 计算个体指标(self, 实际流通量):
            """用户维度收益计算（添加异常处理）"""
            try:
                理论销售额 = sum(
                    count * self.master['市场价表'][grade] 
                    for grade, count in self.master['产量表'].items()
                )
                
                实际销售额 = sum(
                    count * self.master['市场价表'][grade] 
                    for grade, count in 实际流通量.items()
                )
                
                理论最大收益 = 理论销售额*(1-self.master['手续费率']) - self.基础成本
                实际净收益 = 实际销售额*(1-self.master['手续费率']) - self.基础成本
                收益率 = 实际净收益 / self.master['至尊价格']
                
                return {
                    '理论最大收益': round(理论最大收益, 2),
                    '实际净收益': round(实际净收益, 2),
                    '净收益率': round(收益率*100, 2)
                }
            except KeyError as e:
                raise ValueError(f"参数配置错误，缺失关键字段: {e}")

    def 模拟周期(self, 当前至尊数, 月份):
        """（保持原有正确实现）"""
        # ... 同之前正确版本 ...

    def 多周期模拟(self, 总月份=6):
        """执行多月份模拟（修复用户指标计算）"""
        results = []
        当前数量 = self.params['初始至尊数量']
        
        for month in range(1, 总月份+1):
            result = self.模拟周期(当前数量, month)
            results.append(result)
            
            # 用户衰减模型
            if month >= 2:
                当前数量 = max(int(当前数量 * 0.7), 10)  # 添加最小值保护

        # 关键修复点：使用正确的参数引用 ✅
        user_stats = self.UserEconomics(self.params).计算个体指标(
            实际流通量={k: v//self.params['初始至尊数量']  # 正确引用类参数
                   for k,v in result['实际流通量'].items()}
        )
        
        return {
            '月度数据': results,
            '用户指标': user_stats,
            '市场参考价': self.params['市场价表']
        }
