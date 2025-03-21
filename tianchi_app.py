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
            breeding_cycle = st.number_input("繁殖周期(天)", min_value=1, value=30, step=1)
            supreme_count = st.number_input("每期至尊数量", min_value=1, value=300, step=1)
        with col2:
            release_rate = st.number_input("放生率", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
            transaction_fee = st.number_input("手续费率", min_value=0.0, max_value=1.0, value=0.03, step=0.01)
        
        st.subheader("后代市场价格")
        market_prices = {
            "普通": st.number_input("普通价格", min_value=0, value=20, step=1),
            "稀有": st.number_input("稀有价格", min_value=0, value=50, step=1),
            "传说": st.number_input("传说价格", min_value=0, value=80, step=1),
            "史诗": st.number_input("史诗价格", min_value=0, value=160, step=1)
        }
        
        st.subheader("繁殖比例")
        offspring_ratios = {
            "普通": st.number_input("普通比例", min_value=0.0, max_value=1.0, value=0.4, step=0.01),
            "稀有": st.number_input("稀有比例", min_value=0.0, max_value=1.0, value=0.3, step=0.01),
            "传说": st.number_input("传说比例", min_value=0.0, max_value=1.0, value=0.2, step=0.01),
            "史诗": st.number_input("史诗比例", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
        }
        
        st.subheader("道具成本")
        item_prices = {
            "姻缘丹": st.number_input("姻缘丹价格", min_value=0, value=5, step=1),
            "饲料": st.number_input("饲料价格", min_value=0, value=5, step=1),
            "仙草": st.number_input("仙草价格", min_value=0, value=15, step=1)
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
    try:
        single_data = calculate_single_breeding(**params)
        phase_df = calculate_phase_data(supreme_count=supreme_count, **params)
    except Exception as e:
        st.error(f"参数错误: {str(e)}")
        return
    
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
    df = pd.DataFrame(display_data)
    st.dataframe(
        df.style.format({"数值": lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x}),
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
