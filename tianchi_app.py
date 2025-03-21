# tianchi_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from economic_model import calculate_single_breeding, calculate_phase_data

def main():
    st.set_page_config(page_title="天池经济模型模拟器", layout="wide")
    st.title("🦄 天池放生系统经济模型模拟器")
    
    with st.sidebar:
        st.header("核心参数")
        col1, col2 = st.columns(2)
        with col1:
            supreme_price = st.slider("至尊价格", 500, 2000, 1000)
            supreme_count = st.slider("每月至尊数量", 100, 1000, 300)
        with col2:
            release_rate = st.slider("放生率", 0.5, 0.9, 0.7)
            transaction_fee = st.slider("手续费率", 0.01, 0.05, 0.03)
        
        st.subheader("后代市场价格")
        market_prices = {
            "普通": st.number_input("普通价格", 10, 100, 20),
            "稀有": st.number_input("稀有价格", 30, 200, 50),
            "传说": st.number_input("传说价格", 50, 300, 80),
            "史诗": st.number_input("史诗价格", 100, 500, 160)
        }
        
        st.subheader("繁殖比例")
        offspring_ratios = {
            "普通": st.slider("普通比例", 0.2, 0.6, 0.4),
            "稀有": st.slider("稀有比例", 0.15, 0.45, 0.3),
            "传说": st.slider("传说比例", 0.1, 0.3, 0.2),
            "史诗": st.slider("史诗比例", 0.05, 0.15, 0.1)
        }
        
        st.subheader("道具成本")
        item_prices = {
            "姻缘丹": st.number_input("姻缘丹价格", 3, 10, 5),
            "饲料": st.number_input("饲料价格", 3, 10, 5),
            "仙草": st.number_input("仙草价格", 10, 30, 15)
        }

    # 参数整合
    params = {
        "supreme_price": supreme_price,
        "release_rate": release_rate,
        "transaction_fee": transaction_fee,
        "item_prices": item_prices,
        "offspring_ratios": offspring_ratios,
        "market_prices": market_prices
    }
    
    # 实时计算
    single_data = calculate_single_breeding(**params)
    phase_df = calculate_phase_data(supreme_count=supreme_count, **params)
    
    # 核心指标展示
    col1, col2, col3 = st.columns(3)
    col1.metric("单只用户收益", f"¥{single_data['单只收益']:,.0f}", 
              delta_color="inverse" if single_data['单只收益']<0 else "normal")
    col2.metric("单只平台收益", f"¥{single_data['平台收入']:,.0f}")
    col3.metric("单只市场流通", f"{sum(single_data['市场流通量'].values()):,.0f}只")
    
    # 全局影响分析
    st.subheader("月度全局影响分析")
    display_df = phase_df.T.reset_index()
    display_df.columns = ["指标", "数值"]
    st.dataframe(
        display_df.style.format({"数值": "{:,.0f}"}),
        use_container_width=True,
        hide_index=True
    )
    
    # 可视化分析
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            names=list(single_data["市场流通量"].keys()),
            values=list(single_data["市场流通量"].values()),
            title="市场流通构成"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        cost_data = {
            "至尊购买": supreme_price,
            "道具成本": sum([30*item_prices["姻缘丹"], 37*item_prices["饲料"], 2*item_prices["仙草"]])
        }
        fig = px.pie(
            names=list(cost_data.keys()),
            values=list(cost_data.values()),
            title="成本构成分析"
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
