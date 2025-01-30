# ShowMarkPreview

*View > Show Mark Preview* is a [Glyphs.app](https://glyphsapp.com/) plug-in for previewing mark-to-base and mark-to-mark attachment directly in Edit view.

![Show Mark Preview in action, showing Ben Mitchell’s font ‘Monkey’ with Thai and Burmese glyphs, with custom colors set in Font Info.](ShowMarkPreview.png)

*Sample font shown: ‘Monkey’ by Ben Mitchell (@ohbendy), showing Thai and Burmese glyphs, with custom colors set in Font Info.*

### Installation

Please install the plugin via the built-in Plugin Manager, available via *Window > Plugin Manager,* and restart the application.

### Usage Instructions

1. Activate *View > Show Mark Preview.*
2. Open an Edit tab with any number of letters and marks containing appropriate mark attachment anchors (e.g., `top` and `_top`, respectively).

The marks will be stacked onto all letters in the Edit tab, provided they have respective anchors.

You can also do the opposite: have _base letters_ shown while editing _marks._ To activate this, paste the following line in _Window > Macro Window,_ and press _Run:_

```python
Glyphs.defaults["com.mekkablue.ShowMarkPreview.previewBaseInMarks"] = True
```

To reset to the old behavior, either replace `True` with `False`, or delete the setting like this:

```python
del Glyphs.defaults["com.mekkablue.ShowMarkPreview.previewBaseInMarks"]
```

### Custom mkmk extension

If you are using special anchors to separate `mkmk` from `mark` positioning, you can define an anchor name extension by running the following command in *Window > Macro Panel:*

```python
Glyphs.defaults["com.mekkablue.ShowMarkPreview.extension"] = "_MKMK"
```

Then the plug-in will prefer anchors with an `_MKMK` suffix for mark-to-mark positioning, e.g. `_top_MKMK` and `top_MKMK`. To reset to defaults again, run this command in Macro Window:

```python
del Glyphs.defaults["com.mekkablue.ShowMarkPreview.extension"]
```

The setting is also available in the mekkablue script *App > Set Hidden App Preferences.*

### Custom Colors

You can set font-specific custom colors with parameters in *File > Font Info > Custom Parameters.* Add these parameters *properties:*

* `MarkPreviewColor`: color for the marks in the currently active glyph in Edit view, defaults: `0.3, 0.0, 0.6, 0.4` (Light Mode), `0.8, 0.0, 1.0, 0.5` (Dark Mode).
* `MarkPreviewColorInactive`: color for the marks in all other (inactive) glyphs in Edit view, defaults: `0.15, 0.05, 0.3, 0.5` (Light Mode), `0.45, 0.15, 0.6, 0.6` (Dark Mode).

As values, take comma-separated values between 0.0 and 1.0 for R, G, B, and A. If you only want to override one of these values, simply add invalid values (e.g., `x`) for the ones you want to keep, or leave out trailing values you do not want to change. E.g., `x, 0.3`  will only change the G value to 30%, and leave R, B and A at their defaults.

### Known Problems

* Unfortunately, I cannot disable the default mark cloud under all circumstances (yet).
* Typing new sidebearings in the grey glyph info box (*View > Show Glyph Info*) does not work when *View > Show Mark Preview* is on, at least in 2.5b (1072).

### License

Copyright 2017 Rainer Erich Scheichelbauer (@mekkablue). Based on sample code by the Glyphs team.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
