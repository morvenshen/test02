"""
天池应用前端
版本：2.0
包含数据可视化和交互界面
"""
from economic_model import TaoistEconSimulator
import pandas as pd
import altair as alt

class TianchiApp:
    def __init__(self, params):
        self.simulator = TaoistEconSimulator(params)
        self.simulation_data = None
        
    def 运行模拟(self, 月份数=6):
        """执行模拟并缓存结果"""
        self.simulation_data = self.simulator.多周期模拟(月份数)
        return self.simulation_data
    
    def 生成折线图(self, 字段):
        """通用折线图生成器"""
        df = pd.DataFrame(self.simulation_data['月度数据'])
        return alt.Chart(df).mark_line().encode(
            x='月份:O',
            y=f'{字段}:Q',
            tooltip=[f'{字段}']
        ).properties(
            width=400,
            height=300
        )
    
    def 显示仪表盘(self):
        """生成完整可视化看板"""
        if not self.simulation_data:
            raise ValueError("请先运行模拟")
            
        # 关键指标卡
        平台总收益 = sum([m['平台收益']['总收益'] for m in self.simulation_data['月度数据']])
        总功德值 = sum([m['总功德值'] for m in self.simulation_data['月度数据']])
        
        # 生成图表
        市场图表 = self.生成折线图('市场饱和度')
        收益图表 = self.生成折线图('实际流通量')
        功德图表 = self.生成折线图('总功德值')
        
        # 组合图表
        return alt.vconcat(
            market_chart | revenue_chart,
            merit_chart
        ).resolve_scale(
            y='independent'
        )

# 示例用法
if __name__ == "__main__":
    # 初始化应用
    app = TianchiApp({
        '放生率': 0.7,
        '初始至尊数量': 300
    })
    
    # 运行模拟
    data = app.运行模拟()
    
    # 打印基础数据
    print("=== 首月关键指标 ===")
    print(f"市场饱和度: {data['月度数据'][0]['市场饱和度']}%")
    print(f"用户收益率: {data['用户指标']['净收益率']}%")
    
    # 显示图表
    app.显示仪表盘().show()
