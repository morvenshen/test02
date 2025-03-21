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
            breeding_cycle = st.slider("繁殖周期(天)", 15, 60, 30)
            supreme_count = st.slider("每期至尊数量", 100, 1000, 300)
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
        "breeding_cycle": breeding_cycle,
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
    col1.metric("单用户净收益", f"¥{single_data['单只收益']:,.0f}", 
              delta_color="inverse" if single_data['单只收益']<0 else "normal")
    col2.metric("单平台收益", f"¥{single_data['平台收入']:,.0f}")
    col3.metric("总流通量", f"{sum(single_data['市场流通量'].values())*supreme_count:,.0f}只")
    
    # 周期影响分析
    st.subheader("周期全局影响分析")
    display_data = {
        "指标": ["平台总收益", "用户总收益", "至尊数量", "繁殖周期"],
        "数值": [
            phase_df["平台总收益"].iloc[0],
            phase_df["用户总收益"].iloc[0],
            phase_df["至尊数量"].iloc[0],
            f"{breeding_cycle}天"
        ]
    }
    st.dataframe(
        pd.DataFrame(display_data).style.format({"数值": "{:,.0f}"}),
        use_container_width=True,
        hide_index=True
    )
    
    # 市场流通明细
    st.subheader("市场流通分布")
    circulation_data = {
        "等级": ["普通", "稀有", "传说", "史诗"],
        "数量": [
            phase_df["市场流通量-普通"].iloc[0],
            phase_df["市场流通量-稀有"].iloc[0],
            phase_df["市场流通量-传说"].iloc[0],
            phase_df["市场流通量-史诗"].iloc[0]
        ]
    }
    fig = px.bar(
        circulation_data,
        x="等级",
        y="数量",
        text="数量",
        title="各等级流通量明细"
    )
    fig.update_traces(texttemplate='%{text:,.0f}')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
