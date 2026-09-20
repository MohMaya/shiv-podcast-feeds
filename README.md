# Shiv private podcast feeds (Listen + Discover)

Two Apple Podcasts–compatible RSS feeds with unguessable URL paths.

| Feed | Purpose |
| --- | --- |
| **Listen** | Taste profile — episodes only from Shiv’s follow list |
| **Discover** | Stimulating new episodes from follows + brand-new shows |

Cadence (ops): each feed gets ~1 new item / 4h (Karan / curation agents append).

## Follow in Apple Podcasts

1. Open Apple Podcasts → Library → … → Follow a Show by URL  
2. Paste the feed URL (get current URLs with the command below)

```bash
cd /workspace/shiv-podcast-feeds
PYTHONPATH=. python3 -m shiv_podcast_feeds urls
```

Live URLs (GitHub Pages):

- Listen: `https://mohmaya.github.io/shiv-podcast-feeds/feeds/<LISTEN_TOKEN>/rss.xml`
- Discover: `https://mohmaya.github.io/shiv-podcast-feeds/feeds/<DISCOVER_TOKEN>/rss.xml`

Exact tokens are in `feed_map.json` (obscurity = security; do not publish in Slack).

## Append an episode (agents)

```bash
cd /workspace/shiv-podcast-feeds
PYTHONPATH=. python3 -m shiv_podcast_feeds append \
  --feed listen|discover \
  --title "Episode title" \
  --show "Podcast Name" \
  --enclosure-url "https://.../episode.mp3" \
  --guid "stable-unique-id" \
  --duration 3600 \
  --description "optional" \
  --link "https://optional-episode-page"

# or JSON file drop:
PYTHONPATH=. python3 -m shiv_podcast_feeds append-json /path/to/ep.json
```

`enclosure_url` must be the **playable audio URL from the source podcast’s RSS enclosure**, not an Apple episode web page.

Then commit + push so Pages updates:

```bash
git add feeds feed_map.json
git commit -m "podcast: append episode"
git push
```

## Rules

- Dedupe by `guid` (re-append is a no-op)
- Keep last **80** items per feed
- **Never Lex Fridman** — append rejects matching title/show/description
- No directory listing of `/feeds/` root on Pages (only token paths)

## Railway note

HTTP append API was planned on Railway; Shiv’s Railway trial is expired. CLI + GitHub Pages is the live path until a paid host is available.
