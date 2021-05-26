import re
from datetime import datetime
from pykml import parser
from os import path


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
        doc = parser.parse(f).getroot()
        for e in doc.Document.Placemark:
            driving_label = 'Driving'

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

                print("On " + str(start_datetime.month) + "/" + str(start_datetime.day) + " from " + str(start_datetime.hour) + ":" + str(start_datetime.minute) +
                      " to " + str(end_datetime.hour) + ":" + str(end_datetime.minute) + " you drove " +
                      str(mileage) + " miles!")


def main():
    test_file = 'test.kml'
    parse_drives(test_file)


if __name__ == "__main__":
    main()
