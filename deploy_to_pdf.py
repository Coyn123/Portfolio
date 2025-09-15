import pandas as pd
from fpdf import FPDF

#Config
TEMPLATE_FILE = "C:/Users/noahc/Desktop/placeholder.PDF"

OUTPUT_FILE = "C:/Users/noahc/Desktop/placeholderOutput.PDF"

df = pd.read_csv("C:/Users/noahc/Desktop/clean_room_date.csv")

dates = df["cycle_1_date"].to_list()

rooms  = df["room_num"].to_list()


#DRAW PDF DECLARATIONS
class PDF(FPDF):
    def header(self):
        margin_mm = 6.35  # 0.25 inch
        self.set_font("Helvetica", size=10)

        #Checklist
    def draw_checklist(self, box_size=4):
        self.set_font("Helvetica", size=10)

        # Hardcoded checklist items: (x, y, label, checked)
        items = [
            (20, 50, "", True),
            (20, 60, "", True),
            (20, 70, "", True),
            (20, 80, "", True),

            (40, 50, "", True),
            (40, 60, "", True),
            (40, 70, "", True),
            (40, 80, "", True),

            (60, 50, "", True),
            (60, 60, "", True),
            (60, 70, "", True),
            (60, 80, "", True),

            (80, 50, "", True),
            (80, 60, "", True),
            (80, 70, "", True),
            (80, 80, "", True),
        ]

        #Fill in the checked items or not
        for x, y, label, checked in items:
            if checked:
                self.set_fill_color(0, 0, 0)
                self.rect(x, y, box_size, box_size, style="F")
            else:
                self.rect(x, y, box_size, box_size, style="D")
            self.set_xy(x + box_size + 2, y - 0.5)
            self.cell(0, box_size + 1, label, border=0)

    #Build Dynamic Page, room_num -> cycle_1_date (1) per page
    def build_page(self, room, date):
        self.add_page()
        self.set_font("Helvetica", size=10)
        self.set_y(5)
        self.set_x(50)
        self.cell(50, 8, f"{str(room)}", border=0)
        self.set_y(5)
        self.set_x(145)
        self.cell(0, 8, f"{str(date)}", border=0)
        self.ln(5)

        # Checklist
        self.draw_checklist()

# FINAL BUILD
pdf = PDF()
for i in range(len(rooms)):
    pdf.build_page(rooms[i], dates[i])
pdf.output(OUTPUT_FILE)
