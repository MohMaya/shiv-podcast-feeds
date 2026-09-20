from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shiv_podcast_feeds.rss import is_lex_blocked, render_rss

ROOT = Path(__file__).resolve().parents[1]
FEED_MAP = json.loads((ROOT / "feed_map.json").read_text())


def feed_dir(feed_key: str) -> Path:
    token = FEED_MAP[feed_key]["token"]
    return ROOT / "feeds" / token


def load_store(feed_key: str) -> dict[str, Any]:
    path = feed_dir(feed_key) / "store.json"
    return json.loads(path.read_text())


def save_store(feed_key: str, store: dict[str, Any], public_base: str) -> Path:
    d = feed_dir(feed_key)
    d.mkdir(parents=True, exist_ok=True)
    max_items = int(store.get("max_items") or 80)
    items = store.get("items") or []
    # newest first
    items = sorted(items, key=lambda x: x.get("pub_date") or "", reverse=True)[:max_items]
    store["items"] = items
    (d / "store.json").write_text(json.dumps(store, indent=2) + "\n")
    token = FEED_MAP[feed_key]["token"]
    feed_url = f"{public_base.rstrip('/')}/feeds/{token}/rss.xml"
    rss = render_rss(store, feed_url=feed_url)
    out = d / "rss.xml"
    out.write_text(rss)
    return out


def append_item(
    feed_key: str,
    *,
    title: str,
    show: str,
    enclosure_url: str,
    guid: str,
    pub_date: str | None = None,
    duration: str | int | None = None,
    link: str | None = None,
    description: str | None = None,
    mime_type: str = "audio/mpeg",
    length_bytes: int = 0,
    image_url: str | None = None,
    public_base: str,
) -> dict[str, Any]:
    if feed_key not in FEED_MAP:
        raise KeyError(f"unknown feed_key={feed_key}; use listen|discover")
    if is_lex_blocked(title=title, show=show, description=description or ""):
        raise ValueError("blocked: Lex Fridman (taste rule)")
    if not enclosure_url.startswith("http"):
        raise ValueError("enclosure_url must be http(s) to playable audio")
    store = load_store(feed_key)
    items = store.setdefault("items", [])
    if any(i.get("guid") == guid for i in items):
        return {"status": "duplicate", "guid": guid, "feed": feed_key}
    item = {
        "title": title,
        "show": show,
        "enclosure_url": enclosure_url,
        "guid": guid,
        "pub_date": pub_date or datetime.now(timezone.utc).isoformat(),
        "duration": duration,
        "link": link,
        "description": description,
        "mime_type": mime_type,
        "length_bytes": length_bytes,
        "image_url": image_url,
    }
    items.insert(0, item)
    path = save_store(feed_key, store, public_base=public_base)
    return {"status": "added", "guid": guid, "feed": feed_key, "rss": str(path), "n_items": len(store["items"])}


def rebuild_all(public_base: str) -> list[str]:
    outs = []
    for key in FEED_MAP:
        outs.append(str(save_store(key, load_store(key), public_base=public_base)))
    return outs


def feed_urls(public_base: str) -> dict[str, str]:
    base = public_base.rstrip("/")
    return {
        key: f"{base}/feeds/{meta['token']}/rss.xml"
        for key, meta in FEED_MAP.items()
    }
