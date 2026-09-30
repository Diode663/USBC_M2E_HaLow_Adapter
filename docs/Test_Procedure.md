# Board test procedure — Rev A

For the USB-C to M.2 Key-E HaLow adapter as sent to JLCPCB on 2026-09-20. Work through the
stages in order and stop at the first failure: each stage assumes the one before it passed.
Fill in the record sheet at the end for every board.

## Probe points

Coordinates are millimetres from the board's top-left corner (the origin the gerbers and
placement file use), X to the right, Y down. All test pads are on the top side.

| Point | Net | Where | What it is for |
|---|---|---|---|
| **TP2** | VBUS | 1.5 mm pad at (12.0, 14.6), above the USB-C, left of TP3 | USB input voltage as it arrives |
| **TP1** | +3V3 | 1.5 mm pad at (33.0, 35.0), below the socket's pin 2/4 end | regulator output, at the socket end of the rail |
| **TP3** | GND | 1.5 mm pad at (15.5, 14.6), right of TP2 | meter ground; scope ground spring for TP2 |
| H1–H4 | GND | the four M3 hole rings | scope ground clip; H2 is the closest ground to TP1 |
| C1 top pad | VBUS | 1210 capacitor at (18.2, 2.8), the pad nearer the board edge | VBUS at the regulator input: the drop across the board is TP2 minus this |
| L1 left pad | SW | inductor at (21.3, 4.3) | switch node, scope only |
| L1 right pad | +3V3 | inductor at (27.0, 4.3) | regulator output before the trace to the socket |
| U2 top-left pin | FB | pin 4 of the SOT-23-6 at (11.8, 3.4), or R4's right pad at (10.3, 3.4) | feedback reference, 0.768 V |
| J2 pins 2, 4, 72, 74 | +3V3 | socket pads, even row (the row under the card), both ends | rail at the card |

TP1 and TP2 sit outside the card outline, so they stay reachable with the card fitted.
The 0402 and SOT-23 pads are small: use a fine probe tip and steady your hand on the board.

## Equipment

- Bench supply with adjustable current limit, and a USB-C breakout board or a cut USB-C cable
  (VBUS and GND only). A USB power meter that shows volts and amps in-line is a good substitute
  for stages 3 and 5 if you have no breakout.
- Multimeter.
- Oscilloscope, at least 50 MHz, with a ground spring for the probe.
- Electronic load, or a 2.7 Ω, 10 W resistor with leads (a 5 W part gets hot at 4 W).
- A USB-A-to-C cable and a C-to-C cable, both 3 A rated, short.
- Host computer with a USB 3 or USB-C port (a 500 mA USB 2.0 port is not enough for the card).
- Gateworks GW16170 card with its MMCX antenna or pigtail, and an M2 screw.
- Hand magnifier or USB microscope for stage 1.

## Stage 1 — visual inspection, unpowered

The placement file carried corrections that were derived from JLCPCB's footprints and not all
seen in their viewer before ordering. Check these first; a turned part fails everything after.

| Part | Check |
|---|---|
| U1 (ESD, next to the USB-C) | pin-1 dot on the silkscreen triangle, bottom-right corner |
| U2 (regulator, top-left) | pin-1 dot on the silkscreen triangle, bottom-right corner |
| J1 (USB-C) | contacts sit centred on their pads; shell stakes soldered in all four holes |
| D1 (TVS above the USB-C) | cathode band on the side nearer J1 |
| J2 (M.2 socket) | slot opening toward H5 (the standoff), both hold-down tabs soldered |
| L1 | flat on its pads, no tilt |
| H5 | nut sits flush in its hole, fillet all round |
| C1 (the tall 1210 standing on end) | not tombstoned |
| all 0402s | both ends wetted |

Also confirm the hidden designators were not populated by mistake: nothing should sit at
FID1–FID3 or on TP1–TP3.

## Stage 2 — resistance checks, unpowered

Meter on ohms, black lead on TP3.

| Red lead on | Expect | Fail if |
|---|---|---|
| TP2 (VBUS) | rises toward several kΩ as capacitors charge; no short | under 100 Ω and steady |
| TP1 (+3V3) | rises toward tens of kΩ (R3 + R4 = 43 kΩ across the rail) | under 100 Ω and steady |
| J1 CC1 and CC2 pads (A5 and B5, the outer signal pads) | 5.1 kΩ each | open, or anything but ~5.1 kΩ |
| J2 pin 3 and pin 5 (USB D+, D−, odd row) | open, over 1 MΩ | short to ground |
| each M3 hole ring | 0 Ω | open |
| H5 | 0 Ω | open |

Diode test, red on TP3, black on TP2: D1 should read as a diode, about 0.6–0.7 V. Reversed
(red on TP2) it should read open, because at meter currents the 5 V TVS does not conduct.

## Stage 3 — first power, no card

1. Bench supply to 5.00 V, current limit 0.10 A, output off. Connect it to VBUS and GND
   through the breakout. Card not fitted.
2. Output on. Supply current must be **under 10 mA** (the regulator idles at about 0.4 mA and
   the feedback divider takes 0.08 mA). If the supply goes into current limit, power off:
   there is a short, most likely at U2 or L1.
3. Measure:

| Point | Expect | Note |
|---|---|---|
| TP2 | 4.95–5.05 V | equals the supply |
| TP1 | **3.25–3.39 V** (3.32 V nominal) | 0.768 V reference ±1 %, resistors ±1 % |
| U2 pin 4 (FB) | 0.76–0.78 V | if TP1 is wrong but FB is right, the divider is wrong |
| L1 right pad | same as TP1 within 5 mV | |

4. Scope, ground spring on TP3 or H2, 20 MHz bandwidth limit, AC coupled, 20 mV/div:
   ripple on TP1. With no load the regulator pulse-skips (TI's Eco-mode), so expect an irregular
   low-frequency pattern rather than a clean 580 kHz. Record the peak-to-peak; **under 50 mV**
   is the pass line.
5. Raise the current limit to 0.5 A and repeat step 2 briefly. Current should not change.

## Stage 4 — load test, no card

This stands in for the card's transmit bursts (about 1.2 A at 3.3 V) without risking the card.

1. Supply 5.00 V, current limit 1.5 A.
2. Load between TP1 and TP3: electronic load at 1.2 A constant current, or the 2.7 Ω resistor
   (1.23 A). Keep the leads short; the load's own voltage reading is not TP1.
3. Measure within a minute of applying the load:

| Point | Expect | Fail if |
|---|---|---|
| TP1 | 3.25–3.39 V, droop from stage 3 under 50 mV | below 3.20 V |
| supply current | 0.85–1.0 A | over 1.1 A |
| TP2 minus C1 top pad | under 50 mV | over 100 mV: VBUS trace or via problem |
| TP1 ripple, scope as before | under 50 mV pk-pk at ~580 kHz | |
| L1 left pad (SW), scope DC 2 V/div, ×10 probe | 0 to 5 V square wave at 580 kHz ±15 %, no ringing above about 7 V | ringing above 10 V, or frequency far off |
| U2 and L1 by touch after two minutes | warm, touchable | too hot to touch: about 60 °C is expected, 100 °C is not |

4. Step the load from 0 to 1.2 A and back while watching TP1 on the scope, DC coupled, 100
   mV/div: a dip or overshoot of under 150 mV that settles within about 100 µs with no
   oscillation. This is the check the design review asked for after the inductor change; it is
   the one stage-4 result worth keeping a screenshot of.
5. Remove the load.

## Stage 5 — cable and host checks, no card

1. Move from the bench supply to the host computer with the **A-to-C cable**. TP2 should show
   the host's VBUS, 4.75–5.25 V. Some hosts sit low; note the value.
2. Repeat with the **C-to-C cable**. VBUS must still appear: this proves the 5.1 kΩ CC
   resistors, because a C-to-C source gives no VBUS without them.
3. Flip the plug and check TP2 again with each cable.

## Stage 6 — card fitted, idle

1. Host off or cable out. Fit the GW16170: slide it into J2 at an angle, press down, fix with
   the M2 screw into H5. Fit the antenna before powering; a HaLow module transmitting into no
   antenna can be damaged.
2. Connect the host through the USB power meter, A-to-C cable.
3. Within ten seconds the host must see a new USB device (`dmesg`, `lsusb`, or Device Manager).
   If it does not, first measure J2 pins 56 and 54 (odd row, both near the pin 74 end): both
   must read 3.3 V. Gateworks' wiki names those two pins as the reason a card fails to
   enumerate. They are pulled up on the card and left open on this board, so anything but 3.3 V
   points at the socket.
4. Record the idle current from the power meter and TP1, TP2 with the card idle. Gateworks
   publishes no current figures; whatever you measure becomes the reference for later boards.

## Stage 7 — card transmitting

1. Bring the interface up and run traffic against a second HaLow node (iperf, or the driver's
   own test mode) at the power level you will use in service.
2. During transmit:

| Point | Expect | Fail if |
|---|---|---|
| TP2, meter min-hold or scope | **at least 4.50 V** | below 4.45 V: the regulator needs 4.43 V in for 3.3 V out and its undervoltage lockout is at 4.3 V; try a shorter cable or a stronger port before blaming the board |
| TP1 | above 3.20 V throughout | |
| TP1 on the scope, DC, 100 mV/div, slow timebase | bursts visible as small dips, under 150 mV | rail collapsing during bursts |
| power meter | note the peak; about 0.9 A is the design estimate | |

3. Receive check: compare received signal strength or throughput from the far node with this
   board against a known-good host for the same card and antenna. The regulator is 25 mm from
   the radio; a noticeably worse receive figure here would mean its harmonics are getting in.
4. After ten minutes of traffic, U2 and L1 by touch: warm, not hot.

## Record sheet

Board serial: ______   Date: ______   Tester: ______   Host / cable: ______

| Stage | Measurement | Limit | Value | Pass |
|---|---|---|---|---|
| 1 | U1, U2, J1, D1, J2 orientation | as listed | | |
| 2 | VBUS to GND, +3V3 to GND | not shorted | | |
| 2 | CC1, CC2 to GND | 5.1 kΩ | | |
| 3 | idle current, no card | < 10 mA | | |
| 3 | TP2 | 4.95–5.05 V | | |
| 3 | TP1 | 3.25–3.39 V | | |
| 3 | FB | 0.76–0.78 V | | |
| 3 | TP1 ripple, no load | < 50 mV pp | | |
| 4 | TP1 at 1.2 A | > 3.20 V, droop < 50 mV | | |
| 4 | supply current at 1.2 A | < 1.1 A | | |
| 4 | TP2 − C1 at 1.2 A | < 100 mV | | |
| 4 | SW frequency | 580 kHz ±15 % | | |
| 4 | load step on TP1 | < 150 mV, no oscillation | | |
| 5 | VBUS with C-to-C cable | present | | |
| 6 | card enumerates | yes | | |
| 6 | idle current with card | record | | |
| 7 | TP2 minimum during transmit | ≥ 4.50 V | | |
| 7 | TP1 minimum during transmit | ≥ 3.20 V | | |
| 7 | peak current during transmit | record | | |
| 7 | receive figure vs reference host | comparable | | |

Rev A result: the first boards worked as designed (2026-09-29). The README status and the
placement corrections in `jlc_rotations.json` were updated to say so.

## Where the limits come from

- 3.32 V nominal and the FB voltage: TI TPS563201 datasheet, 0.768 V reference, R3/R4 33.2k/10k.
- 4.43 V minimum input and 4.3 V undervoltage lockout: TI, section 9 and the electrical table.
- 580 kHz and the pulse-skipping at light load: TI, sections 7.4.1 and 7.4.2.
- About 0.9 A from VBUS and 1.2 A at 3.3 V: estimate for the GW16170 at full power; Gateworks
  publishes none, which is why stages 6 and 7 record rather than judge those numbers.
- Enumeration and pins 54/56: Gateworks GW16167/GW16170 wiki.
- Ripple, droop and load-step limits are engineering judgement for a rail feeding a radio, not
  datasheet figures.
