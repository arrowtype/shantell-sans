# Shantell Font Project

A custom font based on the handwriting of the artist Shantell Martin.

- Website: https://shantellmartin.art/
- Instagram: https://www.instagram.com/shantell_martin/
- TED talk: https://www.ted.com/talks/shantell_martin_how_drawing_can_set_you_free

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

### Build

```bash
python3 scripts--build/prep-build.py
```

This will prep a folder like `sources/wght_BNCE_IRGL--prepped`. Copy in the designspace, such as `sources/wght_BNCE_IRGL--prepped/shantell_sans-wght_BNCE_IRGL.designspace`.

Build the variable font:

```bash
scripts--build/build-vf.sh sources/wght_BNCE_IRGL--prepped/shantell_sans-wght_BNCE_IRGL.designspace
```

Build the static fonts (note the `--static` addition to the designspace path):

```bash
scripts--build/build-static.sh sources/wght_BNCE_IRGL--prepped/shantell_sans-wght_BNCE_IRGL--static.designspace
```
