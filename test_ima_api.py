"""
测试IMA知识库API访问
"""

import requests
import json

# IMA API配置
API_BASE_URL = "https://ima.qq.com"
CLIENT_ID = "e5d40036560f53a3a161dbede81bcbce"
API_KEY = "8a7nfU0hRrrsY5ARn4nB/rolftIPnFS3ftMBQFBU/zm8cZ7wa+oOvMLfXjitnwNfIVe4BUvrxQ=="

def test_ima_api():
    """测试IMA API连接"""
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "X-Client-Id": CLIENT_ID,
        "X-API-Key": API_KEY
    }
    
    # 尝试搜索知识库
    search_payload = {
        "query": "八字命理",
        "limit": 10
    }
    
    try:
        # 尝试不同的API端点
        endpoints = [
            "/api/v1/knowledge/search",
            "/api/knowledge/search", 
            "/v1/knowledge/search",
            "/knowledge/search",
            "/api/search",
            "/search"
        ]
        
        for endpoint in endpoints:
            url = f"{API_BASE_URL}{endpoint}"
            print(f"\n尝试端点: {url}")
            
            try:
                response = requests.post(url, headers=headers, json=search_payload, timeout=10)
                print(f"状态码: {response.status_code}")
                
                if response.status_code != 404:
                    print(f"响应内容: {response.text[:500]}")
                    
                    if response.status_code == 200:
                        print("成功！找到可用端点")
                        return True
                        
            except requests.exceptions.RequestException as e:
                print(f"请求错误: {e}")
                continue
        
        print("\n所有端点尝试失败")
        return False
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_with_different_auth():
    """尝试不同的认证方式"""
    
    # 方法1: Authorization header
    headers_v1 = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "X-Client-Id": CLIENT_ID
    }
    
    # 方法2: 查询参数
    params = {
        "client_id": CLIENT_ID,
        "api_key": API_KEY
    }
    
    search_payload = {
        "query": "风水",
        "limit": 5
    }
    
    test_url = f"{API_BASE_URL}/api/v1/knowledge/search"
    
    print("\n尝试认证方式1: Authorization header")
    try:
        response = requests.post(test_url, headers=headers_v1, json=search_payload, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:300]}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n尝试认证方式2: 查询参数")
    try:
        response = requests.post(test_url, params=params, json=search_payload, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:300]}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("IMA知识库API测试")
    print("=" * 60)
    
    # 测试基础连接
    test_ima_api()
    
    # 测试不同认证方式
    test_with_different_auth()