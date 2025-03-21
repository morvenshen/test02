# tianchi_app.py
import streamlit as st
import pandas as pd
from economic_model import calculate_phase_data

def main():
    st.set_page_config(page_title="经济模型优化模拟器", layout="wide")
    st.title("📈 天池经济收益优化系统")
    
    with st.sidebar:
        st.header("收益增强参数")
        col1, col2 = st.columns(2)
        with col1:
            price_multiplier = st.slider("价格倍率", 0.5, 2.0, 1.0, 0.1)
            item_discount = st.slider("道具折扣", 0.5, 1.0, 1.0, 0.05)
        with col2:
            fee_rate = st.slider("手续费率", 0.0, 0.15, 0.03, 0.01)
            cycle = st.slider("繁殖加速", 10, 60, 30, 
                            help="缩短繁殖周期可提升收益率")
        
        st.subheader("市场价格体系")
        base_prices = {
            "普通": st.number_input("普通基准价", 20),
            "稀有": st.number_input("稀有基准价", 50),
            "传说": st.number_input("传说基准价", 80),
            "史诗": st.number_input("史诗基准价", 160)
        }
        prices = {k:v*price_multiplier for k,v in base_prices.items()}
        
        st.subheader("成本控制")
        items = {
            "姻缘丹": st.number_input("姻缘丹成本", 5) * item_discount,
            "饲料": st.number_input("饲料成本", 5) * item_discount,
            "仙草": st.number_input("仙草成本", 15) * item_discount
        }

    try:
        df = calculate_phase_data(
            supreme_count=300,
            breeding_cycle=cycle,
            item_prices=items,
            market_prices=prices,
            transaction_fee=fee_rate,
            price_multiplier=price_multiplier,
            item_discount=item_discount
        )
    except Exception as e:
        st.error(f"模拟失败: {str(e)}")
        return

    # 可视化看板
    st.header("收益优化仪表盘")
    
    # 第一行关键指标
    cols = st.columns(4)
    cols[0].metric("用户收益率", f"{df['用户收益率'].iloc[0]:.1f}%",
                 delta=f"+{(df['用户收益率'].iloc[0]-14.3):.1f}%" if df['用户收益率'].iloc[0]>14.3 else None)
    cols[1].metric("收益杠杆率", f"{price_multiplier}x",
                 f"道具折扣{item_discount}x")
    cols[2].metric("净收益增幅", 
                 f"{(df['用户净收益'].iloc[0]/70650-1)*100:.1f}%" if df['用户净收益'].iloc[0] else "N/A",
                 "基准: 首月70,650")
    cols[3].metric("生态健康度", 
                 "✅ 优良" if df['用户收益率'].iloc[0] > 15 else "⚠️ 警戒",
                 f"{df['市场消化率'].iloc[0]*100:.0f}%消化率")

    # 第二行收益分析
    st.subheader("收益结构优化")
    profit_df = pd.DataFrame({
        "项目": ["理论最大值", "当前值", "建议阈值"],
        "价格倍率": [2.0, price_multiplier, "≤1.8"],
        "道具折扣": [0.5, item_discount, "≥0.6"],
        "手续费率": [0.01, fee_rate, "≤0.05"]
    }).set_index("项目")
    st.bar_chart(profit_df.T)

    # 第三行参数建议
    st.subheader("优化建议引擎")
    advice = []
    if price_multiplier < 1.5:
        advice.append("提高价格倍率至1.5x以上（当前%.1fx）" % price_multiplier)
    if item_discount > 0.7:
        advice.append("道具折扣可降至0.7x以下（当前%.2fx）" % item_discount)
    if fee_rate > 0.05:
        advice.append("手续费率建议低于5%（当前%.0f%%）" % (fee_rate*100))
    
    if advice:
        st.warning("🚀 收益提升机会：" + " | ".join(advice))
    else:
        st.success("✅ 当前参数处于最优区间")

if __name__ == "__main__":
    main()
