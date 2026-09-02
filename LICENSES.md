# Licensing

This repository holds three kinds of material, and they are licensed differently.
Everything in it is my own work.

| What | License | Covers |
|---|---|---|
| **The book** | [CC BY 4.0](LICENSE) | `chapters/*.html`, `index.html`, `toc.html`, `introduction.html`, the `infographics-*.html` pages, `assets/`, `reports/` |
| **The datasets** | [CC BY 4.0](LICENSE) | `data/` |
| **The code** | [MIT](LICENSE-CODE) | `chapters/notebooks/*.ipynb`, `scripts/`, `.github/workflows/`, and code shown inside a chapter page |

## What that means in practice

**You may use any of it, including commercially, as long as you credit me.** Teach from
it, translate it, quote it, build on it, put a chapter in front of a class or a team.

A reasonable credit:

> John Fisher, *Statistics, Data Science and AI: A Visual Handbook*.
> https://johnfisher-ai.github.io/Statistics-Data-Science-AI-Visual-Book/

For code, the MIT license asks only that the notice travels with any substantial
portion. Copying a few lines out of a notebook into your own work needs nothing.

## The datasets

Every dataset in `data/` was written for this book. They are scenarios, not
observations: generated so that a specific method has something honest to work on, and
often deliberately dirtied so a chapter can show the cleaning as well as the analysis.

**Two are named after well-known public datasets and are not those datasets.**
`ames_housing.csv` is 610 rows and 16 columns; the real Ames Housing data (De Cock,
2011) is 2,930 rows and 82 columns with entirely different column names. `bike_share.csv`
is likewise modeled on the UCI Bike Sharing data rather than drawn from it. If you are
comparing results against published analyses of the originals, the numbers will not
agree, and that is why. See [`data/README.md`](data/README.md).

## What this does not cover

Trademarks and the visual identity, the banner and the branded report styling, are not
licensed for reuse as marks. Use the material, not the branding, to represent your own
work.
