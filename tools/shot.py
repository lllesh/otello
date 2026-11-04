#!/usr/bin/env python3
"""Capture screenshots through CDP, scrolling first so reveal animations run."""
import base64
import json
import subprocess
import time
import urllib.request

import websocket

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9333


def start():
    proc = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--remote-debugging-port={PORT}", "--user-data-dir=/tmp/cdp-profile",
         "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1)
            break
        except Exception:
            time.sleep(0.25)
    return proc


def tab():
    data = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list"))
    return data[0]["webSocketDebuggerUrl"]


class C:
    def __init__(self, ws):
        self.ws = websocket.create_connection(ws, timeout=60)
        self.i = 0

    def send(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.i:
                return msg

    def eval(self, expr):
        return self.send("Runtime.evaluate", expression=expr, awaitPromise=True)

    def warm(self):
        self.eval("""(async () => {
          const h = document.body.scrollHeight;
          for (let y = 0; y < h; y += 350) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 120));
          }
          window.scrollTo(0, h);
          await new Promise(r => setTimeout(r, 600));
          window.scrollTo(0, 0);
          await new Promise(r => setTimeout(r, 800));
          return h;
        })()""")
        time.sleep(2)

    def shot(self, path, width, height, full=False, scale=1):
        self.send("Emulation.setDeviceMetricsOverride", width=width, height=height,
                  deviceScaleFactor=1, mobile=False)
        m = self.send("Page.getLayoutMetrics")["result"]["cssContentSize"]
        h = min(int(height if not full else m["height"]), 14000)
        self.send("Emulation.setDeviceMetricsOverride", width=width, height=h,
                  deviceScaleFactor=1, mobile=False)
        r = self.send("Page.captureScreenshot", format="png",
                      clip={"x": 0, "y": 0, "width": width, "height": h, "scale": scale},
                      captureBeyondViewport=True)
        if "result" not in r:
            print("erro:", r)
            return
        with open(path, "wb") as f:
            f.write(base64.b64decode(r["result"]["data"]))


def main():
    proc = start()
    try:
        c = C(tab())
        c.send("Page.enable")
        c.send("Runtime.enable")
        jobs = [
            ("http://127.0.0.1:4321/index.html", "/tmp/cdp-index.png", True),
            ("http://127.0.0.1:4321/the-hotel.html", "/tmp/cdp-hotel.png", True),
            ("http://127.0.0.1:4321/rooms.html", "/tmp/cdp-rooms.png", True),
            ("http://127.0.0.1:4321/stay-with-us.html", "/tmp/cdp-stay.png", True),
        ]
        for url, out, full in jobs:
            c.send("Page.navigate", url=url)
            time.sleep(4)
            c.warm()
            c.shot(out, 1440, 1100, full=full, scale=0.6)
            print("ok", out)
    finally:
        proc.terminate()


if __name__ == "__main__":
    main()


def sections(url, prefix, ys, width=1440, height=1100):
    proc = start()
    try:
        c = C(tab())
        c.send("Page.enable")
        c.send("Runtime.enable")
        c.send("Page.navigate", url=url)
        time.sleep(4)
        c.send("Emulation.setDeviceMetricsOverride", width=width, height=height,
               deviceScaleFactor=1, mobile=False)
        h = c.eval("document.body.scrollHeight")["result"]["result"]["value"]
        print("altura", h)
        for y in ys:
            c.eval(f"window.scrollTo(0,{y})")
            time.sleep(1.6)
            r = c.send("Page.captureScreenshot", format="png")
            with open(f"{prefix}-{y}.png", "wb") as f:
                f.write(base64.b64decode(r["result"]["data"]))
            print("ok", y)
    finally:
        proc.terminate()
