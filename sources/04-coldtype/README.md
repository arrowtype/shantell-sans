# ColdType Animations

Uses [ColdType](https://github.com/coldtype/coldtype) to make several animations for demonstrating the variable axes of Shantell Sans.

## Basic build process (subject to change in future versions of ColdType)

Set up the project requirements as specified in the main project [README](https://github.com/arrowtype/shantell-sans/README.md).

Then, in a command line, with the venv activated, run ColdType like this:

```bash
coldtype "sources/04-coldtype/irregularity.coldtype.py"
```

This will open a little preview window. Click on that and press the **space** key to play it. Press **A** to render all of the frames, and then press **R** to render the gif.

More info on my current process at https://github.com/coldtype/coldtype/issues/118.

Some animations have multiple "versions"; Coldtype supports a special `__VERSIONS__` macro that lets you preprocess code to support multiple versions without having to write multiple animations. (Useful here for different language versions of the same animation.) To switch between versions of an animation in a running Coldtype viewer, hit **Shift+V**.

To render all of the animations, run:

```bash
python sources/04-coldtype/_package.py
```

This renders the frames of each version of all of the animations and then runs each animation’s "release" function (to create either a gif or an mp4), and then places those artifacts in the top-level `specimens/coldtype` directory (not currently tracked in git).