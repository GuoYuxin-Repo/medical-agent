import streamlit as st  
import time
from agent import run_agent

# 页面基本设置
st.set_page_config(
    page_title="医疗文献调研 AI Agent",
    page_icon="🔬",
    layout="wide"  
)

st.title("🔬 医疗文献调研 AI Agent")
st.caption("基于 PubMed + DeepSeek，自动检索文献并生成结构化研究报告")

# 左侧说明栏
with st.sidebar:
    st.header("使用说明")
    st.markdown("""
    1. 在输入框里输入你的研究问题
    2. 点击"开始调研"
    3. Agent会自动拆解问题、检索PubMed、生成报告
    4. 报告中每条结论都附有PMID引用
    """)
    st.divider()
    st.caption("数据来源：PubMed | 推理模型：DeepSeek")

# 主界面
question = st.text_area(
    "输入你的研究问题",
    placeholder="例如：肌少症的血液生物标志物有哪些，在临床诊断中的应用价值如何？",
    height=100
)

col1, col2 = st.columns([1, 4])  
with col1:
    start_button = st.button("开始调研", type="primary", use_container_width=True)

if start_button and question:
    # 显示进度提示
    with st.status("Agent运行中...", expanded=True) as status:
        st.write("正在拆解研究问题...")
        time.sleep(1)
        st.write("正在检索PubMed数据库...")
        
        # 运行Agent
        start_time = time.time()
        report = run_agent(question)
        elapsed = round(time.time() - start_time, 1)
        # time.time()：返回当前时间戳，两次相减得到耗时
        
        st.write(f"报告生成完成，耗时 {elapsed} 秒")
        status.update(label="调研完成", state="complete")
    
    # 显示报告
    st.divider()
    st.subheader("📄 研究报告")
    st.markdown(report)  
    
    # 显示耗时指标
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("报告生成耗时", f"{elapsed} 秒")
    with col2:
        st.metric("数据来源", "PubMed")
    
    # 下载按钮
    st.download_button(
        label="下载报告（Markdown格式）",
        data=report,
        file_name="research_report.md",
        mime="text/markdown"
    )

elif start_button and not question:
    st.warning("请先输入研究问题")