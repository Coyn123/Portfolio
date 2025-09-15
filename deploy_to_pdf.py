import io
import pandas as pd
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter

# Config
TEMPLATE_FILE = "C:/Users/noahc/Desktop/placeholder.PDF"
OUTPUT_FILE = "C:/Users/noahc/Desktop/placeholderOutput.PDF"
CSV_FILE = "C:/Users/noahc/Desktop/clean_room_date.csv"

# Load CSV data
df = pd.read_csv(CSV_FILE)
dates = df["cycle_1_date"].to_list()
rooms = df["room_num"].to_list()

# PDF overlay build
class PDF(FPDF):
    def __init__(self):
        # Portrait, millimeters, US Letter to match template
        super().__init__(orientation="P", unit="mm", format="Letter")

    def draw_checklist(self, box_size=4):
        self.set_font("Helvetica", size=10)
        items = [
            (20, 50, "", True), (20, 60, "", True), (20, 70, "", True), (20, 80, "", True),
            (40, 50, "", True), (40, 60, "", True), (40, 70, "", True), (40, 80, "", True),
            (60, 50, "", True), (60, 60, "", True), (60, 70, "", True), (60, 80, "", True),
            (80, 50, "", True), (80, 60, "", True), (80, 70, "", True), (80, 80, "", True),
        ]
        for x, y, label, checked in items:
            if checked:
                self.set_fill_color(0, 0, 0)
                self.rect(x, y, box_size, box_size, style="F")
            else:
                self.rect(x, y, box_size, box_size, style="D")
            self.set_xy(x + box_size + 2, y - 0.5)
            self.cell(0, box_size + 1, label, border=0)

    def build_page(self, room, date):
        self.add_page()
        self.set_font("Helvetica", size=10)
        self.set_xy(50, 5)
        self.cell(50, 8, str(room), border=0)
        self.set_xy(145, 5)
        self.cell(0, 8, str(date), border=0)
        self.draw_checklist()

# --- Merge logic: one writer, fresh template page each iteration ---
writer = PdfWriter()

for room, date in zip(rooms, dates):
    # 1) Build overlay with FPDF (Letter size so it aligns with template)
    overlay_pdf = PDF()
    overlay_pdf.build_page(room, date)

    overlay_bytes = overlay_pdf.output(dest="S")
    if isinstance(overlay_bytes, str):
        overlay_bytes = overlay_bytes.encode("latin1")

    overlay_stream = io.BytesIO(overlay_bytes)
    overlay_reader = PdfReader(overlay_stream)
    # 2) Read template fresh each loop to avoid cumulative mutations
    base_reader = PdfReader(TEMPLATE_FILE)
    base_page = base_reader.pages[0]

    # 3) Merge overlay onto the template page
    base_page.merge_page(overlay_reader.pages[0])

    # 4) Add merged page to the output writer
    writer.add_page(base_page)

# --- Save final multi-page PDF ---
with open(OUTPUT_FILE, "wb") as f:
    writer.write(f)

print(f"PDF created: {OUTPUT_FILE}")
