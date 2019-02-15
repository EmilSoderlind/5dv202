from tkinter import *

from tkinter import ttk
import random

window = Tk()

window.geometry("700x700")
window.title("SR CRUD CLIENT")

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)

tab_control.add(tab1, text='EDIT Program')
tab_control.add(tab2, text='Browse Program')
tab_control.add(tab3, text='EDIT Broadcast')
tab_control.add(tab4, text='Browse Broadcast')

def clicked():

    print("Adding button!")
    newBtn = Button(tab1, text="newBtn")
    newBtn.grid(column=random.randint(1, 10), row=random.randint(1, 50))

lbl1 = Label(tab1, text='ID', font=("Arial Bold", 50))
lbl1_b = Label(tab1, text='Name', font=("Arial Bold", 50))

parseBtn = Button(tab1, text="Parse")
parseBtn.grid(column=0, row=0)
addBtn = Button(tab1, text="Add")
addBtn.grid(column=1, row=0)
removeBtn = Button(tab1, text="Remove", command=clicked)
removeBtn.grid(column=2, row=0)

lbl1_b.grid(column=1,row=1)
lbl1.grid(column=0, row=1)

scrollbar = Scrollbar(tab2)

listbox = Listbox(tab2, yscrollcommand=scrollbar.set)
for i in range(1000):
    listbox.insert(END, str(i) + " | Jag gillar glass, det är gott med glass. MUMS!")
listbox.pack(side=TOP, fill=BOTH)

scrollbar.config(command=listbox.yview)


tab_control.pack(expand=1, fill='both')

window.mainloop()