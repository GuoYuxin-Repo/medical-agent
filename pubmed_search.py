import requests

def search_pubmed(query, max_results=5):
    # 第一步：搜索拿ID列表
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    search_response = requests.get(search_url, params=search_params)
    id_list = search_response.json()["esearchresult"]["idlist"]
    
    if not id_list:
        return []

    # 第二步：用summary接口拿标题，JSON格式，没有XML解析问题
    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    summary_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "json"
    }
    summary_response = requests.get(summary_url, params=summary_params)
    summary_data = summary_response.json()

    # 第三步：单独拿摘要，还是用efetch但改用text格式
    results = []
    for pmid in id_list:
        doc = summary_data.get("result", {}).get(pmid, {})
        title = doc.get("title", "N/A")
        
        # 单篇拿摘要，用text格式
        abstract_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        abstract_params = {
            "db": "pubmed",
            "id": pmid,
            "rettype": "abstract",
            "retmode": "text"  # 用纯文本格式，不用XML
        }
        abstract_response = requests.get(abstract_url, params=abstract_params)
        abstract_text = abstract_response.text[:500]  # 只取前500字符
        
        results.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract_text,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        })
    
    return results

# 测试
if __name__ == "__main__":
    results = search_pubmed("sarcopenia biomarkers", max_results=3)
    for r in results:
        print(f"PMID: {r['pmid']}")
        print(f"标题: {r['title']}")
        print(f"摘要: {r['abstract'][:200]}")
        print("---")