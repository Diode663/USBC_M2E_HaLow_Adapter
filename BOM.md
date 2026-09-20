# Bill of materials — Rev A

Machine-readable copy, exactly as uploaded to JLCPCB: [`fab/USBC_M2E_HaLow_Adapter_bom.csv`](fab/USBC_M2E_HaLow_Adapter_bom.csv).
Placement file: [`fab/USBC_M2E_HaLow_Adapter_cpl.csv`](fab/USBC_M2E_HaLow_Adapter_cpl.csv).

## Assembled by JLCPCB (15 lines, 20 parts, all top side)

| Ref | Qty | Value | Part number | Manufacturer | Package | LCSC |
|---|---|---|---|---|---|---|
| U2 | 1 | 3 A synchronous buck, 3.3 V rail | TPS563201DDCR | Texas Instruments | SOT-23-6 | C116592 |
| U1 | 1 | USB 2.0 ESD array | USBLC6-2SC6 | STMicroelectronics | SOT-23-6 | C7519 |
| D1 | 1 | 5 V TVS on VBUS | SMF5.0A | R+O | SOD-123FL | C19077497 |
| L1 | 1 | 2.2 µH, 7 A / 10 A sat, 15.5 mΩ | CYA0630-2.2UH | SHOU HAN | 7.2 x 6.6 x 3.0 mm | C5189746 |
| J1 | 1 | USB-C receptacle, USB 2.0, 16 pin | TYPE-C-31-M-12 | HRO (Korean Hroparts) | SMD, right angle | C165948 |
| J2 | 1 | M.2 Key-E socket, 4.2 mm high | MLD-NGFF-E-4.2H | MLD (Minlenda) | SMD, 67 pin | C52766479 |
| H5 | 1 | M2 x 2.5 mm SMT nut, card standoff | SMTSOM225BTR | YIYUAN | 5.6 mm body, 3.7 mm hole | C5301773 |
| C1 | 1 | 10 µF 25 V X7R | GRM32DR71E106KA12L | Murata | 1210 | C77100 |
| C6 | 1 | 100 µF 6.3 V X5R | CL31A107MQHNNNE | Samsung Electro-Mechanics | 1206 | C15008 |
| C4, C5 | 2 | 22 µF 25 V X5R | CL21A226MAQNNNE | Samsung Electro-Mechanics | 0805 | C45783 |
| C7 | 1 | 10 µF 10 V X5R | CL10A106KP8NNNC | Samsung Electro-Mechanics | 0603 | C19702 |
| C2, C3, C8, C9 | 4 | 100 nF 16 V X7R | CL05B104KO5NNNC | Samsung Electro-Mechanics | 0402 | C1525 |
| R1, R2 | 2 | 5.1 kΩ 1 % | 0402WGF5101TCE | Uniroyal | 0402 | C25905 |
| R3 | 1 | 33.2 kΩ 1 % | FRC0402F3322TS | Uniroyal | 0402 | C2930001 |
| R4 | 1 | 10 kΩ 1 % | 0402WGF1002TCE | Uniroyal | 0402 | C25744 |

Notes
- J1, J2 and H5 are listed by JLCPCB as "SMT Assembly, PCBA Type: Economic and Standard" (checked 2026-09-20). All three, and most of the ICs, are Extended-library parts.
- The CSV sent to JLCPCB names the Samsung capacitors' manufacturer as "CCTC". JLCPCB matches on the LCSC number, so the order is unaffected; the table above has the correct maker.
- L1 is 2.2 µH on purpose: TI's table for the TPS563201 gives 2.2 µH typical at 3.3 V, and with the socket's bulk capacitor on the same rail it keeps the output filter inside TI's range. See `docs/Design_Review_2026-09-20.md`.

## On the board but not populated

| Ref | What | Footprint |
|---|---|---|
| H1–H4 | M3 mounting holes, plated and grounded | 3.2 mm hole, 6.4 mm pad |
| FID1–FID3 | 1 mm fiducials | — |
| TP1, TP2, TP3 | 1.5 mm test pads: +3V3, VBUS, GND | — |

## You supply

| Qty | Item | Notes |
|---|---|---|
| 1 | Gateworks GW16170 Wi-Fi HaLow card | M.2 2230 Key-E, USB 2.0 on pins 3/5, 3.3 V only. The GW16167 has the same pinout. The GW16159 is SDIO-only and will not work. |
| 1 | M2 x 3 mm or 4 mm pan-head screw | Holds the card to H5. |
| 1 | MMCX antenna or MMCX pigtail | The antenna connector is on the card, not on this board. 902–928 MHz. |
| 1 | USB-C cable rated 3 A, short | The card can pull about 0.9 A from VBUS in transmit bursts (estimate). Use a USB 3 / USB-C host port or a powered hub, not a 500 mA USB 2.0 port. |
| 4 | M3 screws and standoffs | Optional, for mounting. |
