"""
天池应用前端
版本：2.4
最终修复版：修正所有语法错误
"""
from economic_model import TaoistEconSimulator
import pandas as pd
import altair as alt
import streamlit as st

class TianchiApp:
    def __init__(self, params):
        self._validate_init_params(params)
        self.simulator = TaoistEconSimulator(params)
        self.simulation_data = None
        
    def _validate_init_params(self, params):
        """参数预校验"""
        required = ['放生率', '初始至尊数量']
        missing = [k for k in required if k not in params]
        if missing:
            raise ValueError(f"缺失必要初始化参数: {', '.join(missing)}")

    def 运行模拟(self, 月份数=6):
        """带异常捕获的模拟运行"""
        try:
            self.simulation_data = self.simulator.多周期模拟(月份数)
            return self.simulation_data
        except Exception as e:
            st.error(f"模拟运行失败: {str(e)}")
            raise

    def 生成折线图(self, 字段):
        """增强容错的数据可视化"""
        try:
            df = pd.DataFrame(self.simulation_data['月度数据'])
            
            # 动态字段处理
            if 字段 == '总实际流通量':
                df['总实际流通量'] = [x['总实际流通量'] for x in df['实际流通量']]
            elif 字段 in ['普通', '稀有', '传说', '史诗']:
                df[字段] = df['实际流通量'].apply(lambda x: x.get(字段, 0))
            else:
                df[字段] = df[字段].apply(lambda x: x.get(字段, x) if isinstance(x, dict) else x)
            
            return alt.Chart(df).mark_line().encode(
                x='月份:O',
                y=f'{字段}:Q',
                tooltip=[f'{字段}']
            ).properties(
                width=400,
                height=300
            )
        except KeyError:
            st.error(f"不支持的字段: {字段}")
        except Exception as e:
            st.error(f"图表生成失败: {str(e)}")

    def 显示仪表盘(self):
        """带状态检查的可视化看板"""
        if not self.simulation_data:
            st.warning("请先运行模拟")
            return
        
        try:
            with st.spinner('生成数据看板...'):
                # 关键指标卡
                col1, col2 = st.columns(2)
                
                # 修复点1：补全括号
                平台总收益 = sum([m['平台收益']['总收益'] for m in self.simulation_data['月度数据']])
                col1.metric("平台总收益", f"¥{平台总收益:,.2f}")
                
                # 修复点2：修正字段名
                总功德值 = sum([m['总功德值'] for m in self.simulation_data['月度数据']])
                col2.metric("总功德值", f"{总功德值:,.2f}")
                
                # 图表区
                st.altair_chart(self.生成折线图('市场饱和度'), use_container_width=True)
                st.altair_chart(self.生成折线图('总实际流通量'), use_container_width=True)
                
        except Exception as e:
            st.error(f"看板渲染失败: {str(e)}")

if __name__ == "__main__":
    # Streamlit 适配
    st.title("天池经济模拟系统")
    
    # 参数配置界面
    with st.sidebar:
        st.header("模拟参数")
        放生率 = st.slider("放生率", 0.0, 1.0, 0.7)
        初始数量 = st.number_input("初始至尊数量", 100, 1000, 300)
        
    # 运行模拟
    try:
        app = TianchiApp({
            '放生率': 放生率,
            '初始至尊数量': 初始数量
        })
        app.运行模拟()
        app.显示仪表盘()
        
    except Exception as e:
        st.error(f"系统运行异常: {str(e)}")
        st.stop()
