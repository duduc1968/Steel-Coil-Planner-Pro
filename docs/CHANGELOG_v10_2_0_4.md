# Steel Coil Planner Pro v10.2.0.4

## Manual cargo zones only

- Optimize Preview changes only the selected zone.
- Validate Zone no longer creates additional cargo zones.
- Changing Upper Port / Upper Starboard rebuilds only the selected zone.
- Remaining coils stay in Remaining Cargo until the Master manually creates
  or selects another zone.
- Automatic `Remaining Cargo` zones created by v10.2.0.3 are removed during
  startup; manually created zones and their reservations are preserved.

The variable complete-row rule from v10.2.0.3 remains active.
