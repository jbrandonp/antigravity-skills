#!/usr/bin/env python3
"""
MCP Server — free web tools (DDGS search + requests-based extraction).
No API key. No Docker. No Firecrawl.

Provides tools:
  - web_search(query, limit=5) → [{url, title, description}]
  - web_extract(urls: list[str], char_limit=10000) → [{url, title, content}]

Usage:
  python ~/.hermes/mcp-servers/web_tools/mcp_web_tools.py

Then add to Hermes config.yaml mcp_servers:
  web-tools:
    command: python
    args: ["C:\\Users\\brand\\.hermes\\mcp-servers\\web_tools\\mcp_web_tools.py"]
"""
import json, sys, os, io, re, time

def log(msg):
    print(json.dumps({"type": "log", "msg": msg}), file=sys.stderr, flush=True)

def safe_request(url, timeout=10):
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; HermesAgent/1.0; +https://github.com/nousresearch/hermes-agent)"
    }
    return requests.get(url, headers=headers, timeout=timeout)

def web_search(query, limit=5):
    """Search DDGS and return structured results."""
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=limit):
                results.append({
                    "url": r.get("href", r.get("link", "")),
                    "title": r.get("title", ""),
                    "description": r.get("body", r.get("snippet", ""))
                })
        return {"data": {"web": results}}
    except Exception as e:
        # Fallback: try requests to DuckDuckGo HTML
        log(f"DDGS failed: {e}, falling back to HTML parse")
        try:
            resp = safe_request(f"https://html.duckduckgo.com/html/?q={query}")
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")
            results = []
            for r in soup.select(".result")[:limit]:
                title_el = r.select_one(".result__title")
                link_el = r.select_one(".result__url")
                desc_el = r.select_one(".result__snippet")
                results.append({
                    "url": link_el.text.strip() if link_el else "",
                    "title": title_el.text.strip() if title_el else "",
                    "description": desc_el.text.strip() if desc_el else "",
                })
            return {"data": {"web": results}}
        except Exception as e2:
            log(f"DDGS HTML fallback also failed: {e2}")
            return {"data": {"web": [], "error": str(e2)}}

def web_extract(urls, char_limit=15000):
    """Extract clean text from one or more URLs."""
    results = []
    for url in urls:
        try:
            resp = safe_request(url, timeout=15)
            ct = resp.headers.get("content-type", "")

            if "application/pdf" in ct or url.endswith(".pdf"):
                content = f"[PDF document — {len(resp.content)} bytes]"
            elif "text/html" in ct:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                text = soup.get_text(separator="\n")
                lines = [l.strip() for l in text.splitlines() if l.strip()]
                content = "\n".join(lines)
                if len(content) > char_limit:
                    content = content[:char_limit] + f"\n\n[... truncated at {char_limit} chars, {len(content)} total]"
            else:
                content = resp.text[:char_limit] if len(resp.text) > char_limit else resp.text

            results.append({"url": url, "title": "", "content": content})
        except Exception as e:
            results.append({"url": url, "title": "", "content": "", "error": str(e)})
    return {"results": results}


# ═══════════════════════════════════════════════════════════════════
# MCP JSON-RPC loop
# ═══════════════════════════════════════════════════════════════════
TOOLS = {
    "web_search": {
        "name": "web_search",
        "description": "Search the web using DuckDuckGo. Returns title, URL, description. No API key needed.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results (default 5)", "default": 5},
            },
            "required": ["query"]
        }
    },
    "web_extract": {
        "name": "web_extract",
        "description": "Extract clean text content from web pages. No API key needed.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "urls": {"type": "array", "items": {"type": "string"}, "description": "List of URLs to extract"},
                "char_limit": {"type": "integer", "description": "Max characters per page (default 15000)", "default": 15000},
            },
            "required": ["urls"]
        }
    },
}

def main():
    log("MCP web_tools server started (DDGS + requests)")

    for line in sys.stdin:
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        mid = msg.get("id")
        method = msg.get("method")

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0", "id": mid,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "web_tools", "version": "1.0.0"}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/list":
            tools = list(TOOLS.values())
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            name = msg["params"]["name"]
            args = msg["params"].get("arguments", {})
            if name == "web_search":
                result = web_search(args.get("query", ""), args.get("limit", 5))
            elif name == "web_extract":
                result = web_extract(args.get("urls", []), args.get("char_limit", 15000))
            else:
                result = {"error": f"Unknown tool: {name}"}

            sys.stdout.write(json.dumps({
                "jsonrpc": "2.0", "id": mid,
                "result": {"content": [{"type": "text", "text": json.dumps(result)}]}
            }) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            pass

        else:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Unknown method: {method}"}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
