"""
Name: SampleID QR Generator
Description:
Author: Muhammad Karimi karimi.muhammad@epa.gov
Contact: Timothy Boe boe.timothy@epa.gov and Worth also right?
Requirements:
"""

# import Necessary packages
import os
import qrcode
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import threading

# Import GUI packages
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

# Set setup variables
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

""" This class is main class for GUI, its the main screen w/in which all other screens/widgets/buttons are located """


class MainScreenWidget(BoxLayout):
    row_count = 0
    col_count = 4
    number_count = 1
    letter_count = 0
    curr_preview_img_index = 0
    text_input_array = []
    used_random_values_array = []
    preview_images_array = [''] * 100
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

            # checkboxes
            id_format_spinner = self.ids.idformat
            id_sequential_spinner = self.ids.idsequence

            if id_format_spinner.text == "Insert Number" and id_sequential_spinner.text == "Sequential":
                if "#id" in qr_code_text:  # replace user placeholder '#id' w/number
                    qr_code_text = qr_code_text.replace("#id", f"{self.number_count}")
                else:
                    qr_code_text = f"{qr_code_text}-{self.number_count}"
            elif id_format_spinner.text == "Insert Number" and id_sequential_spinner.text == "Random":
                rand_num = int(random.uniform(1, 1000))
                if "#id" in qr_code_text:  # replace user placeholder '#id' w/rand num
                    qr_code_text = qr_code_text.replace("#id", f"{rand_num}")
                else:
                    qr_code_text = f"{qr_code_text}-{rand_num}"
            if id_format_spinner.text == "Insert Letter" and id_sequential_spinner.text == "Sequential":
                if "#id" in qr_code_text:  # replace user placeholder '#id' w/letter
                    qr_code_text = qr_code_text.replace("#id", f"{self.letter_array[self.letter_count]}")
                else:
                    qr_code_text = f"{qr_code_text}-{self.letter_array[self.letter_count]}"
            elif id_format_spinner.text == "Insert Letter" and id_sequential_spinner.text == "Random":
                rand_letter = random.choice(self.letter_array)
                if "#id" in qr_code_text:  # replace user placeholder '#id' w/rand letter
                    qr_code_text = qr_code_text.replace("#id", f"{rand_letter}")
                else:
                    qr_code_text = f"{qr_code_text}-{rand_letter}"

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

    def create(self):
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

                # handle checkboxes
                id_format_spinner = self.ids.idformat
                id_sequential_spinner = self.ids.idsequence

                if id_format_spinner.text == "Insert Number" and id_sequential_spinner.text == "Sequential":
                    if "#id" in qr_code_text:  # replace user placeholder '#id' w/number
                        qr_code_text = qr_code_text.replace("#id", f"{self.number_count}")
                    else:
                        qr_code_text = f"{qr_code_text}-{self.number_count}"
                    self.number_count += 1
                elif id_format_spinner.text == "Insert Number" and id_sequential_spinner.text == "Random":
                    rand_num = int(random.uniform(1, 1000))
                    while rand_num in self.used_random_values_array:
                        rand_num = int(random.uniform(1, 1000))
                    self.used_random_values_array.append(rand_num)
                    if "#id" in qr_code_text:  # replace user placeholder '#id' w/rand num
                        qr_code_text = qr_code_text.replace("#id", f"{rand_num}")
                    else:
                        qr_code_text = f"{qr_code_text}-{rand_num}"
                if id_format_spinner.text == "Insert Letter" and id_sequential_spinner.text == "Sequential":
                    if "#id" in qr_code_text:  # replace user placeholder '#id' w/letter
                        qr_code_text = qr_code_text.replace("#id", f"{self.letter_array[self.letter_count]}")
                    else:
                        qr_code_text = f"{qr_code_text}-{self.letter_array[self.letter_count]}"
                    self.letter_count += 1
                elif id_format_spinner.text == "Insert Letter" and id_sequential_spinner.text == "Random":
                    rand_letter = random.choice(self.letter_array)
                    while rand_letter in self.used_random_values_array:
                        rand_letter = random.choice(self.letter_array)
                    self.used_random_values_array.append(rand_letter)
                    if "#id" in qr_code_text:  # replace user placeholder '#id' w/rand letter
                        qr_code_text = qr_code_text.replace("#id", f"{rand_letter}")
                    else:
                        qr_code_text = f"{qr_code_text}-{rand_letter}"

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
                img.save(file_name)

            # reset the used random element array if used
            self.used_random_values_array = []

            # reset the counts
            self.number_count = 1
            self.letter_count = 0

    def add_row(self):
        if self.row_count + 1 <= 20:
            self.row_count += 1
            new_row = RowWidget()
            new_row.main_screen = self

            # set row number
            new_row.children[4].text = f"{self.row_count}"

            # add fields to array of text_inputs, so I can access them later
            new_row_array = [new_row.children[3], new_row.children[2], new_row.children[1], new_row.children[0]]

            # add the correct number of cols to the new row
            for _ in range(self.col_count - 4):
                new_col = ColWidget()
                new_row.add_widget(new_col)  # add a col to new row
                new_row_array.append(new_col)  # add a col to new row for internal arr

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

    def add_col(self):
        if self.col_count + 1 <= 20:
            self.col_count += 1

            # add a col to each row widget and to each row in text_input_array
            array_of_curr_rows = self.ids.middlesection.children
            i = len(self.text_input_array) - 1
            for row in array_of_curr_rows:
                new_col = ColWidget()
                row.add_widget(new_col)  # add to ui
                self.text_input_array[i].append(new_col)  # add to internal array
                i -= 1

    def remove_col(self):
        if self.col_count - 1 != 3:  # doesn't remove anything if only 4 col are left
            rows_section = self.ids.middlesection
            i = 0
            self.col_count -= 1  # decrement count of cols
            for row in rows_section.children:
                row.remove_widget(row.children[0])  # remove the end col of each row
                self.text_input_array[i].remove(self.text_input_array[i][self.col_count])  # remove last col from array
                i += 1

    def exit(self, *args):
        exit_widget = ExitWidget()
        exit_widget.exit_widget_popup = Popup(title="                             Are you sure you want to quit?\n"
                                                    "                                 (unsaved data will be lost)",
                                              content=exit_widget, size_hint=(None, None), size=(417, 155),
                                              auto_dismiss=True)
        exit_widget.exit_widget_popup.open()
        return True


class RowWidget(StackLayout):
    pass


class ColWidget(TextInput):
    pass


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
        self.main_screen.add_row()

    def on_maximize(self, *args):
        Window.size = (1000, 500)  # when user tries to maximize, snap back to original size


if __name__ == '__main__':
    SampleIDQRGeneratorApp().run()
