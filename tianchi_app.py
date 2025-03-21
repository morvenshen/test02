import streamlit as st
import pandas as pd
import plotly.express as px
from economic_model import EconomicModel

# 初始化模型
model = EconomicModel()

def main():
    st.set_page_config(page_title="天池经济模拟", layout="wide")
    
    # 侧边栏参数控制
    with st.sidebar:
        st.header("核心参数配置")
        params = {
            '至尊数量': st.slider("至尊级神兽数量", 1, 3000, 300),
            '放生率': st.slider("放生率", 0.0, 1.0, 0.7),
            '姻缘丹': st.number_input("姻缘丹消耗量", 30),
            '饲料': st.number_input("饲料消耗量", 37),
            '仙草': st.number_input("仙草消耗量", 2)
        }
    
    # 模型计算
    results = model.calculate_monthly(params)
    
    # 主界面布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("经济指标")
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("平台收益", f"¥{results['平台收益']:,.0f}")
        metric_col2.metric("用户净收益", f"¥{results['用户净收益']:,.0f}")
        
        st.write("### 市场流通分析")
        fig1 = px.bar(
            x=['当前流通量'],
            y=[results['市场流通量']],
            labels={'x': '指标', 'y': '数量'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("健康度仪表盘")
        st.write("#### 风险监测")
        
        # 风险指标计算
        risk_level = "🟢 正常" 
        if results['用户净收益'] / results['平台收益'] < 0.2:
            risk_level = "🔴 收益失衡"
        elif results['市场流通量'] > 2000 * 5:
            risk_level = "🟡 流通量预警"
            
        st.metric("系统状态", risk_level)
        
        st.write("### 收益结构分析")
        fig2 = px.pie(
            names=['平台收益', '用户收益'],
            values=[results['平台收益'], results['用户净收益']]
        )
        st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
