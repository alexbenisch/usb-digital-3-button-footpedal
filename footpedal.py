#!/usr/bin/env python3
"""
Grundig Digta Foot Control 540 USB → key event daemon.

Reads 4-byte HID reports from /dev/hidraw1 and injects key events
via uinput. Each bit in the first byte represents one pedal:
  0x01 = left
  0x02 = middle
  0x04 = forward (right)
"""

import sys
from pathlib import Path
from evdev import UInput, ecodes as e

DEVICE = Path('/dev/input/footpedal')  # udev symlink; fallback to hidraw1
HIDRAW = Path('/dev/hidraw1')

PEDAL_LEFT    = 0x01
PEDAL_MIDDLE  = 0x02
PEDAL_FORWARD = 0x04

# Map each pedal to a list of keys to hold while pressed
MAPPING = {
    PEDAL_FORWARD: [e.KEY_LEFTMETA, e.KEY_O],
}

CAPABILITIES = {e.EV_KEY: [e.KEY_LEFTMETA, e.KEY_O]}


def run(device_path: Path):
    ui = UInput(CAPABILITIES, name='footpedal', version=0x1)
    prev = 0

    with open(device_path, 'rb') as f:
        while True:
            report = f.read(4)
            if len(report) < 4:
                break
            state = report[0]

            for pedal, keys in MAPPING.items():
                pressed  =     (state & pedal) and not (prev & pedal)
                released = not (state & pedal) and     (prev & pedal)

                if pressed:
                    for key in keys:
                        ui.write(e.EV_KEY, key, 1)
                    ui.syn()

                if released:
                    for key in reversed(keys):
                        ui.write(e.EV_KEY, key, 0)
                    ui.syn()

            prev = state

    ui.close()


if __name__ == '__main__':
    path = DEVICE if DEVICE.exists() else HIDRAW
    if not path.exists():
        print(f'error: device not found ({DEVICE} or {HIDRAW})', file=sys.stderr)
        sys.exit(1)
    print(f'listening on {path}', flush=True)
    run(path)
