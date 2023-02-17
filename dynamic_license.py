# Activate shareable licenses using pywinauto
# Requirements: CATIA runnning and screen resolution height > 951px

from pywinauto.application import Application
from pywinauto import mouse
from pywinauto.keyboard import send_keys
from time import sleep

# Licenses to activate
licenses = ["PEO", "KIN", "GAS", "FMD"]

# Dictionary of scroll position
d = {
    "AMG": 0,
    "ANR": 0,
    "BK2": 0,
    "C12": 0,
    "CBD": 0,
    "CCV": 0,
    "CCW": 0,
    "CD1": 0,
    "CFM": 0,
    "CFO": 0,
    "CLA": 38,
    "CNA": 38,
    "CPB": 38,
    "CPE": 38,
    "CPM": 38,
    "CPR": 38,
    "CT5": 38,
    "DL1": 38,
    "DSS": 38,
    "EC1": 38,
    "ECR": 77,
    "EHF": 77,
    "EHI": 77,
    "ELB": 77,
    "ELD": 77,
    "EQT": 77,
    "EST": 77,
    "EWE": 77,
    "EWR": 77,
    "FAR": 77,
    "FIT": 115,
    "FLX": 115,
    "FM1": 115,
    "FMD": 115,
    "FMP": 115,
    "FMS": 115,
    "FR1": 115,
    "FSK": 115,
    "FSO": 115,
    "FSP": 115,
    "GAS": 153,
    "GDY": 153,
    "GPS": 153,
    "HAA": 153,
    "HAC": 153,
    "HBR": 153,
    "HGR": 153,
    "HME": 153,
    "HPA": 153,
    "HPC": 153,
    "HTC": 192,
    "HVA": 192,
    "HVD": 192,
    "IAE": 192,
    "ICM": 192,
    "IEX": 192,
    "IMA": 192,
    "KIN": 192,
    "LMG": 192,
    "MBG": 192,
    "MLG": 230,
    "MMG": 230,
    "MPA": 230,
    "MPG": 230,
    "MSG": 230,
    "MTD": 230,
    "NCG": 230,
    "NVG": 230,
    "PEO": 230,
    "PFD": 230,
    "PHS": 268,
    "PID": 268,
    "PIP": 268,
    "PLO": 268,
    "PMG": 268,
    "PSO": 268,
    "PX1": 268,
    "QSR": 268,
    "RCD": 268,
    "RSO": 268,
    "RTR": 307,
    "SDD": 307,
    "SDI": 307,
    "SFD": 307,
    "SH1": 307,
    "SMD": 307,
    "SMG": 307,
    "SR1": 307,
    "SRF": 307,
    "SRT": 307,
    "SSR": 345,
    "STC": 345,
    "STL": 345,
    "SXT": 345,
    "TG1": 345,
    "TUB": 345,
    "TUD": 345,
    "VOA": 345,
    "WAV": 345,
    "WGD": 345,
    "WS1": 350,
}

# Connect to CATIA
app = Application()
app.connect(title="CATIA V5")
catia = app.catia_v5
catia.set_focus()

# Tools -> Options...
send_keys("%t")
send_keys("o")

# Connect to Options
app = Application().connect(title="Options", timeout=30)
window = app.Dialog
window.move_window(x=-7, y=0, width=None, height=951, repaint=True)

# Get position of window
rect = window.rectangle()

# Click on "General" in TreeView
mouse.click(button="right", coords=(rect.left + 150, rect.top + 60))
send_keys("r")
mouse.click(button="left", coords=(rect.left + 50, rect.top + 70))

sleep(3)

# Click on "Shareable Products" tab
mouse.click(button="left", coords=(rect.left + 400, rect.top + 54))

# Scroll to check box
option_frame = window.OptionsFrame
option_frame_rect = option_frame.rectangle()

horizontal_pos = option_frame_rect.right - 10
vertical_start_pos = option_frame_rect.top + 30


for license in licenses:
	
    movement = d[license]
    vertical_end_pos = vertical_start_pos + movement

    mouse.press(button="left", coords=(horizontal_pos, vertical_start_pos))
    mouse.release(button="left", coords=(horizontal_pos, vertical_end_pos))

    # Check
    check_box_name = f"Lock{license}_prdCheckBox"
    window[check_box_name].check_by_click()

    if window.texts()[0] == "Licensing Warning":
        window.OK.click()
        if window.texts()[0] == "License Manager":
            window.OK.click()

        print(f"ERROR: {license} license not definied!")

    mouse.press(button="left", coords=(horizontal_pos, vertical_end_pos))
    mouse.release(button="left", coords=(horizontal_pos, vertical_start_pos))

window.OK.click()
