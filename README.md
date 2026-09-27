# Shiv private podcast feeds

Apple Podcasts–compatible RSS feeds with unguessable URL paths.

| Feed | Purpose |
| --- | --- |
| **Listen** | Taste profile — episodes only from Shiv’s follow list |
| **Discover** | Stimulating new episodes from follows + brand-new shows |
| **Side Quest** | Entertainment — true crime, Why Files–style conspiracy, comedy (Brilliant Idiots, Flagrant, Rogan when the guest is good). Not the intellectual Listen/Discover lane |
| **Desi** | Indian creators (Hindi / English) |
| **Arena** | News / social commentary across the spectrum (Breaking Points, Ezra Klein, Bill Maher, Daily Show, Tucker-as-performance). Cap curation to 1–2 eps per drop — not a doomscroll |
| **Venture** | Entrepreneurship + venture capital — Founders/David Senra, 20VC, operator-investor craft, company-building deep cuts. Wild finds welcome; private Legion shelf |
| **Brief** (`brief`) | Sameer — The Brief: daily Morning Brew–style audio Brief (TTS). Separate from Listen/Discover/Arena |

Cadence (ops): Listen/Discover ~1 new item / 4h; Side Quest / Desi / Arena / Venture curated less often (Arena especially capped).

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
- Venture: `https://mohmaya.github.io/shiv-podcast-feeds/feeds/<VENTURE_TOKEN>/rss.xml`
- Brief: `https://mohmaya.github.io/shiv-podcast-feeds/feeds/<BRIEF_TOKEN>/rss.xml`

Exact tokens are in `feed_map.json` (obscurity = security; do not publish in Slack). Prefer the `urls` command over embedding secret URLs in docs or chat.

Repo: https://github.com/MohMaya/shiv-podcast-feeds

## Append an episode (agents)

```bash
cd /workspace/shiv-podcast-feeds
PYTHONPATH=. python3 -m shiv_podcast_feeds append \
  --feed listen|discover|sidequest|desi|arena|venture|brief \
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

## Brief media hosting (Sameer)

Stable HTTPS for MP3 enclosures: commit files under `assets/brief/` and use the Pages URL.

```bash
# after TTS writes /tmp/brief-2026-09-27.mp3
DATE=2026-09-27
cp /tmp/brief-$DATE.mp3 assets/brief/$DATE.mp3
BYTES=$(stat -c%s assets/brief/$DATE.mp3)
ENCLOSURE="https://mohmaya.github.io/shiv-podcast-feeds/assets/brief/$DATE.mp3"

PYTHONPATH=. python3 -m shiv_podcast_feeds append \
  --feed brief \
  --title "The Brief — $DATE" \
  --show "Sameer — The Brief" \
  --enclosure-url "$ENCLOSURE" \
  --guid "brief-$DATE" \
  --duration 480 \
  --length-bytes "$BYTES" \
  --description "Morning Brief for $DATE"

git add assets/brief feeds feed_map.json
git commit -m "brief: $DATE"
git push
```

Prefer Pages `assets/brief/` over R2 until volume needs CDN. Do not paste the subscribe token into Slack; give Shiv the URL out of band / in-app.

## Rules

- Dedupe by `guid` (re-append is a no-op)
- **Permanent library** — feeds keep every curated item forever (no rolling window). Dedupe by `guid` only.
- **Never Lex Fridman** — append rejects matching title/show/description
- No directory listing of `/feeds/` root on Pages (only token paths)

## Railway note

HTTP append API was planned on Railway; Shiv’s Railway trial is expired. CLI + GitHub Pages is the live path until a paid host is available.
