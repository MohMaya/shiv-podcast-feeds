from __future__ import annotations

import html
from datetime import datetime, timezone
from email.utils import format_datetime
from typing import Any
from xml.sax.saxutils import escape


def _rfc2822(dt: datetime | str) -> str:
    if isinstance(dt, str):
        # accept ISO
        try:
            parsed = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except ValueError:
            return dt
        dt = parsed
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def _esc(text: str | None) -> str:
    return escape(text or "", {"'": "&apos;", '"': "&quot;"})


def render_rss(store: dict[str, Any], feed_url: str) -> str:
    """Render podcast RSS 2.0 + iTunes tags from a store dict."""
    items = store.get("items") or []
    channel_parts = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
        "<channel>",
        f"<title>{_esc(store.get('title'))}</title>",
        f"<description>{_esc(store.get('description'))}</description>",
        f"<language>{_esc(store.get('language') or 'en-us')}</language>",
        f"<link>{_esc(feed_url)}</link>",
        f"<itunes:author>{_esc(store.get('author') or 'Shiv')}</itunes:author>",
        f"<itunes:summary>{_esc(store.get('description'))}</itunes:summary>",
        f"<itunes:explicit>{_esc(store.get('explicit') or 'false')}</itunes:explicit>",
        f"<itunes:category text=\"{_esc(store.get('category') or 'Technology')}\"/>",
        f"<itunes:type>episodic</itunes:type>",
        f"<generator>shiv-podcast-feeds/0.1</generator>",
    ]
    image_url = store.get("image_url")
    if image_url:
        channel_parts.append(f'<itunes:image href="{_esc(image_url)}"/>')
        channel_parts.append(
            "<image>"
            f"<url>{_esc(image_url)}</url>"
            f"<title>{_esc(store.get('title'))}</title>"
            f"<link>{_esc(feed_url)}</link>"
            "</image>"
        )
    for it in items:
        enclosure_url = it["enclosure_url"]
        mime = it.get("mime_type") or "audio/mpeg"
        length = int(it.get("length_bytes") or 0)
        duration = it.get("duration")  # seconds or HH:MM:SS
        guid = it["guid"]
        title = it["title"]
        show = it.get("show") or ""
        desc = it.get("description") or (f"{show}: {title}" if show else title)
        link = it.get("link") or enclosure_url
        pub = _rfc2822(it.get("pub_date") or datetime.now(timezone.utc))
        item_xml = [
            "<item>",
            f"<title>{_esc(title)}</title>",
            f"<description>{_esc(desc)}</description>",
            f"<link>{_esc(link)}</link>",
            f'<guid isPermaLink="false">{_esc(guid)}</guid>',
            f"<pubDate>{_esc(pub)}</pubDate>",
            f'<enclosure url="{_esc(enclosure_url)}" length="{length}" type="{_esc(mime)}"/>',
        ]
        if show:
            item_xml.append(f"<itunes:author>{_esc(show)}</itunes:author>")
        if duration is not None:
            item_xml.append(f"<itunes:duration>{_esc(str(duration))}</itunes:duration>")
        if it.get("explicit"):
            item_xml.append(f"<itunes:explicit>{_esc(str(it['explicit']))}</itunes:explicit>")
        if it.get("image_url"):
            item_xml.append(f'<itunes:image href="{_esc(it["image_url"])}"/>')
        item_xml.append("</item>")
        channel_parts.extend(item_xml)
    channel_parts.append("</channel></rss>\n")
    return "\n".join(channel_parts)


LEX_BLOCK = ("lex fridman", "lex friedman")


def is_lex_blocked(title: str = "", show: str = "", description: str = "") -> bool:
    blob = f"{title} {show} {description}".lower()
    return any(b in blob for b in LEX_BLOCK)
