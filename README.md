# Shantell Sans

A custom font based on the handwriting of the artist [Shantell Martin](https://shantellmartin.art/).

Rather than trying to exactly mimick or “replace” Shantell’s writing, Shantell Sans takes inspiration from marker-based fonts like Comic Sans & Inkwell Sans. It aims to create an authetically typographic system with a single core shape per character, in order to deliver a simple, inviting, and energetic tone while encouraging freedom and play.

![Font styles in Shantell Sans](specimens/shantell-sans-styles.png)

## Font Features

### Variable Axes

Shantell’s writing is dynamic and doesn’t adhere to a rigid baseline or precise metrics, so Shantell Sans employs *variable axes* are to reflect this flexibility in a fluid range of styles.

![Axes in Shantell Sans](specimens/axes.png)

Axis | Tag | Range | Default | Description
:-- | :-- | --: | --: | :--
Weight | `wght` | 300–800 | 300 | Light to ExtraBold. Can be defined with the `font-weight` CSS property.
Italic | `ital` | 0–1 | 0 | Upright to Italic. Can be defined with the `font-style` CSS property.
Bounce | `BNCE` | -100–100 | 0 | Emulates the bouncy baseline of handwriting, but extends this for extra fun.
Informality | `INFM` | 0–100 | 0 | Emulates the irregular shaping and proportions of handwriting.
Spacing | `SPAC` | 0–100 | 0 | Adds extra spacing to the left and right of each glyph.

### Character set

Shantell Sans supports a wide range of 380+ languages using Latin & Cyrillic scripts, throughout Europe, the Americas, and central Asia. It includes the following characters:

```
A À Á Â Ã Ä Å Ā Ă Ą Ǎ Ǻ Ȁ Ȃ Ạ Ả Ấ Ầ Ẩ Ẫ Ậ Ắ Ằ Ẳ Ẵ Ặ B C Ç Ć Ĉ Ċ Č D Ď E È É Ê Ë Ē Ĕ Ė Ę Ě Ȅ Ȇ Ẹ Ẻ Ẽ Ế Ề Ể Ễ Ệ F G Ĝ Ğ Ġ Ģ Ǧ H Ĥ I Ì Í Î Ï Ĩ Ī Ĭ Į İ Ȉ Ȋ Ỉ Ị J Ĵ K Ķ L Ĺ Ļ Ľ M N Ñ Ń Ņ Ň O Ò Ó Ô Õ Ö Ō Ŏ Ő Ơ Ǫ Ȍ Ȏ Ȫ Ȭ Ȱ Ọ Ỏ Ố Ồ Ổ Ỗ Ộ Ớ Ờ Ở Ỡ Ợ P Q R Ŕ Ŗ Ř Ȑ Ȓ S Ś Ŝ Ş Š Ș T Ţ Ť Ț U Ù Ú Û Ü Ũ Ū Ŭ Ů Ű Ų Ư Ǔ Ȕ Ȗ Ụ Ủ Ứ Ừ Ử Ữ Ự V W Ŵ Ẁ Ẃ Ẅ X Y Ý Ŷ Ÿ Ȳ Ỳ Ỵ Ỷ Ỹ Z Ź Ż Ž Æ Ǽ Ð Ø Ǿ Þ Đ Ħ Ĳ Ŀ Ł Ŋ Œ Ŧ Ə Ǆ Ǉ Ǌ ẞ Ω Ђ Є Ѕ І Ї Ј Љ Њ Ћ Џ А Ӑ Ӓ Б В Г Ѓ Д Е Ѐ Ё Ӗ Ж Ӂ Ӝ З Ӟ И Ѝ Ӣ Ӥ К Ќ Л М Н О Ӧ П Р С Т У Ў Ӯ Ӱ Ӳ Ф Х Ц Ч Ӵ Ш Щ Ъ Ы Ӹ Ь Э Ю Я Ѣ Ѫ Ѳ Ѵ Ґ Ғ Ҕ Җ Ҙ Қ Ҝ Ҡ Ң Ҥ Ҫ Ү Ұ Ҳ Ҷ Ҹ Һ Ӏ Ӌ Ӕ Ә Ө Ӷ Ԛ Ԝ a à á â ã ä å ā ă ą ǎ ǻ ȁ ȃ ạ ả ấ ầ ẩ ẫ ậ ắ ằ ẳ ẵ ặ b c ç ć ĉ ċ č d ď e è é ê ë ē ĕ ė ę ě ȅ ȇ ẹ ẻ ẽ ế ề ể ễ ệ f g ĝ ğ ġ ģ ǧ h ĥ i ì í î ï ĩ ī ĭ į ȉ ȋ ỉ ị j ĵ k ķ l ĺ ļ ľ m n ñ ń ņ ň o ò ó ô õ ö ō ŏ ő ơ ǫ ȍ ȏ ȫ ȭ ȱ ọ ỏ ố ồ ổ ỗ ộ ớ ờ ở ỡ ợ p q r ŕ ŗ ř ȑ ȓ s ś ŝ ş š ș t ţ ť ț u ù ú û ü ũ ū ŭ ů ű ų ư ǔ ȕ ȗ ụ ủ ứ ừ ử ữ ự v w ŵ ẁ ẃ ẅ x y ý ÿ ŷ ȳ ỳ ỵ ỷ ỹ z ź ż ž ß æ ǽ ð ø ǿ þ đ ħ ı ĳ ĸ ŀ ł ŋ œ ŧ ǆ ǉ ǌ ə π а ӑ ӓ б в г ѓ д е ѐ ё ӗ ж ӂ ӝ з ӟ и й ѝ ӣ ӥ к ќ л м н о ӧ п р с т у ў ӯ ӱ ӳ ф х ц ч ӵ ш щ ъ ы ӹ ь э ю я ђ є ѕ і ї ј љ њ ћ џ ѣ ѫ ѳ ѵ ґ ғ ҕ җ ҙ қ ҝ ҡ ң ҥ ҫ ҳ ҷ ҹ һ ӌ ӏ ӕ ә ө ӷ ԛ ԝ ǅ ǈ ǋ ʹ ʺ ʼ ª º ̀ ́ ̂ ̃ ̄ ̆ ̇ ̈ ̉ ̊ ̋ ̌ ̏ ̑ ̒ ̛ ̣ ̤ ̦ ̧ ̨ ̮ ̱ 0 1 2 3 4 5 6 7 8 9 ¼ ½ ¾ ⅓ ⅔ ⅛ ⅜ ⅝ ⅞ _ - ‐ – — ( ) [ ] { } ⟨ ⟩ \ # % ‰ ' " ‘ ’ “ ” ‚ „ ‹ › « » * † ‡ . , : ; … ! ¡ ? ¿ / \ ⁄ | ¦ @ & § ¶ ℓ № · • ′ ″ + − ± ÷ × = < > ≤ ≥ ≈ ≠ ¬ ⁒ ∂ ∆ ∏ ∑ ∕ ∙ √ ∞ µ ∫ $ ¢ £ ¤ ¥ ₡ ₤ ₦ ₩ ₫ € ƒ ₭ ₮ ₱ ₲ ₴ ₵ ₸ ₹ ₺ ₼ ₽ ^ ~ ´ ` ˝ ˆ ˇ ˘ ˜ ¯ ¨ ˙ ˚ ¸ ˛ © ® ™ ° ◊ ♡ ♥ ✓ ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ← ↑ → ↓ ↖ ↗ ↘ ↙ @
```

### OpenType Features

Feature | Tag | Description
:-- | :-- | :--
Contexual Alternates | `calt` | On by default; activates a ligature for `її`, used in Ukrainian
Case-sensitive punctuation | `case` | Makes punctuation fit cap-height for uppercase typesetting
Arbitrary Fractions | `frac` | Makes proper fractions from strings like 1/2
Tabular Figures | `tnum` | Numbers & currencies are monospaced across styles by default to improve table layout, but this makes certain punctuation become tabular as well
Proportional Figures | `pnum` | Makes numbers take up a natural amount of space
Localized Forms | `locl` | Supports special character-design requirements for various languages (TRK, CAT, ROM, MOL, NLD, BGR, SRB, MKD, UKR, and more)
Standard Ligatures | `liga` | Converts 3+ repeated hyphens into wavy lines, just for fun
Required Ligatures | `rlig` | On by default; adds pseudo-random pattern to alternates in Irregular & Bouncy styles

## Build

<details>
<summary><b><!-------->How to build the fonts locally<!--------></b> (Click to expand)</summary>

### Set up requirements

Make a virtual environment:

```bash
python3 -m venv venv
```

Activate venv:

```
source venv/bin/activate
```

Install dependencies:

```bash
pip install -U -r requirements.txt
```

Finally, give the build scripts permission to run:

```bash
chmod +x scripts--build/*.sh
```

Finally, you will also need to separately install [google/woff2](https://github.com/google/woff2) to enable the `woff2_compress` and `woff2_decompress` commands. Open a new terminal session, window, or tab to do this step.

```bash
# 👉 open a new terminal session first, then run this
git clone --recursive https://github.com/google/woff2.git
cd woff2
make clean all
```

### Building the fonts

```bash
source venv/bin/activate # activate venv if not already active
```

Clean the prior run prep:

```bash
make clean
```

Then, run the variable font build:

```bash
make vf
```

This will take the `.glyphspackage` source and create the folder `sources/build-prep` with intermediate sources required for the final font build. When the build succeeds, the variable font will open in your default font-opening application (I recommend Font Goggles).

If you want, you can also build the static fonts. Be aware: there are a lot of static fonts, so this takes some time!

```bash
make statics
```

If you want to build everything all at once, you can use `make full`. If you just want to run the build prep pipeline, you can use `make prep`.


## Release

Update the version number in `version.txt` to the desired next release number, then build fonts with the `make` workflow described above.

A zipped archive of the fonts folder is created as the final step of the `make statics` command.

Finally, go update the download links in the Shantell Sans web specimen.

</details>
