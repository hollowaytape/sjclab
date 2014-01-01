"""xlotl.py
Loads/updates a database from the specified Excel documents.
Excel is an easier implementation for the client, so
they should just be able to run this and ignore all the SQL stuff.
"""
from django.conf import settings
settings.configure()
import sqlite3
from xlrd import open_workbook
from inventory.models import Material, Text, Experiment

db = "baros.db"

# Filenames of all relevant excel sheets. Not all created yet.
tables = {"xls_experiments_fr": "experiments.xls",
          "xls_experiments_jr": None,
          "xls_experiments_sr": None,

          "xls_inventory_fr": None,
          "xls_inventory_jr": None,
          "xls_inventory_sr": "Senior Lab Inventory.xls",

          "xls_texts_fr": None,
          "xls_texts_jr": None,
          "xls_texts_sr": None}
conn = sqlite3.connect(db)
c = conn.cursor()


"""def update(table):            # I can make a universal function later. I need to get just one working first.
    # Open the first (0th) sheet of the Excel workbook whose filename is specified in the tables dictionary.
    sheet = open_workbook(tables[table]).sheet_by_index(0)"""


def initialize_sr_inventory():
    sheet = open_workbook("Senior Lab Inventory.xls").sheet_by_index(0)
    new_materials = []
    for row_index in range(1, sheet.nrows):           # Skip the first row, which gives column names.
        name =     sheet.cell(row_index, 2).value     # The ordering is not consistent from xls to the db models, hm...
        room =     int(sheet.cell(row_index, 1).value)
        location = sheet.cell(row_index, 4).value
        try:
            count = int(sheet.cell(row_index, 3).value)
        except ValueError:
            count = sheet.cell(row_index, 3).value    # Some are listed in alternate qtys, like gloves - "1pr".

        new_materials.append((name, room, location, count))
    print new_materials
    print "Proceed? y/n"
    yes_no = raw_input("> ")
    if "y" in yes_no:
        c.executemany('INSERT INTO inventory_material (name, room, location, count) VALUES (?,?,?,?)', new_materials)

initialize_sr_inventory()

c.commit()

conn.close()