import io
import pandas as pd
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter

# Config
TEMPLATE_FILE = "/Users/noahcoyner/Desktop/placeholder.PDF"
OUTPUT_FILE = "/Users/noahcoyner/Desktop/placeholderOutput.PDF"
CSV_FILE = "/Users/noahcoyner/Desktop/clean_room_date.csv"

# Load CSV data
df = pd.read_csv(CSV_FILE)
dates = df["cycle_1_date"].to_list()
rooms = df["room_num"].to_list()

# PDF overlay build
class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.set_auto_page_break(auto=False)

    def draw_checklist(self, page, box_size=2):
        self.set_font("Arial", size=10)
        
            #FIRST PAGE
        if page == 1:
            items = [
                # Entry checks
                (11.3, 122.8, "", True),
                (11.3, 133, "", True),
                (11.4, 140.5, "", True),
                (11.4, 148.3, "", True),
                (11.4, 153.3, "", True),
                (11.5, 161, "", True),

                # Bedroom Checks
                (115.15, 122.8, "", True),
                (115.165, 127.2, "", True),
                (115.16, 132.4, "", True),
                (115.3, 136.8, "", True),
                (115.2, 142, "", True),
                (115.4, 146.5, "", True),
                (115.21, 154, "", True),
                (115.25, 158.5, "", True),
                (115.2, 163.5, "", True),
                (115.2, 168.1, "", True),
                (115.2, 173.3, "", True),

                # Bathroom Checks
                (11.32, 176.5, "", True), #1
                (11.32, 181.8, "", True), #2
                (11.32, 186.1, "", True), #3
                (11.32, 191, "", True), #4
                (11.32, 195.8, "", True), #5
                (11.32, 200.8, "", True), #6
                (11.32, 205.5, "", True), #7
                (11.32, 213, "", True), #8
                (11.32, 217.8, "", True), #9
                (11.32, 222.5, "", True), #10
                (11.32, 227, "", True), #11
                (11.32, 231.9, "", True), #12
                (11.32, 239.5, "", True), #13
                (11.32, 247.2, "", True), #14
                (11.32, 254.8, "", True), #15
                (11.32, 259.5, "", True), #16
                
                #HVAC Checks
                (115.2, 214.1, "", True), #1
                (115.23, 257.3, "", True), #2
            ]
            #SECOND PAGE
        elif page == 2:
            items = [

                #Fire, Life & Safety Checks
                (11.4, 39.5, "", True), #1
                (11.4, 52.9, "", True), #2
                (11.35, 62.5, "", True), #3
                (11.4, 67.5, "", True), #4

                #Suites / Extended Stay Checks
                (114, 39.5, "", True), #1
                (114, 44, "", True), #2
                (113.9, 48.7, "", True), #3
                (113.9, 53.5, "", True), #4
                (113.9, 58.7, "", True), #5
                (113.9, 63.2, "", True), #6
                (113.9, 68.2, "", True), #7
                (113.9, 72.8, "", True), #8

            ]
        else:
            sys.exit("No page selected error")
        for x, y, label, checked in items:
            if checked:
                self.set_fill_color(0, 0, 0)
                self.rect(x, y, box_size, box_size, style="F")
            else:
                self.rect(x, y, box_size, box_size, style="D")
            self.set_xy(x + box_size + 2, y - 0.5)
            self.cell(0, box_size + 1, label, border=0)

    def build_page1(self, room, date):
        self.add_page()
        self.set_font("Arial", size=10)
        self.set_xy(34, 75)
        self.cell(50, 8, str(room), border=0)
        self.set_xy(84, 75)
        self.cell(0, 8, str(date), border=0)
        self.set_xy(155, 75)
        self.set_font("Courier", size=10)
        self.cell(0, 8, "Noah Coyner", border=0)
        self.draw_checklist(1)

    def build_page2(self, room, date):
        self.add_page()
        self.set_font("Arial", size=10)

        self.set_xy(120, 9)
        self.cell(50, 8, f"{room}", border=0)
        self.set_xy(120, 13.9)
        self.cell(0, 8, str(date), border=0)
        self.draw_checklist(2)


# Now execute:
writer = PdfWriter()
for room, date in zip(rooms, dates):
    # Build overlay with both pages
    overlay_pdf = PDF()
    overlay_pdf.build_page1(room, date)
    overlay_pdf.build_page2(room, date)

    # Encode in string (debug) to ensure output is string format on template merge (edge case??!!!)
    overlay_bytes = overlay_pdf.output(dest="S")
    if isinstance(overlay_bytes, str):
        overlay_bytes = overlay_bytes.encode("latin1")

    # Memory stream consistency
    overlay_reader = PdfReader(io.BytesIO(overlay_bytes))

    # Read template fresh each loop
    base_reader = PdfReader(TEMPLATE_FILE)

    # MERGE time -- each overlay page with corresponding template page
    for page_index in range(2):
        base_page = base_reader.pages[page_index]
        base_page.merge_page(overlay_reader.pages[page_index])
        writer.add_page(base_page)

# Save
with open(OUTPUT_FILE, "wb") as f:
    writer.write(f)

#Add more to print so we can debug in console?
print(f"PDF created: {OUTPUT_FILE}")
