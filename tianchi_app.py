# tianchi_app.py
import streamlit as st
import pandas as pd
from economic_model import EconomicModel

def main():
    st.set_page_config(page_title="天池经济沙盘", layout="wide")
    st.title("📊 天池经济模型沙盘推演系统")
    
    with st.sidebar:
        st.header("推演参数配置")
        phase_month = st.slider("推演阶段月份", 1, 6, 1)
        col1, col2 = st.columns(2)
        with col1:
            supreme_count = st.number_input("至尊级投放量", min_value=1, value=300, step=10)
        with col2:
            dynamic_price = st.number_input("动态定价(元)", min_value=50, value=55, step=5)
        
        st.markdown("**系统常数**")
        st.metric("道具成本/至尊级", "365神由币")
        st.metric("基础产量/周期", "30只(12+9+6+3)")

    # 执行经济推演
    try:
        df = EconomicModel.calculate_phase(
            supreme_count=supreme_count,
            phase_month=phase_month
        )
        df["动态定价"] = dynamic_price  # 覆盖动态定价参数
    except Exception as e:
        st.error(f"推演失败: {str(e)}")
        return

    # 可视化展示
    st.subheader("经济指标看板")
    
    # 第一行指标卡
    cols = st.columns(4)
    cols[0].metric("平台总收益", f"¥{df['平台总收益'].iloc[0]:,.0f}", 
                 delta="+14.3%" if phase_month>1 else None)
    cols[1].metric("用户净收益", f"¥{df['用户净收益'].iloc[0]:,.0f}",
                 delta_color="inverse" if df['用户净收益'].iloc[0]<0 else "normal")
    cols[2].metric("市场流通量", f"{df['后代总产量'].iloc[0]:,.0f}只")
    cols[3].metric("用户留存率", f"{df['用户留存率'].iloc[0]*100:.1f}%")

    # 第二行数据表格
    st.subheader("明细数据矩阵")
    detail_df = df[['至尊投放量', '动态定价', '至尊级成本', '道具总成本', 
                  '交易手续费', '市场消化率']].T.reset_index()
    detail_df.columns = ['指标', '数值']
    st.dataframe(
        detail_df.style.format({"数值": "{:,.0f}"}), 
        hide_index=True,
        use_container_width=True
    )

    # 第三阶段趋势图
    st.subheader("阶段趋势预测")
    phase_data = [EconomicModel.calculate_phase(phase_month=m).iloc[0] for m in range(1,7)]
    trend_df = pd.DataFrame(phase_data)
    fig = px.line(
        trend_df, 
        x='阶段月份', 
        y=['平台总收益', '用户净收益'],
        title="6个月经济趋势预测",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
