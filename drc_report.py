"""Run KiCad's DRC and print everything except library-internal silkscreen noise."""
import collections, json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import placement_config as cfg
cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
out = os.path.join(here, "drc.json")
subprocess.run([cli, "pcb", "drc", "--severity-error", "--severity-warning", "--schematic-parity", "--format", "json",
                "-o", out, os.path.join(here, cfg.NAME + ".kicad_pcb")], capture_output=True, text=True)
d = json.load(open(out))
ox, oy = cfg.ORIGIN
c = collections.Counter((v["severity"], v["type"]) for v in d.get("violations", []))
for k, n in sorted(c.items()):
    print("%3d  %-8s %s" % (n, k[0], k[1]))
print("unconnected: %d   schematic parity: %d" % (len(d.get("unconnected_items", [])), len(d.get("schematic_parity", []))))
fmt = lambda i: "%s @(%.2f,%.2f)" % (i["description"][:52], i["pos"]["x"] - ox, i["pos"]["y"] - oy)
for v in d.get("violations", []):
    if v["type"].startswith("silk"):
        continue
    print(" -", v["type"], "|", v["description"][:100], "|", "; ".join(fmt(i) for i in v["items"][:2]))
for u in d.get("unconnected_items", []):
    print(" U", "; ".join(fmt(i) for i in u["items"][:2]))
for u in d.get("schematic_parity", []):
    print(" P", u["description"][:120])
