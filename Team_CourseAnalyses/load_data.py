import csv
import django
from django.conf import settings
settings.configure()
django.setup()

import courses.models

def load_data(csv_path):
    # load data
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            c = Course.objects.create(
                course_id=row[1],
                course_title=row[2],
                units=row[3],
                section=row[4],
                mini=row[5],
                days=row[6],
                begin=row[7],
                end=row[8],
                teaching_location=row[9],
                bldg_room=row[10],
                instructor=row[11],
                department=row[12],
                description=row[13]
            )

if __name__ == "__main__":
    load_data('../parser/all_spring_courses.csv')