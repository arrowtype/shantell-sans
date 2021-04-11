# Shantell Font Project

A custom font based on the handwriting of the artist Shantell Martin.

- Website: [shantellmartin.art](https://shantellmartin.art/)
- Instagram: [instagram.com/shantell_martin](https://www.instagram.com/shantell_martin/)
- TED talk: [How Drawing Can Set You Free](https://www.ted.com/talks/shantell_martin_how_drawing_can_set_you_free)

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
