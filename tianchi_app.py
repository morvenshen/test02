# tianchi_app.py
import streamlit as st
import pandas as pd
from economic_model import calculate_phase_data

def main():
    st.set_page_config(page_title="经济模型调控模拟器", layout="wide")
    st.title("🎛️ 天池经济调控模拟系统")
    
    with st.sidebar:
        st.header("调控参数面板")
        col1, col2 = st.columns(2)
        with col1:
            cycle = st.slider("繁殖周期(天)", 1, 120, 30)
            count = st.number_input("至尊投放量", 1, 1000, 300)
            price = st.number_input("至尊价格", 0, 5000, 1000)
        with col2:
            release_rate = st.slider("目标放生率", 0.0, 1.0, 0.7)
            fee_rate = st.slider("手续费率", 0.0, 0.2, 0.03)
        
        st.subheader("市场价格调控")
        prices = {
            "普通": st.number_input("普通级价格", 0, 1000, 20),
            "稀有": st.number_input("稀有级价格", 0, 1000, 50),
            "传说": st.number_input("传说级价格", 0, 1000, 80),
            "史诗": st.number_input("史诗级价格", 0, 1000, 160)
        }
        
        st.subheader("道具成本调控")
        items = {
            "姻缘丹": st.number_input("姻缘丹价格", 0, 100, 5),
            "饲料": st.number_input("饲料价格", 0, 100, 5),
            "仙草": st.number_input("仙草价格", 0, 100, 15)
        }

    try:
        df = calculate_phase_data(
            supreme_count=count,
            breeding_cycle=cycle,
            release_rate=release_rate,
            item_prices=items,
            market_prices=prices,
            transaction_fee=fee_rate,
            supreme_price=price
        )
    except Exception as e:
        st.error(f"模拟失败: {str(e)}")
        return

    # 可视化仪表盘
    st.header("经济调控看板")
    
    # 第一行指标
    cols = st.columns(4)
    cols[0].metric("总调控规模", f"{count}只至尊", 
                 f"{df['普通后代'].iloc[0]:.0f}普通")
    cols[1].metric("市场总供给", f"{df.iloc[0,9:13].sum():.0f}只",
                 f"稀有 {df['稀有后代'].iloc[0]:.0f}只")
    cols[2].metric("用户净收益", f"¥{df['用户净收益'].iloc[0]:,.0f}", 
                 delta_color="inverse" if df['用户净收益'].iloc[0]<0 else "normal")
    cols[3].metric("用户净收益率", f"{df['用户净收益率(%)'].iloc[0]:.1f}%")  # 新增指标卡

    # 第二行数据
    st.subheader("成本收益分析")
    cost_df = pd.DataFrame({
        "项目": ["至尊成本", "道具成本", "手续费"],
        "金额": [df["至尊总成本"].iloc[0], df["至尊总成本"].iloc[0]-count*price, df["交易手续费"].iloc[0]]
    })
    st.bar_chart(cost_df.set_index("项目"))

    # 第三行明细
    st.subheader("模拟明细数据")
    st.dataframe(
        df.style.format({
            "总销售额": "¥{:.0f}",
            "用户净收益": "¥{:.0f}",
            "平台总收益": "¥{:.0f}",
            "用户净收益率(%)": "{:.2f}%"  # 新增格式化
        }),
        use_container_width=True
    )

if __name__ == "__main__":
    main()
