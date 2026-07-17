# https://gomcpserver.fastmcp.app/mcp

# web_search_mcp.py
from fastmcp import FastMCP
from duckduckgo_search import DDGS

# MCP 서버 초기화 (이름 지정)
mcp = FastMCP("Web Search MCP")

@mcp.tool()
def search_web(query: str, max_results: int = 5) -> str:
    """
    DuckDuckGo를 사용하여 실시간 웹 검색을 수행하고 결과를 반환합니다.
    
    Args:
        query (str): 검색할 쿼리 문장이나 단어
        max_results (int): 가져올 최대 결과 개수 (기본값: 5)
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return "검색 결과가 없습니다."
            
            formatted_results = []
            for idx, r in enumerate(results, 1):
                formatted_results.append(
                    f"[{idx}] {r.get('title')}\n"
                    f"URL: {r.get('href')}\n"
                    f"요약: {r.get('body')}\n"
                )
            return "\n---\n".join(formatted_results)
            
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}"

if __name__ == "__main__":
    # fastmcp 실행
    mcp.run(transport="http", host="0.0.0.0", port=8000)


# cd D:\My-Dev\AI\MCP
# .\.venv\Scripts\ollmcp.exe mcp add web-search --transport stdio .\.venv\Scripts\python.exe web_search_mcp.py

# .\.venv\Scripts\ollmcp.exe --model qwen2.5-coder:3b --mcp-server web_search_mcp.py

# .\.venv\Scripts\ollmcp.exe mcp remove web-search --scope local

# 등록된 MCP 설정을 제거하고, 현재 사용 중인 도구 설정이 남아 있지 않은지 바로 정리하겠습니다.

# C:\Users\khd.config\ollmcp\mcp.local.json
# {
#   "projects": {
#     "D:\\My-Dev\\AI\\MCP": {
#       "mcpServers": {}
#     }
#   }
# }
