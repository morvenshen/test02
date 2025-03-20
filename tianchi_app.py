import streamlit as st
import pandas as pd
import plotly.express as px

# 初始化配置
st.set_page_config(layout="wide")

# 侧边栏参数控制
with st.sidebar:
    st.header("🛠️ 参数设置")
    price_ss = st.number_input("至尊神兽售价", 1000, 5000, 1000)
    breed_cycle = st.slider("繁殖周期(天)", 7, 90, 30)
    release_rate = st.slider("放生率阈值", 0.5, 0.9, 0.7)
    
    st.subheader("后代分布比例")
    ratio_pt = st.slider("普通级", 0.1, 0.8, 0.4)
    ratio_rare = st.slider("稀有级", 0.1, 0.8, 0.3)
    ratio_legend = st.slider("传说级", 0.0, 0.5, 0.2)
    ratio_epic = max(0, 1 - ratio_pt - ratio_rare - ratio_legend)  # 自动计算史诗比例

# 经济模型计算
supply_month1 = 300
prices = [20, 50, 80, 160]
offspring_counts = [
    supply_month1 * ratio_pt * 12,
    supply_month1 * ratio_rare * 9,
    supply_month1 * ratio_legend * 6,
    supply_month1 * ratio_epic * 3
]

# 可视化展示
col1, col2 = st.columns(2)
with col1:
    st.header("📊 收益分析")
    revenue = sum([qty*price for qty,price in zip(offspring_counts, prices)])
    df_income = pd.DataFrame({
        "分类": ["平台收益", "用户收益"],
        "金额": [
            supply_month1*price_ss + revenue*0.03,
            revenue - (supply_month1*1000 + revenue*0.03)
        ]
    })
    fig = px.bar(df_income, x='分类', y='金额', color='分类', text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("⚠️ 风险监测")
    circulation = supply_month1 * sum(offspring_counts) * (1 - release_rate)
    health_status = "正常" if (circulation/2000)<5 else "通胀预警"
    
    gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = circulation/2000,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [0, 10]},
                'steps': [
                    {'range': [0, 5], 'color': "lightgreen"},
                    {'range': [5, 10], 'color': "red"}]
    ))
    st.plotly_chart(gauge, use_container_width=True)

# 数据下载
st.download_button(
    label="📥 下载测算报告",
    data=pd.DataFrame({
        '至尊售价': [price_ss],
        '用户收益率': [(revenue - 300000)/300000],
        '市场饱和度': [circulation/2000]
    }).to_csv(index=False),
    file_name='天池经济报告.csv'
)
