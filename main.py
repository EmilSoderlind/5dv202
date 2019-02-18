

from tkinter import *
from tkinter import ttk
import random
import psycopg2
import DB_config
from easygui import *
import time

root = Tk()
root.geometry('1000x700')


# Latest parse of programs/broadcast entries
DB_entries_program = {"ID programnamn1", "ID programnamn2", "ID programnamn3"}
DB_entries_broadcast = {"ID broadcast1", "ID broadcast2", "ID broadcast3"}
currentTable = ""

# ADD / UPDATE broadcast
def addingBroadcast(id,name,etc,etc2):

    # CHECK IF ID exist --> Update

    # Otherwise VVV
    # SQL
    print("Adding broadcast")

# ADD / UPDATE program
def addingProgram(id,name,etc,etc2):

    # CHECK IF ID exist --> Update

    # Otherwise VVV

    # SQL
    print("Adding program")

def deleteBroadcastWithID(id):
    # SQL HERE
    print("deleting broadcast with ID")

def deleteProgramWithID(id):
    # SQL HERE
    print("deleting program with ID")


def parseDBEntries_broadcast():
    global DB_entries_broadcast
    DB_entries_broadcast = parseDBEntries("broadcast")
    print("parsed broadcasts!")

# fetching programs -> Save in DB_entries_program
def parseDBEntries_program():
    global DB_entries_program
    DB_entries_program = parseDBEntries("program")
    print("parsed programs!")

def parseDBEntries(tableName):

    try:
        connection = psycopg2.connect(user=DB_config.user,
                                  password=DB_config.password,
                                  host=DB_config.host,
                                  port=DB_config.port,
                                  database=DB_config.database)

        connection.set_client_encoding('UTF8')
        cursor = connection.cursor()

        # Print PostgreSQL version
        cursor.execute("SELECT * FROM {};".format(tableName))
        record = cursor.fetchall()

        return record

    except (Exception, psycopg2.Error) as error:

        print ("Error while connecting to PostgreSQL: ", error)

    finally:

        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# State variables
radioButtonVal = StringVar()

# Called when the user double clicks an item in the listbox, presses
# the "Send Gift" button, or presses the Return key.  In case the selected
# item is scrolled out of view, make sure it is visible.
#
# Figure out which country is selected, which gift is selected with the
# radiobuttons, "send the gift", and provide feedback that it was sent.
def performAction(*args):
    global currentTable

    if(currentTable == "program"):

        if(radioButtonVal.get() == "add"):
            print("add in ", currentTable)

        if (radioButtonVal.get() == "update"):
            print("update in ", currentTable)

        if (radioButtonVal.get() == "delete"):
            print("Delete in ", currentTable)
            print("selected: ", DB_entries_program[lbox.curselection()[0]])

    elif(currentTable == "broadcast"):

        if (radioButtonVal.get() == "add"):
            print("add in ", currentTable)

        if (radioButtonVal.get() == "update"):
            print("update in ", currentTable)

        if (radioButtonVal.get() == "delete"):
            print("Delete in ", currentTable)
            print("selected: ", DB_entries_program[lbox.curselection()[0]])

# Perform parse of program in DB and fill table
def viewProgramInTable(*args):
    global currentTable

    if(currentTable == "program"):
        return

    viewProgramsBtn["state"] = "disabled"
    parseDBEntries_program()
    updateTableWithList(DB_entries_program)
    currentTable = "program"
    viewBroadcastsBtn["state"] = "enabled"

# Perform parse of broadcast in DB and fill table
def viewBroadcastInTable(*args):
    global currentTable

    if(currentTable == "broadcast"):
        return

    viewBroadcastsBtn["state"] = "disabled"
    parseDBEntries_broadcast()
    updateTableWithList(DB_entries_broadcast)
    currentTable = "broadcast"
    viewProgramsBtn["state"] = "enabled"

# Called to change content of table with invoked list
def updateTableWithList(list):

    print("list[0]", list[0])

    lbox.delete(0, 'end')
    for item in list:
        lbox.insert('end', str(item[0]) + " | " + str(item[1]) + " | " + str(item[2]))

    # Colorize alternating lines of the listbox
    for i in range(0, len(list), 2):
        lbox.itemconfigure(i, background='#f0f0ff')

# oldEntry = if we are about to update old entry. Contains old entry:s fields.
def presentPopup(oldEntry):
    global currentTable

    if(currentTable == "program"):

        programFieldNames = ["Id", "Name", "Tagline", "Email", "Url", "Editor", "Channel", "Category"]

        if(oldEntry != ""):
            fieldValues = [str(oldEntry[0]), str(oldEntry[1]), str(oldEntry[2]), str(oldEntry[3]), str(oldEntry[4]),
                           str(oldEntry[5]), str(oldEntry[6]), str(oldEntry[7])]
            fieldValues = multenterbox("UPDATE PROGRAM", "UPDATE PROGRAM", programFieldNames, fieldValues)
        else:
            fieldValues = multenterbox("ADD PROGRAM", "ADD PROGRAM", programFieldNames)

        print(fieldValues)

    else:

        broadcastFieldNames = ["Id", "Program", "Tagline", "Date", "Duration", "Image_url"]

        if (oldEntry != ""):
            fieldValues = [str(oldEntry[0]), str(oldEntry[1]), str(oldEntry[2]), str(oldEntry[3]), str(oldEntry[4]),
                           str(oldEntry[5])]
            fieldValues = multenterbox("UPDATE BROADCAST", "UPDATE BROADCAST", broadcastFieldNames, fieldValues)
        else:
            fieldValues = multenterbox("ADD BROADCAST", "ADD BROADCAST", broadcastFieldNames)

        print(fieldValues)
    return fieldValues

def setRadioButtonToAdd():
    radioButtonVal.set('add')

def setRadioButtonToDelete():
    radioButtonVal.set('delete')

def setRadioButtonToUpdate():
    radioButtonVal.set('update')

# V----- CREATING GUI -------V

# Create and grid the outer content frame
c = ttk.Frame(root, padding=(10, 10, 24, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

# Create the different widgets; note the variables that many
# of them are bound to, as well as the button callback.
# Note we're using the StringVar() 'cnames', constructed from 'countrynames'
lbox = Listbox(c, height=7)
lbl = ttk.Label(c, text="Manipulate database (selected):")

g1 = ttk.Radiobutton(c, text="Delete (selected)", variable=radioButtonVal, value='delete')
g2 = ttk.Radiobutton(c, text="Update (selected)", variable=radioButtonVal, value='update')
g3 = ttk.Radiobutton(c, text="Add new entry", variable=radioButtonVal, value='add')

#sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
viewProgramsBtn = ttk.Button(c, text='View Programs', command=viewProgramInTable)
viewBroadcastsBtn = ttk.Button(c, text='View Broadcasts', command=viewBroadcastInTable)
send = ttk.Button(c, text='Perform', command=performAction, default='active')


# Grid all the widgets
lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
lbl.grid(column=1, row=0, padx=10, pady=5)
g1.grid(column=1, row=1, sticky=W, padx=20)
g2.grid(column=1, row=2, sticky=W, padx=20)
g3.grid(column=1, row=3, sticky=W, padx=20)
send.grid(column=2, row=4, sticky=E, pady=15)
viewProgramsBtn.grid(column=1, row=6, columnspan=1)
viewBroadcastsBtn.grid(column=2, row=6, columnspan=1)
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

# ^----- CREATING GUI -------^


# Set the starting state of the interface, including selecting the
# default gift to send, and clearing the messages.  Select the first
# country in the list; because the <<ListboxSelect>> event is only
# generated when the user makes a change, we explicitly call showPopulation.
radioButtonVal.set("")
#sentmsg.set('')
#statusmsg.set('')
lbox.selection_set(0)

viewProgramInTable()

parseDBEntries_program()

root.mainloop()


# PARSE BOTH


