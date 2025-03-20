import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # 必须导入的图表库

# ========== 页面配置 ==========
st.set_page_config(
    page_title="天池经济模拟器",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 侧边栏控制面板 ==========
with st.sidebar:
    st.header("🛠️ 核心参数设置")
    
    # 基础参数
    price_ss = st.number_input("至尊神兽售价（元）", 1000, 5000, 1000, step=500)
    breed_cycle = st.slider("繁殖周期（天）", 7, 90, 30, help="神兽繁殖冷却时间")
    release_rate = st.slider("放生率阈值", 0.5, 0.9, 0.7, step=0.05, 
                           help="触发市场调控的临界值")
    
    # 后代分布
    st.subheader("🦄 后代品级分布")
    ratio_pt = st.slider("普通级", 0.1, 0.8, 0.4, step=0.05)
    ratio_rare = st.slider("稀有级", 0.1, 0.8, 0.3, step=0.05)
    ratio_legend = st.slider("传说级", 0.0, 0.5, 0.2, step=0.05)
    ratio_epic = max(0.0, round(1 - ratio_pt - ratio_rare - ratio_legend, 2))
    st.markdown(f"**史诗级自动计算比例**: {ratio_epic}")

# ========== 经济模型计算 ==========
supply_month1 = 300  # 初始投放量
prices = [20, 50, 80, 160]  # 各品级单价

# 计算各品级后代数量
offspring_counts = [
    supply_month1 * ratio_pt * 12,   # 普通级
    supply_month1 * ratio_rare * 9,  # 稀有级
    supply_month1 * ratio_legend * 6, # 传说级
    supply_month1 * ratio_epic * 3    # 史诗级
]

# ========== 可视化展示 ==========
col1, col2 = st.columns([2, 1])

# 左列 - 收益分析
with col1:
    st.header("📊 收益动态分析")
    
    # 计算总收益
    revenue = sum([qty*price for qty, price in zip(offspring_counts, prices)])
    
    # 构建收益数据
    df_income = pd.DataFrame({
        "分类": ["平台收益", "用户收益"],
        "金额": [
            supply_month1*price_ss + revenue*0.03,  # 平台收益公式
            revenue - (supply_month1*1000 + revenue*0.03)  # 用户收益公式
        ]
    })
    
    # 交互式柱状图
    fig = px.bar(
        df_income, 
        x='分类', 
        y='金额', 
        color='分类',
        text_auto='.2s',
        color_discrete_map={
            "平台收益": "#636EFA",
            "用户收益": "#EF553B"
        }
    )
    fig.update_layout(
        yaxis_title="金额（元）",
        xaxis_title="",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# 右列 - 风险监测
with col2:
    st.header("⚠️ 市场风险仪表盘")
    
    # 计算市场流通量
    circulation = supply_month1 * sum(offspring_counts) * (1 - release_rate)
    health_status = "正常" if (circulation/2000) < 5 else "通胀预警"
    
    # 构建仪表盘
    gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=circulation/2000,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "市场饱和度指数"},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 5], 'color': "lightgreen"},
                {'range': [5, 10], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 5
            }
        }
    ))
    gauge.update_layout(height=400)
    st.plotly_chart(gauge, use_container_width=True)
    
    # 风险状态显示
    st.metric("系统健康状态", 
             value=health_status, 
             delta="安全阈值：饱和度<5" if health_status=="正常" else "危险！请调整参数")

# ========== 数据导出模块 ==========
st.divider()
st.header("📤 数据导出")

# 生成报告数据
report_df = pd.DataFrame({
    '核心指标': ['至尊售价', '用户收益率', '市场饱和度'],
    '数值': [
        f"{price_ss}元",
        f"{(revenue - 300000)/300000:.2%}",
        f"{circulation/2000:.1f}倍"
    ]
})

# 下载按钮
st.download_button(
    label="下载完整分析报告（CSV）",
    data=report_df.to_csv(index=False).encode('utf-8'),
    file_name='天池经济模拟报告.csv',
    mime='text/csv'
)

# ========== 运行说明 ==========
st.sidebar.markdown("""
---
**操作指南**：
1. 调整左侧参数实时观察变化
2. 红色预警时需降低放生阈值
3. 点击底部按钮导出报告
""")
