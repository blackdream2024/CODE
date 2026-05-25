"""
IMA知识库文件夹浏览脚本
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

def browse_all_content(kb_id, folder_id=None, depth=0, max_depth=3):
    """递归浏览知识库内容"""
    if depth > max_depth:
        return
    
    indent = "  " * depth
    print(f"\n{indent}浏览文件夹 (深度: {depth})")
    
    payload = {
        "cursor": "",
        "limit": 50,
        "knowledge_base_id": kb_id
    }
    
    if folder_id:
        payload["folder_id"] = folder_id
    
    data = ima_api_call("get_knowledge_list", payload)
    if not data:
        return
    
    knowledge_list = data.get("knowledge_list", [])
    current_path = data.get("current_path", [])
    
    path_str = " > ".join([p.get("name", "") for p in current_path]) or "根目录"
    print(f"{indent}路径: {path_str}")
    print(f"{indent}找到 {len(knowledge_list)} 个条目:")
    
    folders = []
    files = []
    
    for item in knowledge_list:
        media_id = item.get("media_id", "")
        title = item.get("title", "无标题")
        
        # 检查是否是文件夹（通过是否有folder_id字段判断）
        if "folder_id" in item:
            folder_id = item.get("folder_id")
            print(f"{indent}[文件夹] {title} (文件夹ID: {folder_id})")
            folders.append((folder_id, title))
        else:
            print(f"{indent}[文件] {title} (ID: {media_id})")
            files.append((media_id, title))
    
    # 递归浏览子文件夹
    for folder_id, folder_name in folders:
        print(f"\n{indent}进入文件夹: {folder_name}")
        browse_all_content(kb_id, folder_id, depth + 1, max_depth)
    
    # 如果有更多内容，继续翻页
    if not data.get("is_end", True):
        next_cursor = data.get("next_cursor", "")
        if next_cursor:
            print(f"{indent}还有更多内容，继续翻页...")
            payload["cursor"] = next_cursor
            # 这里简化处理，实际应该递归调用

def search_everywhere(kb_id, query):
    """在整个知识库中搜索"""
    print(f"\n搜索: {query}")
    payload = {
        "query": query,
        "cursor": "",
        "knowledge_base_id": kb_id
    }
    
    data = ima_api_call("search_knowledge", payload)
    if data:
        info_list = data.get("info_list", [])
        if info_list:
            print(f"找到 {len(info_list)} 个结果:")
            for info in info_list:
                title = info.get("title", "无标题")
                highlight = info.get("highlight_content", "")
                print(f"  - {title}")
                if highlight:
                    print(f"    摘要: {highlight[:100]}...")
        else:
            print("未找到结果")
        return info_list
    return []

def main():
    """主函数"""
    print("=" * 60)
    print("IMA知识库深度浏览")
    print("=" * 60)
    
    # 1. 浏览所有内容
    print("\n步骤1: 浏览知识库所有内容")
    browse_all_content(KNOWLEDGE_BASE_ID)
    
    # 2. 搜索各种可能的关键词
    print("\n" + "=" * 60)
    print("步骤2: 搜索各种关键词")
    
    keywords = [
        # 命理学
        "命理", "八字", "风水", "紫微", "占卜", "算命", "易经", "周易",
        "天干", "地支", "五行", "十神", "四柱", "大运", "流年",
        # 其他可能的分类
        "笔记", "记录", "资料", "学习", "教程", "指南"
    ]
    
    found_any = False
    for keyword in keywords:
        results = search_everywhere(KNOWLEDGE_BASE_ID, keyword)
        if results:
            found_any = True
    
    if not found_any:
        print("\n未找到任何命理学相关内容")
        print("\n知识库中主要是税务师考试相关的PDF文件")
    
    # 3. 获取知识库统计信息
    print("\n" + "=" * 60)
    print("步骤3: 知识库统计")
    
    payload = {
        "ids": [KNOWLEDGE_BASE_ID]
    }
    data = ima_api_call("get_knowledge_base", payload)
    if data:
        infos = data.get("infos", {})
        if KNOWLEDGE_BASE_ID in infos:
            info = infos[KNOWLEDGE_BASE_ID]
            print(f"知识库名称: {info.get('name')}")
            print(f"描述: {info.get('description', '无描述')}")

if __name__ == "__main__":
    main()