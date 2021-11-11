import re
import os

from os import path
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from datetime import datetime
from pykml import parser

def extractDateAndTime(date_time_string):
    # Python ISO8601 can't handle the Z
    replace_date_time = str(date_time_string).replace('Z', '+00:00')
    return datetime.fromisoformat(replace_date_time)


def calculateMileage(distance_in_meters):
    meters_to_miles_denom = 1609.344
    return float(distance_in_meters)/meters_to_miles_denom


def parse_drives(file_name):
    parse_assertion_error = 'Invalid File Extension'
    assert(file_name.lower().endswith('.kml')), parse_assertion_error
    kml_file = path.join(file_name)

    with open(kml_file) as f:

        drives = []
        doc = parser.parse(f).getroot()
        for e in doc.Document.Placemark:
            driving_label = 'Driving'

            total_miles = 0
            total_hours = 0

            if driving_label in e.name.text:
                description_text = e.description.text
                date_times = re.findall(
                    r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)', description_text)

                mileage_assertion_error = 'Invalid Driving Data: Mileage'
                # Should have a from and to
                assert(len(date_times) == 2), mileage_assertion_error

                start_datetime = extractDateAndTime(date_times[0])
                end_datetime = extractDateAndTime(date_times[1])

                mileage = calculateMileage(re.findall(
                    r'\d+m', description_text)[0][:-1])

                drives.append("On " + str(start_datetime.month) + "/" + str(start_datetime.day) + " from " + str(start_datetime.hour) + ":" + str(start_datetime.minute) +
                      " to " + str(end_datetime.hour) + ":" + str(end_datetime.minute) + " you drove " +
                      str(mileage) + " miles!")

    return drives                 

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        test_file = filename[0]
        drives = parse_drives(test_file)

        for drive in drives:
            self.text_input.text += drive + "\n"

        self.dismiss_popup()
    
    def clear(self):
        self.text_input.text = ''

        self.dismiss_popup()


class KMLApp(App):
    def build(self):
        pass

def main():
    KMLApp().run()

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == "__main__":
    main()
