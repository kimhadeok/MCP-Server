# https://gomcpserver.fastmcp.app/mcp

# .\.venv\Scripts\python.exe -c "from server import search_web; print(search_web('서울 오늘 날씨', 5))"

# [1] [날씨] 서울 32도, 대구 35도 무더위…충청 이남 장맛비
# URL: https://www.msn.com/ko-kr/weather/기상학/날씨-서울-32도-대구-35도-무더위-충청-이남-장맛비/vi-AA280T7n
# Date: 2026-07-16T04:00:56+00:00
# 요약: 밖에 나오자마자 후텁지근한 공기가 온몸을 감쌉니다.잠시 서 있기만 해도 이마에 땀이 맺히고, 조금만 걸어도 등줄기를 타고 땀이 흐르는데요.폭염이 주춤했던 어제와 달리 서울 등 중북부 지역에서 더위가 다시 기세를 올렸습니다.오늘 서울의 낮 최고기온은 32도.어제보다 무려 6도 높습니다.다만, 하늘이 흐리고 습도도 어제보다 낮아 체감온도는 32도 안팎에 머물겠

# ---
# [2] [오늘 날씨] 서울 낮기온 32도 무더위…충청 이남 오후부터 비
# URL: https://www.msn.com/ko-kr/weather/기상학/오늘-날씨-서울-낮기온-32도-무더위-충청-이남-오후부터-비/ar-AA27ZCtt
# Date: 2026-07-15T21:03:34+00:00
# 요약: 오늘(16일)은 전국 곳곳에 장맛비가 내리는 가운데 대부분 지역에서 무더위가 이어지겠습니다

# ---
# [3] [오늘 날씨] 낮 가장 긴 '하지', 흐린 날씨 계속…서울 최고 29도
# URL: https://www.msn.com/ko-kr/news/national/오늘-날씨-낮-가장-긴-하지-흐린-날씨-계속-서울-최고-29도/ar-AA269qjp
# Date: 2026-06-21T06:20:00+00:00
# 요약: 1년 중 낮이 가장 긴 절기 '하지'(夏至)이자 일요일인 오늘(21일)은 전국 대부분이 구름 많고 흐린 날씨가 이어지겠다. 기상청에 따르면 21일 아침 최저기온은 15~21도, 낮 최고기온은 22~30도로 예상된다. 아침 최저기온은 △서울 19도 △인천 19도 △춘천 17도 △강릉 18도 △대전 18도 △청주 18도 △대구 19도 △전주 18도 △광주 19

# ---
# [4] [오늘날씨] 소나기, 낮 최고 37도 열대야 날씨에 '외출주의'
# URL: https://www.pennmike.com/news/articleView.html?idxno=123526
# Date: 2026-07-12T11:21:00+00:00
# 요약: 12일(일요일)은 낮 최고기온이 37도까지 오르면서 전국에 폭염이 기승을 부리겠다. 남부 지방을 중심으로 비가 내리고, 일부 내륙 및 산지 지역에는 오후 한때 소나기도 예보됐다.기상청에 따르면, 이날 주요도시 낮 최고기온은 △서울·경기 37도 △인천 33도, △대전 35도, △대구 3

# ---
# [5] [날씨] 오늘 서울 체감 34℃, 더위 계속...내일 제주 장마 시작할 듯
# URL: https://www.ytn.co.kr/_ln/0108_202606300001335220
# Date: 2026-06-29T15:01:00+00:00
# 요약: 서울에 다시 폭염주의보가 내려진 가운데, 오늘(30일)도 한여름 같은 더위가 이어지겠습니다. 오늘 서울의 낮 기온은 33도, 체감온도는 34도까지 오르겠고, 수도권과 충청 등 폭염주의보가 내려진 지역을 중심으로도 33도 안팎의 더위가 예상됩니다. 낮 동안 기온이 오르며 대기가 불안정해지면서 오늘도 오후부터 저녁 사이 내륙 대부분 지역에 5∼40mm의 소나기


from fastmcp import FastMCP
from ddgs import DDGS

# MCP 서버 초기화 (이름 지정)
mcp = FastMCP("Web-Search-MCP")

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
            results = list(ddgs.news(query, max_results=max_results))
            if not results:
                return "검색 결과가 없습니다."
            
            formatted_results = []
            for idx, r in enumerate(results, 1):
                formatted_results.append(
                    f"[{idx}] {r.get('title')}\n"
                    f"URL: {r.get('url')}\n"
                    f"Date: {r.get('date')}\n"
                    f"요약: {r.get('body')}\n"
                )
            return "\n---\n".join(formatted_results)

    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}"

if __name__ == "__main__":
    # fastmcp 실행
    #mcp.run(transport="http", host="0.0.0.0", port=8000)
    mcp.run()


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

# import requests
# from fastmcp import FastMCP

# # 1. MCP 서버 초기화
# mcp = FastMCP("SearXNG-Free-Search")

# 전 세계에 열려 있는 안전한 SearXNG 퍼블릭 인스턴스 주소 중 하나입니다.
# 만약 해당 주소가 느려지면 다른 퍼블릭 주소(https://searx.space 에서 확인 가능)로 바꿀 수 있습니다.
# SEARXNG_URL = "https://searx.be/search"
# SEARXNG_URL = "https://search.mdcnet.de/search"
# SEARXNG_URL = "https://searx.work/search"
# SEARXNG_URL = "https://searx.tiekoetter.com/"

# @mcp.tool()
# def search_web_free(query: str) -> str:
#     """
#     구글, 빙, 덕덕고 등을 결합하여 실시간 최신 웹 정보(날씨, 뉴스 등)를 무료로 검색합니다.
#     args:
#         query (str): 검색할 쿼리 문장이나 단어
#     """
#     # SearXNG가 구글/뉴스 인덱스에서 JSON 형태로 결과를 반환하도록 파라미터 구성
#     params = {
#         "q": query,
#         "format": "json",
#         "pageno": 1,
#         "language": "ko-KR"  # 한국어 결과 우선
#     }
    
#     # 봇(Bot) 차단을 우회하기 위해 일반 브라우저처럼 User-Agent 설정
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#     }
    
#     try:
#         response = requests.get(SEARXNG_URL, params=params, headers=headers, timeout=10)
#         response.raise_for_status()
#         data = response.json()
        
#         results = data.get("results", [])
#         if not results:
#             return "검색 결과를 찾지 못했습니다."
            
#         # AI 에이전트가 읽기 좋은 가독성 높은 텍스트 형태로 정제
#         output = []
#         for item in results[:4]:  # 최상위 결과 4개만 추출
#             title = item.get("title", "제목 없음")
#             snippet = item.get("content", "내용 없음")
#             url = item.get("url", "")
            
#             output.append(f"▶ {title}\n- 내용: {snippet}\n- 출처: {url}\n")
            
#         return "\n".join(output)
        
#     except Exception as e:
#         return f"SearXNG 검색 중 오류가 발생했습니다: {str(e)}"

# # if __name__ == "__main__":
# #     mcp.run()
# if __name__ == "__main__":
#     # AI 연결 모드 대신, 직접 함수를 실행해서 테스트하기
#     print("--- 실시간 검색 테스트 ---")
#     print(search_web_free("서울 오늘 날씨"))
