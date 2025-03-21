"""
天池应用前端
版本：2.1
适配修正后的数据结构
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
        
        # 处理实际流通量字段
        if 字段 == '总实际流通量':
            df['总实际流通量'] = [x['总实际流通量'] for x in df['实际流通量']]
        elif 字段 in ['普通', '稀有', '传说', '史诗']:
            df[字段] = df['实际流通量'].apply(lambda x: x.get(字段, 0))
        
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
        流通图表 = self.生成折线图('总实际流通量')  # 使用新字段 ✅
        功德图表 = self.生成折线图('总功德值')
        
        # 组合图表
        return alt.vconcat(
            市场图表 | 流通图表,
            功德图表
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
