# Shiv private podcast feeds

Apple Podcasts–compatible RSS feeds with unguessable URL paths.

| Feed | Purpose |
| --- | --- |
| **Listen** | Taste profile — episodes only from Shiv’s follow list |
| **Discover** | Stimulating new episodes from follows + brand-new shows |
| **Side Quest** | Entertainment — true crime, Why Files–style conspiracy, comedy (Brilliant Idiots, Flagrant, Rogan when the guest is good). Not the intellectual Listen/Discover lane |
| **Desi** | Indian creators (Hindi / English) |
| **Arena** | News / social commentary across the spectrum (Breaking Points, Ezra Klein, Bill Maher, Daily Show, Tucker-as-performance). Cap curation to 1–2 eps per drop — not a doomscroll |

Cadence (ops): Listen/Discover ~1 new item / 4h; Side Quest / Desi / Arena curated less often (Arena especially capped).

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
- Side Quest: `https://mohmaya.github.io/shiv-podcast-feeds/feeds/<SIDEQUEST_TOKEN>/rss.xml`
- Desi: `https://mohmaya.github.io/shiv-podcast-feeds/feeds/<DESI_TOKEN>/rss.xml`
- Arena: `https://mohmaya.github.io/shiv-podcast-feeds/feeds/<ARENA_TOKEN>/rss.xml`

Exact tokens are in `feed_map.json` (obscurity = security; do not publish in Slack). Prefer the `urls` command over embedding secret URLs in docs or chat.

Repo: https://github.com/MohMaya/shiv-podcast-feeds

## Append an episode (agents)

```bash
cd /workspace/shiv-podcast-feeds
PYTHONPATH=. python3 -m shiv_podcast_feeds append \
  --feed listen|discover|sidequest|desi|arena \
  --title "Episode title" \
  --show "Podcast Name" \
  --enclosure-url "https://.../episode.mp3" \
  --guid "stable-unique-id" \
  --duration 3600 \
  --description "optional" \
  --link "https://optional-episode-page" \
  --image-url "https://.../episode-art.jpg"

# or JSON file drop:
PYTHONPATH=. python3 -m shiv_podcast_feeds append-json /path/to/ep.json
```

Optional artwork: pass `--image-url` (or `image_url` in JSON). Channel cover lives on each feed’s `store.json` as top-level `image_url` (served from `/assets/*-cover.jpg` on Pages).

`enclosure_url` must be the **playable audio URL from the source podcast’s RSS enclosure**, not an Apple episode web page.

Then commit + push so Pages updates:

```bash
git add feeds feed_map.json assets
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
