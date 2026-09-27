#!/usr/bin/env python3
"""Lab 3 UML component diagram — hand-laid-out SVG, monochrome."""

W, H = 1800, 800
INK   = "#000000"
WHITE = "#FFFFFF"
EXT   = "#EDEDED"       # external / device fill
BAND  = "#A6A6A6"       # band outline
BANDT = "#6E6E6E"       # band label
SUB   = "#555555"       # stereotype / secondary text

out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  'font-family="Helvetica, Arial, sans-serif">')
A(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')
A('<defs>'
  f'<marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="3.2" orient="auto">'
  f'<path d="M0,0 L9,3.2 L0,6.4" fill="none" stroke="{INK}" stroke-width="1.4"/></marker>'
  '</defs>')

BW, BH = 180, 74

def comp(x, y, lines, stereo="component", fill=WHITE):
    A(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" fill="{fill}" stroke="{INK}" stroke-width="1.7"/>')
    ix, iy = x + BW - 27, y + 9
    A(f'<rect x="{ix}" y="{iy}" width="17" height="13" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/>')
    A(f'<rect x="{ix-4}" y="{iy+2}" width="8" height="3.5" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/>')
    A(f'<rect x="{ix-4}" y="{iy+7.5}" width="8" height="3.5" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/>')
    A(f'<text x="{x+BW/2}" y="{y+25}" font-size="10.5" fill="{SUB}" text-anchor="middle">&#171;{stereo}&#187;</text>')
    dy = y + 43 if len(lines) > 1 else y + 47
    for i, ln in enumerate(lines):
        A(f'<text x="{x+BW/2}" y="{dy+i*15}" font-size="12.5" font-weight="bold" fill="{INK}" '
          f'text-anchor="middle">{ln}</text>')
    return x + BW/2, y + BH/2

def ball(px, py, label, lx, ly, anchor="middle", stub=None):
    if stub:
        A(f'<line x1="{stub[0]}" y1="{stub[1]}" x2="{px}" y2="{py}" stroke="{INK}" stroke-width="1.5"/>')
    A(f'<circle cx="{px}" cy="{py}" r="7.5" fill="{WHITE}" stroke="{INK}" stroke-width="1.8"/>')
    A(f'<text x="{lx}" y="{ly}" font-size="10.5" font-weight="bold" fill="{INK}" text-anchor="{anchor}">{label}</text>')

def socket(cx, cy, facing, stub=None):
    r = 11
    d = (f'M {cx},{cy-r} A {r},{r} 0 0 0 {cx},{cy+r}' if facing == "r"
         else f'M {cx},{cy-r} A {r},{r} 0 0 1 {cx},{cy+r}')
    A(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    if stub:
        A(f'<line x1="{stub[0]}" y1="{stub[1]}" x2="{cx}" y2="{cy}" stroke="{INK}" stroke-width="1.5"/>')

def dep(pts, label=None, lx=None, ly=None, anchor="middle"):
    d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    A(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.3" stroke-dasharray="6,4" marker-end="url(#arr)"/>')
    if label:
        A(f'<text x="{lx}" y="{ly}" font-size="10" fill="{INK}" text-anchor="{anchor}">{label}</text>')

def band(x, y, w, h, title):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{BAND}" '
      'stroke-width="1" stroke-dasharray="5,4"/>')
    A(f'<text x="{x+10}" y="{y+17}" font-size="10.5" font-weight="bold" fill="{BANDT}" '
      f'letter-spacing="0.6">{title}</text>')

# ---------------- header ----------------
A(f'<text x="28" y="36" font-size="17" font-weight="bold" fill="{INK}">'
  'Public Bus Live Tracking &amp; Crowding Estimator &#8212; UML Component Diagram</text>')
A(f'<text x="28" y="57" font-size="11.5" fill="{SUB}">'
  'Architecture: Microservices &#160;|&#160; Problem Statement #24 &#160;|&#160; '
  'SRN PES1UG24CS392 &#160;|&#160; Section G</text>')
A(f'<line x1="28" y1="70" x2="{W-28}" y2="70" stroke="{INK}" stroke-width="1"/>')

# ---------------- grid ----------------
C = [24, 330, 636, 942, 1248, 1554]
R1, R2, R3 = 140, 296, 452
Rt = lambda x: x + BW

band(10,   112, 240, 278, "FIELD DEVICES")
band(316,  112, 208, 278, "INGESTION")
band(622,  112, 208, 122, "COMPUTATION")
band(928,  112, 208, 278, "EXPERIENCE")
band(1234, 112, 208, 122, "EDGE")
band(1540, 112, 222, 414, "CLIENTS / EXTERNAL")
band(592,  500, 216, 122, "DATA")

# ---------------- components ----------------
gps = comp(C[0]+14, R1, ["Onboard GPS Unit"], "device", EXT)
tkt = comp(C[0]+14, R2, ["Ticketing /", "APC Sensor"], "device", EXT)
ing = comp(C[1], R1, ["Telemetry Ingestion", "Service"])
crw = comp(C[1], R2, ["Crowding Estimator", "Service"])
eta = comp(C[2], R1, ["ETA Engine", "Service"])
cqs = comp(C[3], R1, ["Commuter Query", "Service"])
fos = comp(C[3], R2, ["Fleet Operations", "Service"])
gw  = comp(C[4], R1, ["API Gateway", "Component"])
app = comp(C[5], R1, ["Commuter", "Mobile App"], "client", EXT)
con = comp(C[5], R2, ["Fleet Controller", "Console"], "client", EXT)
prv = comp(C[5], R3, ["Push Notification", "Provider"], "external", EXT)
db  = comp(606, 520, ["Transit Data Store", "Component"])

L0, L1, L2, L3, L4, L5 = C[0]+14, C[1], C[2], C[3], C[4], C[5]
MY1, MY2 = R1 + 37, R2 + 37          # mid-height of each row

# ---------------- assembly connectors, left to right ----------------
def assembly(prev_right, next_left, y, name):
    """ball on the provider (right box), socket on the consumer (left box)."""
    bx = next_left - 63
    ball(bx, y, name, bx, y - 16, "middle", (next_left, y))
    socket(bx - 13, y, "r", (prev_right, y))

def assembly_rev(prev_right, next_left, y, name):
    """ball on the provider (left box), socket on the consumer (right box)."""
    bx = next_left - 63
    ball(bx, y, name, bx, y - 16, "middle", (prev_right, y))
    socket(bx - 13, y, "l", (next_left, y))

assembly(Rt(L0), L1, MY1, "ITelemetryIngest")          # GPS  -> Telemetry Ingestion
assembly(Rt(L0), L1, MY2, "ICrowdingIngest")     # TKT  -> Crowding Estimator
assembly_rev(Rt(L1), L2, MY1, "IVehiclePosition")      # Ingestion -> ETA Engine
assembly_rev(Rt(L2), L3, MY1, "IEtaQuery")             # ETA  -> Commuter Query
assembly_rev(Rt(L3), L4, MY1, "ICommuterQuery")        # CQS  -> API Gateway
assembly_rev(Rt(L4), L5, MY1, "ICommuterApi")          # GW   -> Mobile App

# ---------------- remaining interfaces ----------------
# ICrowdingQuery : provided by Crowding Estimator; used by Fleet Ops and Commuter Query
ball(Rt(L1)+30, MY2, "ICrowdingQuery", Rt(L1)+30, MY2+50, "middle", (Rt(L1), MY2))
dep([(Rt(L1)+38, MY2-8), (L2+34, MY2-8), (L2+34, MY1+BH+18), (L3+40, MY1+BH+18), (L3+40, R1+BH+4)],
    "&#171;use&#187; REST", L2+150, MY1+BH+12)
dep([(Rt(L1)+38, MY2+8), (L3-16, MY2+8), (L3-16, MY2), (L3-4, MY2)],
    "&#171;use&#187; REST", L2+130, MY2+22)

# IFleetControl : provided by Fleet Ops; used by API Gateway
ball(Rt(L3)+38, MY2, "IFleetControl", Rt(L3)+38, MY2+50, "middle", (Rt(L3), MY2))
dep([(Rt(L3)+46, MY2-8), (L4+44, MY2-8), (L4+44, R1+BH+4)],
    "&#171;use&#187; REST + RBAC", L4+54, MY2-14, "start")

# IFleetConsoleApi : provided by API Gateway; used by Fleet Controller Console
ball(Rt(L4)+38, MY1+26, "IFleetConsoleApi", Rt(L4)+38, MY1+52, "middle", (Rt(L4), MY1+26))
dep([(Rt(L4)+46, MY1+26), (L5+42, MY1+26), (L5+42, R2-4)],
    "&#171;use&#187; HTTPS", L5+50, MY1+48, "start")

# Commuter Query -> Push Notification Provider
PG = L3 + BW + 30
dep([(Rt(L3), MY1+22), (PG, MY1+22), (PG, R3+37), (L5-4, R3+37)],
    "&#171;use&#187; FCM / APNs", PG+12, R3+30, "start")

# ---------------- data tier ----------------
BUS = 470
DBX = db[0]
A(f'<line x1="440" y1="{BUS}" x2="1062" y2="{BUS}" stroke="{INK}" stroke-width="1.5"/>')
A(f'<line x1="{DBX}" y1="{BUS}" x2="{DBX}" y2="512" stroke="{INK}" stroke-width="1.5"/>')
ball(DBX, 492, "ITransitData", DBX+92, 496, "start")

for sx in (440, 596, 676, 1062):
    socket(sx, BUS, "l")

# vertical drops from each consumer to the bus
A(f'<path d="M {L1+120},{R1+BH} L {L1+120},{R1+BH+22} L 596,{R1+BH+22} L 596,{BUS-11}" '
  f'fill="none" stroke="{INK}" stroke-width="1.3" stroke-dasharray="6,4"/>')
A(f'<text x="604" y="{BUS-30}" font-size="10" fill="{INK}">&#171;use&#187; DB write</text>')
for sx, sy, lbl in [(440, R2+BH, "DB query"), (676, R1+BH, "DB query"), (1062, R2+BH, "DB query")]:
    A(f'<line x1="{sx}" y1="{sy}" x2="{sx}" y2="{BUS-11}" stroke="{INK}" stroke-width="1.3" stroke-dasharray="6,4"/>')
    A(f'<text x="{sx+8}" y="{BUS-30}" font-size="10" fill="{INK}">&#171;use&#187; {lbl}</text>')

# ---------------- legend ----------------
lx, ly = 28, 660
A(f'<rect x="{lx}" y="{ly}" width="600" height="108" fill="none" stroke="{INK}" stroke-width="1"/>')
A(f'<text x="{lx+16}" y="{ly+22}" font-size="11.5" font-weight="bold" fill="{INK}" letter-spacing="0.6">NOTATION</text>')

A(f'<line x1="{lx+18}" y1="{ly+43}" x2="{lx+30}" y2="{ly+43}" stroke="{INK}" stroke-width="1.5"/>')
A(f'<circle cx="{lx+38}" cy="{ly+43}" r="7.5" fill="{WHITE}" stroke="{INK}" stroke-width="1.8"/>')
A(f'<text x="{lx+62}" y="{ly+47}" font-size="10.5" fill="{INK}">'
  'Provided interface (ball) &#8212; a service the component offers</text>')

A(f'<path d="M {lx+36},{ly+58} A 11,11 0 0 1 {lx+36},{ly+80}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
A(f'<line x1="{lx+36}" y1="{ly+69}" x2="{lx+48}" y2="{ly+69}" stroke="{INK}" stroke-width="1.5"/>')
A(f'<text x="{lx+62}" y="{ly+73}" font-size="10.5" fill="{INK}">'
  'Required interface (socket) &#8212; a service the component needs</text>')

A(f'<path d="M {lx+18},{ly+95} L {lx+48},{ly+95}" fill="none" stroke="{INK}" stroke-width="1.3" '
  'stroke-dasharray="6,4" marker-end="url(#arr)"/>')
A(f'<text x="{lx+62}" y="{ly+99}" font-size="10.5" fill="{INK}">'
  '&#171;use&#187; dependency &#8212; labelled with the protocol / technology</text>')

sx0 = 680
A(f'<rect x="{sx0}" y="{ly}" width="300" height="108" fill="none" stroke="{INK}" stroke-width="1"/>')
A(f'<text x="{sx0+16}" y="{ly+22}" font-size="11.5" font-weight="bold" fill="{INK}" letter-spacing="0.6">SUMMARY</text>')
for i, (k, v) in enumerate([("System components", "7"), ("Interfaces", "10"), ("External actors / systems", "5")]):
    A(f'<text x="{sx0+16}" y="{ly+47+i*21}" font-size="10.5" fill="{INK}">{k}</text>')
    A(f'<text x="{sx0+284}" y="{ly+47+i*21}" font-size="10.5" font-weight="bold" fill="{INK}" text-anchor="end">{v}</text>')

A('</svg>')
open("component_diagram.svg", "w").write("\n".join(out))
print("svg written")
