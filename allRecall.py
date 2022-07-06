from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from pystray import MenuItem as item
import pystray as pys
from datetime import datetime as dt
import pyperclip as clip
from PIL import Image, ImageTk

class app(Tk):
    def __init__(self):
        super().__init__()

        self.selected_items = []

        #vars
        self.value = StringVar()
        self.value.set(clip.paste())

        img = Image.open("favicon.png").convert("RGBA")
        test = ImageTk.PhotoImage(img)
        label1 = Label(image=test, bg="#262626", bd=0, highlightthickness=0)
        label1.image = test
        label1.pack()


        """img = Image.open("favicon.png").convert("RGBA")
        photoimage = ImageTk.PhotoImage(img)
        width, height = photoimage.width(), photoimage.height()
        canvas = Canvas(self, width=width, height=height, bg="#262626", bd=0, highlightthickness=0)
        canvas.pack()
        canvas.create_image(0, 0, image=photoimage, anchor=NW)"""


        estyle = ttk.Style()
        estyle.element_create("plain.field", "from", "clam")
        estyle.layout("EntryStyle.TEntry",
                        [('Entry.plain.field', {'children': [(
                            'Entry.background', {'children': [(
                                'Entry.padding', {'children': [(
                                    'Entry.textarea', {'sticky': 'nswe'})],
                            'sticky': 'nswe'})], 'sticky': 'nswe'})],
                            'border':'2', 'sticky': 'nswe'})])
        estyle.configure("EntryStyle.TEntry",
                        background="green", 
                        foreground="white",
                        fieldbackground="#404040", padding='5 0 5 0')
        estyle.configure('mystyle.Treeview.Heading', font=('Calibri', 11, BOLD))
        estyle.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 10), background='#404040', fieldbackground="#404040", foreground='white')
        estyle.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.entry1 = ttk.Entry(width=25, exportselection=0, font=('Arial', 10), textvariable=self.value, style="EntryStyle.TEntry")
        self.entry1.bind('<Return>', lambda e: self.btnaction())
        self.entry1.pack(ipady=6, pady=15)

        Border = Frame(self,
                    highlightbackground="white",
                                  highlightthickness=2, bd=0)
        

        self.btn = Button(Border, text="Add", command=self.btnaction, bg='#404040', fg='white', relief="solid", borderwidth=0, width=10)
        self.btn.pack()
        Border.pack()

        self.treeview = ttk.Treeview(columns=('text', 'size', 'doe', 'status'), show='headings', height=10, style="mystyle.Treeview", selectmode="browse", cursor="tcross")
        
        self.treeview.heading('text', text='Text')
        self.treeview.heading('size', text='Size')
        self.treeview.heading('doe', text='Date of Entry')
        self.treeview.heading('status', text='Status')

        self.treeview.bind('<<TreeviewSelect>>', self.itemfocus)
        
        self.treeview.column('text', minwidth=250, anchor=W)
        self.treeview.column('size', width=50, anchor=CENTER)
        self.treeview.column('doe', width=150, anchor=CENTER)
        self.treeview.column('status', width=110, anchor=CENTER)
        
        self.treeview.pack(pady=15)

        #adding Items to treeview
        self.initItems('f')

    def itemfocus(self, event):
        for item_ in self.selected_items:
            self.treeview.set(item_, column='status', value='')
            del(self.selected_items[0])

        for selected_item in self.treeview.selection():
            
            item = self.treeview.item(selected_item)
            value = item['values'][0]
            clip.copy(value)

            self.selected_items.append(selected_item)
            self.treeview.set(selected_item, column='status', value='Copied!')
            
            break

    def initItems(self, e):
        #Setting Data inside the Treeview
        # generate sample data
        
        """contacts = []
        for n in range(1, 50):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com', ''))"""

        data = []
        self.f = open("data_allread.txt", "a+")
        self.f.seek(0, 0)
        lines = self.f.readlines()
        for line in reversed(lines):
            line.replace('\n', '')
            word_list = line.split(',')
            mainval = word_list[0].replace('xxx', ',')
            data.append((mainval, word_list[1], word_list[2]))
        
        self.f.close()
        # add data to the treeview
        self.n = 1
        self.ids = []
        for data_ in data:
            if(self.n%2)!=0:
                id = self.treeview.insert('', END, values=data_, tags=('tag'+str(self.n), 'odd'))
            else:
                id = self.treeview.insert('', END, values=data_, tags=('tag'+str(self.n),))
            self.ids.append(id)
            self.n +=1

        self.treeview.tag_configure('odd', background='#2E5984', foreground='white')

    def btnaction(self):
        val = self.value.get()
        valnew = val.replace(',', 'xxx')
        now = dt.now()
        date = str(now.strftime("%b-%d %Y"))
        
        self.f = open("data_allread.txt", "a+")
        self.f.seek(0, 0)
        filedata = valnew+","+str(len(val))+","+date
        self.f.write(filedata.rstrip("\t\r\n")+"\n")
        self.f.close()
        
        id = self.treeview.insert('', 0, values=[val, str(len(val)), date], tags=('tag'+str(self.n),))
        self.ids.append(id)

        self.entry1.delete(0, 'end')

        ###for id in self.ids:
        #self.treeview.delete(id)
        #self.initItems()###

    def quit_window(self, icon):
        icon.stop()
        self.destroy()

    def show_window(self, icon):
        icon.stop()
        self.after(0, self.deiconify)

    def hide_window(self):
        self.withdraw()
        image = Image.open("favicon.ico")
        menu = (item('Show', self.show_window)), item('Quit', self.quit_window)
        icon = pys.Icon("allRecall", image, "Open allRecall", menu)
        icon.run()

    def hide_window_esc(self, e):
        self.hide_window()

if(__name__ == "__main__"):
    appw = app()
    appw.title("allRecall")
    appw.geometry('680x400+750+455')
    appw.protocol("WM_DELETE_WINDOW", appw.hide_window)
    appw.wm_state('normal')
    appw.resizable(0, 0)
    appw.configure(bg='#262626')
    appw.overrideredirect(1)
    appw.attributes("-topmost", True)
    appw.bind('<Escape>', appw.hide_window_esc)
    appw.mainloop()









