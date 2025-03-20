import streamlit as st
import pandas as pd
import plotly.express as px

# ===== PRD核心参数（不可修改）=====
INITIAL_INVESTMENT = 1000  # 用户初始投入
TARGET_RETURN = 0.2        # 目标收益率20%
MONTHS = [1, 2, 3, 6]      # 必须计算的月份

# ===== 经济模型函数 =====
def calculate_economics(params):
    """
    根据PRD第4章公式计算多周期经济指标
    输入参数：
        params: dict 包含所有可调参数
    返回：
        DataFrame 包含各月份完整指标
    """
    results = []
    cumulative_supply = 0
    
    for month in MONTHS:
        # 繁殖量计算（PRD Eq.3）
        new_supply = params['base_supply'] * (1 + params['growth_rate'])**month
        
        # 市场流通量（PRD Eq.7）
        circulation = new_supply * (1 - params['release_rate'])
        
        # 用户收益计算（PRD Eq.11）
        platform_cut = params['price'] * new_supply * params['platform_fee']
        user_income = (params['price'] * new_supply - platform_cut) - INITIAL_INVESTMENT
        
        # 收益率验证
        return_rate = user_income / INITIAL_INVESTMENT
        
        results.append({
            "月份": month,
            "新增投放量": round(new_supply),
            "市场流通量": round(circulation),
            "平台抽成": round(platform_cut,2),
            "用户净收益": round(user_income,2),
            "累计收益率": f"{return_rate:.1%}",
            "达标状态": "✅" if return_rate >= TARGET_RETURN else "⚠️"
        })
        
    return pd.DataFrame(results)

# ===== 界面构建 =====
st.set_page_config(layout="wide")
st.title("天链经济模拟器 v2.0")

# 参数控制面板
with st.sidebar:
    st.header("⚙️ 调控参数")
    params = {
        'base_supply': st.slider("基础投放量", 100, 5000, 1000, step=100),
        'growth_rate': st.slider("月增长率", 0.05, 0.5, 0.15, step=0.05),
        'price': st.number_input("单位价格（元）", 10, 1000, 100),
        'release_rate': st.slider("放生率", 0.3, 0.9, 0.6),
        'platform_fee': st.slider("平台费率", 0.01, 0.2, 0.03)
    }

# 计算并展示结果
df = calculate_economics(params)

# 主显示区
col1, col2 = st.columns([1,2])

with col1:
    st.metric("当前收益率", 
             df.iloc[-1]['累计收益率'],
             delta=f"目标 {TARGET_RETURN:.0%}",
             help="最终月份达标即视为整体成功")
    
    st.dataframe(
        df.style.applymap(lambda x: "background-color: #E8F5E9" if "✅" in str(x) else ""),
        height=400
    )

with col2:
    # 收益率趋势图
    fig = px.line(
        df, x='月份', y='累计收益率',
        markers=True, 
        title=f"收益达成进程（最终：{df.iloc[-1]['累计收益率']}）",
        labels={'累计收益率': '收益率'}
    )
    fig.add_hline(y=TARGET_RETURN, line_dash="dot",
                 annotation_text="目标线", 
                 annotation_position="bottom right")
    st.plotly_chart(fig, use_container_width=True)

# ===== 调试信息 =====
with st.expander("📊 原始数据"):
    st.write("计算参数：", params)
    st.write("详细计算结果：", df)

