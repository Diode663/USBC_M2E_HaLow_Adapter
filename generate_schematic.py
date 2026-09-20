#!/usr/bin/env python3
"""USB-C (USB 2.0) to M.2 Key-E carrier for the Gateworks GW16170 HaLow card.

The .kicad_sch is GENERATED -- edit this script, then run it with KiCad's Python:

    "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" generate_schematic.py [--force]

Spec first (PARTS / NETS / NO_CONNECT), drawing second, then KiCad's own
netlist proves the drawing matches the spec.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from schlib import Design, snap                     # noqa: E402
from subcircuits import Refs, Spec, UsbCSink, passive  # noqa: E402

NAME = "USBC_M2E_HaLow_Adapter"
LIB = "HaLowAdapter"

# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------
refs, spec = Refs(), Spec()
# U1 pin 5 (VBUS) is left open: it sits between D+ and D- in a flow-through layout,
# so on two layers the only way to reach it is a bottom trace that slots the ground
# plane under the data lines. The array clamps through its internal TVS either way;
# VBUS has its own clamp, D1.
usb = spec.add(UsbCSink(refs, vbus="VBUS", dp="USB_D_P", dm="USB_D_N", esd_vbus=False,
                        title="USB-C INPUT, ESD & VBUS CLAMP (J1/U1/D1)"))
J1, U1 = usb.j, usb.esd
# LCSC numbers below come from the owner's ordered CM4 OpenMANET BOM
p = usb.parts
# project copy of the stock footprint: it carries the vendor 3D model
p[J1] = p[J1][:2] + (f"{LIB}:USB_C_Receptacle_HRO_TYPE-C-31-M-12", "C165948", "HRO", "TYPE-C-31-M-12")
p[U1] = p[U1][:3] + ("C7519", "STMicroelectronics", "USBLC6-2SC6")
spec.PARTS.update(p)


def add(ref, tup):
    refs.reserve(ref)
    spec.PARTS[ref] = tup
    return ref


D1 = add("D1", ("Device:D_Zener", "SMF5.0A", "Diode_SMD:D_SOD-123F", "C19077497", "R+O", "SMF5.0A"))
U2 = add("U2", ("Regulator_Switching:TPS563201", "TPS563201DDCR", "Package_TO_SOT_SMD:SOT-23-6",
                "C116592", "Texas Instruments", "TPS563201DDCR"))
# 2.2 uH, not 4.7: TI Table 2 gives 2.2 uH typical for 3.3 V and 20-68 uF of output
# capacitance. This rail carries ~87 uF effective (154 uF nominal) with the socket's bulk
# cap, and 2.2 uH keeps the LC double pole (8.6-11.5 kHz) inside TI's envelope.
L1 = add("L1", ("Device:L", "2.2uH", f"{LIB}:IND-SMD_L7.2-W6.6_GPSR07X0", "C5189746", "SHOU HAN",
                "CYA0630-2.2UH"))
C1 = add("C1", ("Device:C", "10uF/25V", "Capacitor_SMD:C_1210_3225Metric", "C77100", "Murata",
                "GRM32DR71E106KA12L"))
C2 = add("C2", passive("C", "100nF"))
C3 = add("C3", passive("C", "100nF"))
C4 = add("C4", passive("C", "22uF"))
C5 = add("C5", passive("C", "22uF"))
R3 = add("R3", ("Device:R", "33.2k", "Resistor_SMD:R_0402_1005Metric", "C2930001", "Uniroyal",
                "FRC0402F3322TS"))
R4 = add("R4", passive("R", "10k"))
J2 = add("J2", (f"{LIB}:M2_Socket_E_MLD-NGFF-E-4.2H", "M.2 Key-E (GW16170)",
                f"{LIB}:CONN-SMD_MLD-NGFF-E-4.2H", "C52766479", "MLD", "MLD-NGFF-E-4.2H"))
C6 = add("C6", ("Device:C", "100uF", "Capacitor_SMD:C_1206_3216Metric", "C15008", "Samsung",
                "CL31A107MQHNNNE"))
C7 = add("C7", passive("C", "10uF"))
C8 = add("C8", passive("C", "100nF"))
C9 = add("C9", passive("C", "100nF"))
M3 = ("Mechanical:MountingHole_Pad", "M3", "MountingHole:MountingHole_3.2mm_M3_Pad_Via", "", "", "")
HOLES = [add(f"H{i}", M3) for i in range(1, 5)]
# 2.5 mm: the MLD drawing puts the card centre 2.92 mm above the board and the
# card is 0.8 mm thick, so its underside sits at 2.52 mm
H5 = add("H5", ("Mechanical:MountingHole_Pad", "M2 standoff H2.5",
                f"{LIB}:SMTSO_M2_H2.5_SMTSOM225BTR", "C5301773", "YIYUAN", "SMTSOM225BTR"))
FIDS = [add(f"FID{i}", ("Mechanical:Fiducial", "Fiducial", "Fiducial:Fiducial_1mm_Mask2mm", "", "", ""))
        for i in range(1, 4)]
TPS = {add(f"TP{i}", ("Connector:TestPoint", net, "TestPoint:TestPoint_Pad_D1.5mm", "", "", "")): net
       for i, net in enumerate(("+3V3", "VBUS", "GND"), 1)}

M2_GND = ["1", "7", "18", "33", "39", "45", "51", "57", "63", "69", "75"]
M2_3V3 = ["2", "4", "72", "74"]
M2_USED = set(M2_GND + M2_3V3 + ["3", "5", "76", "77"])
M2_ALL = [str(n) for n in range(1, 78) if not 24 <= n <= 31]

N = spec.NETS
N["VBUS"] += [(D1, "1"), (U2, "3"), (U2, "5"), (C1, "1"), (C2, "1")]
N["GND"] += ([(D1, "2"), (U2, "1"), (C1, "2"), (C2, "2"), (C4, "2"), (C5, "2"), (R4, "2"),
              (C6, "2"), (C7, "2"), (C8, "2"), (C9, "2"), (J2, "76"), (J2, "77"), (H5, "1")]
             + [(J2, n) for n in M2_GND] + [(h, "1") for h in HOLES])
N["+3V3"] += ([(L1, "2"), (R3, "1"), (C4, "1"), (C5, "1"), (C6, "1"), (C7, "1"), (C8, "1"),
               (C9, "1")] + [(J2, n) for n in M2_3V3])
for _tp, _net in TPS.items():
    N[_net] += [(_tp, "1")]
N["SW"] += [(U2, "2"), (L1, "1"), (C3, "1")]
N["VBST"] += [(U2, "6"), (C3, "2")]
N["FB"] += [(U2, "4"), (R3, "2"), (R4, "1")]
N["USB_D_P"] += [(J2, "3")]
N["USB_D_N"] += [(J2, "5")]
spec.NO_CONNECT += [(J2, n) for n in M2_ALL if n not in M2_USED]


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------
def build(d):
    s = d.sheet(f"{NAME}.kicad_sch", "USB-C to M.2 Key-E HaLow Adapter", paper="A3",
                comment="USB 2.0 over USB-C to a Gateworks GW16170 (MM8108) M.2 2230 card")

    def put(ref, x, y, rot=0, mirror=None):
        lib_id, value, fp, lcsc, mfr, mpn = spec.PARTS[ref]
        props = {"Footprint": fp}
        for k, v in (("LCSC", lcsc), ("Manufacturer", mfr), ("MPN", mpn)):
            if v:
                props[k] = v
        # a bare mounting hole is not a part: keep it out of the BOM, as its footprint already says
        s.place(ref, lib_id, value, snap(x), snap(y), rot, mirror, props=props,
                in_bom=not fp.startswith(("MountingHole:", "Fiducial:", "TestPoint:")))

    def hang(ref, at):
        """Vertical two-pin part with pin 1 on `at`, pin 2 to ground."""
        put(ref, at[0], at[1] + 3.81)
        assert s.pin(ref, "1") == (snap(at[0]), snap(at[1])), (ref, s.pin(ref, "1"), at)
        s.stub(ref, "2", 2.54, power="GND")

    # ---- 1. USB-C input ------------------------------------------------------
    with s.block(usb.title):
        x, y = 50.8, 101.6
        usb._draw(s, x, y)
        # VBUS clamp: cathode up on VBUS, anode to ground
        put(D1, x + 66.04, y - 5.08, rot=270)
        k, a = s.pin(D1, "1"), s.pin(D1, "2")
        assert k[1] < a[1], "D1 cathode must be the upper pin"
        s.stub(D1, "1", 2.54, power="VBUS")
        s.stub(D1, "2", 2.54, power="GND")
        ny = y + 38.1
        for i, n in enumerate((
                "CC1/CC2: 5.1k to GND each (sink Rd). One shared resistor breaks C-to-C cables.",
                "No PD controller: the host sees a default-power sink and supplies 5 V only.",
                "U1 pin 5 open on purpose: reaching it would slot the ground plane under D+/D-. D1 clamps VBUS.",
                "U1 and D1 sit at J1, before anything else. Route D+/D- as a 90 ohm pair,",
                "no stubs: J1 -> U1 pads -> J2. Shell is tied straight to GND.")):
            s.note(n, x - 12.7, ny + i * 2.54, 1.0)

    # ---- 2. 3.3 V buck --------------------------------------------------------
    with s.block("3.3 V / 3 A BUCK (U2 TPS563201)"):
        x, y = 215.9, 101.6
        put(U2, x, y)
        vin, en = s.pin(U2, "VIN"), s.pin(U2, "EN")
        sw, bst, fb = s.pin(U2, "SW"), s.pin(U2, "VBST"), s.pin(U2, "VFB")
        # input rail: VBUS port, bulk, HF cap, EN tied to VIN
        x_en, x_c2, x_c1, x_in = vin[0] - 5.08, vin[0] - 15.24, vin[0] - 30.48, vin[0] - 40.64
        s.wire(vin, (x_in, vin[1]))
        s.wire((x_in, vin[1]), (x_in, vin[1] - 2.54))
        s.power("VBUS", x_in, vin[1] - 2.54)
        s.wire(en, (x_en, en[1]), (x_en, vin[1]))
        hang(C1, (x_c1, vin[1]))
        hang(C2, (x_c2, vin[1]))
        s.stub(U2, "GND", 2.54, power="GND")
        # switch node over the top, bootstrap cap between SW (top) and VBST
        top = sw[1] - 10.16
        x_sw, x_bst = sw[0] + 5.08, sw[0] + 12.7
        put(L1, x_bst + 12.7, top, rot=90)
        l1, l2 = s.pin(L1, "1"), s.pin(L1, "2")
        assert l1[0] < l2[0], "L1 pin 1 must face the switch node"
        s.wire(sw, (x_sw, sw[1]), (x_sw, top), l1)
        put(C3, x_bst, top + 6.35)
        c3t, c3b = s.pin(C3, "1"), s.pin(C3, "2")
        assert c3t[1] < c3b[1]
        s.wire(c3t, (x_bst, top))
        s.wire(bst, (x_bst, bst[1]), c3b)
        s.label("SW", l1[0] - 5.08, top)
        s.label("VBST", bst[0] + 6.35, bst[1])
        # output node: rail port, divider, output caps, ERC flag
        xo = l2[0] + 7.62
        s.wire(l2, (xo, top))
        s.wire((xo, top), (xo, top - 2.54))
        s.power("+3V3", xo, top - 2.54)
        r3_top = (xo, fb[1] - 7.62)
        s.wire((xo, top), r3_top)
        put(R3, xo, r3_top[1] + 3.81)
        put(R4, xo, fb[1] + 3.81)
        assert s.pin(R3, "2") == s.pin(R4, "1") == (xo, fb[1])
        s.wire(fb, (xo, fb[1]))
        s.label("FB", fb[0] + 7.62, fb[1])
        s.stub(R4, "2", 2.54, power="GND")
        xc4, xc5, xf = xo + 15.24, xo + 30.48, xo + 43.18
        s.wire((xo, top), (xf, top), (xf, top - 2.54))
        s.power("PWR_FLAG", xf, top - 2.54)
        hang(C4, (xc4, top))
        hang(C5, (xc5, top))
        ny = y + 25.4
        for i, n in enumerate((
                "Vout = 0.768 V x (1 + R3/R4) = 0.768 x (1 + 33.2k/10k) = 3.32 V. EN tied to VIN: on with VBUS.",
                "Load: GW16170 at 28.5 dBm, about 3-4 W in Tx bursts = ~1.2 A at 3.3 V = ~0.9 A from VBUS.",
                "That is more than a 500 mA USB 2.0 port guarantees: use a USB 3 / USB-C host port or a powered hub.",
                "Only C1 + C2 (10 uF) sit on VBUS, the USB inrush limit; the bulk is after the soft-started buck.",
                "L1 2.2 uH (TI typical for 3.3 V): with the socket bulk cap this rail has ~87 uF effective,",
                "and 2.2 uH keeps the LC pole inside TI Table 2 (20-68 uF at up to 4.7 uH).",
                "Layout: C1/C2 tight to VIN-GND, SW copper short, L1 and C4/C5 close, FB trace away from SW/L1.")):
            s.note(n, x_in - 2.54, ny + i * 2.54, 1.0)

    # ---- 3. M.2 socket ----------------------------------------------------------
    with s.block("M.2 KEY-E SOCKET (J2) - GATEWORKS GW16170, USB 2.0 ONLY"):
        x, y = 388.62, 127.0
        put(J2, x, y)
        s.stub(J2, "3", 7.62, label="USB_D_P")
        s.stub(J2, "5", 7.62, label="USB_D_N")
        s.stub(J2, "2", 2.54, power="+3V3")
        g = s.stub(J2, "1", 5.08, power="GND")
        sh = s.pin(J2, "76")
        s.wire(sh, (sh[0], sh[1] + 2.54), (g[0], sh[1] + 2.54))
        s.nc(J2, *[n for n in M2_ALL if n not in M2_USED])
        # bulk + decoupling at the socket's 3.3 V pins
        s.rail_bank([C6, C7, C8, C9], x + 50.8, y - 25.4, "+3V3",
                    place=lambda ref, px, py: put(ref, px, py))
        nx, ny = x + 40.64, y + 2.54
        for i, n in enumerate((
                "GW16170 (MM8108-M20): 3.3 V on pins 2/4/72/74, USB D+ pin 3, D- pin 5. Nothing else is used.",
                "Pin 56 W_DISABLE1# = card RESET_N (200k pull-up on the card), pin 54 W_DISABLE2# = WAKE",
                "(10k pull-up on the card): both left open, so the card runs whenever +3V3 is up.",
                "C6 covers the Tx burst edge; C8/C9 go one at pins 2/4 and one at pins 72/74.",
                "Card is 22 x 30 x 3.5 mm with an MMCX antenna jack: no RF on this board.",
                "H5: 2.5 mm SMT nut (LCSC C5301773), 29.75 mm from the socket centre on the peg side (card stop is 1.75 mm behind the pegs).")):
            s.note(n, nx, ny + i * 2.54, 1.0)

    # ---- 4. Mechanical ------------------------------------------------------------
    with s.block("MOUNTING (GROUNDED)"):
        x, y = 520.7, 101.6
        ends = []
        for i, h in enumerate(HOLES + [H5]):
            put(h, x + i * 20.32, y)
            pn = s.pin(h, "1")
            s.wire(pn, (pn[0], pn[1] + 2.54))
            ends.append((pn[0], pn[1] + 2.54))
        s.wire(ends[0], ends[-1])
        s.wire(ends[0], (ends[0][0], ends[0][1] + 2.54))
        s.gnd(ends[0][0], ends[0][1] + 2.54)
        s.note("H1-H4: M3 board corners. H5: M2 standoff under the card's", x - 2.54, y + 15.24, 1.0)
        s.note("mounting notch, 30 mm card length (2230).", x - 2.54, y + 17.78, 1.0)

    # ---- 5. Assembly and bring-up aids ---------------------------------------------
    with s.block("FIDUCIALS & TEST PADS (NOT IN BOM)"):
        x, y = 520.7, 160.0
        for i, f in enumerate(FIDS):
            put(f, x + i * 15.24, y)
        for i, (tp, net) in enumerate(TPS.items()):
            put(tp, x + i * 15.24, y + 22.86)
            s.stub(tp, "1", 5.08, power=net)
        for i, n in enumerate(("FID1-3: 1 mm fiducials for the",
                               "0.5 mm pitch socket. TP1-3: 1.5 mm",
                               "probe pads, outside the card outline.")):
            s.note(n, x - 2.54, y + 38.1 + i * 2.54, 1.0)

    s.arrange()
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--render", default=None, help="directory for SVG/PDF renders")
    args = ap.parse_args()
    d = Design(HERE, NAME, title="USB-C to M.2 Key-E HaLow Adapter", rev="A",
               company="diode663")
    print("== lint ==")
    spec.lint(lib=d.lib)
    build(d)
    d.write(force=args.force)
    ok = d.verify(dict(spec.NETS), spec.NO_CONNECT)
    d.erc()
    d.check_text()
    if args.render:
        d.render(args.render)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
