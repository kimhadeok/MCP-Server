# https://mcp.tavily.com/mcp/?tavilyApiKey=TAVILY_API_KEY

import requests
from fastmcp import FastMCP
from dotenv import load_dotenv
import os

load_dotenv()

# MCP 서버 초기화
mcp = FastMCP("Tavily-Free-Search")

# 💡 발급받은 무료 API 키를 여기에 넣으세요 (매달 1,000회 평생 무료 자동 리필)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@mcp.tool()
def search_web_free(query: str) -> str:
    """
    Tavily API를 이용하여 차단 없이 실시간 최신 정보(날씨, 뉴스 등)를 검색합니다.
    args:
        query (str): 검색할 쿼리 문장이나 단어
    """
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 1
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        results = response.json().get("results", [])
        
        if not results:
            return "검색 결과를 찾지 못했습니다."
            
        output = []
        for item in results:
            output.append(f"▶ 제목: {item['title']}\n- 내용: {item['content']}\n- 출처: {item['url']}\n")
        return "\n".join(output)
        
    except Exception as e:
        return f"Tavily 검색 중 오류 발생: {str(e)}"

if __name__ == "__main__":
    print("--- Tavily 실시간 검색 테스트 ---")
    print(search_web_free("서울 오늘 날씨"))
    # print(search_web_free("최신 해외 톱 뉴스는?"))
