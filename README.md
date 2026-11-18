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
2026", with **32 verified stories**: six illustrated tiles — the day's most
consequential events, each with a picture, a headline and a short deck — and
a "THE DAY IN BRIEF" digest of 26 further one-line headlines across regions
and fields, so the day reads from the image alone.

Illustrated stories:

1. **Drones over Gulf** (Middle East) — Kuwait shoots down hostile drones
   overnight; Bahrain sounds the all-clear after a threat alert.
2. **Nvidia +103%** (USA · Business) — revenue $115.8bn, up 103% year on
   year, in its first report since Jensen Huang was ousted as CEO; the
   board rules out his return and guides $130bn next quarter.
3. **Quad in Manila** (Asia · Diplomacy) — the first Quad leaders' summit
   since 2024 opens in Manila with Trump, Modi, Albanese and Takaichi.
4. **Kyiv bridges hit** (Europe · War) — Ukraine damages the Crimean bridge
   as Russia strikes bridges in Kyiv.
5. **Latvia's new govt** (Europe · Politics) — parliament approves
   Kulbergs' cabinet 57–34 ahead of Independence Day.
6. **Akvan strengthens** (Asia · Weather) — the Bay of Bengal cyclone is
   set to turn severe by Thursday; Odisha readies 74 teams.

The brief adds 26 more: the Dow's 848-point plunge, the Trump–BBC
deposition deadline, Merchant's 27.5-year sentence, the reported Iran
dirty-bomb plot, Taiwan flight curbs, Modi at the East Asia Summit, India's
ITU re-election, Amazon's $7bn India plan, Japan's Asian energy agency,
Deutsche Bank's ignored warnings, the BofA fund-manager poll, Salesforce's
slide, Costco's outage-driven gains, St Kitts ending its citizenship
scheme, Australia's settlement sanctions, Singapore's export jump,
Malaysia's investment figures, Microsoft's outage cause, the WFP's Gaza
warning, the UN's Ukraine and Sudan civilian tolls, Jordan 2–0 Australia,
Celtic 2–1 Dundee, Malaysia 10–0 Guam, and early voting in Victoria.

Sources: Reuters, AP, Al Jazeera, Nvidia, US DOJ, UN, Bernama, ABC — all
events of, or first reported on, 18 November 2026.

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
