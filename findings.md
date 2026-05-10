# USB Digital 3-Button Foot Pedal — Findings

## Device

**Grundig Business Systems GmbH — Digta Foot Control 540 USB**

| Property | Value |
|---|---|
| Vendor ID | `0x15d8` |
| Product ID | `0x0024` |
| Serial | `0402762` |
| USB speed | 12.0 Mb/s (Full Speed) |
| HID driver | `hid-generic` |
| HID phys | `usb-0000:00:14.0-6.1.2/input0` |
| hidraw node | `/dev/hidraw1` |

## Problem

The device is recognized at the USB level and bound to the `hid-generic` driver, but does **not** expose a standard input event device (`/dev/input/eventX`). It only exposes a raw HID interface at `/dev/hidraw1`, so it produces no key events out of the box.

## HID Report Format

Reports are **4 bytes**. The first byte is a bitmask of pedal state; bytes 2–4 are unused (always `0x00`).

| First byte | Pedal |
|---|---|
| `0x00` | All released |
| `0x01` | Left pedal |
| `0x02` | Middle pedal |
| `0x04` | Right pedal |
| `0x03` | Left + Middle simultaneously |

### Raw capture (`sudo cat /dev/hidraw1 | xxd`)

```
00000000: 0200 0000 0200 0000 0200 0000 0400 0000  ................
00000010: 0400 0000 0100 0000 0100 0000 0100 0000  ................
00000020: 0400 0000 0400 0000 0200 0000 0200 0000  ................
00000030: 0400 0000 0200 0300 0200 0000 0100 0000  ................
00000040: 0100 0000 0200 0000 0200 0000 0200 0000  ................
```
