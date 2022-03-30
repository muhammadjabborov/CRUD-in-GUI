from tkinter import *
from menu import makeMenu

window = Tk()
window.title("Talabalar bilan ishlash dasturi")
from styles import style

menubar = makeMenu(window)
window.config(menu=menubar)
window.state('zoomed')

window.mainloop()

from models import Region,District




