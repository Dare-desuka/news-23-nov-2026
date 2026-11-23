[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Dare-desuka/news-23-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Dare-desuka/news-23-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in One Day — Monday, 23 November 2026

A newspaper front page that sums up Monday 23 November 2026 in a single
image, drawn with Python and PIL. It is an entry for the
[news-image-20261123 bounty](https://make.fun/bounty/news-image-20261123)
on [make.fun](https://make.fun/r/q3egcwt3) (referral code `q3egcwt3`).

## The four stories

- **Dymer, Ukraine** — Rescuers pulled 7-year-old David alive from the
  rubble of an apartment block 14 hours after a Russian drone strike;
  at least 10 people were killed.
- **Tokyo, markets** — The AI stock sell-off spread across Asia: the
  Nikkei fell 5.06%, Korea and Hong Kong slid again, and gold rose about
  2.7% as investors sought safety.
- **Brussels, Europe** — Air-traffic control provider Skeyes suspended
  services from 07:00 to 21:00 in a nationwide strike against austerity
  cuts; 429 flights were cancelled and about 60,000 passengers affected.
- **Seoul, trade** — South Korean customs data released on Monday put
  2026 exports at $1.0076 trillion, a first for the country, driven by
  AI-chip demand.

The "Also today" strip adds Marc Márquez's eighth MotoGP title at
Portimão, Liverpool's 4-0 win over Manchester United in Mauricio
Pochettino's first game in charge, the Houthis' claimed strike on Saudi
Arabia's Rabigh refinery, and the resumed search at the Cikande candy
factory fire in Indonesia.

## How it is built

`gen_image.py` draws the 1024×1024 front page (PIL, deterministic: two
runs produce byte-identical output) and writes `entry.png`. `main.py`
is standard library only and just copies `entry.png` to
`/output/entry.png`, as the bounty requires.
