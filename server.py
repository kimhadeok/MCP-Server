import os

from fastmcp import FastMCP
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
client = TavilyClient(TAVILY_API_KEY)

# MCP 서버 초기화
mcp = FastMCP("Tavily-Search")

@mcp.tool()
def search_web(query: str) -> str:
    """
    Tavily API를 이용하여 차단 없이 실시간 최신 정보(날씨, 뉴스 등)를 검색합니다.
    args:
        query (str): 검색할 쿼리 문장이나 단어
    """

    try:
        response = client.search(
            query=query,
            # include_answer="advanced",
            # search_depth="advanced",
            search_depth="basic",
            max_results=2,
        )

        results = response.get("results", [])
        if not results:
            return "검색 결과를 찾지 못했습니다."
            
        # output = []
        # for index, item in enumerate(results, 1):
        #     output.append(f"▶ [{index}] 제목: {item['title']}\n- 내용: {item['content']}\n- 출처: {item['url']}\n")
        # return "\n".join(output)
        return results
        
    except Exception as e:
        return f"Tavily 검색 중 오류 발생: {str(e)}"

if __name__ == "__main__":
    print("===*** Tavily 실시간 검색 테스트 ***===")
    print(search_web("한국 AI 관련 최신 뉴스는?"))
    # mcp.run()
