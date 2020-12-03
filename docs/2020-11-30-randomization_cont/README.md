# Randomization

Basic process to update "organic" sources:

1. Duplicate now-expanded primary UFOs
2. The "organic" sources only had changes to the core A–Z & a–z, so I just copied these into the duplicated primary UFOs
3. Correct UFO names to make things conform to the prior UFO file naming

## Todo

- [ ] make `a` more differently-sized in Organic sources
- [ ] make sure `i` and `j` alts are getting `idotless` & `jdotless` alts (they don’t seem to be)
- [ ] make sure accent components shift along with base components

Maybe
- [x] look into whether the alts can be avoided for the extended character set ... people don’t need alts for symbols, do they? (maybe...) OR look into subsetting approach. - UPDATE: yes, this is looking like the most sensible approach – see **Testing simplified alt approach**, below


- Filed issue about challenges of accent placement in alts for Bouncy axis: https://github.com/googlefonts/ufo2ft/issues/437


```Python
# Useful snippet for getting space-separated glyph names from robofont, for a string of characters

# characters from Python string.printable
altsToMake = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

# get integer unicode values for string of characters from above
altsToMakeList = [ord(char) for char in altsToMake]

glyphNames = []

for g in CurrentFont():
    if g.unicodes and g.unicodes[0] in altsToMakeList:
        glyphNames.append(g.name)
        
print(" ".join(sorted(glyphNames)))
```

## Testing simplified alt approach

Due to the build issue of linking accents in alts *and* due to the large filesize of attempting this (294KB for the variable TTF), I wanted to look into making font with fewer alts.

Additionally, there are few words in any language which have multiple repeating accented characters [citation needed], so this cycling wouldn’t really do much good in almost any case, anyway.