from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from shiv_podcast_feeds.store import FEED_MAP, append_item, feed_urls, rebuild_all


def _public_base(args: argparse.Namespace) -> str:
    return (
        args.public_base
        or os.environ.get("PODCAST_FEEDS_PUBLIC_BASE")
        or "https://mohmaya.github.io/shiv-podcast-feeds"
    )


def cmd_urls(args: argparse.Namespace) -> int:
    print(json.dumps(feed_urls(_public_base(args)), indent=2))
    return 0


def cmd_rebuild(args: argparse.Namespace) -> int:
    outs = rebuild_all(_public_base(args))
    print(json.dumps({"rebuilt": outs, "urls": feed_urls(_public_base(args))}, indent=2))
    return 0


def cmd_append(args: argparse.Namespace) -> int:
    try:
        result = append_item(
            args.feed,
            title=args.title,
            show=args.show,
            enclosure_url=args.enclosure_url,
            guid=args.guid,
            pub_date=args.pub_date,
            duration=args.duration,
            link=args.link,
            description=args.description,
            mime_type=args.mime_type,
            length_bytes=args.length_bytes,
            image_url=args.image_url,
            public_base=_public_base(args),
        )
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def cmd_append_json(args: argparse.Namespace) -> int:
    payload = json.loads(Path(args.file).read_text())
    try:
        result = append_item(
            payload["feed"],
            title=payload["title"],
            show=payload.get("show") or "",
            enclosure_url=payload["enclosure_url"],
            guid=payload["guid"],
            pub_date=payload.get("pub_date"),
            duration=payload.get("duration"),
            link=payload.get("link"),
            description=payload.get("description"),
            mime_type=payload.get("mime_type") or "audio/mpeg",
            length_bytes=int(payload.get("length_bytes") or 0),
            image_url=payload.get("image_url"),
            public_base=_public_base(args),
        )
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="shiv-podcast-feeds")
    p.add_argument("--public-base", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("urls")
    u.set_defaults(func=cmd_urls)

    r = sub.add_parser("rebuild")
    r.set_defaults(func=cmd_rebuild)

    a = sub.add_parser("append")
    a.add_argument("--feed", required=True, choices=list(FEED_MAP))
    a.add_argument("--title", required=True)
    a.add_argument("--show", required=True)
    a.add_argument("--enclosure-url", required=True)
    a.add_argument("--guid", required=True)
    a.add_argument("--pub-date", default=None)
    a.add_argument("--duration", default=None)
    a.add_argument("--link", default=None)
    a.add_argument("--description", default=None)
    a.add_argument("--mime-type", default="audio/mpeg")
    a.add_argument("--length-bytes", type=int, default=0)
    a.add_argument("--image-url", default=None)
    a.set_defaults(func=cmd_append)

    j = sub.add_parser("append-json")
    j.add_argument("file")
    j.set_defaults(func=cmd_append_json)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
