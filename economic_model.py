"""
虚拟经济系统核心模型
版本：2.1
修复实际流通量数据结构问题
"""

class TaoistEconSimulator:
    def __init__(self, base_params):
        # 初始化基础参数
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
        self.params.update(base_params)
        self._validate_parameters()

    def _validate_parameters(self):
        """参数校验"""
        assert 0 <= self.params['放生率'] <= 1, "放生率必须在0-1之间"
        assert self.params['市场容量系数'] >= 1, "市场容量系数至少为1"

    class UserEconomics:
        """个体用户经济模型"""
        def __init__(self, master_params):
            self.master = master_params
            self.基础成本 = (
                master_params['至尊价格'] 
                + 30*master_params['道具成本']['姻缘丹'] 
                + 37*master_params['道具成本']['饲料'] 
                + 2*master_params['道具成本']['仙草']
            )

        def 计算个体指标(self, 实际流通量):
            """计算用户维度收益"""
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

    def 模拟周期(self, 当前至尊数, 月份):
        """执行单个月份的经济模拟"""
        总产量 = {grade: count*当前至尊数 for grade, count in self.params['产量表'].items()}
        实际流通量 = {k: int(v*(1-self.params['放生率'])) for k,v in 总产量.items()}
        
        # 平台收益计算
        平台收益 = {
            '至尊销售': 当前至尊数 * self.params['至尊价格'],
            '道具销售': 30*self.params['道具成本']['姻缘丹']*当前至尊数 
                     + 37*self.params['道具成本']['饲料']*当前至尊数 
                     + 2*self.params['道具成本']['仙草']*当前至尊数,
            '手续费': sum(v*self.params['市场价表'][k] for k,v in 实际流通量.items()) 
                   * self.params['手续费率']
        }
        平台收益['总收益'] = sum(平台收益.values())
        
        # 功德体系
        放生功德 = sum(
            (总产量[grade]-实际流通量[grade]) * self.params['市场价表'][grade] * 0.5 
            for grade in 实际流通量
        )
        繁殖功德 = (30*self.params['道具成本']['姻缘丹'] + 2*self.params['道具成本']['仙草']) * 0.3
        总功德 = round(放生功德 + 繁殖功德, 2)
        
        # 市场健康度
        市场容量 = self.params['初始至尊数量'] * self.params['市场容量系数']
        饱和度 = sum(实际流通量.values()) / 市场容量 * 100
        
        return {
            '月份': 月份,
            '至尊数量': 当前至尊数,
            '新增后代': sum(总产量.values()),
            '实际流通量': 实际流通量,  # 保持字典结构 ✅
            '总实际流通量': sum(实际流通量.values()),  # 新增总和字段 ✅
            '市场饱和度': round(饱和度, 2),
            '平台收益': 平台收益,
            '总功德值': 总功德,
            '健康预警': '⚠️通胀' if 饱和度 > 100 else '正常'
        }

    def 多周期模拟(self, 总月份=6):
        """执行多月份模拟"""
        results = []
        当前数量 = self.params['初始至尊数量']
        
        for month in range(1, 总月份+1):
            result = self.模拟周期(当前数量, month)
            results.append(result)
            
            # 用户衰减模型
            if month >= 2:
                当前数量 = int(当前数量 * 0.7)
                if 当前数量 < 10:
                    当前数量 = 10
        
        # 用户指标计算
        user_stats = self.UserEconomics(self.params).计算个体指标(
            实际流通量={k:v//self.params['初始至尊数量'] 
                   for k,v in result['实际流通量'].items()}  # 使用修正后的字典结构 ✅
        )
        
        return {
            '月度数据': results,
            '用户指标': user_stats,
            '市场参考价': self.params['市场价表']
        }
