"""
Name: SampleID QR Generator
Description:
Author: Muhammad Karimi karimi.muhammad@epa.gov
Contact: Timothy Boe boe.timothy@epa.gov and Worth also right?
Requirements:
"""

# Import necessary packages
import os
import qrcode
import random

from datetime import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Import GUI packages
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

# Import Tkinter packages for file chooser
from tkinter import Tk
import tkinter.filedialog as filedialog

# Import fpdf for PDF creation
from fpdf import FPDF

# Set setup variables
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

""" This class is main class for GUI, its the main screen w/in which all other screens/widgets/buttons are located """


class MainScreenWidget(BoxLayout):
    file_settings_widget = None

    row_count = 0  # num of rows
    number_count = 1  # where the current number id is
    letter_count = 0  # where the current letter id is
    curr_preview_img_index = 0  # which image is being displayed in preview
    text_input_array = []  # 2d array of textinput fields to read from when creating/previewing
    used_random_values_array = []  # used to prevent random values from being repeated
    preview_images_array = [''] * 100  # array of images that are previewable
    uploaded_file_path = None  # file path for the uploaded file
    save_folder_path = None  # path to folder where files should be saved
    array_of_codes = []  # array of qr codes to be printed to PDF
    letter_array = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z", 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK',
                    'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA',
                    'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ',
                    'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG',
                    'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW',
                    'CX', 'CY', 'CZ', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM',
                    'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ', 'EA', 'EB', 'EC',
                    'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES',
                    'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ', 'FA', 'FB', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI',
                    'FJ', 'FK', 'FL', 'FM', 'FN', 'FO', 'FP', 'FQ', 'FR', 'FS', 'FT', 'FU', 'FV', 'FW', 'FX', 'FY',
                    'FZ', 'GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GJ', 'GK', 'GL', 'GM', 'GN', 'GO',
                    'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GV', 'GW', 'GX', 'GY', 'GZ', 'HA', 'HB', 'HC', 'HD', 'HE',
                    'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL', 'HM', 'HN', 'HO', 'HP', 'HQ', 'HR', 'HS', 'HT', 'HU',
                    'HV', 'HW', 'HX', 'HY', 'HZ', 'IA', 'IB', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IJ', 'IK',
                    'IL', 'IM', 'IN', 'IO', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IU', 'IV', 'IW', 'IX', 'IY', 'IZ', 'JA',
                    'JB', 'JC', 'JD', 'JE', 'JF', 'JG', 'JH', 'JI', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JO', 'JP', 'JQ',
                    'JR', 'JS', 'JT', 'JU', 'JV', 'JW', 'JX', 'JY', 'JZ', 'KA', 'KB', 'KC', 'KD', 'KE', 'KF', 'KG',
                    'KH', 'KI', 'KJ', 'KK', 'KL', 'KM', 'KN', 'KO', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KU', 'KV', 'KW',
                    'KX', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LJ', 'LK', 'LL', 'LM',
                    'LN', 'LO', 'LP', 'LQ', 'LR', 'LS', 'LT', 'LU', 'LV', 'LW', 'LX', 'LY', 'LZ', 'MA', 'MB', 'MC',
                    'MD', 'ME', 'MF', 'MG', 'MH', 'MI', 'MJ', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS',
                    'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI',
                    'NJ', 'NK', 'NL', 'NM', 'NN', 'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY',
                    'NZ', 'OA', 'OB', 'OC', 'OD', 'OE', 'OF', 'OG', 'OH', 'OI', 'OJ', 'OK', 'OL', 'OM', 'ON', 'OO',
                    'OP', 'OQ', 'OR', 'OS', 'OT', 'OU', 'OV', 'OW', 'OX', 'OY', 'OZ', 'PA', 'PB', 'PC', 'PD', 'PE',
                    'PF', 'PG', 'PH', 'PI', 'PJ', 'PK', 'PL', 'PM', 'PN', 'PO', 'PP', 'PQ', 'PR', 'PS', 'PT', 'PU',
                    'PV', 'PW', 'PX', 'PY', 'PZ', 'QA', 'QB', 'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QJ', 'QK',
                    'QL', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QU', 'QV', 'QW', 'QX', 'QY', 'QZ', 'RA',
                    'RB', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI', 'RJ', 'RK', 'RL', 'RM', 'RN', 'RO', 'RP', 'RQ',
                    'RR', 'RS', 'RT', 'RU', 'RV', 'RW', 'RX', 'RY', 'RZ', 'SA', 'SB', 'SC', 'SD', 'SE', 'SF', 'SG',
                    'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SQ', 'SR', 'SS', 'ST', 'SU', 'SV', 'SW',
                    'SX', 'SY', 'SZ', 'TA', 'TB', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TJ', 'TK', 'TL', 'TM',
                    'TN', 'TO', 'TP', 'TQ', 'TR', 'TS', 'TT', 'TU', 'TV', 'TW', 'TX', 'TY', 'TZ', 'UA', 'UB', 'UC',
                    'UD', 'UE', 'UF', 'UG', 'UH', 'UI', 'UJ', 'UK', 'UL', 'UM', 'UN', 'UO', 'UP', 'UQ', 'UR', 'US',
                    'UT', 'UU', 'UV', 'UW', 'UX', 'UY', 'UZ', 'VA', 'VB', 'VC', 'VD', 'VE', 'VF', 'VG', 'VH', 'VI',
                    'VJ', 'VK', 'VL', 'VM', 'VN', 'VO', 'VP', 'VQ', 'VR', 'VS', 'VT', 'VU', 'VV', 'VW', 'VX', 'VY',
                    'VZ', 'WA', 'WB', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WJ', 'WK', 'WL', 'WM', 'WN', 'WO',
                    'WP', 'WQ', 'WR', 'WS', 'WT', 'WU', 'WV', 'WW', 'WX', 'WY', 'WZ', 'XA', 'XB', 'XC', 'XD', 'XE',
                    'XF', 'XG', 'XH', 'XI', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XO', 'XP', 'XQ', 'XR', 'XS', 'XT', 'XU',
                    'XV', 'XW', 'XX', 'XY', 'XZ', 'YA', 'YB', 'YC', 'YD', 'YE', 'YF', 'YG', 'YH', 'YI', 'YJ', 'YK',
                    'YL', 'YM', 'YN', 'YO', 'YP', 'YQ', 'YR', 'YS', 'YT', 'YU', 'YV', 'YW', 'YX', 'YY', 'YZ', 'ZA',
                    'ZB', 'ZC', 'ZD', 'ZE', 'ZF', 'ZG', 'ZH', 'ZI', 'ZJ', 'ZK', 'ZL', 'ZM', 'ZN', 'ZO', 'ZP', 'ZQ',
                    'ZR', 'ZS', 'ZT', 'ZU', 'ZV', 'ZW', 'ZX', 'ZY', 'ZZ']

    def __init__(self, **kwargs):
        super(MainScreenWidget, self).__init__(**kwargs)
        Window.bind(on_request_close=self.exit)

    def preview_right(self):
        preview_image = self.ids.previewimage  # set the preview image
        if self.preview_images_array[self.curr_preview_img_index + 1] != '':
            self.curr_preview_img_index += 1  # if there is an img to the right, increment to go right
        preview_image.source = self.preview_images_array[self.curr_preview_img_index]  # set new img as preview img

    def preview_left(self):
        preview_image = self.ids.previewimage  # set the preview image
        if self.preview_images_array[self.curr_preview_img_index - 1] != '' and (self.curr_preview_img_index - 1) >= 0:
            self.curr_preview_img_index -= 1  # if there is an img to the left, decrement to go left
        preview_image.source = self.preview_images_array[self.curr_preview_img_index]  # set new img as preview img

    def set_preview(self):
        i = 0
        for row in self.text_input_array:
            qr_code_text = ""
            for col in row:
                if col == row[0]: continue
                if col == row[1]:
                    qr_code_text = f"{col.text}"
                else:
                    qr_code_text = f"{qr_code_text}-{col.text}"

                    # Replace any ids in the text with the appropriate sequential or random number/alphabet letter
                    if "#num_seq" in qr_code_text:  # replace user placeholder '#num_seq' w/number
                        qr_code_text = qr_code_text.replace("#num_seq", f"{self.number_count}")

                    if "#num_rand" in qr_code_text:  # replace user placeholder 'num_rand' w/rand num
                        rand_num = int(random.uniform(1, 1000))
                        qr_code_text = qr_code_text.replace("#num_rand", f"{rand_num}")

                    if "#alpha_seq" in qr_code_text:  # replace user placeholder '#alpha_seq' w/letter
                        qr_code_text = qr_code_text.replace("#alpha_seq", f"{self.letter_array[self.letter_count]}")

                    if "#alpha_rand" in qr_code_text:  # replace user placeholder '#alpha_rand' w/rand letter
                        rand_letter = random.choice(self.letter_array)
                        qr_code_text = qr_code_text.replace("#alpha_rand", f"{rand_letter}")

            # make QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )

            qr.add_data(qr_code_text)
            qr.make(fit=True)

            img = qr.make_image()
            file_name = f"{qr_code_text}.jpg"
            file_path = f"Temp/{file_name}"
            img.save(file_path)

            # Draw label on image
            img = Image.open(file_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial", 24)
            color = 0
            draw.text((37, 10), qr_code_text, font=font, fill=color)
            img.save(file_path)

            preview_image = self.ids.previewimage  # set the preview image
            preview_image.source = file_path

            self.preview_images_array[i] = file_path  # add the preview image filepath to the preview imgs array
            i += 1  # increment i so that the next preview image is saved in the correct index

        self.curr_preview_img_index = i  # the current preview image displayed is the last one that was created

    def create_popup(self):
        self.file_settings_widget = FileSettingsWidget()
        self.file_settings_widget.main_screen = self
        self.file_settings_widget.file_settings_popup = Popup(title="                             Are you sure you want to create?",
                                          content=self.file_settings_widget, size_hint=(None, None), size=(650, 240),
                                          auto_dismiss=True)
        self.file_settings_widget.file_settings_popup.open()
        return True

    def create(self):
        if self.uploaded_file_path is None or self.uploaded_file_path == "":
            t = datetime.now()
            csv_file_name = f"SampleIDQRCodes-{t.year}-{t.month}-{t.day}-{t.hour}_{t.minute}_{t.second}.csv"
            for row in self.text_input_array:
                # get # of codes to make and then run creation that many times
                num_codes = int(row[0].children[0].text)

                for _ in range(num_codes):
                    qr_code_text = ""
                    for col in row:
                        if col == row[0]: continue
                        if col == row[1]:
                            qr_code_text = f"{col.text}"
                        else:
                            qr_code_text = f"{qr_code_text}-{col.text}"

                    # Replace any ids in the text with the appropriate sequential or random number/alphabet letter
                    if "#num_seq" in qr_code_text:  # replace user placeholder '#num_seq' w/number
                        qr_code_text = qr_code_text.replace("#num_seq", f"{self.number_count}")
                        self.number_count += 1

                    if "#num_rand" in qr_code_text:  # replace user placeholder 'num_rand' w/rand num
                        rand_num = int(random.uniform(1, 1000))
                        while rand_num in self.used_random_values_array:
                            rand_num = int(random.uniform(1, 1000))
                        self.used_random_values_array.append(rand_num)
                        qr_code_text = qr_code_text.replace("#num_rand", f"{rand_num}")

                    if "#alpha_seq" in qr_code_text:  # replace user placeholder '#alpha_seq' w/letter
                        qr_code_text = qr_code_text.replace("#alpha_seq", f"{self.letter_array[self.letter_count]}")
                        self.letter_count += 1

                    if "#alpha_rand" in qr_code_text:  # replace user placeholder '#alpha_rand' w/rand letter
                        rand_letter = random.choice(self.letter_array)
                        while rand_letter in self.used_random_values_array:
                            rand_letter = random.choice(self.letter_array)
                        self.used_random_values_array.append(rand_letter)
                        qr_code_text = qr_code_text.replace("#alpha_rand", f"{rand_letter}")

                    if self.ids.gencsv.active:
                        self.generate_csv(csv_file_name, qr_code_text)

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4
                    )

                    qr.add_data(qr_code_text)
                    qr.make(fit=True)

                    img = qr.make_image()
                    file_name = f"{qr_code_text}.jpg"
                    if self.ids.individualcodes.active:
                        if self.save_folder_path is not None and self.save_folder_path is not "":
                            file_name = f"{self.save_folder_path}/{file_name}"
                    else:
                        file_name = f"Temp/{file_name}"
                    img.save(file_name)  # save qr code as a jpg file

                    # Draw label on image
                    img = Image.open(file_name)
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype("arial", 21)
                    color = 0
                    draw.text((37, -6), f"{qr_code_text[:32]}\n{qr_code_text[32:64]}\n{qr_code_text[64:]}", font=font, fill=color)
                    img.save(file_name)

                    self.array_of_codes.append(file_name)  # add to array of codes to be printed to pdf

                # reset the used random element array if used
                self.used_random_values_array = []

                # reset the counts
                self.number_count = 1
                self.letter_count = 0
        else:  # if there is an uploaded file, use that to gen qrcodes instead
            with open(self.uploaded_file_path, "r") as input_csv:
                for line in input_csv:
                    qr_code_text = line.replace(",", "-")[:len(line) - 1]

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4
                    )

                    qr.add_data(qr_code_text)
                    qr.make(fit=True)

                    img = qr.make_image()
                    file_name = f"{qr_code_text}.jpg"
                    if self.ids.individualcodes.active:
                        if self.save_folder_path is not None and self.save_folder_path is not "":
                            file_name = f"{self.save_folder_path}/{file_name}"
                    else:
                        file_name = f"Temp/{file_name}"
                    img.save(file_name)  # save qr code as a jpg file

                    # Draw label on image
                    img = Image.open(file_name)
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype("arial", 21)
                    color = 0
                    draw.text((37, -6), f"{qr_code_text[:32]}\n{qr_code_text[32:64]}\n{qr_code_text[64:]}", font=font, fill=color)
                    img.save(file_name)

                    self.array_of_codes.append(file_name)  # add to array of codes to be printed to pdf

        # Create PDF file with QR Codes in it
        self.create_pdf()

    def create_pdf(self):
        pdf = FPDF(orientation='P')
        pdf.add_page()
        x, y = (5.0, 5.0)
        pdf.set_xy(x, y)

        # Set up variables based on layout chosen by user
        layout = self.file_settings_widget.ids.pdflayout.text

        # Default values for option: "Default (5x4)"
        w = 50; h = 50  # set width and height
        x_change = 50  # set x distance between this code and next
        y_change = 50  # set y distance between this code and next
        max_in_row = 3  # set the max # codes in row - 1
        max_in_pg = 20  # set the max # codes in pg

        if layout == "4x1":
            w = 60; h = 60  # set same vars as above but for diff layout
            x_change = 60; y_change = 60
            max_in_row = 0; max_in_pg = 4
        elif layout == "4x2":
            w = 70; h = 70
            x_change = 65; y_change = 65
            max_in_row = 1; max_in_pg = 8
        elif layout == "4x3":
            w = 70; h = 70
            x_change = 65; y_change = 65
            max_in_row = 2; max_in_pg = 12
        elif layout == "4x4":
            w = 50; h = 55
            x_change = 50; y_change = 55
            max_in_row = 3; max_in_pg = 16
        elif layout == "3x2":
            w = 90; h = 90
            x_change = 90; y_change = 90
            max_in_row = 1; max_in_pg = 6
        elif layout == "3x3":
            w = 70; h = 70
            x_change = 70; y_change = 70
            max_in_row = 2; max_in_pg = 9
        elif layout == "2x2":
            w = 100; h = 100
            x_change = 100; y_change = 100
            max_in_row = 1; max_in_pg = 4
        elif layout == "1x2 and 5/8":
            w = 35; h = 92.20
            x_change = 33; y_change = 88
            max_in_row = 5; max_in_pg = 18

        num_in_row = 0  # used to measure how many will fit in a row
        num_in_page = 0  # used to measure how many will fit in a pg
        for code in self.array_of_codes:  # print qr codes to pdf file
            pdf.image(code, w=w, h=h)
            num_in_page += 1
            x += x_change
            if num_in_row == max_in_row: x = 5.0; y += y_change; num_in_row = -1  # when 4 codes are printed in a row, move to next row
            if num_in_page == max_in_pg: y = 5.0; pdf.add_page(); num_in_page = 0  # when 5 rows printed in pg, move to nxt pg
            pdf.set_xy(x, y)
            num_in_row += 1

        if not self.ids.individualcodes.active:  # if Individual QR Codes checkbox not checked
            for code in self.array_of_codes:  # Then delete qrcodes
                os.remove(code)
        self.array_of_codes = []  # empty the array_of_codes array for the next create

        file_name = "test3.pdf"
        if self.save_folder_path is not None and self.save_folder_path is not "":
            file_name = f"{self.save_folder_path}/{file_name}"
        pdf.output(file_name, 'F')  # output final PDF file

    def generate_csv(self, csv_file_path, qr_code_text):
        if self.save_folder_path is not None and self.save_folder_path is not "":
            csv_file_path = f"{self.save_folder_path}/{csv_file_path}"
        with open(csv_file_path, "a") as csv:
            qr_code_text = qr_code_text.replace("-", ",")
            csv.write(qr_code_text + "\n")

    def upload(self):
        Tk().withdraw()  # keep root window form appearing as we don't want full GUI
        self.uploaded_file_path = filedialog.askopenfilename()
        if self.uploaded_file_path == "":  # if canceled change back to default
            self.ids.uploadedfilename.text = "No file uploaded."
            self.ids.uploadedfilename.pos = (155, 5)
        elif ".csv" not in self.uploaded_file_path:
            self.ids.uploadedfilename.text = "Must be a CSV file."
            self.ids.uploadedfilename.pos = (155, 5)
            self.uploaded_file_path = None
        else:  # else if a file was chosen, put the file name on the screen
            string_arr = self.uploaded_file_path.split("/")
            self.ids.uploadedfilename.text = string_arr[len(string_arr) - 1]
            self.ids.uploadedfilename.pos = (270, 5)

    def add_row(self):
        if self.row_count + 1 <= 20:
            self.row_count += 1
            new_row = RowWidget()
            new_row.main_screen = self

            # set row number
            new_row.children[2].text = f"{self.row_count}"

            # add fields to array of text_inputs, so I can access them later
            new_row_array = [new_row.children[1], new_row.children[0]]

            # add the correct number of cols to the new row
            for _ in range(new_row.col_count - 2):
                new_col = ColWidget()
                new_row.add_widget(new_col)  # add a col to new row
                new_row_array.append(new_col)  # add a col to new row for internal arr

            # Add the add/remove column btns
            new_buttons = AddRemoveColWidget()
            new_buttons.main_screen = self  # set main_screen
            new_row.add_widget(new_buttons)

            rows_section = self.ids.middlesection
            rows_section.add_widget(new_row)  # add new row to UI
            self.text_input_array.append(new_row_array)  # add new row to internal arr

    def remove_row(self):
        if self.row_count - 1 != 0:  # doesn't remove anything if only one row is left
            rows_section = self.ids.middlesection
            rows_section.remove_widget(rows_section.children[0])  # remove end widget by removing widget at 0 position
            self.row_count -= 1  # decrement count of rows
            self.text_input_array.remove(self.text_input_array[self.row_count])  # remove text_inputs from that array
            self.preview_images_array.remove(self.preview_images_array[self.row_count])  # remove file from preview arr
            self.curr_preview_img_index = 0  # set this to 0 so it doesn't get stuck on an img that no longer exists

    def add_col(self, col):
        if col.parent.col_count + 1 <= 20:
            col.parent.col_count += 1

            # add a col to this row widget and to this row in text_input_array
            row = col.parent
            row_index_to_edit = int(row.ids.rownumber.text) - 1

            new_col = ColWidget()
            row.remove_widget(row.children[0])  # remove the add/remove cols
            row.add_widget(new_col)  # add to ui

            # Add the add/remove col btns back
            new_buttons = AddRemoveColWidget()
            new_buttons.main_screen = self  # set main_screen
            row.add_widget(new_buttons)

            self.text_input_array[row_index_to_edit].append(new_col)  # add newcol to its row in the array

    def remove_col(self, col):
        if col.parent.col_count - 1 != 1:  # doesn't remove anything if only 2 col are left
            col.parent.col_count -= 1  # decrement count of cols

            row = col.parent  # getting the row widget this col is in
            row.remove_widget(row.children[1])  # remove the end col of each row (before the add/rem btns)

            row_index_to_edit = int(row.ids.rownumber.text) - 1  # get the index to edit in the array
            self.text_input_array[row_index_to_edit].remove(self.text_input_array[row_index_to_edit][col.parent.col_count])  # remove last col from array

    def exit(self, *args):
        exit_widget = ExitWidget()
        exit_widget.exit_widget_popup = Popup(title="                             Are you sure you want to quit?\n"
                                                    "                                 (unsaved data will be lost)",
                                              content=exit_widget, size_hint=(None, None), size=(417, 155),
                                              auto_dismiss=True)
        exit_widget.exit_widget_popup.open()
        return True


class RowWidget(StackLayout):
    col_count = 2


class ColWidget(TextInput):
    pass


class AddRemoveColWidget(BoxLayout):
    main_screen = None

    def call_add_col(self):
        self.main_screen.add_col(self)

    def call_remove_col(self):
        self.main_screen.remove_col(self)


class FileSettingsWidget(BoxLayout):
    main_screen = None
    file_settings_popup = None

    def call_create(self):
        self.main_screen.create()

    def choose_save_folder(self):
        Tk().withdraw()
        self.main_screen.save_folder_path = filedialog.askdirectory()
        if self.main_screen.save_folder_path is None and self.main_screen.save_folder_path is "":
            self.ids.folderpath.text = "No folder selected, default is root folder."
        else:
            self.ids.folderpath.text = self.main_screen.save_folder_path


class ExitWidget(BoxLayout):
    exit_widget_popup = None

    """ This function closes the program if the user clicked 'Yes' when asked """

    def confirm_exit(self):
        self.get_root_window().close()
        App.get_running_app().stop()


""" This class exists to instantiate a scrollview (used on main screen to allow user to scroll the text displayed) """


class ScreenWidget(ScrollView):
    pass


""" This class represents the app itself, and everything starts from and runs from this """


class SampleIDQRGeneratorApp(App):
    main_screen = None

    """ Builds the App by instantiating a MainScreenWidget and returning it """

    def build(self):
        self.main_screen = MainScreenWidget()
        Window.size = (1000, 500)
        Window.bind(on_maximize=self.on_maximize)
        return self.main_screen

    def on_start(self):
        if not os.path.isdir("Temp"):
            os.mkdir("Temp")
        self.main_screen.add_row()  # add a row to the layout, and add/remove col btns

    def on_maximize(self, *args):
        Window.size = (1000, 500)  # when user tries to maximize, snap back to original size


if __name__ == '__main__':
    SampleIDQRGeneratorApp().run()
