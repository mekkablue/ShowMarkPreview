# ShowMarkPreview

*View > Show Mark Preview* is a [Glyphs.app](https://glyphsapp.com/) plug-in for previewing mark-to-base and mark-to-mark attachment directly in Edit view.

![ShowMarkPreview](ShowMarkPreview.png)

*Sample font shown: Lao Pali by Ben Mitchell (@ohbendy).*

### Installation

Please install the plugin via the built-in Plugin Manager, available via *Window > Plugin Manager,* and restart the application.

### Usage Instructions

1. Activate *View > Show Mark Preview.*
2. Open an Edit tab with any number of letters and marks containing appropriate mark attachment anchors (e.g., `top` and `_top`, respectively).

The marks will be stacked onto all letters in the Edit tab, provided they have respective anchors.

### Custom Colors

You can set font-specific custom colors with parameters in *File > Font Info > Custom Parameters.* Add these parameters *properties:*

* `MarkPreviewColor`: color for the marks in the currently active glyph in Edit view, defaults: `0.8, 0.0, 1.0, 0.5`
* `MarkPreviewColorInactive`: color for the marks in all other (inactive) glyphs in Edit view, defaults: `0.45, 0.15, 0.6, 0.6`

As values, take comma-separated values between 0.0 and 1.0 for R, G, B, and A. If you only want to override one of these values, simply add invalid values (e.g., `x`) for the ones you want to keep, or leave out trailing values you do not want to change. E.g., `x, 0.3`  will only change the G value to 30%, and leave R, B and A at their defaults.

### Known Problems

* Unfortunately, I cannot disable the default mark cloud under all circumstances (yet).
* Typing new sidebearings in the grey glyph info box (*View > Show Glyph Info*) does not work when *View > Show Mark Preview* is on, at least in 2.5b (1072).

### License

Copyright 2017 Rainer Erich Scheichelbauer (@mekkablue). Based on sample code by Georg Seifert (@schriftgestalt) and Jan Gerner (@yanone).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
