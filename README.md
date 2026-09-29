# Hatoun copper prospect

A satellite screening of the Hatoun copper occurrence near Gahkuch, Ghizer District, Gilgit-Baltistan, Pakistan (36.20–36.32°N, 73.68–73.84°E).

**Live platform:** https://dinarwali4.github.io/hatoun-copper/

RegenX.eco Geospatial Computational Model · Prepared by **Dinar Wali** · dinar.wali@regenx.eco · [LinkedIn](https://www.linkedin.com/in/dinar-wali-621954102/)

## Ranked zones
A zone is where NASA EMIT shows three absorptions together on at least 2 of 3 reflectance dates (Jun 2023, Jun 2024, Jun 2026): ferric iron at 900 nm, Al-OH (sericite) at 2200 nm and jarosite at 2265 nm. Coordinates are WGS84, ±60 m.

| Zone | Area | Peak | Dates |
|---|---|---|---|
| HZ1 east tributary | 68.2 ha | 36.27525 N, 73.80625 E | 3/3 |
| HZ2 west bank | 28.0 ha | 36.30525 N, 73.77825 E | 2/3 |
| HZ3 west bank | 16.9 ha | 36.30175 N, 73.79175 E | 3/3 |
| HZ5 | 13.9 ha | 36.31225 N, 73.75975 E | 3/3 |
| HZ6 | 10.7 ha | 36.29775 N, 73.77325 E | 3/3 |

The published coordinate (36°15′39.13″N 73°45′23″E) lies on village fields. The nearest anomalies are HZ11–HZ13, 1.5–2.4 km east.

**Validation.** No cells on the control slopes pass the zone rule (0 of 4,800). The June 2026 date was not used to find the zones and reproduces the band depths.

**Limits.** The satellites map alteration, not copper grade. Copper minerals themselves were not robustly detected. The same alteration can form over barren pyrite, so ground sampling is needed.

## Contents
| Path | What |
|---|---|
| `docs/` | Interactive platform (GitHub Pages), annotated Google Earth imagery, KML |
| `Hatoun_Copper_RegenX_zones.kml` | Zone outlines and labelled peaks for Google Earth |
| `data/` | Zones, EMIT mineral persistence, 2026 validation (JSON) |
| `figures/` | Spectra, zone map, persistence chart |
| `scripts/` | Python pipeline |

## Pipeline
1. **Download:** `s2_fetch.py`, then `dl.sh`. EMIT needs a NASA Earthdata token in `~/.edl_token`.
2. **Process:** `emit_min.py`, `emit_rfl.py`, `emit_feat.py`, `rfl_check.py`, `s2_cu.py`.
3. **Zones and validation:** `cu_targets.py`, `zones.py`, `validate2026.py`.
4. **Outputs:** `make_kml.py`, `fig_spectra.py`, `fig_zonemap.py`, `figs.py`, `finish_ge.py`.

## Sources
- ACM Mines and Minerals (Pvt) Ltd, *Hatoun, Ghizer* site assessment. Summary only.
- *Journal of Water and Climate Change* 14(7), Ghizer River Basin potentially harmful elements.
- Data: NASA EMIT (LP DAAC), Copernicus Sentinel-2 and GLO-30. Google Earth Pro imagery © Airbus, used for annotation.
