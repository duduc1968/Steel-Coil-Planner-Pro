# Foundation v8.12 – Manual Validation Correction

## Rule
In Manual Bottom mode, the application preserves the user's Bottom Port and Bottom Starboard values.

The pattern becomes INVALID only when the physical bottom tier plus wedge coverage is less than the hold width, or when the bottom row itself exceeds the hold width.

Upper row support shortages do not automatically invalidate the entire bottom/wedge arrangement. They are warnings and the renderer displays only supported upper coils.

## Auto Mode
Auto mode optimizes the bottom count according to hold width and diameter and is not invalidated by this manual coverage rule.
