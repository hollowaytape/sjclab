import os
from xlrd import open_workbook

inventory_sheet = "Senior Lab Inventory.xls"


def populate():
    sheet = open_workbook(inventory_sheet).sheet_by_index(0)
    for row_index in range(1, sheet.nrows):           # Skip the 0th row, which gives column names.
        name =     sheet.cell(row_index, 2).value     # The ordering is not consistent from xls to the db models, hm...
        room =     int(sheet.cell(row_index, 1).value)
        location = sheet.cell(row_index, 4).value
        count = int(sheet.cell(row_index, 3).value)

        add_material(name, room, location, count)
        add_room(room)                            # Grossly inefficient and highly specific.

    # Print out what has been added.
    for r in Room.objects.all():
        for m in Material.objects.filter(room=r):
            print "- {0} - {1}".format(str(r), str(m))


def add_material(name, room, loc, count=0):
    m = Material.objects.get_or_create(name=name, room=room, location=loc, count=count)[0]
    return m


def add_room(number, year='SR', room_type='C'):                             # No non-senior/non-class data yet.
    p = Room.objects.get_or_create(number=number, year=year, type=room_type)[0]         # What does the [0] do?
    return p

# Start execution here!
if __name__ == '__main__':
    print "Starting inventory population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baros.settings')
    from inventory.models import Material, Room
    populate()