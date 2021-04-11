# Shantell Font Project

A custom font based on the handwriting of the artist [Shantell Martin](https://shantellmartin.art/).

![Typographic waterfalls showing the font](specimens/shantell_sans-waterfalls-2021_04_11.png)

## Font Features

### Variable Axes

Axis | Tag | Range | Default | Description
-- | -- | -- | -- | --
Weight | wght | 300 to 800 | 300 | Light to ExtraBold. Can be defined with the `font-weight` CSS property.
Irregularity | IRGL | 0 to 1 | 0 | Emulates the irregular sizing of handwriting.
Bounce | BNCE | -100 to 100 | 0 | Emulates the bouncy baseline of handwriting, but extends this for extra fun.

### Character set

[to do]

### OpenType Features

- Contexual Alternates `calt` – On by default; adds randomization to Irregular & Bouncy styles
- Case-sensitive punctuation `case` – Makes punctuation fit cap-height for uppercase typesetting
- Arbitrary Fractions `frac` – Makes proper fractions from strings like 1/2
- Tabular Figures `tnum` – Numbers & currencies are monospaced across styles by default to improve table layout, but this makes certain punctuation become tabular as well
- Proportional Figures `pnum` – Makes numbers take up a natural amount of space
- Localized Forms `locl` – Supports special language requirements for Catalan, Moldovian & Romanian, Dutch, Turkish, and more
- Standard Ligatures `liga` – Converts 3+ repeated hyphens into wavy lines, just for fun

## Building the fonts

### Set up requirements

Install pipenv.

```bash
pip install pipenv
```

Start the `pipenv` shell:

```bash
pipenv shell
```

Install dependencies from `Pipfile.lock`.

```bash
pipenv sync
```

Finally, give the build scripts permission to run:

```bash
chmod +x scripts--build/*.sh
```

### Build

```bash
python3 scripts--build/prep-build.py
```

This will prep a folder like `sources/wght_BNCE_IRGL--prepped`. Copy in the designspace, such as `sources/wght_BNCE_IRGL--prepped/shantell_sans-wght_BNCE_IRGL.designspace`.

Build the variable font:

```bash
scripts--build/build-vf.sh
```

Build the static fonts:

```bash
scripts--build/build-static.sh
```

## Release

Update the version number in `version.txt` to the desired next release number, then build fonts.

Then, run this script to create a zipped archive of the fonts folder:

```bash
scripts--build/make-release.sh
```
