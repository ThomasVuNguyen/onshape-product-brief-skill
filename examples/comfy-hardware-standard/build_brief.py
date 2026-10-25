from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
OUT = ROOT / "comfy-hardware-standard-product-brief.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Roboto", str(ROOT / "fonts/Roboto-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Roboto-Bold", str(ROOT / "fonts/Roboto-Bold.ttf")))

W, H = A4
NAVY = colors.HexColor("#173B57")
INK = colors.HexColor("#242B30")
MUTED = colors.HexColor("#66737B")
GOLD = colors.HexColor("#D5A52F")
PAPER = colors.HexColor("#F5F6F3")
RULE = colors.HexColor("#D5DEE0")
WHITE = colors.white
X = 61
RIGHT = W - X

c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
c.setTitle("Comfy Hardware Standard - Product Brief")
c.setAuthor("ComfySpace concept study")
c.setSubject("CAD concept brief based on the Total Assembly in Onshape")
c.setKeywords("Comfy Hardware Standard, product brief, CAD, modular platform")


def text(x, y, value, font="Roboto", size=10, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, value)


def para(value, x, top, width, size=10.4, leading=15.6, color=INK, font="Roboto"):
    style = ParagraphStyle(
        "body", fontName=font, fontSize=size, leading=leading,
        textColor=color, alignment=TA_LEFT, spaceAfter=0,
    )
    p = Paragraph(value, style)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, top - height)
    return top - height


def image(name, x, y, w, h):
    c.drawImage(ImageReader(str(ASSETS / name)), x, y, w, h, mask="auto")


def footer(page, title="Comfy Hardware Standard"):
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.9)
    c.line(X, 66, RIGHT, 66)
    text(X, 49, title, "Roboto-Bold", 7.2, NAVY)
    text(X + 184, 49, "Concept brief  /  24 October 2026", "Roboto", 7.2, MUTED)
    c.setFont("Roboto-Bold", 7.2)
    c.setFillColor(NAVY)
    c.drawRightString(RIGHT, 49, str(page))


def heading(section, sub=None):
    text(X, 756, section, "Roboto-Bold", 13.5, NAVY)
    if sub:
        text(X, 730, sub, "Roboto", 9.2, MUTED)


def mark(x, y, size, color=WHITE):
    # Ten panels in a 3 x 4 field: the visible CAD pattern in miniature.
    c.setStrokeColor(color)
    c.setLineWidth(max(0.8, size / 22))
    unit = size / 4.8
    for row in range(4):
        for col in range(3):
            if (row, col) in ((0, 2), (3, 0)):
                continue
            px = x + col * unit * 1.13
            py = y + (3 - row) * unit * 1.13
            c.roundRect(px, py, unit, unit, unit * 0.15, fill=0, stroke=1)
            c.circle(px + unit / 2, py + unit / 2, unit * 0.11, fill=0, stroke=1)


def dimension_h(x0, x1, y, label):
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(x0, y, x1, y)
    for x in (x0, x1):
        c.line(x, y - 5, x, y + 5)
    c.setFillColor(GOLD)
    c.setFont("Roboto-Bold", 8.2)
    tw = pdfmetrics.stringWidth(label, "Roboto-Bold", 8.2)
    c.setFillColor(WHITE)
    c.rect((x0 + x1 - tw) / 2 - 8, y - 4, tw + 16, 11, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.drawCentredString((x0 + x1) / 2, y - 1, label)


def dimension_v(x, y0, y1, label):
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(x, y0, x, y1)
    for y in (y0, y1):
        c.line(x - 5, y, x + 5, y)
    c.saveState()
    c.translate(x - 5, (y0 + y1) / 2)
    c.rotate(90)
    c.setFillColor(WHITE)
    tw = pdfmetrics.stringWidth(label, "Roboto-Bold", 8.2)
    c.rect(-tw / 2 - 8, -4, tw + 16, 11, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Roboto-Bold", 8.2)
    c.drawCentredString(0, -1, label)
    c.restoreState()


# 1 - an assured, spare opening in the rhythm of the reference brief.
c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)
mark(X, 712, 54)
text(X, 648, "Comfy Hardware", "Roboto-Bold", 25, WHITE)
text(X, 616, "Standard", "Roboto", 25, WHITE)
text(X, 576, "A modular, articulated hardware platform", "Roboto", 11.8, WHITE)
text(X, 550, "CAD concept brief  /  24 October 2026", "Roboto", 9.2, colors.HexColor("#C7D8E2"))
image("hero-lines.png", 125, 104, 380, 430)
c.setStrokeColor(GOLD)
c.setLineWidth(1.2)
c.line(X, 71, RIGHT, 71)
text(X, 52, "COMFY HARDWARE STANDARD", "Roboto-Bold", 7.3, WHITE)
c.showPage()


# 2 - overview, with the current CAD rather than an invented product render.
heading("Overview")
c.setFillColor(PAPER)
c.rect(X, 385, RIGHT - X, 325, fill=1, stroke=0)
image("hero-color.png", 172, 392, 288, 307)
text(X + 13, 691, "01  /  TOTAL ASSEMBLY", "Roboto-Bold", 7.2, NAVY)
y = para(
    "Comfy Hardware Standard combines a repeatable slotted panel field, "
    "electronics enclosures, and an articulated support in one compact assembly.",
    X, 359, RIGHT - X, 10.6, 16.1,
)
para(
    "The panel pattern creates a mounting surface above the electronics. "
    "A central pivot and lower arm position the field as a single module. "
    "This brief documents the current CAD concept for design review.",
    X, y - 20, RIGHT - X, 10.6, 16.1,
)
footer(2)
c.showPage()


# 3 - specification follows the restrained label/value logic of the reference.
heading("Specification")
rows = [
    ("Design state", "In progress - current Onshape Total Assembly"),
    ("Panel field", "Ten visible panels in a three-column, four-row footprint"),
    ("CAD envelope", "150 x 200 x 163.1 mm, from the exported visible assembly"),
    ("Architecture", "Slotted panel surface; electronics housings; pivot; support arm"),
    ("Model references", "Raspberry Pi Zero 2 W components and MG996R appear in the assembly tree"),
    ("Drawing status", "Reference views only; materials and production tolerances are unverified"),
]
y = 684
for i, (label, value) in enumerate(rows):
    text(X, y, label, "Roboto-Bold", 10.2, NAVY)
    end = para(value, 200, y + 2, RIGHT - 200, 10.1, 14.6)
    bottom = min(y - 42, end - 16)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.45)
    c.line(X, bottom, RIGHT, bottom)
    y = bottom - 34
text(X, 217, "Basis", "Roboto-Bold", 10.2, NAVY)
para(
    "Onshape: Comfy Hardware Standard / Total Assembly, Main workspace. "
    "The envelope is calculated from a GLB export of the visible model on 24 October 2026.",
    200, 219, RIGHT - 200, 9.5, 14.1, MUTED,
)
c.linkURL(
    "https://cad.onshape.com/documents/ec0ae1b4c4cadcdb734d768e/w/0cbf39a01f73b28f05e10cb3/e/174f79a682a32b34424348cb",
    (200, 174, RIGHT, 222), relative=0,
)
footer(3)
c.showPage()


# 4 - drawing-led plan view with only defensible overall measurements.
heading("Physical specification", "Panel field  /  top view")
image("top-lines.png", 116, 185, 360, 471)
dimension_h(123, 468, 678, "150 mm")
dimension_v(94, 192, 650, "200 mm")
text(X, 124, "01  /  PANEL FIELD", "Roboto-Bold", 8.2, NAVY)
para(
    "Ten panels occupy a three-column by four-row field. The two open positions "
    "preserve the asymmetric outline visible in the current assembly.",
    X, 111, RIGHT - X, 8.5, 12.0, MUTED,
)
footer(4)
c.showPage()


# 5 - side elevation and pivot detail.
heading("Physical specification", "Support and joint  /  reference elevations")
image("left-lines.png", 88, 350, 420, 346)
dimension_h(95, 507, 330, "200 mm")
dimension_v(523, 360, 688, "163.1 mm")
text(X, 712, "02  /  SIDE ELEVATION", "Roboto-Bold", 8.2, NAVY)
text(X, 294, "03  /  PIVOT DETAIL", "Roboto-Bold", 8.2, NAVY)
image("front-lines.png", 126, 84, 92, 230)
para(
    "The circular pivot joins the panel platform to the lower support. "
    "The stated height is the overall CAD envelope, not a pivot dimension.",
    270, 273, 260, 9.2, 13.8, MUTED,
)
footer(5)
c.showPage()


# 6 - quiet closing page.
c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)
mark(X, 118, 44)
text(120, 142, "Comfy Hardware Standard", "Roboto-Bold", 16.5, WHITE)
text(X, 89, "CAD concept brief  /  24 October 2026", "Roboto", 8.6, colors.HexColor("#C7D8E2"))
c.setStrokeColor(GOLD)
c.setLineWidth(1.2)
c.line(X, 71, RIGHT, 71)
c.showPage()

c.save()
print(OUT)
