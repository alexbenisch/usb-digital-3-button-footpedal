# Plan — Map Foot Pedal to Key Events

## Goal

Map the 3 pedals to virtual key events (e.g. F14, F15, F16) so they can be bound to application actions system-wide.

## Approach

Write a small Python daemon that:

1. Opens `/dev/hidraw1` for reading
2. Reads 4-byte HID reports in a loop
3. Compares the current pedal bitmask to the previous one to detect press and release edges
4. Injects the corresponding key events into a `uinput` virtual device via `python-evdev`

Run it as a systemd service (similar to the existing `evremap-*.service` units).

## Steps

- [ ] **1. Confirm key targets** — decide which keys each pedal maps to (e.g. F14/F15/F16)
- [ ] **2. Write `footpedal.py`** — hidraw reader + uinput injector using `python-evdev`
- [ ] **3. Handle device path robustly** — use a udev rule to create a stable symlink (e.g. `/dev/input/footpedal`) instead of hardcoding `/dev/hidraw1`
- [ ] **4. Write udev rule** — match on `idVendor=15d8`, `idProduct=0024`, symlink and set permissions
- [ ] **5. Write systemd service** — `footpedal.service`, depend on the udev symlink being present
- [ ] **6. Test** — verify key events appear in `evtest` when pedals are pressed
- [ ] **7. Bind keys** — wire F14/F15/F16 to application actions (clipboard manager, etc.)

## Key Mapping (proposed)

| Pedal | Key |
|---|---|
| Left (`0x01`) | F14 |
| Middle (`0x02`) | F15 |
| Right (`0x04`) | F16 |

## Dependencies

- `python-evdev` (`pip install evdev` or `pacman -S python-evdev`)
- `udev` (already present)
- `systemd` (already present)

## Reference

- HID device: `0x15d8:0x0024` — Grundig Digta Foot Control 540 USB
- Existing pattern: `~/key-remapper/evremap-*.service` + `evremap-*.toml`
