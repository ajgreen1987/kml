from pykml import parser
from os import path
import re

def main():
    test_file = 'test.kml'
    parseKML(test_file)

def parseKML(file_name):
    parse_assertion_error = 'Invalid File Extension'
    assert(file_name.lower().endswith('.kml')), parse_assertion_error
    kml_file = path.join(file_name)

    with open(kml_file) as f:
        doc = parser.parse(f).getroot()
        for e in doc.Document.Placemark:
            driving = "Driving"
            
            if driving in e.name.text:
                description_text = e.description.text
                dates = re.findall(r'(\d{4}-\d{02}-\d{02}T\d{02}:\d{02}:\d{02}.\d{03}Z)',description_text)
                distance = re.findall(r'\d+m', description_text)[0][:-1]

                mileage_assertion_error = 'Invalid Driving Data: Mileage'
                assert(len(dates)>0), mileage_assertion_error

                #remove whitespace and 'm' at the end of distance
                meters_to_miles_denom = 1609.344
                print("On " + dates[0] + " until " + dates[1] + " you drove " + str(int(distance)/meters_to_miles_denom) + " miles!")


if __name__ == "__main__":
    main()