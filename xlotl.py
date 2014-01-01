"""xlotl.py
Loads/updates a database from the specified Excel documents.
Excel is an easier implementation for the client, so
they should just be able to run this and ignore all the SQL stuff.
"""

from inventory.models import Material, Experiment, Text
import sqlite3
from xlrd import open_workbook

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
    for row_index in range(sheet.nrows):
        name =     sheet.cell(row_index, 2).value     # The ordering is not consistent from xls to the db models, hm...
        room =     sheet.cell(row_index, 1).value
        location = sheet.cell(row_index, 4).value
        count =    sheet.cell(row_index, 3).value
        new_materials.append([name, room, location, count])
    print new_materials
    print "Proceed? y/n"
    yes_no = raw_input("> ")
    if "y" in yes_no:
        c.executemany('INSERT INTO materials VALUES (?,?,?,?,?)', new_materials)

c.execute("relevant sql statements")

c.commit()

conn.close()