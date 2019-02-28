
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
def addingBroadcast(id, program_id ,tagline,date, duration, image_url):

    addBroadcastQuery = "INSERT INTO \"public\".\"broadcast\"(\"program\", \"tagline\", " \
               "\"broadcast_date\", \"duration\", \"image_url\") VALUES({}, \'{}\', " \
               "\'{}\', {}, \'{}\') RETURNING \"broadcast_id\", \"program\", \"tagline\", " \
               "\"broadcast_date\", duration, \"image_url\";".format(program_id,tagline,date,duration,image_url)

    # SQL
    performSqlQuery(addBroadcastQuery)
    print("Adding broadcast")


def updateBroadcast(oldId, id, program_id ,tagline, date, duration, image_url):
    print("updateBroadcast: ", oldId, id, program_id ,tagline,date, duration, image_url)

    updateBroadcastQuery = "SELECT updateBroadcast({},{},{},{},{},{},{})"
    performSqlQuery(updateBroadcastQuery)
    print("Updated broadcast")

def updateProgram(oldId, id, name, tagline, email, url, editor, channel, category):
    print("updateProgram: ", oldId, id, name, tagline, email, url, editor, channel, category)

    updateProgramQuery = ""
    performSqlQuery(updateProgramQuery)
    print("Updated program")



# ADD / UPDATE program
def addingProgram(id , name ,tagline ,email, url, editor, channel, category):

    addProgramQuery = "INSERT INTO \"public\".\"program\"(\"program_id\", \"name\", \"tagline\", \"email\", \"url\", \"editor\", \"channel\", \"category\")" \
                      " VALUES({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\') RETURNING \"program_id\"" \
                      ", \"name\", \"tagline\", \"email\", \"url\", \"editor\", \"channel\", \"category\";".format(id,name,tagline,email,url,editor,channel, category)

    # SQL
    performSqlQuery(addProgramQuery)
    print("Adding program")

def deleteFromTableWithID(table, id):
    # SQL HERE
    if(table == "broadcast"):
        res = performSqlQuery("DELETE FROM \"public\".\"broadcast\" WHERE \"broadcast_id\"={};".format(id))
        print("deleting program with ID: ", id)
    elif(table == "program"):
        res = performSqlQuery("DELETE FROM \"public\".\"program\" WHERE \"program_id\"={};".format(id))
        print("deleting program with ID: ", id)

    print("Res: ", res)

def parseDBEntries_broadcast():
    global DB_entries_broadcast
    DB_entries_broadcast = parseDBEntries("broadcast ORDER BY broadcast_id")
    print("parsed broadcasts!")

# fetching programs -> Save in DB_entries_program
def parseDBEntries_program():
    global DB_entries_program
    DB_entries_program = parseDBEntries("program ORDER BY program_id")
    print("parsed programs!")


def parseDBEntries(table_name):
    return performSqlQuery("SELECT * FROM {};".format(table_name))


def performSqlQuery(query):

    print("Invoking query: ", query)

    try:
        connection = psycopg2.connect(user=DB_config.user,
                                  password=DB_config.password,
                                  host=DB_config.host,
                                  port=DB_config.port,
                                  database=DB_config.database)

        connection.set_client_encoding('UTF8')

        cursor = connection.cursor()
        # Print PostgreSQL version
        cursor.execute(query)
        connection.commit()

        record = cursor.fetchall()

        connection.commit()

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
            res = presentPopup("")
            addingProgram(res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7])

        if (radioButtonVal.get() == "update"):
            print("update in ", currentTable)
            oldId = DB_entries_program[lbox.curselection()[0]][0]
            print("oldId:", oldId)
            res = presentPopup(DB_entries_program[lbox.curselection()[0]])

            updateProgram(oldId, res[0],res[1],res[2],res[3],res[4],res[5], res[6], res[7])


        if (radioButtonVal.get() == "delete"):
            print("Delete in ", currentTable)
            id = DB_entries_program[lbox.curselection()[0]][0]
            print("selected: ", id)
            deleteFromTableWithID(currentTable,id)

        viewProgramInTable()

    elif(currentTable == "broadcast"):

        if (radioButtonVal.get() == "add"):
            print("add in ", currentTable)
            res = presentPopup("")
            print("Res: ", res)
            addingBroadcast(res[0],res[1],res[2],res[3],res[4],res[5])

        if (radioButtonVal.get() == "update"):
            print("update in ", currentTable)
            res =  presentPopup(DB_entries_broadcast[lbox.curselection()[0]])
            print(res)
            updateBroadcast(oldId, res[0],res[1],res[2],res[3],res[4],res[5])

        if (radioButtonVal.get() == "delete"):
            print("Delete in ", currentTable)
            id = DB_entries_broadcast[lbox.curselection()[0]][0]
            print("selected: ", id)
            deleteFromTableWithID(currentTable, id)

        viewBroadcastInTable()

# Perform parse of program in DB and fill table
def viewProgramInTable(*args):
    global currentTable

    viewProgramsBtn["state"] = "disabled"
    parseDBEntries_program()
    updateTableWithList(DB_entries_program)
    currentTable = "program"
    viewBroadcastsBtn["state"] = "enabled"

# Perform parse of broadcast in DB and fill table
def viewBroadcastInTable(*args):
    global currentTable

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
        outStr = ""
        for field in item:
            outStr += " |   " + str(field)
        lbox.insert('end', outStr)

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
        return fieldValues

    else:

        broadcastFieldNames = ["Program", "Tagline", "Date", "Duration", "Image_url"]

        if (oldEntry != ""):
            fieldValues = [str(oldEntry[1]), str(oldEntry[2]), str(oldEntry[3]), str(oldEntry[4]), str(oldEntry[5])]
            fieldValues = multenterbox("UPDATE BROADCAST", "UPDATE BROADCAST", broadcastFieldNames, fieldValues)
        else:
            fieldValues = multenterbox("ADD BROADCAST", "ADD BROADCAST", broadcastFieldNames)

        print(fieldValues)
        return [str(oldEntry[0]),fieldValues[0],fieldValues[1],fieldValues[2],fieldValues[3],fieldValues[4]]

def setRadioButtonToAdd():
    radioButtonVal.set('add')

def setRadioButtonToDelete():
    radioButtonVal.set('delete')

def setRadioButtonToUpdate():
    radioButtonVal.set('update')

# V----- CREATING GUI -------V

# Create and grid the outer content frame
c = ttk.Frame(root, padding=(10, 10, 24, 0))
c.grid(column=0, row=0, sticky=(N ,W ,E ,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0 ,weight=1)

# Create the different widgets; note the variables that many
# of them are bound to, as well as the button callback.
# Note we're using the StringVar() 'cnames', constructed from 'countrynames'
lbox = Listbox(c, height=7)
lbl = ttk.Label(c, text="Manipulate database (selected):")

g1 = ttk.Radiobutton(c, text="Delete (selected)", variable=radioButtonVal, value='delete')
g2 = ttk.Radiobutton(c, text="Update (selected)", variable=radioButtonVal, value='update')
g3 = ttk.Radiobutton(c, text="Add new entry", variable=radioButtonVal, value='add')

viewProgramsBtn = ttk.Button(c, text='View Programs', command=viewProgramInTable)
viewBroadcastsBtn = ttk.Button(c, text='View Broadcasts', command=viewBroadcastInTable)
send = ttk.Button(c, text='Perform', command=performAction, default='active')


# Grid all the widgets
lbox.grid(column=0, row=0, rowspan=6, sticky=(N ,S ,E ,W))
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

lbox.selection_set(0)

viewProgramInTable()

root.mainloop()


# PARSE BOTH
