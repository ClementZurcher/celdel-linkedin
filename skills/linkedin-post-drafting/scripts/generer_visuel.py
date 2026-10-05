#!/usr/bin/env python3
"""Generate a LinkedIn post visual for free via Pollinations.ai.

Usage:
    python3 generer_visuel.py "english prompt" out.png [width] [height]

- No key or account needed. Some endpoint/model combinations answer 402 (throttling,
  anonymous tier is ~1 request/15 s); this script tries several variants and you can
  simply re-run it after a pause.
- If POLLINATIONS_API_KEY is set (free key from https://enter.pollinations.ai) it is
  sent and normally removes the watermark and raises the quota.
- The result is re-encoded to the exact requested size (1200x627 = LinkedIn landscape).
"""
import os, sys, io, urllib.parse, urllib.request

HOST = "https://image.pollinations.ai/prompt/"


def variants(prompt, W, H):
    base = urllib.parse.quote(prompt)
    q = lambda extra: urllib.parse.urlencode({"width": W, "height": H, **extra})
    return [
        f"{HOST}{base}?{q({'model': 'flux', 'nologo': 'true'})}",
        f"{HOST}{base}?{q({'model': 'turbo', 'nologo': 'true'})}",
        f"{HOST}{base}?{q({'model': 'turbo'})}",
        f"{HOST}{base}?{q({})}",
    ]


def is_image(b):
    return b[:2] == b"\xff\xd8" or b[:8] == b"\x89PNG\r\n\x1a\n"


def fetch(url, key):
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-celdel/1.0"})
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.headers.get("Content-Type", "")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    prompt, out = sys.argv[1], sys.argv[2]
    W = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    H = int(sys.argv[4]) if len(sys.argv) > 4 else 627
    key = os.environ.get("POLLINATIONS_API_KEY", "").strip()

    data = ctype = None
    for url in variants(prompt, W, H):
        try:
            data, ctype = fetch(url, key)
        except Exception as e:
            print("  variant KO:", getattr(e, "code", type(e).__name__), url.split("?")[-1])
            continue
        if is_image(data):
            print("  variant OK:", url.split("?")[-1])
            break
        data = None
    if not data:
        print("FAILED: no variant returned an image (402 = throttled; wait ~60s and retry).")
        sys.exit(1)

    try:
        from PIL import Image
        im = Image.open(io.BytesIO(data)).convert("RGB")
        sw, sh = im.size
        s = max(W / sw, H / sh)
        im = im.resize((max(1, int(sw * s)), max(1, int(sh * s))))
        nw, nh = im.size
        im.crop(((nw - W) // 2, (nh - H) // 2, (nw - W) // 2 + W, (nh - H) // 2 + H)).save(out, "PNG")
    except Exception as e:
        print("Pillow warning:", e)
        open(out, "wb").write(data)

    print(f"OK -> {out} | source {ctype} | {W}x{H} | key: {'yes (watermark removed)' if key else 'no (anonymous)'}")


if __name__ == "__main__":
    main()
