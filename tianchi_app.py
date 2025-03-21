# tianchi_app.py
import streamlit as st
import pandas as pd
from economic_model import calculate_phase_data

def main():
    st.set_page_config(page_title="经济模型模拟器", layout="wide")
    st.title("🦄 天池经济模型模拟器")
    
    with st.sidebar:
        st.header("核心参数")
        col1, col2 = st.columns(2)
        with col1:
            cycle = st.number_input("繁殖周期(天)", min_value=1, value=30, step=1)
            count = st.number_input("至尊数量", min_value=1, value=300, step=1)
            price = st.number_input("至尊价格", min_value=0, value=1000, step=100)
        with col2:
            release_rate = st.number_input("放生率", value=0.7, min_value=0.0, max_value=1.0, step=0.01)
            fee_rate = st.number_input("手续费率", value=0.03, min_value=0.0, max_value=1.0, step=0.01)
        
        st.subheader("市场价格设置")
        prices = {
            "普通": st.number_input("普通级价格", value=413, min_value=0),
            "稀有": st.number_input("稀有级价格", value=413, min_value=0),
            "传说": st.number_input("传说级价格", value=413, min_value=0),
            "史诗": st.number_input("史诗级价格", value=413, min_value=0)
        }
        
        st.subheader("繁殖比例")
        ratios = {
            "普通": st.number_input("普通比例", value=0.4, min_value=0.0, max_value=1.0, step=0.01),
            "稀有": st.number_input("稀有比例", value=0.3, min_value=0.0, max_value=1.0, step=0.01),
            "传说": st.number_input("传说比例", value=0.2, min_value=0.0, max_value=1.0, step=0.01),
            "史诗": st.number_input("史诗比例", value=0.1, min_value=0.0, max_value=1.0, step=0.01)
        }
        
        st.subheader("道具价格")
        items = {
            "姻缘丹": st.number_input("姻缘丹价格", value=5),
            "饲料": st.number_input("饲料价格", value=5),
            "仙草": st.number_input("仙草价格", value=15)
        }

    try:
        df = calculate_phase_data(
            supreme_count=count,
            breeding_cycle=cycle,
            release_rate=release_rate,
            transaction_fee=fee_rate,
            item_prices=items,
            offspring_ratios=ratios,
            market_prices=prices,
            supreme_price=price
        )
    except Exception as e:
        st.error(f"计算错误：{str(e)}")
        return

    # 结果展示
    st.subheader("核心指标")
    cols = st.columns(4)
    cols[0].metric("总销售额", f"¥{df['后代总销售额'].iloc[0]:,.0f}")
    cols[1].metric("总成本", f"¥{df['至尊总投入'].iloc[0]:,.0f}", 
                delta_color="inverse")
    cols[2].metric("用户净收益", f"¥{df['购买至尊级用户净收益'].iloc[0]:,.0f}", 
                 delta_color="inverse" if df['购买至尊级用户净收益'].iloc[0]<0 else "normal")
    cols[3].metric("收益率", f"{df['单只收益率'].iloc[0]:.1f}%")

    st.subheader("明细数据")
    st.dataframe(df.T.style.format("{:,.0f}"), height=400)

if __name__ == "__main__":
    main()
