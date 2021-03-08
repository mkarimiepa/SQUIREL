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
import weakref

# Set setup variables

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

""" This class is main class for GUI, its the main screen w/in which all other screens/widgets/buttons are located """


class MainScreenWidget(BoxLayout):
    row_count = 0
    number_count = 1
    letter_count = 0
    curr_preview_img_index = 0
    text_input_array = []
    preview_images_array = [''] * 100
    letter_array = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK",
                    "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ", "BA",
                    "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BK", "BL", "BM", "BN", "BO", "BP", "BQ",
                    "BR", "BS", "BT", "BU", "BV", "BW", "BX", "BY", "BZ", "CA", "CB", "CC", "CD", "CE", "CF", "CG",
                    "CH", "CI", "CJ", "CK", "CL", "CM", "CN", "CO", "CP", "CQ", "CR", "CS", "CT", "CU", "CV", "CW",
                    "CX", "CY", "CZ", "DA", "DB", "DC", "DD", "DE", "DF", "DG", "DH", "DI", "DJ", "DK", "DL", "DM",
                    "DN", "DO", "CP", "DQ", "DR", "DS", "DT", "DU", "DV", "DW", "DX", "DY", "DZ", "EA", "EB", "EC",
                    "ED", "EE", "EF", "EG", "EH", "EI", "EJ", "EK", "EL", "EM", "EN", "EO", "EP", "EQ", "ER", "ES",
                    "ET", "EU", "EV", "EW", "EX", "EY", "EZ", "FA", "FB", "FC", "FD", "FE", "FF", "FG", "FH", "FI",
                    "FJ", "FK", "FL", "FM", "FN", "FO", "FP", "FQ", "FR", "FS", "FT", "FU", "FV", "FW", "FX", "FY",
                    "FZ"]

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
            text_input1 = row[1].text
            text_input2 = row[2].text
            text_input3 = row[3].text

            qr_code_text = f"{text_input1}-{text_input2}-{text_input3}"

            # checkboxes
            id_format_spinner = self.ids.idformat
            id_sequential_spinner = self.ids.idsequence

            if id_format_spinner.text == "Insert Number":
                qr_code_text = f"{qr_code_text}-{self.number_count}"
            if id_format_spinner.text == "Insert Letter":
                qr_code_text = f"{qr_code_text}-{self.letter_array[self.letter_count]}"
            if id_sequential_spinner.text == "Sequential":
                pass
            if id_sequential_spinner.text == "Random":
                pass

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
            text_input1 = row[1].text
            text_input2 = row[2].text
            text_input3 = row[3].text

            # get # of codes to make and then run creation that many times
            num_codes = row[0].text

            for _ in range(int(num_codes)):
                qr_code_text = f"{text_input1}-{text_input2}-{text_input3}"

                # handle checkboxes
                id_format_spinner = self.ids.idformat
                id_sequential_spinner = self.ids.idsequence

                if id_format_spinner.text == "Insert Number":
                    qr_code_text = f"{self.number_count}-{qr_code_text}"
                    self.number_count += 1
                if id_format_spinner.text == "Insert Letter":
                    qr_code_text = f"{self.letter_array[self.letter_count]}-{qr_code_text}"
                    self.letter_count += 1
                if id_sequential_spinner.text == "Sequential":
                    pass
                if id_sequential_spinner.text == "Random":
                    pass

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

            rows_section = self.ids.middlesection
            rows_section.add_widget(new_row)
            self.text_input_array.append(new_row_array)

    def remove_row(self):
        if self.row_count - 1 != 0:  # doesn't remove anything if only one row is left
            rows_section = self.ids.middlesection
            rows_section.remove_widget(rows_section.children[0])  # remove end widget by removing widget at 0 position
            self.row_count -= 1  # decrement count of rows
            self.text_input_array.remove(self.text_input_array[self.row_count])  # remove text_inputs from that array
            self.preview_images_array.remove(self.preview_images_array[self.row_count])  # remove file from preview arr
            self.curr_preview_img_index = 0  # set this to 0 so it doesn't get stuck on an img that no longer exists

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
