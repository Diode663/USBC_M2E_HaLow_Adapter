# USB-C to M.2 Key-E HaLow Adapter — Design Review

**Project:** USBC_M2E_HaLow_Adapter (KiCad 10, single sheet, 2-layer PCB 56.5 x 40.5 mm, JLCPCB turnkey)
**Date:** 2026-09-20
**Analyzers run:** analyze_schematic.py, analyze_pcb.py `--full --proximity`, cross_analysis.py, analyze_emc.py, analyze_thermal.py, lifecycle_audit.py (LCSC only), KiCad DRC with schematic parity, project `check_m2_clearance.py`, deep review pass with the citation gate.
**Run folder:** `analysis/2026-09-20_1330/`, deep review in `analysis/deep_review.json`, numbers from `analysis/helpers/buck_usb_checks.py`.

## Overview
USB 2.0 over a USB-C receptacle (J1) to an M.2 2230 Key-E socket (J2) for a Gateworks GW16170 HaLow card. A TPS563201 buck (U2) makes 3.3 V from VBUS. ESD array U1 on D+/D-, TVS D1 on VBUS, 5.1k sink resistors on CC1/CC2. 24 parts, 10 routed nets, everything on the top side, solid ground pour on both layers.

No prior review or analyzer runs existed, so there is no delta section.

## Critical Findings

| Severity | Issue | Section |
|---|---|---|
| WARNING | +3V3 output capacitance (154 uF nominal, ~87 uF effective) is above TI's 20-68 uF range with L1 at its 4.7 uH maximum. LC pole 5.9-7.9 kHz vs TI's 8.9-24 kHz envelope. | Power |
| WARNING | A ground stitching via sits inside J2's hold-down tab pad 76. Solder will wick down it and weaken a mechanical joint. | Layout |
| WARNING | The ground via under U1 is 0.5/0.3 mm: 0.10 mm annular ring, below IPC Class 2 (0.125 mm). JLCPCB can build it; a 0.6/0.3 via fits. | Layout |

No CRITICAL issues. Nothing found that would stop the board from working.

## Component Summary
Capacitors 9, resistors 4, inductor 1, TVS 1, ICs 2, connectors 2, mounting parts 5. 63 nets (53 are single-pin no-connect nets on J2), 3 rails. MPN coverage 100 % of BOM parts. Two BOM lines have no manufacturer recorded: D1 (C19077497) and H5 (C5301773).

## Power Tree
```
USB-C VBUS 5 V --D1 SMF5.0A clamp-- C1 10uF + C2 100nF
   |
   U2 TPS563201 buck, 580 kHz, EN tied to VIN
   |   R3 33.2k / R4 10k -> 0.768 x 4.32 = 3.318 V   (Vref from datasheet)
   |   L1 4.7 uH, C4 + C5 22 uF at the inductor
   +3V3 --> J2 pins 2/4/72/74, C6 100 uF + C7 10 uF + C8/C9 100 nF at the socket
```
Load: GW16170, about 1.2 A at 3.3 V in transmit bursts (estimate; Gateworks publishes no figure), about 0.9 A from VBUS.

## Analyzer Verification (raw file and datasheet)
- Component count: 24 in schematic, 24 footprints on the board. DRC schematic parity 0. **Raw-file verified.**
- U2 pad nets 1 GND, 2 SW, 3 VBUS, 4 FB, 5 VBUS, 6 VBST match TI's pin table (p.3). **Datasheet-verified.**
- U1 pad nets 1/6 D-, 3/4 D+, 2 GND, 5 open match ST Figure 1. **Datasheet-verified.**
- J2 pad numbering, odd/even row positions, locating pegs and card direction match the MLD drawing; USB on pins 3/5 and 3.3 V on 2/4/72/74 match Gateworks' wiki. **Datasheet-verified.**
- D1 cathode (pad 1) on VBUS. **Raw-file verified**; no datasheet for this exact LCSC part.
- J1: KiCad's stock footprint and symbol for this exact MPN, LCSC C165948 as ordered before. **Library-consistent, not re-derived from the HRO datasheet.**
- Regulator Vout: analyzer 3.283 V (heuristic Vref), hand calculation with TI's 0.768 V: 3.318 V. Use 3.32 V.

## Deep Review
Seven findings passed the citation gate (all marked partial because no structured datasheet extractions exist; quotes are from the PDFs). One was quarantined for lack of a datasheet (D1) and is reported below as inference only.

## Signal Analysis — USB 2.0
- Coupled section uses JLCPCB's calculated geometry (0.3345 / 0.1524 mm, ground 0.2032 mm either side) over unbroken bottom ground. JLCPCB does not test impedance on 2-layer boards.
- From J1 through U1 (about 9 mm) D+ and D- run uncoupled, 1.9 mm apart at U1, because the part is flow-through. That section is well above 90 ohm differential. At 9 mm (about 60 ps) against a 500 ps USB 2.0 edge this is acceptable. **Inference-only.**
- Skew about 3 mm, 20 ps, against a 100 ps budget. Each line has one 1.3 mm bottom strap plus two vias as a side branch for the flip pads, not in the main path.
- No series resistors or common-mode choke. Fine for a bus-powered adapter; a choke is the usual fix if radiated emissions from the cable ever matter.

## Power Analysis
- **Output capacitance vs TI Table 2 (WARNING).** TI: "use the values recommended in Table 2": 3.3 V, L 2.2 typ / 4.7 max uH, Cout 20 to 68 uF. The socket's 100 uF sits on the same node through 11 mOhm of trace, so it counts. Effective capacitance uses typical X5R bias curves, not the capacitor datasheets. **Datasheet-verified limit, inference on the effective value.** Fix: L1 to 2.2 uH (same CYA0630 footprint; pole moves to 8.6-11.5 kHz, ripple 0.87 A pk-pk, peak 1.64 A, still far below the 3.3 A valley limit) and optionally C6 to 47 uF.
- **VBUS headroom (INFO).** TI's 75 % duty limit means VIN of at least 4.43 V for 3.3 V out; UVLO wake-up is 4.3 V max. Only 10 uF is allowed on VBUS. A long or thin cable can sag below that during transmit. Measure VBUS at C1 on the first board.
- C1 + C2 = 10.1 uF nominal on VBUS, at the USB limit of 10 uF; effective value under 5 V bias is lower. Acceptable.
- Current paths: VBUS trunk 0.8 mm bottom, +3V3 1.2 mm top, SW 1.2 mm bottom with two vias at each end. One 0.8/0.4 via carries all VBUS current at D1 (0.9 A): within rating, a second via is cheap.
- M.2 3.3 V pins: four at 0.5 A each, 2 A capacity for a 1.2 A load.

## PCB Layout
- DRC: 0 errors, 0 unconnected, parity 0. 51 silkscreen warnings, 49 of them inside stock KiCad footprints (silk 0.10-0.13 mm from their own pads; JLCPCB clips silk at pads).
- M.2 mechanical check: all clear. L1 2.90 mm from the socket housing, 0402s under the card 0.50 mm tall against a 0.90 mm limit, standoff on the notch at 2.50 mm.
- **Via in J2 pad 76 (WARNING):** stitching via at (19.4, 32.4) lands in the hold-down tab. Move it 1 mm south.
- **Under-U1 via ring (WARNING):** change to 0.6/0.3; clearance to U1's pads becomes 0.18 mm against a 0.15 mm rule.
- Buck follows TI Figure 36 with one known deviation (output caps return through pour and plane, not a shared top island). Solid pour connections on all buck ground pads.
- Tombstoning: analyzer rates six 0402s "medium". C2's ground pad is solid into the pour by choice (input loop); the rest have thermal spokes. Accepted.

## Thermal
analyze_thermal.py produced no assessments (no dissipation data in the schematic). Hand estimate: 0.38 W in U2 at 1.2 A, 92.6 C/W, about 35 C rise. Efficiency is assumed at 90 %, not read from TI's curves. No concern. The radio card's own heat is outside this board.

## EMC / Cross-Domain
- SW-001 harmonics of 580 kHz in the 30-88 MHz band: generic to any buck. SW is 24 mm of copper, 18 mm of it on the bottom under the buck. Inductor is shielded (metal composite).
- The HaLow radio listens at 902-928 MHz, 25 mm from the buck. Harmonic energy that high is small, but the receiver is sensitive. **Inference-only:** check receive sensitivity with the buck loaded on the first board.

## Component Lifecycle
LCSC returns no lifecycle status, so all 14 MPNs read "unknown". No distributor API keys are configured. **Not verified.** TPS563201, USBLC6-2SC6 and the Samsung/Murata capacitors are mainstream active parts to my knowledge.

## Manufacturing / DFM / Testability
- JLCPCB Economic PCBA limits met (2-layer, single side, 0402 minimum, 0.5 mm pitch). Not confirmed: whether J1 (overhangs the edge 0.5 mm) and J2 are allowed in Economic assembly.
- No fiducials (analyzer FD-001 "error"). JLCPCB Economic does not require them. Three 1 mm fiducials cost nothing and help with the 0.5 mm pitch socket. **Suggestion.**
- No test points. Suggest pads on +3V3, VBUS and GND, and optionally J2 pin 56 (card reset).
- Silkscreen has no board name, revision or date.
- CPL: five rotations unverified (D1, J1, J2, U1, U2). Check in JLCPCB's preview.
- BOM: add manufacturers for D1 and H5.

## False Positives / Reviewer Overrides
- UC-002 "no TVS on VBUS": D1 is the VBUS TVS; the analyzer does not recognise the Zener symbol.
- EMC DC-002 "no decoupling near U1": U1 is a passive ESD array with its supply pin open by design.
- EMC EF-001 / LC-DET "EMI filter at 232 kHz": that is L1 with the bootstrap capacitor, not a filter.
- EMC RP-001 "missing stitching via at layer transition" on USB: the transitions are the 1.3 mm flip-pad branches, not the signal path. Downgraded to info.
- RP-002 / PS-002 "SW crosses VBUS plane gap, VBUS split into 5 islands": VBUS is routed as tracks, not a plane.
- VP-001 says "untented": board setup tents vias on both sides. The via-in-pad part of the finding is real.
- CC-DET "+3V3 0.2 mm min trace": that is the feedback sense line, which carries no load current.
- Pin 56/54 pull-ups: reviewed separately; must stay open (Morse Micro reset RC).

## Not Performed / Review Limits
- SPICE: no simulator installed (ngspice, LTspice, Xyce all absent).
- Gerber analysis: no fabrication outputs exist yet.
- Lifecycle: no usable data (see above).
- Structured datasheet extraction: none; PDFs read directly. No datasheets on hand for D1, H5, the 0402/0603 capacitors or the 5.1k resistors.
- GW16170 current draw is an estimate; Gateworks publishes none.
- Capacitor DC-bias figures are typical-curve estimates.

## Verdict
**Ready for fabrication after three small fixes:** move the via out of J2 pad 76, enlarge the under-U1 via to 0.6/0.3, and change L1 to 2.2 uH (or accept the stability risk knowingly and check load-step response). Everything else is optional polish: second VBUS via, fiducials, test points, silkscreen ID, BOM manufacturers.

## Post-Review Changes (2026-09-20, same day)
All three warnings and the optional items were applied, then every check was re-run.

| Item | Change | Result |
|---|---|---|
| Output filter | L1 4.7 uH -> 2.2 uH, CYA0630-2.2UH, LCSC C5189746 (7 A / 10 A, 15.5 mOhm), same footprint | LC pole 8.6-11.5 kHz; effective Cout (~87 uF est.) is still above TI's 68 uF. Ripple 0.87 A pk-pk, 1.64 A peak. |
| Via in J2 pad 76 | stitching via moved 1.3 mm south, clear of the hold-down tab | analyzer VP-001 gone |
| Under-U1 ground via | 0.5/0.3 -> 0.6/0.3 mm | DFM-001 / DFM-002 gone |
| VBUS at D1 | second 0.8/0.4 via | two vias share 0.9 A |
| Fiducials | FID1-FID3, 1 mm, asymmetric triangle | FD-001 gone |
| Test pads | TP1 +3V3, TP2 VBUS, TP3 GND, 1.5 mm, outside the card outline | reachable with the card fitted |
| Silkscreen | "HaLow USB-M.2E  Rev A  2026-09" | 1.0 mm / 0.15 mm, JLCPCB legend minimum |
| BOM | D1 manufacturer R+O, H5 manufacturer YIYUAN | complete |

Re-check: KiCad DRC 0 errors / 0 unconnected / parity 0; M.2 clearance all clear; schematic netlist
matches the spec, ERC 0; PCB analyzer has no errors and one warning left (test-point coverage metric);
gerber analysis of `fab/gerbers/`: 9 layers + 2 drill files, complete, aligned, 56.5 x 40.5 mm, no findings.
Still open and not fixable on paper: JLCPCB Economic vs Standard assembly for J1/J2, five CPL
rotations to confirm in JLCPCB's preview, and the bring-up measurements listed in `fab/ORDER_NOTES.txt`.

