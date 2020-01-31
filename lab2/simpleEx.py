import PySimpleGUI as sg

layout = [ [sg.Text('Enter your name'), sg.InputText()],      
           [sg.OK()] ]

window = sg.Window('My first GUI').Layout(layout)
button, (name,) = window.Read()
