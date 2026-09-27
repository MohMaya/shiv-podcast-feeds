# Podcast RSS description doctrine (Karan routine)

**Locked template for Legion private feeds** (`feeds/*/store.json` → RSS `<description>`):

1. **Brief-style body** — clear, sober, listener-facing. Say what the episode is about in one or two sentences. India/news Brief tone: nouns and verbs, no hot takes.
2. **No densifier jargon** — ban: densifier, Commentary-as-performance, Arena craft, stack/TTS scrap, “sharpens taste,” “craft move,” “operator OS,” “pressure-test” as self-praise.
3. **YouTube line when a mirror exists** — append a blank line then exactly:
   ```
   Watch: https://youtu.be/VIDEOID
   ```
   (or `YouTube: https://www.youtube.com/watch?v=VIDEOID`). Never invent a URL.
4. **Audio-only** — leave without a Watch line.
5. **Feed-level `description`** — same Brief-style show blurb (see store.json channel description).

## Example (episode)

```
Sean Carroll with physicist Jim Al-Khalili on time: whether it is fundamental or emergent, why it has an arrow, and how physics meets lived experience of its passage.

Watch: https://youtu.be/JVJP_d9U8Gs
```

## Example (show — Brief)

```
A daily morning news Brief for people who want the world clear before the day starts. India first, then the week’s decisive stories abroad — markets, politics, tech, and the forces that move them. Two anchors, eight to twelve minutes, no hot takes.
```

Playlist map: `yt_playlist_map.json`. Cached items: `yt_playlist_items.json` (refresh via ytmusicapi + auth).
