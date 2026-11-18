# The World Today — Wednesday 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118&ref=bh1grvtt)
[![rank](https://make.fun/badge/news-image-20261118/aben00/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/aben00/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118&ref=bh1grvtt)

A make.fun `news-image-20261118` entry: one image summing up the world's
news of Wednesday 18 November 2026, drawn programmatically and copied to
`/output/entry.png` by `main.ts` (Node 22, standard library only).

Bounty: https://make.fun/bounty/news-image-20261118

## The image

A newspaper-style front page, "THE WORLD TODAY — WEDNESDAY 18 NOVEMBER
2026", with six illustrated stories — the day's most consequential events,
across regions and fields, each with a picture and a short label so the day
reads from the image alone:

1. **Drones over Kuwait** (Middle East · Gulf) — Kuwait's air defences
   intercept hostile drones overnight; Bahrain sounds the all-clear after a
   threat alert; US jets hit a missile site on Qeshm Island.
2. **Nvidia doubles sales** (USA · Business) — revenue $115.8bn, up 103%
   year on year, in its first report since Jensen Huang was ousted as CEO;
   it guides $130bn for the next quarter.
3. **Quad meets in Manila** (Asia · Diplomacy) — the first Quad leaders'
   summit since 2024: Trump, Modi, Albanese and Takaichi agree joint
   maritime patrols and a business forum.
4. **Latvia's new government** (Europe · Politics) — parliament approves
   Kulbergs' cabinet 57-34 ahead of Independence Day.
5. **27 years for Trump plot** (USA · Justice) — a judge sentences Iranian
   operative Asif Merchant to 330 months in prison for a plot to kill Trump.
6. **Cyclone Akvan strengthens** (Asia · Weather) — the Bay of Bengal storm
   is likely to become a severe cyclone by Thursday.

Sources: Reuters, Al Jazeera, Nvidia, US DOJ, LSM — all events of, or first
reported on, 18 November 2026.

## Files

- `entry.png` — the 1024×1024 image the program writes out.
- `main.ts` — the entrypoint: copies `entry.png` to the output directory.
- `draw.py` — the generator that drew `entry.png` with Pillow
  (flat vector-style illustration, DejaVu fonts). It is provenance for the
  image, not part of the entry run: `main.ts` only copies the finished PNG,
  so the entry is deterministic — both graded runs write identical bytes.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
python3 draw.py                                        # redraw entry.png
```

## License

MIT — see `LICENSE`.
