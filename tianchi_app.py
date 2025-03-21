# tianchi_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from economic_model import calculate_single_breeding, calculate_phase_data

def main():
    st.set_page_config(page_title="天池经济模型模拟器", layout="wide")
    st.title("🦄 天池放生系统经济模型模拟器")
    
    with st.sidebar:
        st.header("调控参数")
        supreme_price = st.slider("至尊级价格", 500, 2000, 1000)
        release_rate = st.slider("放生率", 0.5, 0.9, 0.7)
        transaction_fee = st.slider("交易手续费率", 0.01, 0.05, 0.03)
        
        st.subheader("道具价格")
        yn_price = st.number_input("姻缘丹价格", 3, 10, 5)
        feed_price = st.number_input("饲料价格", 3, 10, 5)
        herb_price = st.number_input("仙草价格", 10, 30, 15)
        
        st.subheader("后代比例")
        col1, col2 = st.columns(2)
        with col1:
            common_ratio = st.slider("普通比例", 0.2, 0.6, 0.4)
            rare_ratio = st.slider("稀有比例", 0.15, 0.45, 0.3)
        with col2:
            legend_ratio = st.slider("传说比例", 0.1, 0.3, 0.2)
            epic_ratio = st.slider("史诗比例", 0.05, 0.15, 0.1)

    # 实时计算
    params = {
        "supreme_price": supreme_price,
        "release_rate": release_rate,
        "transaction_fee": transaction_fee,
        "item_prices": {"姻缘丹": yn_price, "饲料": feed_price, "仙草": herb_price},
        "offspring_ratios": {
            "普通": common_ratio,
            "稀有": rare_ratio,
            "传说": legend_ratio,
            "史诗": epic_ratio
        }
    }
    
    single_data = calculate_single_breeding(**params)
    phase_df = calculate_phase_data(**params)
    
    # 指标展示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("平台单只收益", f"¥{single_data['平台收入']:,.0f}")
    with col2:
        st.metric("用户单只净收益", f"¥{single_data['单只收益']:,.0f}", 
                 delta_color="inverse" if single_data['单只收益']<0 else "normal")
    with col3:
        st.metric("市场流通量", f"{sum(single_data['市场流通量'].values()):,.0f}只")
    
    # 数据可视化
    tab1, tab2, tab3 = st.tabs(["阶段分析", "成本构成", "市场健康度"])
    
    with tab1:
        fig = px.bar(
            phase_df,
            x="月份",
            y=["平台收益", "用户总收益"],
            barmode="group",
            title="各阶段收益对比"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        cost_df = pd.DataFrame({
            "项目": ["至尊购买", "姻缘丹", "饲料", "仙草"],
            "金额": [
                supreme_price,
                30 * yn_price,
                37 * feed_price,
                2 * herb_price
            ]
        })
        fig = px.pie(cost_df, names="项目", values="金额", title="成本构成分析")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.line(
            phase_df,
            x="月份",
            y="市场流通量",
            markers=True,
            title="市场流通量趋势",
            labels={"市场流通量": "流通量（只）"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        health_status = "正常" if phase_df["市场流通量"].iloc[-1] < 10000 else "预警"
        st.metric("当前市场状态", health_status, delta="↓ 健康" if health_status=="正常" else "↑ 风险")

if __name__ == "__main__":
    main()
