#!/usr/bin/env python3
"""Generate the 2026 OpenClaw Hardware Guide PDF lead magnet."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
import os

# ── Colors ──────────────────────────────────────────────────────────────
DARK_BG = HexColor("#1e1e2e")
DARK_HEADER = HexColor("#2d2d3f")
PURPLE = HexColor("#8b5cf6")
PURPLE_LIGHT = HexColor("#a78bfa")
PURPLE_DARK = HexColor("#6d28d9")
LIGHT_TEXT = HexColor("#e2e2e2")
MUTED_TEXT = HexColor("#9ca3af")
WHITE = HexColor("#ffffff")
DARK_ROW = HexColor("#262636")
DARKER_ROW = HexColor("#1e1e2e")
TABLE_BORDER = HexColor("#3d3d5c")
ACCENT_GREEN = HexColor("#34d399")
ACCENT_YELLOW = HexColor("#fbbf24")
ACCENT_RED = HexColor("#f87171")
PAGE_BG = HexColor("#121220")

OUTPUT_PATH = "/home/marketingpatpat/openclaw/openclaw-hardware-guide-2026.pdf"

WIDTH, HEIGHT = letter


# ── Custom flowable: colored block background ───────────────────────────
class ColoredBlock(Flowable):
    """A colored rectangle behind content."""
    def __init__(self, width, height, color):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)


class TipBox(Flowable):
    """A highlighted tip/callout box."""
    def __init__(self, text, width, accent=PURPLE, bg=DARK_HEADER):
        Flowable.__init__(self)
        self.text = text
        self.box_width = width
        self.accent = accent
        self.bg = bg
        self.height = 0
        self._para = None
        self._setup()

    def _setup(self):
        style = ParagraphStyle(
            "tiptext", fontName="Helvetica", fontSize=9,
            textColor=LIGHT_TEXT, leading=13,
        )
        self._para = Paragraph(self.text, style)
        w, h = self._para.wrap(self.box_width - 30, 1000)
        self.height = h + 20

    def wrap(self, availWidth, availHeight):
        self._setup()
        return self.box_width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.box_width, self.height, 6, fill=1, stroke=0)
        c.setFillColor(self.accent)
        c.roundRect(0, 0, 5, self.height, 2, fill=1, stroke=0)
        self._para.drawOn(c, 18, 8)


# ── Page template callbacks ─────────────────────────────────────────────
def on_page(canvas, doc):
    """Draw background, header bar, and footer on every page."""
    canvas.saveState()
    # Full page background
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    # Header bar
    canvas.setFillColor(DARK_HEADER)
    canvas.rect(0, HEIGHT - 50, WIDTH, 50, fill=1, stroke=0)
    canvas.setFillColor(PURPLE)
    canvas.rect(0, HEIGHT - 52, WIDTH, 3, fill=1, stroke=0)

    # Header text
    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(PURPLE_LIGHT)
    canvas.drawString(54, HEIGHT - 35, "AUTOMATYN")
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(MUTED_TEXT)
    canvas.drawString(135, HEIGHT - 35, "OpenClaw Hardware Guide 2026")

    # Footer
    canvas.setFillColor(DARK_HEADER)
    canvas.rect(0, 0, WIDTH, 36, fill=1, stroke=0)
    canvas.setFillColor(PURPLE)
    canvas.rect(0, 35, WIDTH, 1.5, fill=1, stroke=0)

    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED_TEXT)
    canvas.drawString(54, 14, "automatyn.github.io  |  Professional OpenClaw Setup Service")

    # Page number
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(PURPLE_LIGHT)
    canvas.drawRightString(WIDTH - 54, 14, f"Page {doc.page}")

    canvas.restoreState()


def on_first_page(canvas, doc):
    """Cover page — no standard header/footer."""
    canvas.saveState()
    # Full background
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    # Large purple gradient band at top
    canvas.setFillColor(PURPLE_DARK)
    canvas.rect(0, HEIGHT - 280, WIDTH, 280, fill=1, stroke=0)
    canvas.setFillColor(PURPLE)
    canvas.rect(0, HEIGHT - 283, WIDTH, 6, fill=1, stroke=0)

    # Title
    canvas.setFont("Helvetica-Bold", 36)
    canvas.setFillColor(WHITE)
    canvas.drawCentredString(WIDTH / 2, HEIGHT - 120, "OpenClaw")
    canvas.setFont("Helvetica-Bold", 36)
    canvas.drawCentredString(WIDTH / 2, HEIGHT - 162, "Hardware Guide")

    # Year badge
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(PURPLE_LIGHT)
    canvas.drawCentredString(WIDTH / 2, HEIGHT - 200, "2026 EDITION")

    # Subtitle
    canvas.setFont("Helvetica", 13)
    canvas.setFillColor(HexColor("#c4b5fd"))
    canvas.drawCentredString(WIDTH / 2, HEIGHT - 240,
        "Everything you need to build, buy, or rent the right hardware")
    canvas.drawCentredString(WIDTH / 2, HEIGHT - 258,
        "for your open-source claw machine project.")

    # Branding block
    canvas.setFillColor(DARK_HEADER)
    canvas.roundRect(WIDTH / 2 - 120, HEIGHT - 370, 240, 55, 8, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(PURPLE_LIGHT)
    canvas.drawCentredString(WIDTH / 2, HEIGHT - 346, "AUTOMATYN")
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(MUTED_TEXT)
    canvas.drawCentredString(WIDTH / 2, HEIGHT - 362, "automatyn.github.io")

    # What's inside section
    y = HEIGHT - 430
    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(WHITE)
    canvas.drawCentredString(WIDTH / 2, y, "WHAT'S INSIDE")

    items = [
        "Minimum & recommended system specifications",
        "GPU vs CPU decision framework",
        "Cloud, VPS, and bare-metal cost comparison",
        "Three complete build recommendations ($200\u2013$2,000)",
        "OS setup & security hardening checklist",
        "Network & remote access configuration",
        "Quick-start shopping & setup checklist",
    ]
    canvas.setFont("Helvetica", 10.5)
    canvas.setFillColor(LIGHT_TEXT)
    y -= 30
    for item in items:
        canvas.setFillColor(PURPLE_LIGHT)
        canvas.drawString(WIDTH / 2 - 160, y, "\u25b8")
        canvas.setFillColor(LIGHT_TEXT)
        canvas.drawString(WIDTH / 2 - 145, y, item)
        y -= 20

    # Footer on cover
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED_TEXT)
    canvas.drawCentredString(WIDTH / 2, 30,
        "\u00a9 2026 Automatyn. Free to share. Not for resale.")

    canvas.restoreState()


# ── Style definitions ───────────────────────────────────────────────────
def build_styles():
    s = {}
    s["h1"] = ParagraphStyle(
        "H1", fontName="Helvetica-Bold", fontSize=22, leading=28,
        textColor=WHITE, spaceAfter=6, spaceBefore=14,
    )
    s["h2"] = ParagraphStyle(
        "H2", fontName="Helvetica-Bold", fontSize=15, leading=20,
        textColor=PURPLE_LIGHT, spaceAfter=6, spaceBefore=16,
    )
    s["h3"] = ParagraphStyle(
        "H3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
        textColor=WHITE, spaceAfter=4, spaceBefore=10,
    )
    s["body"] = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=10, leading=14.5,
        textColor=LIGHT_TEXT, spaceAfter=6,
    )
    s["bullet"] = ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=10, leading=14,
        textColor=LIGHT_TEXT, leftIndent=18, bulletIndent=6,
        spaceAfter=3, bulletFontName="Helvetica", bulletFontSize=10,
    )
    s["small"] = ParagraphStyle(
        "Small", fontName="Helvetica", fontSize=8.5, leading=12,
        textColor=MUTED_TEXT, spaceAfter=4,
    )
    s["center"] = ParagraphStyle(
        "Center", fontName="Helvetica", fontSize=10, leading=14,
        textColor=LIGHT_TEXT, alignment=TA_CENTER, spaceAfter=6,
    )
    return s


# ── Helpers ─────────────────────────────────────────────────────────────
def heading_bar():
    return HRFlowable(
        width="100%", thickness=1.5, color=PURPLE,
        spaceAfter=8, spaceBefore=2,
    )

def thin_rule():
    return HRFlowable(
        width="100%", thickness=0.5, color=TABLE_BORDER,
        spaceAfter=6, spaceBefore=6,
    )

def spacer(h=10):
    return Spacer(1, h)


def make_table(data, col_widths=None, highlight_header=True):
    """Build a styled dark-theme table."""
    available = 500
    if col_widths is None:
        ncols = len(data[0])
        col_widths = [available / ncols] * ncols

    # Build cell paragraphs
    header_style = ParagraphStyle(
        "TH", fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=WHITE, alignment=TA_CENTER,
    )
    cell_style = ParagraphStyle(
        "TD", fontName="Helvetica", fontSize=9, leading=12,
        textColor=LIGHT_TEXT, alignment=TA_CENTER,
    )
    cell_left = ParagraphStyle(
        "TDL", fontName="Helvetica", fontSize=9, leading=12,
        textColor=LIGHT_TEXT,
    )

    table_data = []
    for ri, row in enumerate(data):
        new_row = []
        for ci, cell in enumerate(row):
            if ri == 0 and highlight_header:
                new_row.append(Paragraph(str(cell), header_style))
            elif ci == 0:
                new_row.append(Paragraph(str(cell), cell_left))
            else:
                new_row.append(Paragraph(str(cell), cell_style))
        table_data.append(new_row)

    t = Table(table_data, colWidths=col_widths)

    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, TABLE_BORDER),
    ]
    if highlight_header:
        style_cmds.append(("BACKGROUND", (0, 0), (-1, 0), PURPLE_DARK))

    # Alternating row colors
    for i in range(1, len(data)):
        bg = DARK_ROW if i % 2 == 1 else DARKER_ROW
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    t.setStyle(TableStyle(style_cmds))
    return t


# ── Content builders ────────────────────────────────────────────────────

def section_introduction(S, cw):
    elements = []
    elements.append(Paragraph("1. Introduction", S["h1"]))
    elements.append(heading_bar())
    elements.append(Paragraph(
        "<b>OpenClaw</b> is the leading open-source framework for building internet-connected "
        "claw machines\u2014arcade-style grabber games that anyone can play remotely through a "
        "web browser. Whether you are building a stream-interactive claw machine, an automated "
        "prize-fulfillment kiosk, or a robotics learning platform, your hardware choices will "
        "directly affect reliability, latency, and total cost of ownership.",
        S["body"]
    ))
    elements.append(spacer(4))
    elements.append(Paragraph(
        "This guide gives you the complete picture: what specs you actually need, when to "
        "spend more (and when not to), and concrete build recommendations at three price points. "
        "Every recommendation has been tested or validated by the Automatyn team in real "
        "deployments during 2025\u20132026.",
        S["body"]
    ))
    elements.append(spacer(4))
    elements.append(Paragraph("Why hardware matters for OpenClaw:", S["h3"]))
    for point in [
        "\u25b8  <b>Latency</b> \u2014 Players expect sub-200ms control response. Underpowered hardware adds jitter and lag.",
        "\u25b8  <b>Video streaming</b> \u2014 720p/1080p live feeds consume real CPU cycles. Encoding on weak hardware drops frames.",
        "\u25b8  <b>AI features</b> \u2014 Prize detection, chat bots, and image generation all require compute headroom.",
        "\u25b8  <b>Uptime</b> \u2014 A claw machine that crashes mid-game loses players permanently. Thermal and power stability matter.",
        "\u25b8  <b>Cost efficiency</b> \u2014 The wrong hosting choice can quietly cost you $100+/month more than necessary.",
    ]:
        elements.append(Paragraph(point, S["bullet"]))

    elements.append(spacer(6))
    elements.append(TipBox(
        "<b>Who is this guide for?</b>  Hobbyists building their first OpenClaw machine, "
        "small business owners adding interactive experiences, and developers who want to "
        "self-host without overspending. No prior hardware expertise required.",
        cw
    ))
    return elements


def section_specs(S, cw):
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("2. Minimum vs Recommended Specs", S["h1"]))
    elements.append(heading_bar())
    elements.append(Paragraph(
        "The table below shows the hardware floor (it will run, but expect limitations) versus "
        "the sweet spot for a smooth experience. Going above \u201cRecommended\u201d yields "
        "diminishing returns unless you are running local AI models.",
        S["body"]
    ))
    elements.append(spacer(6))

    data = [
        ["Component", "Minimum", "Recommended", "Notes"],
        ["CPU", "4-core / 4-thread\n(e.g. Intel i3-12100)", "8-core / 16-thread\n(e.g. Ryzen 7 5700X)",
         "Video encoding is the biggest CPU consumer"],
        ["RAM", "8 GB DDR4", "16\u201332 GB DDR4/DDR5",
         "16 GB is the sweet spot;\n32 GB if running local LLMs"],
        ["Storage", "64 GB SSD (SATA OK)", "256 GB+ NVMe SSD",
         "NVMe cuts boot & container\nstart times in half"],
        ["Network", "10 Mbps upload\nsymmetric", "50+ Mbps upload\nsymmetric",
         "Each 720p stream uses\n~3\u20135 Mbps upload"],
        ["GPU", "Not required*", "RTX 3060 12 GB\nor better",
         "*Required only for local AI;\nsee Section 3"],
        ["PSU", "Integrated / 200W", "500\u2013650W 80+ Bronze",
         "Only relevant for\ndesktop/custom builds"],
    ]
    elements.append(make_table(data, col_widths=[80, 115, 120, 185]))
    elements.append(spacer(8))
    elements.append(TipBox(
        "<b>Pro tip:</b>  If you are buying used hardware, prioritize a good SSD over extra RAM. "
        "A machine with 8 GB RAM and an NVMe SSD will feel faster than 16 GB RAM with a spinning hard drive. "
        "You can always add RAM later.",
        cw
    ))
    elements.append(spacer(6))
    elements.append(Paragraph("Understanding the bottlenecks", S["h3"]))
    elements.append(Paragraph(
        "OpenClaw\u2019s primary workloads are (1) real-time video encoding via FFmpeg/GStreamer, "
        "(2) a Node.js or Python web server handling WebSocket connections, and (3) GPIO or serial "
        "communication with motor controllers. Workload #1 dominates CPU usage\u2014a single 1080p "
        "H.264 stream can saturate two cores. If you plan to run multiple cameras or add overlay "
        "processing, budget for the recommended tier.",
        S["body"]
    ))
    return elements


def section_gpu_vs_cpu(S, cw):
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("3. GPU vs CPU Trade-offs", S["h1"]))
    elements.append(heading_bar())

    elements.append(Paragraph("When you need a GPU", S["h2"]))
    elements.append(Paragraph(
        "A dedicated GPU is <b>not</b> required to run a basic OpenClaw setup. However, the "
        "following use cases make a GPU essential:",
        S["body"]
    ))
    for item in [
        "\u25b8  <b>Local image generation</b> \u2014 Stable Diffusion, Flux, or ComfyUI for custom prize images or marketing content. Minimum VRAM: 8 GB (12 GB recommended).",
        "\u25b8  <b>Local LLM inference</b> \u2014 Running Llama 3, Mistral, or similar models for an AI chat assistant on your claw machine\u2019s web interface. Minimum VRAM: 12 GB for 7B-parameter models.",
        "\u25b8  <b>Computer vision</b> \u2014 Real-time prize detection, claw position tracking, or player gesture recognition using YOLO or MediaPipe with CUDA acceleration.",
        "\u25b8  <b>Hardware-accelerated video encoding</b> \u2014 NVENC offloads H.264/H.265 encoding from the CPU, freeing cores for other tasks. Useful when streaming multiple cameras simultaneously.",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(6))
    elements.append(Paragraph("When CPU-only is fine", S["h2"]))
    for item in [
        "\u25b8  <b>Standard claw operation</b> \u2014 Single-camera streaming, web server, motor control. A 4-core CPU handles this without breaking a sweat.",
        "\u25b8  <b>Text-based bots & automation</b> \u2014 Chat moderation, Twitch integration, queue management, and API calls are all CPU-light.",
        "\u25b8  <b>Cloud AI offloading</b> \u2014 If you call OpenAI, Anthropic, or Replicate APIs instead of running models locally, your server only needs to handle HTTP requests.",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(8))
    elements.append(Paragraph("GPU Recommendations", S["h2"]))
    gpu_data = [
        ["GPU", "VRAM", "Use Case", "Used Price (2026)"],
        ["NVIDIA RTX 3060", "12 GB", "Best entry point for local AI", "$150\u2013$200"],
        ["NVIDIA RTX 3090", "24 GB", "13B+ LLMs, heavy Stable Diffusion", "$500\u2013$650"],
        ["NVIDIA RTX 4060 Ti", "16 GB", "Efficient, low power, good for 24/7", "$280\u2013$350"],
        ["NVIDIA RTX 4090", "24 GB", "Overkill for most; great for Wan2.1 video", "$1,200\u2013$1,500"],
        ["AMD RX 7900 XTX", "24 GB", "Good value but ROCm support is hit-or-miss", "$600\u2013$750"],
    ]
    elements.append(make_table(gpu_data, col_widths=[115, 60, 195, 130]))
    elements.append(spacer(8))
    elements.append(TipBox(
        "<b>Recommendation:</b>  For most OpenClaw builders who want local AI capability, the "
        "<b>RTX 3060 12 GB</b> is the best value in 2026. It handles Stable Diffusion, 7B LLMs, "
        "and NVENC encoding. Only step up to a 3090/4090 if you need video generation (Wan2.1/2.2) "
        "or 13B+ parameter models.",
        cw, accent=ACCENT_GREEN
    ))
    return elements


def section_hosting(S, cw):
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("4. Cloud vs Bare-Metal vs VPS", S["h1"]))
    elements.append(heading_bar())
    elements.append(Paragraph(
        "Your hosting choice is one of the highest-impact cost decisions. Here is an honest "
        "comparison of the three main approaches for running an OpenClaw instance.",
        S["body"]
    ))
    elements.append(spacer(4))

    data = [
        ["Factor", "Cloud VPS", "Dedicated / Bare Metal", "Home Server"],
        ["Monthly cost", "$20\u2013$50/mo", "$40\u2013$100/mo", "$0/mo (after purchase)"],
        ["Setup difficulty", "Easy (5\u201315 min)", "Medium (30\u201360 min)", "Hard (2\u20134 hours)"],
        ["Performance", "Shared CPU, variable", "Full dedicated hardware", "Full dedicated hardware"],
        ["GPU access", "Expensive add-on", "Available (Hetzner, OVH)", "Your own card"],
        ["Scaling", "Instant", "Hours to days", "Buy more hardware"],
        ["Uptime SLA", "99.9%+", "99.9%+", "Depends on you"],
        ["Latency control", "Datacenter location", "Datacenter location", "Your ISP quality"],
        ["Best for", "Getting started, testing", "Production, 24/7 uptime", "Budget builds, AI work"],
    ]
    elements.append(make_table(data, col_widths=[100, 133, 133, 133]))
    elements.append(spacer(10))

    elements.append(Paragraph("Provider Comparison", S["h2"]))
    provider_data = [
        ["Provider", "Type", "Spec Example", "Monthly Cost", "Best For"],
        ["DigitalOcean", "VPS", "4 vCPU, 8 GB RAM, 160 GB SSD", "$48", "Beginners, US/EU"],
        ["Hetzner Cloud", "VPS", "4 vCPU, 8 GB RAM, 160 GB SSD", "\u20ac15 (~$17)", "Budget VPS"],
        ["Hetzner Dedicated", "Bare Metal", "Ryzen 5 3600, 64 GB, 2\u00d7512 GB NVMe", "\u20ac39 (~$44)", "Best value overall"],
        ["OVH Dedicated", "Bare Metal", "Xeon E-2386G, 32 GB, 2\u00d74 TB", "\u20ac55 (~$62)", "EU, storage-heavy"],
        ["AWS EC2 (c6i.xlarge)", "Cloud", "4 vCPU, 8 GB RAM, EBS", "$125+", "Enterprise, scaling"],
        ["GCP (e2-standard-4)", "Cloud", "4 vCPU, 16 GB RAM", "$100+", "GCP ecosystem"],
    ]
    elements.append(make_table(provider_data, col_widths=[95, 72, 165, 75, 93]))
    elements.append(spacer(8))

    elements.append(TipBox(
        "<b>Our pick:</b>  <b>Hetzner Dedicated Server Auction</b> \u2014 you can get a Ryzen 5/7 "
        "with 64 GB RAM and NVMe storage for \u20ac35\u201345/month. That is 3\u20135x cheaper than "
        "equivalent AWS/GCP instances. For OpenClaw, where you need consistent CPU performance "
        "for video encoding, dedicated beats shared every time.",
        cw, accent=ACCENT_GREEN
    ))
    elements.append(spacer(6))
    elements.append(TipBox(
        "<b>When to use a home server:</b>  If you already have a PC with decent specs sitting "
        "idle, running OpenClaw on it costs nothing monthly. The trade-off is you are responsible "
        "for uptime, power, cooling, and your ISP\u2019s upload bandwidth. Great for development "
        "and AI-heavy workloads where GPU cloud pricing is brutal.",
        cw, accent=ACCENT_YELLOW
    ))
    return elements


def section_builds(S, cw):
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("5. Recommended Builds", S["h1"]))
    elements.append(heading_bar())
    elements.append(Paragraph(
        "Three concrete hardware configurations, tested and validated for OpenClaw. Prices reflect "
        "US used/refurbished market as of early 2026.",
        S["body"]
    ))
    elements.append(spacer(6))

    # Budget build
    elements.append(Paragraph("Budget Build: $200\u2013$400", S["h2"]))
    elements.append(Paragraph(
        "Ideal for a first build, testing, or deployments where AI features are handled by cloud APIs.",
        S["body"]
    ))
    budget_data = [
        ["Component", "Option A: Mini PC", "Option B: Raspberry Pi 5"],
        ["Platform", "HP/Lenovo/Dell mini PC (used)", "Raspberry Pi 5 (8 GB)"],
        ["CPU", "Intel i5-8500T or similar (6C/6T)", "Broadcom BCM2712 (4C/4T)"],
        ["RAM", "16 GB DDR4 (upgrade if 8 GB)", "8 GB LPDDR4X"],
        ["Storage", "256 GB NVMe SSD", "128 GB microSD + USB SSD"],
        ["Network", "Gigabit Ethernet built-in", "Gigabit Ethernet built-in"],
        ["GPU", "Intel UHD 630 (no local AI)", "VideoCore VII (no local AI)"],
        ["Power draw", "35\u201365W", "5\u201312W"],
        ["Estimated cost", "$180\u2013$280", "$120\u2013$180 (with case & SSD)"],
    ]
    elements.append(make_table(budget_data, col_widths=[100, 200, 200]))
    elements.append(spacer(6))
    elements.append(TipBox(
        "<b>Budget tip:</b>  eBay, Amazon Renewed, and local electronics recyclers often have "
        "corporate-lease mini PCs for $100\u2013$150. Add a $30 NVMe SSD and you have a solid "
        "OpenClaw server for under $200.",
        cw
    ))

    elements.append(spacer(10))

    # Mid-range build
    elements.append(Paragraph("Mid-range Build: $500\u2013$800", S["h2"]))
    elements.append(Paragraph(
        "A capable all-around machine. Handles video encoding, multiple cameras, and can run "
        "lightweight local AI with an optional GPU.",
        S["body"]
    ))
    mid_data = [
        ["Component", "Option A: Refurb Workstation", "Option B: Intel NUC / Beelink"],
        ["Platform", "Dell Optiplex 7080 / HP Z2 (used)", "Beelink SER7 or Intel NUC 13 Pro"],
        ["CPU", "Intel i7-10700 (8C/16T)", "AMD Ryzen 7 7840HS (8C/16T)"],
        ["RAM", "32 GB DDR4", "32 GB DDR5"],
        ["Storage", "512 GB NVMe SSD", "500 GB NVMe SSD"],
        ["GPU", "Optional: GTX 1660 Super (6 GB)", "Integrated Radeon 780M"],
        ["Power draw", "80\u2013200W", "45\u201365W"],
        ["Estimated cost", "$350\u2013$550 (+ $80\u2013120 for GPU)", "$500\u2013$700"],
    ]
    elements.append(make_table(mid_data, col_widths=[100, 200, 200]))

    elements.append(PageBreak())

    # Power user build
    elements.append(Paragraph("Power User Build: $1,000\u2013$2,000", S["h2"]))
    elements.append(Paragraph(
        "For serious operators who want local AI (image generation, LLMs, computer vision) "
        "alongside full OpenClaw operation. No cloud API costs.",
        S["body"]
    ))
    power_data = [
        ["Component", "Recommendation"],
        ["CPU", "AMD Ryzen 7 5700X or Ryzen 5 7600X ($130\u2013$180)"],
        ["Motherboard", "B550 or B650 ATX with PCIe 4.0 x16 ($80\u2013$130)"],
        ["RAM", "32 GB DDR4-3600 or DDR5-5600 ($60\u2013$100)"],
        ["GPU", "NVIDIA RTX 3060 12 GB ($150\u2013$200) or RTX 3090 ($500\u2013$650)"],
        ["Storage", "1 TB NVMe Gen4 SSD ($60\u2013$80)"],
        ["PSU", "650W 80+ Bronze ($50\u2013$70)"],
        ["Case", "Any mid-tower with good airflow ($40\u2013$60)"],
        ["Cooling", "Tower air cooler, e.g. Thermalright PA120 ($25\u2013$35)"],
        ["Total (RTX 3060)", "$595\u2013$855"],
        ["Total (RTX 3090)", "$945\u2013$1,305"],
    ]
    elements.append(make_table(power_data, col_widths=[120, 380]))
    elements.append(spacer(8))
    elements.append(TipBox(
        "<b>Power user tip:</b>  If you go with a 3090, ensure your case has adequate airflow\u2014"
        "the card pulls 350W under load and throttles quickly in cramped enclosures. A mesh-front "
        "case with 2\u20133 intake fans is non-negotiable for 24/7 operation.",
        cw, accent=ACCENT_YELLOW
    ))
    return elements


def section_os_setup(S, cw):
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("6. Operating System Setup", S["h1"]))
    elements.append(heading_bar())

    elements.append(Paragraph(
        "We recommend <b>Ubuntu 22.04 LTS</b> or <b>Ubuntu 24.04 LTS</b> for OpenClaw deployments. "
        "Both have long-term support, excellent driver compatibility, and the largest ecosystem of "
        "tutorials and community help. Debian 12 is a solid alternative if you prefer minimal installs.",
        S["body"]
    ))
    elements.append(spacer(4))
    elements.append(Paragraph("Initial Setup Steps", S["h2"]))
    for step in [
        "\u25b8  Flash Ubuntu Server (or Desktop if you want a GUI) to a USB drive using Balena Etcher or Rufus.",
        "\u25b8  Install with LVM and full-disk encryption if the machine stores any user data.",
        "\u25b8  After first boot: <font face='Courier' size=9>sudo apt update && sudo apt upgrade -y</font>",
        "\u25b8  Install Docker and Docker Compose \u2014 OpenClaw runs best in containers.",
        "\u25b8  Install NVIDIA drivers if using a GPU: <font face='Courier' size=9>sudo apt install nvidia-driver-550</font>",
        "\u25b8  Install nvidia-container-toolkit for GPU passthrough to Docker containers.",
    ]:
        elements.append(Paragraph(step, S["bullet"]))

    elements.append(spacer(8))
    elements.append(Paragraph("Security Hardening Checklist", S["h2"]))
    elements.append(Paragraph(
        "If your OpenClaw server is internet-facing (and it probably is), these steps are not "
        "optional\u2014they are essential.",
        S["body"]
    ))
    elements.append(spacer(4))

    security_data = [
        ["#", "Action", "Command / Detail"],
        ["1", "Disable root SSH login", "Set PermitRootLogin no in /etc/ssh/sshd_config"],
        ["2", "Use SSH key authentication only", "Set PasswordAuthentication no, add your public key"],
        ["3", "Change default SSH port", "Set Port 2222 (or any non-standard port)"],
        ["4", "Enable UFW firewall", "sudo ufw allow 2222/tcp && sudo ufw enable"],
        ["5", "Allow only required ports", "HTTP (80), HTTPS (443), SSH, and your app ports"],
        ["6", "Install fail2ban", "sudo apt install fail2ban \u2014 blocks brute-force attempts"],
        ["7", "Enable automatic security updates", "sudo apt install unattended-upgrades"],
        ["8", "Set up log monitoring", "Install Netdata or Grafana agent for alerts"],
    ]
    elements.append(make_table(security_data, col_widths=[25, 160, 315]))
    elements.append(spacer(8))
    elements.append(TipBox(
        "<b>Critical:</b>  Steps 1\u20133 should be done within minutes of first boot. Automated "
        "bots scan for new servers constantly. An exposed SSH port with password auth will receive "
        "brute-force attempts within hours.",
        cw, accent=ACCENT_RED
    ))
    return elements


def section_network(S, cw):
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("7. Network & Remote Access", S["h1"]))
    elements.append(heading_bar())
    elements.append(Paragraph(
        "Getting your OpenClaw machine accessible from the internet is often the trickiest part "
        "of a home or office deployment. Here are three proven approaches, ranked by complexity.",
        S["body"]
    ))
    elements.append(spacer(6))

    net_data = [
        ["Method", "Difficulty", "Cost", "Pros", "Cons"],
        ["Cloudflare Tunnel", "Easy", "Free", "No port forwarding needed,\nDDoS protection, free SSL",
         "Requires Cloudflare account,\nslightly higher latency"],
        ["Tailscale / WireGuard", "Easy", "Free (personal)", "Encrypted mesh VPN,\nworks behind any NAT",
         "Peers need Tailscale client;\nnot ideal for public access"],
        ["Port Forwarding\n+ Dynamic DNS", "Medium", "Free", "Direct connection,\nlowest latency",
         "Exposes your IP, requires\nrouter config, ISP may block"],
        ["Reverse Proxy\n(nginx + Let's Encrypt)", "Medium", "Free\n(+ VPS cost)", "Professional setup,\nfull control",
         "Requires a VPS as entry\npoint, more maintenance"],
    ]
    elements.append(make_table(net_data, col_widths=[95, 60, 70, 145, 130]))
    elements.append(spacer(8))

    elements.append(Paragraph("Recommended Setup for Home Servers", S["h2"]))
    elements.append(Paragraph(
        "For most home deployments, we recommend <b>Cloudflare Tunnel</b> as the primary access "
        "method, with <b>Tailscale</b> as a backup for SSH management. This combination gives you:",
        S["body"]
    ))
    for item in [
        "\u25b8  No router port forwarding configuration needed",
        "\u25b8  Your home IP address stays private",
        "\u25b8  Free SSL/TLS certificates via Cloudflare",
        "\u25b8  DDoS protection included at the free tier",
        "\u25b8  Tailscale SSH access from anywhere, even on mobile",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(6))
    elements.append(Paragraph("Dynamic DNS (if using port forwarding)", S["h2"]))
    elements.append(Paragraph(
        "If your ISP assigns a dynamic IP address (most residential connections do), you need a "
        "Dynamic DNS service to keep a stable hostname pointed at your server. Free options include "
        "DuckDNS, No-IP, and Dynu. Most routers have a built-in DDNS client\u2014check your router\u2019s "
        "admin panel under WAN or Internet settings.",
        S["body"]
    ))
    elements.append(spacer(6))
    elements.append(TipBox(
        "<b>Bandwidth reality check:</b>  A single 720p OpenClaw stream uses 3\u20135 Mbps upload. "
        "If your home internet only provides 10 Mbps upload, you can serve 2\u20133 simultaneous "
        "viewers at most. For larger audiences, consider using a relay service or upgrading to a "
        "business-class connection.",
        cw
    ))
    return elements


def section_checklist(S, cw):
    elements = []
    elements.append(PageBreak())
    elements.append(Paragraph("8. Quick-Start Checklist", S["h1"]))
    elements.append(heading_bar())
    elements.append(Paragraph(
        "A single-page reference for getting your OpenClaw hardware up and running. "
        "Tear this page out (or bookmark it) and check items off as you go.",
        S["body"]
    ))
    elements.append(spacer(6))

    elements.append(Paragraph("Hardware", S["h2"]))
    for item in [
        "\u2610  Choose your tier: Budget ($200\u2013$400), Mid-range ($500\u2013$800), or Power ($1,000\u2013$2,000)",
        "\u2610  Acquire machine (buy new, buy used, or repurpose existing hardware)",
        "\u2610  Verify: 4+ CPU cores, 8+ GB RAM, SSD storage, Gigabit Ethernet",
        "\u2610  If local AI is planned: confirm GPU has 12+ GB VRAM (NVIDIA recommended)",
        "\u2610  Test all hardware components before mounting near claw machine",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(4))
    elements.append(Paragraph("Operating System & Software", S["h2"]))
    for item in [
        "\u2610  Install Ubuntu 22.04 or 24.04 LTS (Server edition for headless setups)",
        "\u2610  Run full system update: apt update && apt upgrade",
        "\u2610  Install Docker and Docker Compose",
        "\u2610  If GPU: install NVIDIA driver 550+ and nvidia-container-toolkit",
        "\u2610  Clone the OpenClaw repository and follow container setup docs",
        "\u2610  Verify the web interface loads on localhost",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(4))
    elements.append(Paragraph("Security", S["h2"]))
    for item in [
        "\u2610  Disable root SSH login & enable key-only authentication",
        "\u2610  Change SSH port to a non-standard number",
        "\u2610  Enable UFW firewall, allow only necessary ports",
        "\u2610  Install fail2ban for brute-force protection",
        "\u2610  Enable unattended security updates",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(4))
    elements.append(Paragraph("Network & Access", S["h2"]))
    for item in [
        "\u2610  Decide: Cloudflare Tunnel (recommended) vs port forwarding vs VPS proxy",
        "\u2610  Set up chosen access method and test from an external network",
        "\u2610  Install Tailscale for remote SSH management",
        "\u2610  Configure Dynamic DNS if using port forwarding",
        "\u2610  Test video stream latency from a remote device",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(4))
    elements.append(Paragraph("Go Live", S["h2"]))
    for item in [
        "\u2610  Connect claw machine hardware (motors, limit switches, camera)",
        "\u2610  Calibrate claw movement range and speed in OpenClaw config",
        "\u2610  Run a full end-to-end test: web UI \u2192 claw movement \u2192 camera feed",
        "\u2610  Set up monitoring/alerting (Netdata, Uptime Kuma, or similar)",
        "\u2610  Share your claw machine URL and start accepting players!",
    ]:
        elements.append(Paragraph(item, S["bullet"]))

    elements.append(spacer(14))
    elements.append(thin_rule())
    elements.append(spacer(6))
    elements.append(Paragraph("Need help with setup?", S["h2"]))
    elements.append(Paragraph(
        "Automatyn offers professional OpenClaw deployment services\u2014from hardware selection "
        "to full remote setup. We also build custom TikTok and social media automation pipelines "
        "for claw machine operators.",
        S["body"]
    ))
    elements.append(spacer(4))
    for item in [
        "\u25b8  Visit us: <b>automatyn.github.io</b>",
        "\u25b8  Book a free consultation on our website",
        "\u25b8  Follow us on TikTok for OpenClaw builds, tips, and giveaways",
    ]:
        elements.append(Paragraph(item, S["bullet"]))
    elements.append(spacer(6))
    elements.append(TipBox(
        "Thank you for reading the 2026 OpenClaw Hardware Guide. If you found this useful, "
        "share it with a friend who is building their own claw machine. \u2014 The Automatyn Team",
        cw, accent=PURPLE
    ))
    return elements


# ── Main build ──────────────────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        topMargin=68,
        bottomMargin=52,
        leftMargin=54,
        rightMargin=54,
    )

    S = build_styles()
    cw = doc.width  # content width

    story = []

    # Cover page placeholder — the real cover is drawn by on_first_page
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    story.extend(section_introduction(S, cw))
    story.extend(section_specs(S, cw))
    story.extend(section_gpu_vs_cpu(S, cw))
    story.extend(section_hosting(S, cw))
    story.extend(section_builds(S, cw))
    story.extend(section_os_setup(S, cw))
    story.extend(section_network(S, cw))
    story.extend(section_checklist(S, cw))

    doc.build(
        story,
        onFirstPage=on_first_page,
        onLaterPages=on_page,
    )
    print(f"PDF generated: {OUTPUT_PATH}")
    print(f"Size: {os.path.getsize(OUTPUT_PATH) / 1024:.0f} KB")


if __name__ == "__main__":
    build_pdf()
