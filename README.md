# THE WORLD TODAY — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/tanglangbc/news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/tanglangbc/news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the make.fun bounty **news-image-20261124** — *"Sum up 24 November's
world news in one image"*.

One 1024×1024 image, six stories from the 24 November 2026 news cycle,
drawn as a newspaper front page: masthead **THE WORLD TODAY**, six panels,
each with a hand-drawn pictogram and a short truthful headline.

## The six stories

1. **COP31 COLLAPSES — NO DEAL IN ANTALYA**
   The UN climate summit in Antalya ended without an overarching deal after
   countries deadlocked over fossil-fuel language; the collapse dominated
   Monday's coverage.
   Source: https://www.aljazeera.com/news/2026/11/23/cop31-what-next-after-un-climate-talks-collapse

2. **HUANG BACK AT NVIDIA — SHARES JUMP 30%**
   Nvidia's board unanimously reinstated Jensen Huang as CEO and president
   on 23 November, days after his resignation; shares soared more than 30%.
   Source: https://www.cnn.com/2026/11/23/markets/us-stocks-rebound-intl?cid=external-feeds_iluminar_meta

3. **FACTORY FIRE KILLS 24 — DOZENS MISSING IN BANTEN**
   A fire at the PT Fonusa Agung Mulia candy factory in Cikande, Banten,
   killed 24 people; about 30 remained missing as rescuers searched the
   wreckage on 23 November.
   Source: https://www.channelnewsasia.com/asia/indonesia-factory-fire-killed-rescuers-search-missing-6573141

4. **NEW INDIA-NEPAL TRAIN — AYODHYA TO JANAKPUR**
   The first direct Saryu-Kamala Express between Ayodhya and Janakpur was
   flagged off on 23 November; the inaugural train reached Janakpur on
   24 November, with the return leg departing the same day.
   Source: https://indianexpress.com/article/india/india-nepal-train-service-pm-modi-balendra-shah-flag-off-ayodhya-janakpur-saryu-kamala-express-10972887/

5. **DEADLY STRIKES HIT KYIV — HOMES DESTROYED**
   Russian drone strikes on the Kyiv region killed at least 14 people,
   including a child, and partly collapsed a five-storey block in Dymer;
   rescuers pulled survivors from the rubble on 23 November.
   Source: https://www.thehindu.com/news/international/ukraine-says-russian-strikes-kill-several-in-kyiv-region/article71733677.ece

6. **MANCHESTER ARENA CLEARED — 12,000 EVACUATED**
   More than 12,000 people were evacuated from the Co-op Live arena in
   Manchester after an unknown substance was released during Don Toliver's
   concert; dozens were treated for eye and breathing symptoms.
   Source: https://www.cnn.com/2026/11/23/europe/manchester-coop-live-tear-gas-don-toliver-hnk-intl?cid=external-feeds_iluminar_meta

## How it is built

`main.py` — Python 3, **standard library only** (no PIL). It draws the whole
front page pixel by pixel and writes its own PNG with `zlib`/`struct`.

```sh
MAKEFUN_OUTPUT_DIR=./out python3 main.py   # writes out/entry.png
```

Deterministic: two runs produce byte-identical output. Output is a
1024×1024 PNG, well under 1 MiB.

## License

MIT — see [LICENSE](LICENSE).
