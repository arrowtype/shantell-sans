# Shantell Font Project

A custom font based on the handwriting of the artist Shantell Martin.

- Website: https://shantellmartin.art/
- Instagram: https://www.instagram.com/shantell_martin/
- TED talk: https://www.ted.com/talks/shantell_martin_how_drawing_can_set_you_free

## Build

This is evolving, but:

Install pipenv.

Start the shell:

```bash
pipenv shell
```

Install dependencies.

```bash
python scripts--build/prep-wght_bnce_qurk--simplified_charset.py
```

This will prep a folder like `sources/wght_bnce_flux--smpl--prepped`. Copy in the designspace, such as `sources/shantell-wght_BNCE_FLUX--smpl.designspace`.

..then build with FontMake.

```bash
fontmake -o variable -m sources/wght_bnce_flux--smpl--prepped/shantell-wght_BNCE_FLUX--smpl.designspace
```