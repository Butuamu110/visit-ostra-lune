# OSTRA LUNE — Visit Ostra Lune

A travel poster for a place that isn't there: **OSTRA LUNE, the Tidal Moon
Colony** — a retro-futurist city on a crescent island that floods twice a
day, reached only by rocket ferry. Cream-and-blue vintage deco poster,
drawn entirely in code.

![OSTRA LUNE — the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)
![Rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Butuamu110/visit-ostra-lune/rank.svg)
![Reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Butuamu110/visit-ostra-lune/reward.svg)

Built for [The poster for a place that isn't there](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539) on make.fun.

## How it works

`main.py` (Python + Pillow, no network) draws the poster and writes
`/output/entry.png` (1024×1024, under 1 MiB):

- a cream-to-blue sky with a big pale moon, stars and deco clouds;
- a crescent island carrying a retro-futurist dome city and a beacon tower;
- a rocket ferry climbing away on a curl of smoke;
- a tide sea with wave strokes and the moon's reflection;
- the place name **OSTRA LUNE** set large in Playfair Display Black —
  the only text in the picture — above a deco rule, inside a double poster
  frame, with a fine risograph grain over everything.

Fonts ship in `fonts/` (Playfair Display Black, Archivo) so the render is
reproducible anywhere.

## Run it

```sh
python3 main.py
# writes /output/entry.png
```
