"""
IMA知识库内容探索脚本
"""

import requests
import json

# IMA API配置
API_BASE_URL = "https://ima.qq.com"
API_PATH = "/openapi/wiki/v1"
CLIENT_ID = "e5d40036560f53a3a161dbede81bcbce"
API_KEY = "8a7nfU0hRrrsY5ARn4nB/rolftIPnFS3ftMBQFBU/zm8cZ7wa+oOvMLfXjitnwNfIVe4BUvrxQ=="

# 已知知识库ID
KNOWLEDGE_BASE_ID = "mim4sm_1q24G3rkLPAybK1Tzv572vxbkuGjCsKIDwHA="

def ima_api_call(endpoint, payload):
    """调用IMA API"""
    url = f"{API_BASE_URL}{API_PATH}/{endpoint}"
    
    headers = {
        "Content-Type": "application/json",
        "ima-openapi-clientid": CLIENT_ID,
        "ima-openapi-apikey": API_KEY
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            print(f"API错误: {result.get('msg', '未知错误')}")
            return None
            
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def get_knowledge_base_info(kb_id):
    """获取知识库信息"""
    print(f"\n获取知识库信息: {kb_id}")
    payload = {
        "ids": [kb_id]
    }
    
    data = ima_api_call("get_knowledge_base", payload)
    if data:
        infos = data.get("infos", {})
        if kb_id in infos:
            info = infos[kb_id]
            print(f"知识库名称: {info.get('name')}")
            print(f"描述: {info.get('description', '无')}")
            return info
    return None

def browse_knowledge_list(kb_id, folder_id=None, limit=50):
    """浏览知识库内容"""
    print(f"\n浏览知识库内容 (ID: {kb_id})")
    payload = {
        "cursor": "",
        "limit": limit,
        "knowledge_base_id": kb_id
    }
    
    if folder_id:
        payload["folder_id"] = folder_id
    
    data = ima_api_call("get_knowledge_list", payload)
    if data:
        knowledge_list = data.get("knowledge_list", [])
        current_path = data.get("current_path", [])
        
        print(f"当前路径: {'/'.join([p.get('name', '') for p in current_path]) or '根目录'}")
        print(f"找到 {len(knowledge_list)} 个条目:")
        
        for item in knowledge_list:
            media_id = item.get("media_id", "")
            title = item.get("title", "无标题")
            print(f"  - {title} (ID: {media_id})")
        
        return knowledge_list, data.get("is_end", True), data.get("next_cursor", "")
    return [], True, ""

def search_in_knowledge_base(kb_id, query, limit=20):
    """在知识库中搜索"""
    print(f"\n搜索: {query}")
    payload = {
        "query": query,
        "cursor": "",
        "knowledge_base_id": kb_id
    }
    
    data = ima_api_call("search_knowledge", payload)
    if data:
        info_list = data.get("info_list", [])
        print(f"找到 {len(info_list)} 个结果:")
        
        results = []
        for info in info_list:
            title = info.get("title", "无标题")
            media_id = info.get("media_id", "")
            highlight = info.get("highlight_content", "")
            
            print(f"\n  标题: {title}")
            print(f"  ID: {media_id}")
            if highlight:
                print(f"  摘要: {highlight[:200]}...")
            
            results.append({
                "title": title,
                "media_id": media_id,
                "highlight": highlight
            })
        
        return results
    return []

def get_media_info(media_id):
    """获取媒体详细信息"""
    print(f"\n获取媒体信息: {media_id}")
    payload = {
        "media_id": media_id
    }
    
    data = ima_api_call("get_media_info", payload)
    if data:
        media_type = data.get("media_type")
        url_info = data.get("url_info")
        
        print(f"媒体类型: {media_type}")
        
        if url_info:
            url = url_info.get("url")
            headers = url_info.get("headers", {})
            print(f"访问链接: {url}")
            
            # 尝试获取内容
            if url:
                try:
                    response = requests.get(url, headers=headers, timeout=30)
                    if response.status_code == 200:
                        content = response.text[:1000]
                        print(f"\n内容预览:\n{content}...")
                        return content
                    else:
                        print(f"获取内容失败: {response.status_code}")
                except Exception as e:
                    print(f"获取内容错误: {e}")
        
        return data
    return None

def main():
    """主函数"""
    print("=" * 60)
    print("IMA知识库内容探索")
    print("=" * 60)
    
    # 1. 获取知识库信息
    kb_info = get_knowledge_base_info(KNOWLEDGE_BASE_ID)
    
    # 2. 浏览根目录
    print("\n" + "=" * 60)
    print("浏览根目录")
    items, is_end, next_cursor = browse_knowledge_list(KNOWLEDGE_BASE_ID)
    
    # 3. 搜索命理学相关内容
    print("\n" + "=" * 60)
    print("搜索命理学相关内容")
    
    search_queries = [
        "八字",
        "天干地支",
        "十神",
        "五行",
        "风水",
        "紫微斗数",
        "命理",
        "四柱",
        "大运",
        "流年"
    ]
    
    all_results = {}
    for query in search_queries:
        results = search_in_knowledge_base(KNOWLEDGE_BASE_ID, query)
        if results:
            all_results[query] = results
    
    # 4. 尝试获取一些内容的详细信息
    print("\n" + "=" * 60)
    print("获取详细内容")
    
    # 收集所有找到的media_id
    media_ids = set()
    for query, results in all_results.items():
        for result in results:
            media_ids.add(result.get("media_id"))
    
    # 获取前5个媒体的详细信息
    for media_id in list(media_ids)[:5]:
        if media_id:
            get_media_info(media_id)
    
    # 5. 保存搜索结果
    print("\n" + "=" * 60)
    print("保存搜索结果")
    
    output_file = "ima_search_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "knowledge_base_id": KNOWLEDGE_BASE_ID,
            "knowledge_base_info": kb_info,
            "search_results": all_results,
            "media_ids": list(media_ids)
        }, f, ensure_ascii=False, indent=2)
    
    print(f"搜索结果已保存到: {output_file}")

if __name__ == "__main__":
    main()