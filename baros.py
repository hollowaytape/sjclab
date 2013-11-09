from sys import exit
from xlrd import open_workbook
from xlwt import Workbook

# Is it messy to have all these functions run inside each other in a navigation system?
# Conveniently, everything will be fixed as it is moved to Django. Hopefully.

"""This breaks everything. Makes everything run out of order.
It is wonderfully efficicent in my mind, but I think Python
 has eager evaluation - all the potential functions are
 actualizing themselves.
def menu_select(prompt, choices, outcomes):
    print prompt                                                            # "Which grade level?"
    for choice in choices:
        print "\n%s) %s" % ((choices.index(choice)) + 1, choice)            # "2) Junior Lab"
    user_input = raw_input("> ")
    while user_input not in len(choices):
        user_input = raw_input("I'm sorry, where do you see that in the text? > ")
    if user_input == choices.index(user_input):
        outcomes.index(user_input)"""


def prompt_function(prompt, function):
    print prompt
    user_input = raw_input("> ")
    return function(user_input)


class Experiment:
    def __init__(self, title, index, year, author, procedure, materials):
        self.title = title
        self.index = index
        self.year = year
        self.author = author
        self.procedure = procedure
        self.materials = materials

TestExperiment = Experiment('Test Experiment', 77, 'Senior', 'Leo Strauss',
             ['1) Pour water from volumetric flask into glove.',
              '2) Empty glove into petri dish.',
              '3) Weigh dish on triple beam balance.'],
              ['Volumetric flask', 'Orange glove', 'Petri dish', 'Triple beam balance'])


def experiment_page(exp):
    print exp.title, " - ", exp.index
    print exp.author, "\n\nProcedure:"
    for step in exp.procedure:
        print step
    print "\nMaterials:"
    for material in exp.materials:
        print material
    print "\nWhat to do? \n1) Locate materials \n2) Add comment \n3) Exit"
    what_do = raw_input("> ")
    if what_do == '1':
        locate_materials(exp)
        # More graceful way to exit from this loop?
    elif what_do == '2':
        pass
    elif what_do == '3':
        if exp.year == 'Freshman':
            freshman_experiments()
        elif exp.year == 'Junior':
            junior_experiments()
        elif exp.year == 'Senior':
            senior_experiments()


def front_page():
    print "St. John's College - Lab Resources"
    print "1) Experiments \n2) Inventory \n3 Exit"
    choice = raw_input("> ")
    if choice == "1":
        select_class()
    elif choice == "2":
        inventory()
    else:
        exit()


def select_class():
    print "Which class's experiments do you want to access?"
    print "1) Freshman \n2) Junior \n3) Senior \n4) Never mind"
    class_choice = raw_input("> ")
    if class_choice == '1':
        freshman_experiments()
    elif class_choice == '2':
        junior_experiments()
    elif class_choice == '3':
        senior_experiments()
    else:
        front_page()


def locate_one_item(item):
    print "%s:" % item
    book = open_workbook('Senior Lab Inventory.xls')
    inventory = book.sheet_by_index(0)

    for row_index in range(inventory.nrows):
        if item in inventory.cell(row_index, 2).value:                        # Name
            print "%s in %d, %s" % (    inventory.cell(row_index, 3).value,  # Count
                                        inventory.cell(row_index, 1).value,   # Room Number
                                        inventory.cell(row_index, 4).value)   # Location in Room
    print "\n"


def locate_materials(exp):
    for material in exp.materials:
        locate_one_item(material)


def freshman_experiments():
    pass


def junior_experiments():
    pass


def senior_experiments():
    print "Senior Experiments:"
    print "1) Test Experiment"
    exp_choice = raw_input("> ")
    if exp_choice == '1':
        experiment_page(TestExperiment)
    else:
        select_class()


def inventory():
    print "1) By room or 2) by item?"
    inv_choice = raw_input("> ")
    if inv_choice == '1':
        room_list()
    elif inv_choice == '2':
        item_list()
    else:
        front_page()


def room_list():
    # First, get a list of all rooms and display them.
    book = open_workbook('Senior Lab Inventory.xls')
    inv = book.sheet_by_index(0)
    room_set = []

    for row_index in range(inventory.nrows):
        if inv.cell(row_index, 1).value not in room_set:
            room_set.append(inv.cell(row_index, 1))
    for room in room_set:
        print room, "\n"

    while True:                                  # Loop functionality won't be necessary with move to Django.

        print "Which room's contents?"             # Make this a separate function? Like locate_one_item()?
        selected_room = int(raw_input("> "))                    # Must be an int to search the book correctly.

        book = open_workbook('Senior Lab Inventory.xls')
        inventory = book.sheet_by_index(0)

        for row_index in range(inventory.nrows):
            if selected_room in inventory.cell(row_index, 1).value:          # Room Number
                print "%d x %s, %s" % (inventory.cell(row_index, 2).value,   # Item
                                       inventory.cell(row_index, 3).value,   # Count
                                       inventory.cell(row_index, 4).value)   # Location in Room

        print "Search another room? y/n"
        search_again = raw_input("> ")
        if search_again == 'n':
            break

    inventory()


def item_list():
    # First, get a list of all items and display them. (More pleasing way of doing this? Less vertical? Later.)
    # Do I want to separate the various-size beakers? Probably not.

    book = open_workbook('Senior Lab Inventory.xls')
    inv = book.sheet_by_index(0)
    item_set = []

    for row_index in range(inventory.nrows):
        if inv.cell(row_index, 1).value not in item_set:
            room_set.append(inv.cell(row_index, 1))
    for item in item_set:
        print item, "\n"

    while True:
        print "Which item's locations?"
        which_item = raw_input("> ")

        locate_one_item(which_item)

        print "Another item? y/n"
        search_again = raw_input("> ")
        if search_again = 'n':
            break

    inventory()




front_page()