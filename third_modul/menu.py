from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from models import District, Region

def donothing():
    print("dskdslkds")

def oncloseTopWindow(window, toplevel):
    window.deiconify()
    window.state('zoomed')
    toplevel.destroy()

def onOpenRegionWindow(window):
    window.withdraw()
    regionwindow = Toplevel()
    regionwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, regionwindow))
    regionwindow.title("Regions")
    regionwindow.geometry('550x350')
    regionwindow.resizable(0, 0)

    lb_name = Label(regionwindow, text="Region Name: ")
    lb_name.grid(row=0, column=0)

    str_region_name = StringVar()

    entry_name = Entry(regionwindow, text=str_region_name)
    entry_name.grid(row=0, column=1)

    columns = ('region_name', )
    table = ttk.Treeview(regionwindow, columns=columns, show='headings')
    table.heading('region_name', text='Region name')
    table.grid(row=1, column=0)

    sel_region = None

    def onAddRegion():
        region = Region(entry_name.get())
        region.save()
        table.insert('', END, iid=region.id, values=region)

    def onClick(event):
        try:
            global sel_region
            id = int(table.focus())
            sel_region = Region.get_by_id(id)
            str_region_name.set(sel_region.name)
        except ValueError as err:
            pass
            #messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("O'chirishda xatolik", str(err))


    def onUpdateRegion():
        global sel_region
        focused = table.focus()
        sel_region.name = str_region_name.get()
        sel_region.save()
        str_region_name.set('')
        table.item(focused, values=sel_region)
        sel_region = None
    # bu ustoz ni ki
    def onDeleteRegion():
        global sel_region
        if sel_region:
            sel_region.delete()
            sel_region = None
            selected_item = table.selection()[0]
            table.delete(selected_item)
    table.bind('<<TreeviewSelect>>', onClick)

    btn_add = Button(regionwindow, text='Add', command=onAddRegion)
    btn_add.grid(row=0, column=2)

    btn_update = Button(regionwindow, text='Update', command=onUpdateRegion)
    btn_update.grid(row=0, column=3)

    btn_del = Button(regionwindow, text='Delete', command=onDeleteRegion)
    btn_del.grid(row=0, column=4)

    for region in Region.objects():
        table.insert('', END, iid=region.id, values=region)
    
def onOpenDistrictWindow(window):
    window.withdraw()
    districtwindow = Toplevel()
    districtwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, districtwindow))
    districtwindow.title("Districts")
    districtwindow.geometry('800x350')
    districtwindow.resizable(0, 0)

    sel_region = None
    cbb_regions = ttk.Combobox(districtwindow, value=tuple(Region.rows()))
    cbb_regions.grid(row=0, column=0)
    def selectedRegion(event):
        global sel_region
        array = cbb_regions.get().split(' ')
        id = int(array[0])
        sel_region = Region.get_by_id(id)

    current_var = ()
    
    cbb_regions.bind("<<ComboboxSelected>>", selectedRegion)


    lb_name = Label(districtwindow, text="District Name: ")
    lb_name.grid(row=0, column=1)

    str_district_name = StringVar()
    entry_name = Entry(districtwindow, text=str_district_name)
    entry_name.grid(row=0, column=2)

    columns = ('region_name', 'district_name')
    table = ttk.Treeview(districtwindow, columns=columns, show='headings')
    table.heading('region_name', text='Region name')
    table.heading('district_name', text='District name')
    table.grid(row=1, column=0, columnspan=3)

    sel_district = None
    def onAddDistrict():
        global sel_region
        district = District(entry_name.get(), sel_region.id)
        district.save()
        table.insert('', END, iid=district.id, values=district)

    def onClick(event):
        global sel_district, sel_region
        try:
            id = int(table.focus())
            sel_district = District.get_by_id(id)
            str_district_name.set(sel_district.name)
            sel_region = Region.get_by_id(sel_district.regionId)
            i = 0
            for item in Region.objects():
                if item.id == sel_district.regionId:
                    break
                i += 1
            cbb_regions.current(i)
        except:
            pass

    def onUpdateDistrict():
        global sel_region, sel_district
        focused = table.focus()
        sel_district.name = str_district_name.get()
        sel_district.save()
        str_district_name.set('')
        table.item(focused, values=sel_district)
        sel_region = None

    def onDeleteDistrict():
        global sel_region, sel_district
        if sel_district:
            sel_district.delete()
            sel_district = None
            selected_item = table.selection()[0]
            table.delete(selected_item)

    table.bind('<<TreeviewSelect>>', onClick)

    btn_add = Button(districtwindow, text='Add', command=onAddDistrict)
    btn_add.grid(row=0, column=3)

    btn_update = Button(districtwindow, text='Update',
                        command=onUpdateDistrict)
    btn_update.grid(row=0, column=4)

    btn_del = Button(districtwindow, text='Delete', command=onDeleteDistrict)
    btn_del.grid(row=0, column=5)

    for district in District.objects():
        table.insert('', END, iid=district.id, values=district)

def makeMenu(window):
    menubar = Menu(window)

    filemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Close", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)


    editmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=editmenu)
    editmenu.add_command(label="Undo", command=donothing)
    editmenu.add_separator()
    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)

    servicemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Services", menu=servicemenu)
    servicemenu.add_command(label="Regions", command=lambda: onOpenRegionWindow(window))
    servicemenu.add_command(label="Districts", command=lambda: onOpenDistrictWindow(window))

    return menubar
