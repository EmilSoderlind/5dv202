from tkinter import *
from tkinter import ttk
import random
import psycopg2
import DB_config

root = Tk()
root.geometry('1000x700')


# Latest parse of programs/broadcast entries
DB_entries_program = {}
DB_entries_broadcast = {}


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
    # SQL
    print("parsing broadcastsss")

def parseDBEntries_program():
    try:
        connection = psycopg2.connect(user=DB_config.user,
                                      password=DB_config.password,
                                      host=DB_config.host,
                                      port=DB_config.port,
                                      database=DB_config.database)
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print (connection.get_dsn_parameters(), "\n")
        # Print PostgreSQL version
        cursor.execute("SELECT * FROM program;")
        record = cursor.fetchone()

        parsedEntries = {}
        print("Created parsedEntries")
        for entry in record:
            print("Filling parsedEntries")
            parsedEntries += entry[0] + " " + entry[1]

        print("Returning parsedEntries")
        return parsedEntries

    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL: ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# Initialize our country "databases":
#  - the list of country codes (a subset anyway)
#  - a parallel list of country names, in the same order as the country codes
#  - a hash table mapping country code to population<
countrycodes = ('ar', 'au', 'be', 'br', 'ca', 'cn', 'dk', 'fi', 'fr', 'gr', 'in', 'it', 'jp', 'mx', 'nl', 'no', 'es', 'se', 'ch')
countrynames = ('Argentina', 'Australia', 'Belgium', 'Brazil', 'Canada', 'China', 'Denmark', \
        'Finland', 'France', 'Greece', 'India', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway', 'Spain', \
        'Sweden', 'Switzerland')

cnames = StringVar(value=countrynames)
populations = {'ar':41000000, 'au':21179211, 'be':10584534, 'br':185971537, \
        'ca':33148682, 'cn':1323128240, 'dk':5457415, 'fi':5302000, 'fr':64102140, 'gr':11147000, \
        'in':1131043000, 'it':59206382, 'jp':127718000, 'mx':106535000, 'nl':16402414, \
        'no':4738085, 'es':45116894, 'se':9174082, 'ch':7508700}


# State variables
gift = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()


# Called when the selection in the listbox changes; figure out
# which country is currently selected, and then lookup its country
# code, and from that, its population.  Update the status message
# with the new population.  As well, clear the message about the
# gift being sent, so it doesn't stick around after we start doing
# other things.
def showPopulation(*args):
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        code = countrycodes[idx]
        name = countrynames[idx]
        popn = populations[code]
        statusmsg.set("The population of %s (%s) is %d" % (name, code, popn))
    sentmsg.set('')

# Called when the user double clicks an item in the listbox, presses
# the "Send Gift" button, or presses the Return key.  In case the selected
# item is scrolled out of view, make sure it is visible.
#
# Figure out which country is selected, which gift is selected with the
# radiobuttons, "send the gift", and provide feedback that it was sent.
def sendGift(*args):
    viewBroadcastInTable()

    print("selected: ", lbox.curselection())

    send["text"] = str(random.randint(1, 1000))
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = countrynames[idx]
        # Gift sending left as an exercise to the reader
        sentmsg.set("Sent %s to leader of %s" % (gifts[gift.get()], name))



# Perform parse of program in DB and fill table
def viewProgramInTable():
    updateTableWithList({"ID programnamn1", "ID programnamn2", "ID programnamn3"})

# Perform parse of broadcast in DB and fill table
def viewBroadcastInTable():
    updateTableWithList({"ID broadcast1", "ID broadcast2", "ID broadcast3"})

# Called to change content of table with invoked list
def updateTableWithList(list):
    lbox.delete(0, 'end')
    for item in list:
        lbox.insert('end', item)

    # Colorize alternating lines of the listbox
    for i in range(0, len(list), 2):
        lbox.itemconfigure(i, background='#f0f0ff')


# V----- CREATING GUI -------V

# Create and grid the outer content frame
c = ttk.Frame(root, padding=(10, 10, 24, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

# Create the different widgets; note the variables that many
# of them are bound to, as well as the button callback.
# Note we're using the StringVar() 'cnames', constructed from 'countrynames'
lbox = Listbox(c, listvariable=cnames, height=7)
lbl = ttk.Label(c, text="Manipulate database (selected):")

g1 = ttk.Radiobutton(c, text="Delete (selected)", variable=gift, value='delete')
g2 = ttk.Radiobutton(c, text="Update (selected)", variable=gift, value='update')
g3 = ttk.Radiobutton(c, text="Add new entry", variable=gift, value='add')

sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
viewProgramsBtn = ttk.Button(c, text='View Programs')
viewBroadcastsBtn = ttk.Button(c, text='View Broadcasts')
send = ttk.Button(c, text='Perform', command=sendGift, default='active')


# Grid all the widgets
lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
lbl.grid(column=1, row=0, padx=10, pady=5)
g1.grid(column=1, row=1, sticky=W, padx=20)
g2.grid(column=1, row=2, sticky=W, padx=20)
g3.grid(column=1, row=3, sticky=W, padx=20)
send.grid(column=2, row=4, sticky=E, pady=15)
sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
viewProgramsBtn.grid(column=1, row=6, columnspan=1)
viewBroadcastsBtn.grid(column=2, row=6, columnspan=1)
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

# Set event bindings for when the selection in the listbox changes,
# when the user double clicks the list, and when they hit the Return key
lbox.bind('<<ListboxSelect>>', showPopulation)
lbox.bind('<Double-1>', sendGift)
root.bind('<Return>', sendGift)


# ^----- CREATING GUI -------^


# Set the starting state of the interface, including selecting the
# default gift to send, and clearing the messages.  Select the first
# country in the list; because the <<ListboxSelect>> event is only
# generated when the user makes a change, we explicitly call showPopulation.
gift.set('card')
sentmsg.set('')
statusmsg.set('')
lbox.selection_set(0)
showPopulation()

root.mainloop()



