import os
from xlrd import open_workbook
from django.core.exceptions import ObjectDoesNotExist

inventory_sheet = "Senior Lab Inventory.xls"
experiment_sheet = "Freshman Experiments.xls"  # Includes FR texts on sheet 1.


def populate():
    sheet = open_workbook(inventory_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):           # Skip the 0th row, which gives column names.
        name =     sheet.cell(row_index, 2).value
        location = sheet.cell(row_index, 4).value
        count = int(sheet.cell(row_index, 3).value)
        room =  int(sheet.cell(row_index, 1).value)
        add_material(name, location, count, room)

        add_room(room)
        
    sheet = open_workbook(experiment_sheet).sheet_by_index(1)
    for row_index in range(1, sheet.nrows):
        title = sheet.cell(row_index, 0).value
        author = sheet.cell(row_index, 1).value
        manual = sheet.cell(row_index, 2).value
        year = sheet.cell(row_index, 3).value
        
        add_text(title, author, manual, year)

    sheet = open_workbook(experiment_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):
        title = sheet.cell(row_index, 1).value
        session = int(sheet.cell(row_index, 0).value)
        text = None
        procedure = sheet.cell(row_index, 3).value
        materials = None
        tags = sheet.cell(row_index, 6).value

        add_experiment(title=title, session=session, text=text,
                       procedure=procedure, tags=tags)

    # Now, since we can't associate texts with experiments through a M2MField until they're all created,
    # we can now find the corresponding Text to each Experiment and add it to the Experiment.text field.
    for row_index in range(1, sheet.nrows):
        experiment = sheet.cell(row_index, 1).value
        text = sheet.cell(row_index, 2).value
        materials = sheet.cell(row_index, 4).value.split(', ')

        add_text_to_experiment(text, experiment)
        add_materials_to_experiment(materials, experiment)

    # Print out the contents of the database... not just what you've added at this point.
    for t in Text.objects.all():
        print t
    for e in Experiment.objects.all():
        print e
    for m in Material.objects.all():
        print m


def add_material(name, location, room, count):
    m, created = Material.objects.get_or_create(name=name, room=room, location=location, count=count)
    if created:
        return m


def add_experiment(title, text, session, procedure,  resources=None, tags=None):
    e, created = Experiment.objects.get_or_create(title=title, text=text, session=session,
                                                  procedure=procedure, resources=resources, tags=tags)
    if created:
        return e


def add_text(title, manual, year, author):
    t, created = Text.objects.get_or_create(title=title, manual=manual, year=year, author=author)
    if created:
        return t


def add_room(number):
    r, created = Room.objects.get_or_create(number=number)
    if created:
        return r


def add_text_to_experiment(text_title, experiment_title):
    t = Text.objects.get(title=text_title)
    e = Experiment.objects.get(title=experiment_title)
    e.text = t


def add_materials_to_experiment(materials_list, experiment_title):
    try:
        for material in materials_list:
            m = Material.objects.get(name=material)
            e = Experiment.objects.get(title=experiment_title)
            e.materials.add(m)
    except ObjectDoesNotExist:
        print "Material with the name %s does not exist." % (material)

# Start execution here!
if __name__ == '__main__':
    print "Starting inventory population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baros.settings')
    from inventory.models import Material, Experiment, Text, Room

    populate()