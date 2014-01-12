import os
from xlrd import open_workbook

inventory_sheet = "Senior Lab Inventory.xls"


def populate():
    """sheet = open_workbook(inventory_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):           # Skip the 0th row, which gives column names.
        name =     sheet.cell(row_index, 2).value     # The ordering is not consistent from xls to the db models, hm...
        room =     int(sheet.cell(row_index, 1).value)
        location = sheet.cell(row_index, 4).value
        count = int(sheet.cell(row_index, 3).value)

        add_material(name, room, location, count)
        add_room(room)                            # Grossly inefficient and highly specific."""

    plants = add_text(title="An Inquiry into Plants",
                      manual="OBSV",
                      year="FR",
                      author="Theophrastus")

    pencils = add_material(name="Colored pencils",
                           room=104,
                           location="Front drawer",
                           count=48)

    add_experiment(title="Magnolia Observation",
                   text=plants,
                   procedure="Observe magnolia trees in the Mellon courtyard.",
                   # Materials are not specified until after creation.
                   resources=None,
                   tags="plants")

    # Print out what has been added.
    for e in Experiment.objects.all():
        print e
    for m in Material.objects.all():
        print m


def add_material(name, room, location, count=0):
    m, created = Material.objects.get_or_create(name=name, room=room, location=location, count=count)
    return m


def add_experiment(title, text, procedure, resources=None, tags=None):
    e, created = Experiment.objects.get_or_create(title=title, text=text, procedure=procedure,
                                                  resources=resources, tags=tags)
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