# Datasets

Every file here was written for this book. They are teaching scenarios, not collected
observations.

Most `.xlsx` files have three sheets, 109 of the 134:

| Sheet | What it holds |
|---|---|
| the data | One row per unit of analysis, in a sheet named `Data` or named for what it holds. |
| `Codebook` | Every column: name, type, and what it means. |
| `Notes` | The scenario, the question it poses, and where the data is deliberately dirty. |

The other 25 add sheets a chapter needs, such as a second table to join, an analysis plan written
before the data arrived, or a `Truth` sheet holding the values a simulation was built from. Every
workbook has a `Notes` sheet. The `.csv` files are single tables that the notebooks load directly.

They are generated so a specific method has something honest to work on, and many carry
planted problems, missing values, impossible readings, duplicate rows, so a chapter can
show the cleaning as well as the analysis.

## Names that mislead

Three files are named after well-known public datasets and **are not those datasets**:

| File | What it is | The real one |
|---|---|---|
| `ames_housing.csv` | Synthetic, 610 rows, 16 columns, renamed schema | De Cock (2011), 2,930 rows, 82 columns |
| `bike_share.csv` | Synthetic, modeled on the UCI scenario | UCI Bike Sharing, different columns and encoding |
| `penguins.csv` | Synthetic, 347 rows with 3 duplicates, 10 columns, two of them added for encoding practice | Palmer penguins: Gorman, Williams and Fraser (2014), packaged by Horst, Hill and Gorman (2020), 344 rows |

They borrow the setting because it is familiar, not the data. Results computed here will
not match published analyses of the originals. If you want the originals, get them from
their own sources, where their own licenses apply.

## License

CC BY 4.0, the same as the book. Use them, including commercially, with credit. See
[`../LICENSES.md`](../LICENSES.md).
