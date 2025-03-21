"""
天池应用前端（Streamlit集成版）
版本：2.1
"""
import streamlit as st
from economic_model import TaoistEconSimulator
import pandas as pd
import altair as alt

class TianchiApp:
    def __init__(self, params):
        self.simulator = TaoistEconSimulator(params)
        self.simulation_data = None
        
    def run_simulation(self, months=6):
        """执行模拟并缓存结果"""
        self.simulation_data = self.simulator.多周期模拟(months)
        return self.simulation_data
    
    def generate_line_chart(self, field):
        """生成Streamlit兼容的Altair图表"""
        df = pd.DataFrame(self.simulation_data['月度数据'])
        return alt.Chart(df).mark_line().encode(
            x='月份:O',
            y=f'{field}:Q',
            tooltip=[f'{field}']
        ).properties(
            width=600,
            height=300
        )

# Streamlit界面
st.set_page_config(page_title="天池经济模拟", layout="wide")
st.title("🏯 虚拟经济系统模拟看板")

# 侧边栏参数设置
with st.sidebar:
    st.header("模拟参数")
    release_rate = st.slider("放生率", 0.0, 1.0, 0.7, 0.05)
    initial_num = st.number_input("初始至尊数量", 100, 1000, 300)
    months = st.slider("模拟月份", 3, 24, 6)

# 初始化模拟器
app = TianchiApp({
    '放生率': release_rate,
    '初始至尊数量': initial_num
})

# 运行模拟
data = app.run_simulation(months)

# 展示关键指标
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("总平台收益", f"¥{sum([m['平台收益']['总收益'] for m in data['月度数据']]):,.0f}")
with col2:
    st.metric("用户平均收益率", f"{data['用户指标']['净收益率']}%")
with col3:
    st.metric("总功德值", f"{sum([m['总功德值'] for m in data['月度数据']]):,.0f}")

# 展示核心图表
st.altair_chart(
    app.generate_line_chart('市场饱和度'), 
    use_container_width=True
)
st.altair_chart(
    app.generate_line_chart('实际流通量'),
    use_container_width=True
)

# 原始数据展示
with st.expander("查看原始数据"):
    st.write(pd.DataFrame(data['月度数据']))

# 运行说明
st.info("""
⚠️ 注意事项：
1. 参数调整后会自动重新计算
2. 鼠标悬停图表可查看详细数值
3. 首次加载可能需要3-5秒初始化
""")
