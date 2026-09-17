# Lokale Webfonts

Abruf und Prüfung: 2026-09-14. Unveränderte WOFF2-Binärdateien von Google Fonts;
lokal wurden nur die Dateinamen und die CSS-Quellpfade angepasst.

## Google-Fonts-CSS

- [Bisherige Anfrage mit Einzelgewichten](https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@300;400;500&display=swap)
- [Anfrage mit variablen Gewichtsbereichen](https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400..600;1,400&family=Jost:wght@300..500&display=swap)
- Prüf-User-Agent: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`

Beide Antworten verweisen für die bisherigen Gewichte auf dieselben sechs
Latin-/Latin-Ext-Dateien. `../../css/fonts.css` übernimmt deren `unicode-range`,
Familien, Stile und `font-display: swap`; normale Schnitte werden als variable
Bereiche deklariert. Die vollständigen Unicode-Ranges stehen dort pro Font-Face.
Keine zusätzlichen Sprachsubsets, keine lokale Neukonvertierung oder Subsetting.

## Dateien und Zuordnung

| Datei | Stil | CSS-Gewicht | Tatsächliche WOFF2-Achse | Bytes |
| --- | --- | --- | --- | ---: |
| `cormorant-garamond-v21-latin-ext-normal.woff2` | normal | 400–600 | wght 300–700, Standard 300 | 33.736 |
| `cormorant-garamond-v21-latin-normal.woff2` | normal | 400–600 | wght 300–700, Standard 300 | 37.640 |
| `cormorant-garamond-v21-latin-ext-italic.woff2` | italic | 400 | statisch 400 | 20.284 |
| `cormorant-garamond-v21-latin-italic.woff2` | italic | 400 | statisch 400 | 23.660 |
| `jost-v20-latin-ext-normal.woff2` | normal | 300–500 | wght 100–900, Standard 400 | 17.104 |
| `jost-v20-latin-normal.woff2` | normal | 300–500 | wght 100–900, Standard 400 | 26.576 |

Gesamt: **159.000 Bytes (155,27 KiB)** WOFF2. Die größeren internen Achsen werden
im CSS auf die angefragten Bereiche begrenzt. Cormorants variable Normaldateien
tragen intern den Familiennamen `Cormorant Garamond Light`, passend zur
Standardinstanz 300 und den offiziellen Google-Fonts-Metadaten; der CSS-Familienname
bleibt `Cormorant Garamond`.

### Originaldateien

- `cormorant-garamond-v21-latin-ext-normal.woff2`: https://fonts.gstatic.com/s/cormorantgaramond/v21/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYp3tKgS4.woff2
- `cormorant-garamond-v21-latin-normal.woff2`: https://fonts.gstatic.com/s/cormorantgaramond/v21/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtK.woff2
- `cormorant-garamond-v21-latin-ext-italic.woff2`: https://fonts.gstatic.com/s/cormorantgaramond/v21/co3smX5slCNuHLi8bLeY9MK7whWMhyjYrGFEsdtdc62E6zd58jD-htM8Efs.woff2
- `cormorant-garamond-v21-latin-italic.woff2`: https://fonts.gstatic.com/s/cormorantgaramond/v21/co3smX5slCNuHLi8bLeY9MK7whWMhyjYrGFEsdtdc62E6zd58jD-iNM8.woff2
- `jost-v20-latin-ext-normal.woff2`: https://fonts.gstatic.com/s/jost/v20/92zatBhPNqw73ord4iYl.woff2
- `jost-v20-latin-normal.woff2`: https://fonts.gstatic.com/s/jost/v20/92zatBhPNqw73oTd4g.woff2

## Lizenzen

Beide Familien: **SIL Open Font License 1.1**. Die vollständigen Texte samt
Copyright-Zeilen sind bytegleich mit den abgerufenen offiziellen Dateien:

- `OFL-Cormorant-Garamond.txt` (4.387 Bytes): [OFL.txt](https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/OFL.txt), [METADATA.pb](https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/METADATA.pb).
  Copyright 2015 the Cormorant Project Authors (github.com/CatharsisFonts/Cormorant).
- `OFL-Jost.txt` (4.384 Bytes): [OFL.txt](https://raw.githubusercontent.com/google/fonts/main/ofl/jost/OFL.txt), [METADATA.pb](https://raw.githubusercontent.com/google/fonts/main/ofl/jost/METADATA.pb).
  Copyright 2020 The Jost Project Authors (https://github.com/indestructible-type).

## SHA-256

```text
cfa9a397d86f66c5c51775a2500a712d5f632a04f0c5eca6930dfaf612d4566d  cormorant-garamond-v21-latin-ext-normal.woff2
d80df8ff5aecd299a61549f9e29ab1ed0b9b05f4ea71d50fe978e07d5240b235  cormorant-garamond-v21-latin-normal.woff2
96ec6109d044a8f2b279937499923fc0435db3e6bd91ce4cb1fd806d566378b9  cormorant-garamond-v21-latin-ext-italic.woff2
e48e58027030df56869b795ca6f19b7012158275f7ad7cde1900b4a0b68d02e2  cormorant-garamond-v21-latin-italic.woff2
312ef2b80cefd8d6fd0e8553536862e7103f80be117a5aeba333dac68e4c0a6a  jost-v20-latin-ext-normal.woff2
7726a5cd6f3c0e876c028ea2a643d45f7aad4b0f164b70966c669f4a4668f4b9  jost-v20-latin-normal.woff2
60700d351cac4650c51f3f9db318d2a420f8b45052dba2715eb5fec41f0f6956  OFL-Cormorant-Garamond.txt
1af3438a4d5f0ed2bdbc5751a5a67ebf6d537334161184b7fbb68503ef0ea0c5  OFL-Jost.txt
```

## Durchgeführte Font-Prüfungen

- HTTP 200; WOFF2-Signatur `wOF2`, TrueType-Flavor `0x00010000`, deklarierte
  Dateilänge, Tabellenzahl, reserviertes Headerfeld und komprimierte Größe geprüft.
- Alle sechs Dateien mit FontTools/Brotli vollständig dekomprimiert und ihre
  OpenType-Tabellen eingelesen; Familie, Italic-Flag, Gewichtsachsen bzw.
  statisches Gewicht, Copyright und eingebetteter OFL-Link geprüft.
- Glyphenbeispiele: `ÄÖÜäöüßŒ` in jedem Latin-Font, `ĀČŁŠŽẞ` in jedem
  Latin-Ext-Font nachgewiesen. Unicode-Ranges exakt aus dem Google-CSS übernommen;
  diese Ranges bedeuten keine lückenlose Glyphenabdeckung jedes Intervalls.
- SHA-256 der heruntergeladenen Bytes mit den gespeicherten WOFF2-Dateien
  abgeglichen; Lizenztexte byteweise mit den offiziellen Quellen verglichen.
- Alle sechs lokalen CSS-Faces gegen die Google-CSS-Zuordnung geprüft,
  einschließlich der bisherigen Einzelgewichte 400/500/600, italic 400 und
  300/400/500.
