import os
from xlrd import open_workbook

inventory_sheet = "Senior Lab Inventory.xls"
experiment_sheet = "Freshman Experiments.xls"


def populate():
    sheet = open_workbook(inventory_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):           # Skip the 0th row, which gives column names.
        name =     sheet.cell(row_index, 2).value     # The ordering is not consistent from xls to the db models, hm...
        room =     int(sheet.cell(row_index, 1).value)
        location = sheet.cell(row_index, 4).value
        count = int(sheet.cell(row_index, 3).value)

        add_material(name, room, location, count)

    sheet = open_workbook(experiment_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):
        title = sheet.cell(row_index, 1).value
        session = int(sheet.cell(row_index, 0).value)
        text = None
        procedure = sheet.cell(row_index, 3).value
        materials = sheet.cell(row_index, 4).value
        tags = sheet.cell(row_index, 5).value

        add_experiment(title=title, session=session, text=text,
                       procedure=procedure, materials=materials, tags=tags)


    plants = add_text(title="An Inquiry into Plants",
                      manual="OBSV",
                      year="FR",
                      author="Theophrastus")

    pencils = add_material(name="Colored pencils",
                           room=104,
                           location="Front drawer",
                           count=48)

    # Print out what has been added.
    for t in Text.objects.all():
        print t
    for e in Experiment.objects.all():
        print e
    for m in Material.objects.all():
        print m


def add_material(name, room, location, count=0):
    m, created = Material.objects.get_or_create(name=name, room=room, location=location, count=count)
    return m


def add_experiment(title, text, session, materials, procedure, resources=None, tags=None):
    e, created = Experiment.objects.get_or_create(title=title, text=text, session=session,
                                                  procedure=procedure, resources=resources, materials=materials, tags=tags)
    return e


def add_text(title, manual, year, author):
    t, created = Text.objects.get_or_create(title=title, manual=manual, year=year, author=author)
    return t


# Start execution here!
if __name__ == '__main__':
    print "Starting inventory population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baros.settings')
    from inventory.models import Material, Experiment, Text
    populate()