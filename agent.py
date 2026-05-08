from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pubmed_search import search_pubmed

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-b3ff1879b24345ab9fd7dcbb3dc3782f",  # 替换成你的Key
    base_url="https://api.deepseek.com",
    temperature=0.3
)

@tool
def pubmed_search_tool(query: str) -> str:
    """在PubMed上检索医学文献，输入英文检索词，返回相关文献标题和摘要。"""
    results = search_pubmed(query, max_results=5)
    if not results:
        return "未找到相关文献"
    output = ""
    for r in results:
        output += f"PMID:{r['pmid']} | {r['title']}\n摘要:{r['abstract'][:300]}\n---\n"
    return output

system_prompt = """你是一位医学文献调研助手。
当用户提出医学研究问题时：
1. 将问题拆解为2-3个英文检索词，分别调用pubmed_search_tool
2. 综合所有结果，生成包含以下部分的报告：
   - 研究背景
   - 核心发现（每条必须附[PMID: xxxxxxxx]）
   - 研究空白
   - 参考文献
规则：每个结论必须有PMID来源，不允许无引用的论断。"""

agent = create_react_agent(
    model=llm,
    tools=[pubmed_search_tool],
    prompt=system_prompt
)

def run_agent(user_question):
    print(f"\n问题：{user_question}")
    print("Agent正在思考和检索，请稍候...\n")
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_question}]
    })
    return result["messages"][-1].content

if __name__ == "__main__":
    question = "肌少症的血液生物标志物有哪些，在临床诊断中的应用价值如何？"
    report = run_agent(question)
    print(report)