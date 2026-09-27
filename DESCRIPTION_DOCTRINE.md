# Podcast RSS description doctrine (Karan routine)

**Locked template for Legion private feeds** (`feeds/*/store.json` → RSS):

## Title

```
Original episode title (Podcast Name)
```

- Use the episode’s true title + the `show` / podcast name field.
- If the title already ends with `(Podcast Name)` matching `show`, do **not** double-wrap.
- Strip densifier junk from titles only if it somehow appears — never invent show names.

## Description body + links

1. **Brief-style body** — clear, sober, listener-facing. One or two sentences on what the episode is about. No hot takes.
2. **No densifier jargon** — ban: densifier, Commentary-as-performance, Arena craft, stack/TTS scrap, “sharpens taste,” “craft move,” “operator OS,” “pressure-test” as self-praise.
3. **Optional link lines** (never invent URLs), in this order after the body:

```
<body>

Watch: https://youtu.be/VIDEOID

Episode: https://canonical-episode-page
```

- **Watch** — only when a YouTube mirror exists (playlist / known `videoId`).
- **Episode** — only when a canonical episode page exists in `link` (Apple episode URL with `i=` or an episode-slug path, publisher episode page). **Not** the mp3 enclosure, bare show homepage, YouTube search/channel, or show-only Apple URL.
- Audio-only / no page → omit that line.

## Feed-level `description`

Same Brief-style show blurb on each store’s channel `description`.

## Examples

**Title**

```
366 | Jim Al-Khalili on Time, Quantum, Biology, and Cosmology (Sean Carroll's Mindscape)
```

**Description**

```
Sean Carroll with physicist Jim Al-Khalili on time: whether it is fundamental or emergent, why it has an arrow, and how physics meets lived experience of its passage.

Watch: https://youtu.be/JVJP_d9U8Gs

Episode: https://podcasts.apple.com/us/podcast/366-jim-al-khalili-on-time-quantum-biology-and-cosmology/id1406534739?i=1000786961179
```

**Show blurb (Brief)**

```
A daily morning news Brief for people who want the world clear before the day starts. India first, then the week’s decisive stories abroad — markets, politics, tech, and the forces that move them. Two anchors, eight to twelve minutes, no hot takes.
```

Playlist map: `yt_playlist_map.json`. Cached items: `yt_playlist_items.json` (refresh via ytmusicapi + auth).
