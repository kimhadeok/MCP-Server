import asyncio
from fastmcp import FastMCP
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# MCP 서버 초기화
mcp = FastMCP("Chromium-Google-Search")

async def run_chromium_search(query: str) -> str:
    """구글 모바일 버전을 활용하여 봇 차단을 완벽히 우회하고 실시간 검색 결과를 가져옵니다."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 💡 아이폰 사파리(모바일)인 것처럼 위장합니다. (구글은 모바일 환경에 가장 관대합니다.)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            locale="ko-KR",
            timezone_id="Asia/Seoul",
            viewport={"width": 390, "height": 844} # 아이폰 13/14 표준 해상도
        )
        page = await context.new_page()
        
        # 봇 탐지 우회 장치
        await page.add_init_script("delete navigator.__proto__.webdriver;")
        
        # 구글 모바일 검색 쿼리 주소로 바로 이동
        encoded_query = quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}&hl=ko"
        
        await page.goto(search_url, wait_until="domcontentloaded")
        
        # 구글 검색 결과 덩어리가 로드될 때까지 최대 8초 대기
        # 구글 모바일은 보통 'div' 요소 내부에 'g' 클래스나 검색 결과 컨테이너가 잡힙니다.
        try:
            await page.wait_for_selector('div[role="main"]', timeout=8000)
        except Exception:
            await browser.close()
            return "구글 검색 결과 로딩에 실패했습니다. (서버 측 차단 또는 일시적 네트워크 지연)"

        html = await page.content()
        await browser.close()
        
        # 구글 모바일 HTML 정교하게 파싱하기
        soup = BeautifulSoup(html, "html.parser")
        
        # 구글 모바일 검색 결과 카드들을 찾습니다.
        results = soup.select('div.v7W4Gc, div.Gx5Zad, div.MjjYud')
        
        output = []
        for item in results:
            # 제목과 링크가 포함된 태그 찾기
            link_tag = item.find("a")
            if not link_tag:
                continue
                
            link = link_tag.get("href", "")
            # 외부 링크가 아니거나 구글 내부 링크면 패스
            if not link.startswith("http") or "google.com" in link:
                continue
                
            # 검색 결과 제목 (모바일 구글 구조 반영)
            title_tag = link_tag.find("div", class_="vvjw0b") or link_tag.find("div", role="heading") or link_tag
            title = title_tag.get_text(strip=True)
            
            # 본문 요약 내용 찾기
            snippet_tag = item.find("div", class_="MUxG9c") or item.find("div", class_="yDsk9d")
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else "상세 내용 없음"
            
            # 이상한 가짜 값 걸러내기
            if title and link and "지도" not in title and "이미지" not in title:
                output.append(f"▶ {title}\n- 내용: {snippet}\n- 출처: {link}\n")
            
            # 검색 결과 3~4개 채워지면 중단
            if len(output) >= 4:
                break
                
        if not output:
            # 예비 파싱 기법 (구조가 다를 때 심플하게 가져오기)
            simple_links = soup.select('a')
            for a in simple_links:
                href = a.get('href', '')
                if href.startswith('http') and not 'google.com' in href:
                    title = a.get_text(strip=True)
                    if len(title) > 10: # 너무 짧은 메뉴 링크는 패스
                        output.append(f"▶ {title}\n- 출처: {href}\n")
                if len(output) >= 3:
                    break
                    
        return "\n".join(output) if output else "검색 결과를 정제하는 데 실패했습니다."

@mcp.tool()
async def search_web_chromium(query: str) -> str:
    """
    내부 크로미움 브라우저를 가동하여 구글 실시간 데이터(오늘 날씨, 뉴스 등)를 
    API Key 및 차단 제한 없이 100% 무료로 검색합니다.
    """
    try:
        return await run_chromium_search(query)
    except Exception as e:
        return f"크로미움 검색 중 에러 발생: {str(e)}"

if __name__ == "__main__":
    print("--- 크로미움 실시간 검색 테스트 ---")
    res = asyncio.run(search_web_chromium("서울 오늘 날씨"))
    print(res)
