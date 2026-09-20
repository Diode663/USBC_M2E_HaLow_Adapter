# USB-C to M.2 Key-E HaLow adapter

USB 2.0 over a USB-C receptacle to an M.2 2230 Key-E socket, for the Gateworks
GW16170 (Morse Micro MM8108-M20) Wi-Fi HaLow card. 56.5 x 40.5 mm, 2-layer (JLCPCB JLC0216A),
single-sided assembly.

| Block | Parts |
|---|---|
| USB-C input | J1 HRO TYPE-C-31-M-12, R1/R2 5.1k CC pull-downs, U1 USBLC6-2SC6, D1 SMF5.0A |
| 3.3 V / 3 A buck | U2 TPS563201, L1 2.2 uH, C1/C2 in, C4/C5 out, R3/R4 33.2k/10k = 3.32 V |
| M.2 socket | J2 MLD-NGFF-E-4.2H, C6 100 uF, C7 10 uF, C8/C9 100 nF |
| Mechanical | H1-H4 M3, H5 SMTSOM225BTR (LCSC C5301773) M2 x 2.5 mm SMT nut for the card |

Everything is generated. Edit the scripts, not the KiCad files. Run with KiCad's Python:

    "C:\Program Files\KiCad\10.0\bin\python.exe" generate_schematic.py --force
    "C:\Program Files\KiCad\10.0\bin\python.exe" autoplace.py . --floorplan
    "C:\Program Files\KiCad\10.0\bin\python.exe" autoplace.py . --place --force
    "C:\Program Files\KiCad\10.0\bin\python.exe" setup_fab.py

`--place` resets every unlocked footprint. Lock hand-tuned parts in KiCad first.

Mechanical facts, from the MLD-NGFF-E-4.2H drawing:
- the card extends from the even-pin / locating-peg side of the socket;
- the card stop is 1.75 mm behind the pegs, so the 2230 notch is 29.75 mm from the socket centre;
- card underside is 2.52 mm above the board; parts under it must be 0.90 mm or lower.

3D models: J1 is the vendor model from LCSC (C165948). LCSC has no model for the
MLD socket, so `build_models.py` builds its housing and a translucent 2230 card
envelope from the MLD drawing. `check_m2_clearance.py` measures every part against
both and must end in `RESULT: all clear`.

JLCPCB turnkey: `setup_fab.py` writes JLCPCB's 2-layer rules into the project and into
`USBC_M2E_HaLow_Adapter.kicad_dru` (loaded by KiCad automatically), with the source pages and
the date in its docstring. USB pair: 0.3345 / 0.1524 mm with ground pour 0.2032 mm either side,
from JLCPCB's own calculator. JLCPCB does not test impedance on 2-layer boards.

Routed by `route_board.py` (it redraws every track, via and pour; its docstring explains the
plan). Order after a schematic change: generate_schematic, autoplace --place --force, setup_fab,
route_board, drc_report. Editing tracks by hand in KiCad is fine, but route_board.py will
replace them the next time it runs.

Fabrication package: `build_package.py` writes `fab/` (gerbers zip, BOM, placement file, order
notes) and refuses to run unless DRC is clean. Design review: `docs/Design_Review_2026-09-20.md`. Routing notes for the 2-layer
board (USB pair geometry, ground plane, buck output return) are at the top of
`setup_fab.py`.

## Repository contents
- `USBC_M2E_HaLow_Adapter.kicad_*`: the KiCad 10 project, schematic, routed board and custom design rules.
- `fab/`: the package sent to JLCPCB for Rev A (gerbers zip, BOM, placement file, order notes).
- `docs/`: schematic PDF, renders, copper images and the pre-fabrication design review.
- `library/`: project symbols, footprints and 3D models. The M.2 socket and card models are envelopes built from the socket drawing.
- `*.py`: the generators. `schlib.py`, `subcircuits.py`, `pcblib.py`, `autoplace.py`, `recipes.py` and `jlc_cpl.py` are copies of the libraries they were generated with.
- Vendor datasheets are not included. Part numbers and LCSC numbers are in `fab/*_bom.csv`.

Status: Rev A was sent for fabrication on 2026-09-20. The boards have not been tested yet; the bring-up checks are listed in `fab/ORDER_NOTES.txt`.
