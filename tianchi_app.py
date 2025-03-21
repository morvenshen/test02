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
            supreme_price = st.number_input("至尊级价格", min_value=0, value=1000, step=100)
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

    params = {
        "breeding_cycle": breeding_cycle,
        "release_rate": release_rate,
        "transaction_fee": transaction_fee,
        "item_prices": item_prices,
        "offspring_ratios": offspring_ratios,
        "market_prices": market_prices,
        "supreme_price": supreme_price
    }
    
    try:
        phase_df = calculate_phase_data(supreme_count=supreme_count, **params)
    except Exception as e:
        st.error(f"计算错误: {str(e)}")
        return
    
    # 核心指标展示
    st.subheader("核心经济指标")
    col1, col2, col3 = st.columns(3)
    col1.metric("平台总收益", f"¥{phase_df['平台总收益'].iloc[0]:,.0f}")
    col2.metric("用户净收益", f"¥{phase_df['购买至尊级用户净收益'].iloc[0]:,.0f}", 
              delta_color="inverse" if phase_df['购买至尊级用户净收益'].iloc[0]<0 else "normal")
    col3.metric("新增后代总数", f"{phase_df['新增后代总数'].iloc[0]:,.0f}只")

    # 收益构成分析
    st.subheader("收益构成分析")
    profit_data = {
        "来源": ["至尊销售", "道具销售", "交易手续费"],
        "金额": [
            phase_df["至尊级销售额"].iloc[0],
            phase_df["道具总消耗"].iloc[0],
            phase_df["总交易手续费"].iloc[0]
        ]
    }
    fig = px.pie(
        profit_data, 
        names="来源", 
        values="金额",
        title="平台收益构成",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    # 数据验证展示
    st.subheader("计算明细验证")
    verification_data = {
        "项目": ["单只至尊产值", "单只总成本", "单只净收益"],
        "金额": [
            phase_df["后代总销售额"].iloc[0] / supreme_count,
            phase_df["用户总成本"].iloc[0] / supreme_count,
            phase_df["购买至尊级用户净收益"].iloc[0] / supreme_count
        ]
    }
    st.dataframe(
        pd.DataFrame(verification_data).style.format({"金额": "¥{:,.0f}"}),
        use_container_width=True
    )

if __name__ == "__main__":
    main()
