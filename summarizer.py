import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI  # DeepSeek兼容OpenAI的接口格式，直接用这个库
from pubmed_search import search_pubmed  # 引入第一阶段写的检索函数

# 初始化DeepSeek客户端
client = OpenAI(
    api_key="DEEPSEEK_API_KEY",  
    base_url="https://api.deepseek.com"  # DeepSeek的API地址
)

def summarize_articles(query, articles):
    """
    把多篇文献的摘要喂给DeepSeek，让它综合总结
    query: 用户原始问题
    articles: 第一阶段返回的文献列表
    """
    
    # 把所有文献摘要拼成一段文本，带上PMID方便引用
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"""
文献{i}:
PMID: {article['pmid']}
标题: {article['title']}
摘要: {article['abstract']}
---
"""
    
    # 设计Prompt，要求模型必须引用PMID
    prompt = f"""你是一位医学文献综述专家。
    
用户的研究问题是：{query}

以下是从PubMed检索到的相关文献：
{articles_text}

请根据以上文献，生成一份结构化的研究报告，格式如下：

## 研究背景
（用2-3句话说明这个领域的研究现状）

## 核心发现
（列出3-5个最重要的发现，每个发现必须在句末标注来源PMID，格式：[PMID: xxxxxxxx]）

## 研究空白
（指出目前研究还没有解决的问题）

## 参考文献
（列出所有引用的文献，格式：PMID | 标题 | 链接）

重要规则：每一个具体结论都必须附带PMID引用，不能出现没有来源的论断。
"""
    
    response = client.chat.completions.create(
        model="deepseek-chat",  # DeepSeek的模型名称
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3  # temperature越低，输出越稳定保守，适合学术场景
    )
    
    return response.choices[0].message.content
    # choices[0].message.content：取模型返回的第一个回答的文字内容


# 测试
if __name__ == "__main__":
    query = "sarcopenia biomarkers in elderly patients"
    
    print("正在检索PubMed...")
    articles = search_pubmed(query, max_results=5)
    print(f"找到 {len(articles)} 篇文献，正在生成报告...")
    
    report = summarize_articles(query, articles)
    print(report)