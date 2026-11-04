#!/usr/bin/env python3
"""Mirror the Otello Webflow pages and their assets into a self-contained folder."""
import hashlib
import os
import re
import sys
import urllib.parse
import urllib.request

BASE = "https://otello-hotel-travel-template.webflow.io"
OUT = os.path.expanduser("~/otello/site")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

PAGES = {
    "/": "index.html",
    "/the-hotel": "the-hotel.html",
    "/rooms": "rooms.html",
    "/stay-with-us": "stay-with-us.html",
}

HOSTS = {
    "cdn.prod.website-files.com",
    "uploads-ssl.webflow.com",
    "assets.website-files.com",
    "files.website-files.com",
    "d3e54v103j8qbb.cloudfront.net",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "ajax.googleapis.com",
    "code.jquery.com",
}

cache = {}


def fetch(url):
    if url in cache:
        return cache[url]
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    cache[url] = data
    return data


def local_path(url):
    p = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(p.path).lstrip("/")
    if not path or path.endswith("/"):
        path += "index.html"
    if p.query:
        stem, ext = os.path.splitext(path)
        path = f"{stem}-{hashlib.md5(p.query.encode()).hexdigest()[:8]}{ext}"
    return os.path.join(OUT, "assets", p.netloc, path)


def save(url, data):
    dest = local_path(url)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    rel = os.path.relpath(dest, OUT)
    return rel.replace(os.sep, "/")


def is_asset(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https"):
        return False
    if p.netloc not in HOSTS:
        return False
    ext = os.path.splitext(p.path)[1].lower()
    return ext in {
        ".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif",
        ".ico", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".webm",
    }


def rewrite_css(css_text, css_url, done):
    def repl(m):
        ref = m.group(1).strip("'\" ")
        if ref.startswith("data:") or ref.startswith("#"):
            return m.group(0)
        absu = urllib.parse.urljoin(css_url, ref)
        if not is_asset(absu):
            return m.group(0)
        rel = download(absu, done)
        return f"url({rel})" if rel else m.group(0)

    return re.sub(r"url\(([^)]+)\)", repl, css_text)


def download(url, done):
    if url in done:
        return done[url]
    dest = local_path(url)
    if os.path.exists(dest):
        rel = os.path.relpath(dest, OUT).replace(os.sep, "/")
        done[url] = rel
        return rel
    try:
        data = fetch(url)
    except Exception as e:  # noqa: BLE001
        print(f"  ! falhou {url}: {e}", file=sys.stderr)
        done[url] = None
        return None
    if url.lower().split("?")[0].endswith(".css"):
        text = data.decode("utf-8", "replace")
        text = rewrite_css(text, url, done)
        data = text.encode("utf-8")
    rel = save(url, data)
    done[url] = rel
    print(f"  + {rel}")
    return rel


URL_RE = re.compile(r"https://[^\s\"'<>]+")


def main():
    done = {}
    os.makedirs(OUT, exist_ok=True)
    for route, filename in PAGES.items():
        url = BASE + ("/" if route == "/" else route)
        html = fetch(url).decode("utf-8", "replace")
        for asset in sorted(set(URL_RE.findall(html))):
            asset = asset.rstrip("\\,")
            if is_asset(asset):
                download(asset, done)
        for orig, rel in done.items():
            if rel:
                html = html.replace(orig, rel)
        out = os.path.join(OUT, filename)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"pagina {filename}: {len(html)} bytes")

    left = set()
    for filename in PAGES.values():
        with open(os.path.join(OUT, filename), encoding="utf-8") as f:
            for u in URL_RE.findall(f.read()):
                if u not in BASE and not u.startswith("https://fonts.googleapis.com/css"):
                    left.add(u.split("?")[0])
    print(f"URLs externas restantes: {len(left)}")
    for u in sorted(left)[:20]:
        print("  ?", u)


if __name__ == "__main__":
    main()
