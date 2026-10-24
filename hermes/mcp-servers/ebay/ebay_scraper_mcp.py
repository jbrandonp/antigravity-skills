#!/usr/bin/env python3
"""
eBay Scraper MCP — Pure HTML scraping, zero credentials needed.
Uses requests + BeautifulSoup to scrape eBay search results.
Compatible with Hermes MCP protocol via stdin/stdout.
"""
import sys, json, re, asyncio
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "-q"])
    import requests
    from bs4 import BeautifulSoup

# MCP Protocol
class MCPServer:
    def __init__(self):
        self.tools = {
            "ebay_search": {
                "description": "Search eBay listings (all formats: auction + Buy It Now). Returns title, price, condition, shipping, bids, URL. No API key needed.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search keywords"},
                        "country": {"type": "string", "description": "eBay country code: com,fr,de,co.uk,it,es,nl,be,ca,com.au", "default": "fr"},
                        "limit": {"type": "integer", "description": "Max results (5-20)", "default": 10},
                        "condition": {"type": "string", "description": "new, used, or empty for all", "default": ""},
                        "sold": {"type": "boolean", "description": "Search sold listings for price reference", "default": False}
                    },
                    "required": ["query"]
                }
            }
        }
    
    def handle_tools_list(self):
        return {"tools": [
            {"name": name, "description": info["description"], "inputSchema": info["inputSchema"]}
            for name, info in self.tools.items()
        ]}
    
    def ebay_search(self, query, country="fr", limit=10, condition="", sold=False):
        limit = min(max(limit, 1), 20)
        
        # Country → domain + locale
        domains = {
            "fr": ("www.ebay.fr", "fr-FR", "EUR"),
            "de": ("www.ebay.de", "de-DE", "EUR"),
            "com": ("www.ebay.com", "en-US", "USD"),
            "co.uk": ("www.ebay.co.uk", "en-GB", "GBP"),
            "it": ("www.ebay.it", "it-IT", "EUR"),
            "es": ("www.ebay.es", "es-ES", "EUR"),
            "nl": ("www.ebay.nl", "nl-NL", "EUR"),
            "be": ("www.befr.ebay.be", "fr-BE", "EUR"),
            "ca": ("www.ebay.ca", "en-CA", "CAD"),
            "com.au": ("www.ebay.com.au", "en-AU", "AUD"),
        }
        domain, locale, currency = domains.get(country, domains["fr"])
        
        url = f"https://{domain}/sch/i.html"
        params = {
            "_nkw": query,
            "LH_PrefLoc": "1",  # Prefer local listings
        }
        if condition == "new":
            params["LH_ItemCondition"] = "3"
        elif condition == "used":
            params["LH_ItemCondition"] = "4"
        if sold:
            params["LH_Sold"] = "1"
            params["LH_Complete"] = "1"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": locale + ",en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Dnt": "1",
        }
        
        session = requests.Session()
        # First visit homepage to get cookies
        try:
            session.get(f"https://{domain}/", headers=headers, timeout=10)
        except:
            pass
        
        try:
            resp = session.get(url, params=params, headers=headers, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            return json.dumps({"error": f"eBay request failed: {e}", "url": url})
        
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        
        # eBay uses <li class="s-card s-card--vertical"> for each listing
        listings = soup.select(".srp-results li.s-card")[:limit]
        
        for item in listings:
            try:
                # Title
                title_el = item.select_one(".s-card__title span.su-styled-text") or item.select_one(".s-card__title")
                title = title_el.text.strip() if title_el else ""
                
                # Price
                price_el = item.select_one(".s-card__price") or item.select_one("[class*=price]")
                price_text = price_el.text.strip() if price_el else ""
                price_num = None
                if price_text:
                    nums = re.findall(r'[\d\s,]+[.,]\d{2}', price_text.replace('\xa0',' '))
                    if nums:
                        try: price_num = float(nums[0].replace(' ','').replace(',','.'))
                        except: pass
                
                # URL
                link_el = item.select_one("a.s-card__link")
                ebay_url = link_el.get("href", "") if link_el else ""
                
                # Condition + seller type
                subtitle_el = item.select_one(".s-card__subtitle")
                subtitle = subtitle_el.text.strip() if subtitle_el else ""
                
                # Buy format (Achat immédiat / Enchère)
                format_el = item.select_one(".s-card__attribute-row span")
                buy_format = format_el.text.strip() if format_el else ""
                
                # Shipping
                ship_els = item.select(".s-card__attribute-row span")
                shipping_text = ""
                ship_num = None
                for el in ship_els:
                    txt = el.text.strip()
                    if "livraison" in txt.lower() or "expédition" in txt.lower() or "shipping" in txt.lower():
                        shipping_text = txt
                        nums = re.findall(r'[\d\s,]+[.,]\d{2}', txt.replace('\xa0',' '))
                        if nums:
                            try: ship_num = float(nums[0].replace(' ','').replace(',','.'))
                            except: pass
                
                # Bids (for auction items)
                bids_el = item.select_one("[class*=bid]")
                bids = None
                if bids_el:
                    bid_match = re.search(r'(\d+)', bids_el.text)
                    if bid_match: bids = int(bid_match.group(1))
                
                items.append({
                    "title": title,
                    "price_text": price_text,
                    "price_num": price_num,
                    "currency": currency,
                    "condition_subtitle": subtitle,
                    "buy_format": buy_format,
                    "shipping_text": shipping_text,
                    "shipping_num": ship_num,
                    "bids": bids,
                    "url": ebay_url,
                    "country": country,
                    "scraped_at": datetime.now().isoformat()
                })
            except Exception as e:
                continue
        
        return json.dumps({
            "query": query,
            "country": country,
            "domain": domain,
            "currency": currency,
            "total_found": len(items),
            "items": items
        }, ensure_ascii=False, indent=2)


server = MCPServer()

async def main():
    import mcp.server.stdio
    import mcp.types as types
    from mcp.server.lowlevel import Server

    async def list_tools(ctx, params) -> types.ListToolsResult:
        return types.ListToolsResult(tools=[
            types.Tool(
                name="ebay_search",
                description="Search eBay listings via HTML scraping. Returns title, price, condition, shipping, bids, URL. No API key required. Supports all eBay countries (fr,de,com,co.uk,it,es,nl,be,ca,com.au).",
                inputSchema=server.tools["ebay_search"]["inputSchema"]
            )
        ])

    async def call_tool(ctx, params) -> types.CallToolResult:
        if params.name == "ebay_search":
            result = server.ebay_search(
                query=params.arguments.get("query", ""),
                country=params.arguments.get("country", "fr"),
                limit=params.arguments.get("limit", 10),
                condition=params.arguments.get("condition", ""),
                sold=params.arguments.get("sold", False)
            )
            return types.CallToolResult(content=[types.TextContent(type="text", text=result)])
        raise ValueError(f"Unknown tool: {params.name}")

    srv = Server("ebay-scraper", version="1.0.0", on_list_tools=list_tools, on_call_tool=call_tool)

    async with mcp.server.stdio.stdio_server() as (read, write):
        await srv.run(read, write, srv.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
