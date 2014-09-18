import os
import django
from xlrd import open_workbook
from django.core.exceptions import ObjectDoesNotExist
import datetime

inventory_sheet = "data/Senior Lab Inventory.xls"
experiment_sheet = "data/Freshman Experiments.xls"  # Includes FR texts on sheet 1.
room_sheet = "data/Rooms.xls"

def populate():
    # Add rooms.
    sheet = open_workbook(room_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):
        floor = sheet.cell(row_index, 0).value
        hall = sheet.cell(row_index, 1).value
        number = str(sheet.cell(row_index, 2).value).rstrip("0").rstrip(".")
        print number
        
        add_room(floor, hall, number)
        
    # Add materials.
    sheet = open_workbook(inventory_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):           # Skip the 0th row, which gives column names.
        name = sheet.cell(row_index, 2).value
        count = int(sheet.cell(row_index, 3).value)
        location = sheet.cell(row_index, 4).value

        add_material(name, count, location)

        room = str(sheet.cell(row_index, 1).value).rstrip("0").rstrip(".")
        print room

        # Finally, now that both objects are created, place the Room object in the Material's ForeignKey.
        add_room_to_material(name, count, location, room)

    # Then, add the Texts.
    sheet = open_workbook(experiment_sheet).sheet_by_index(1)
    for row_index in range(1, sheet.nrows):
        title = sheet.cell(row_index, 0).value
        author = sheet.cell(row_index, 1).value
        manual = sheet.cell(row_index, 2).value
        year = sheet.cell(row_index, 3).value
        
        add_text(title, author, manual, year)

    # Finally, add the experiments themselves. They require the most associations with other objects, so they go last.
    sheet = open_workbook(experiment_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):
        title = sheet.cell(row_index, 1).value
        procedure = sheet.cell(row_index, 3).value
        text = sheet.cell(row_index, 2).value
        materials = sheet.cell(row_index, 4).value.split(', ')

        add_experiment(title=title, procedure=procedure)

        add_text_to_experiment(text, experiment_title=title)
        add_materials_to_experiment(materials, experiment_title=title)

        tag_list = sheet.cell(row_index, 6).value.split(', ')
        for tag in tag_list:
            add_tag(tag)
        add_tags_to_experiment(tag_list, title)
        
    # Print out the contents of the database... not just what you've added at this point.
    print "\nTexts:"
    for t in Text.objects.all():
        print t
    print "\nExperiments:"
    for e in Experiment.objects.all():
        print e
    print "\nMaterials:"
    for m in Material.objects.all():
        print m
    print "\nRooms:"
    for r in Room.objects.all():
        print r
    print "\nTags:"
    for t in Tag.objects.all():
        print t


# Functions to add different kinds of objects.
def add_material(name, count, location):
    m = Material.objects.get_or_create(name=name, count=count, location=location)[0]
    return m


def add_experiment(title, procedure, resources=None):
    e = Experiment.objects.get_or_create(title=title,
                                         procedure=procedure, resources=resources)[0]
    return e


def add_text(title, author, manual, year):
    t = Text.objects.get_or_create(title=title, author=author, manual=manual, year=year)[0]
    return t


def add_room(floor, hall, number):
    r = Room.objects.get_or_create(floor=floor, hall=hall, number=number, date_modified=datetime.datetime.now())[0]
    return r


def add_tag(name):
    t = Tag.objects.get_or_create(name=name)[0]
    return t


# Functions to associate objects with others in ForeignKey/ManyToManyFields.
def add_text_to_experiment(text_title, experiment_title):
    t = Text.objects.get(title=text_title)
    e = Experiment.objects.get(title=experiment_title)
    e.text = t
    e.save()


def add_materials_to_experiment(materials_list, experiment_title):
    for material in materials_list:
        try:
            m = Material.objects.get(name=material)
            e = Experiment.objects.get(title=experiment_title)
            e.materials.add(m)
            e.save()
        except ObjectDoesNotExist:
            print "Material with the name %s does not exist." % material


def add_tags_to_experiment(tag_list, experiment_title):
    for tag in tag_list:
        try:
            t = Tag.objects.get(name=tag)
            e = Experiment.objects.get(title=experiment_title)
            e.tags.add(t)
            e.save()
        except ObjectDoesNotExist:
            print "Tag with the name %s does not exist." % tag


def add_room_to_material(material_name, material_count, location, room):
    m = Material.objects.get(name=material_name, count=material_count, location=location)
    r = Room.objects.get(number=room)
    m.room = r
    m.save()

# Start execution here!
if __name__ == '__main__':
    print "Starting inventory population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baros.settings')
    from inventory.models import Material, Experiment, Text, Room, Tag
    
    django.setup()

    populate()