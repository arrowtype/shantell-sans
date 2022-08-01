# Tracking axis tests

This could simulate the extra spacing often added in Shantell’s writing / lettering, in a way that would perhaps somewhat protect against browsers deactivating the calt feature, which can happen if users don’t specifically turn it on.

## Basic Approach

Use a FontParts script to duplicate a UFO source, then add *x* amont of margin to either side of every glyph.

Then, add that source to a designspace, and set up a tracking axis.

Later, this source preparation can be worked into the overall font build prep pipeline.

## Experimental results

Okay, so I’ve done some experiments here, and things are looking pretty good.

The key: a "tracking" axis can be added with just a single source, _if_ that source is otherwise at the default location.

Example:
- A Weight + Tracking designspace
```
<axis tag="wght" name="Weight" minimum="300" maximum="800" default="300"/>
<axis tag="TRAK" name="Tracking" minimum="0" maximum="1000" default="0"/>
```

- There is a Light source and an ExtraBold source for weight.
- If we make a Light Tracked source, we can have tracking without doubling the masters. E.g. "ExtraBold Tracked" can be arrived at by adding up the deltas from the defaults.
- If we instead try to use  only an "ExtraBold Tracked" source, we cannot get the Light Tracked result.