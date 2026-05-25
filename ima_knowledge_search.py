"""
IMA知识库搜索脚本 - 搜索命理学相关内容
"""

import requests
import json

# IMA API配置
API_BASE_URL = "https://ima.qq.com"
API_PATH = "/openapi/wiki/v1"
CLIENT_ID = "e5d40036560f53a3a161dbede81bcbce"
API_KEY = "8a7nfU0hRrrsY5ARn4nB/rolftIPnFS3ftMBQFBU/zm8cZ7wa+oOvMLfXjitnwNfIVe4BUvrxQ=="

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

def search_knowledge_base_list(query, limit=20):
    """搜索知识库列表"""
    print(f"\n搜索知识库: {query}")
    payload = {
        "query": query,
        "cursor": "",
        "limit": limit
    }
    
    data = ima_api_call("search_knowledge_base", payload)
    if data:
        info_list = data.get("info_list", [])
        print(f"找到 {len(info_list)} 个知识库:")
        for info in info_list:
            print(f"  - {info.get('name')} (ID: {info.get('id')})")
        return info_list
    return []

def get_knowledge_list(knowledge_base_id, folder_id=None, limit=50):
    """浏览知识库内容"""
    print(f"\n浏览知识库内容 (ID: {knowledge_base_id})")
    payload = {
        "cursor": "",
        "limit": limit,
        "knowledge_base_id": knowledge_base_id
    }
    
    if folder_id:
        payload["folder_id"] = folder_id
    
    data = ima_api_call("get_knowledge_list", payload)
    if data:
        knowledge_list = data.get("knowledge_list", [])
        print(f"找到 {len(knowledge_list)} 个条目:")
        for item in knowledge_list:
            media_id = item.get("media_id", "")
            title = item.get("title", "无标题")
            print(f"  - {title} (ID: {media_id})")
        return knowledge_list
    return []

def search_knowledge_content(knowledge_base_id, query, limit=20):
    """搜索知识库内容"""
    print(f"\n搜索知识库内容: {query}")
    payload = {
        "query": query,
        "cursor": "",
        "knowledge_base_id": knowledge_base_id
    }
    
    data = ima_api_call("search_knowledge", payload)
    if data:
        info_list = data.get("info_list", [])
        print(f"找到 {len(info_list)} 个结果:")
        for info in info_list:
            title = info.get("title", "无标题")
            highlight = info.get("highlight_content", "")[:100]
            print(f"  - {title}")
            if highlight:
                print(f"    摘要: {highlight}...")
        return info_list
    return []

def main():
    """主函数"""
    print("=" * 60)
    print("IMA知识库搜索 - 命理学内容")
    print("=" * 60)
    
    # 1. 搜索知识库列表
    print("\n步骤1: 搜索可用的知识库")
    kb_list = search_knowledge_base_list("命理")
    
    if not kb_list:
        print("\n尝试搜索其他关键词...")
        kb_list = search_knowledge_base_list("八字")
    
    if not kb_list:
        print("\n尝试搜索'风水'...")
        kb_list = search_knowledge_base_list("风水")
    
    if not kb_list:
        print("\n尝试搜索'紫微'...")
        kb_list = search_knowledge_base_list("紫微")
    
    # 2. 如果找到知识库，浏览其内容
    if kb_list:
        print("\n" + "=" * 60)
        print("步骤2: 浏览知识库内容")
        
        for kb in kb_list[:3]:  # 只处理前3个知识库
            kb_id = kb.get("id")
            kb_name = kb.get("name")
            
            print(f"\n知识库: {kb_name}")
            print("-" * 40)
            
            # 浏览内容
            items = get_knowledge_list(kb_id)
            
            # 搜索具体内容
            print(f"\n在 '{kb_name}' 中搜索具体内容:")
            search_knowledge_content(kb_id, "天干地支")
            search_knowledge_content(kb_id, "十神")
            search_knowledge_content(kb_id, "五行")
            search_knowledge_content(kb_id, "风水")
            search_knowledge_content(kb_id, "紫微斗数")
    
    # 3. 获取所有可用知识库
    print("\n" + "=" * 60)
    print("步骤3: 获取所有可用知识库")
    
    payload = {
        "cursor": "",
        "limit": 50
    }
    data = ima_api_call("get_addable_knowledge_base_list", payload)
    if data:
        addable_list = data.get("addable_knowledge_base_list", [])
        print(f"\n共有 {len(addable_list)} 个可访问的知识库:")
        for kb in addable_list:
            print(f"  - {kb.get('name')} (ID: {kb.get('id')})")

if __name__ == "__main__":
    main()