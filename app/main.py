from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image,ImageTk
import sqlite3
import os

class App:
    def __init__(self):
        #! Initialization 
        self.root = Tk()
        self.root.title('Contact Manager')
        icon = PhotoImage(file = 'Image/icon/icon1.png')
        self.root.iconphoto(False, icon)
        
        #! Toggle between fullscreen and maximized 
        self.fullScreenState = True
        self.root.attributes("-fullscreen", self.fullScreenState)
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("<Escape>", self.quit)
        
        #! All variables
        self.id_var = IntVar()
        self.name_var = StringVar()
        self.contact_var = StringVar()
        self.photo_var = StringVar()
        self.info_var = StringVar()
        self.search_by = StringVar()
        self.search_text = StringVar()
        
        #! Title
        title = Label(self.root,text='Contact Manager',bd=10,relief=GROOVE,font=('times new roman',40,'bold'),bg='blue',fg='white')
        title.pack(side=TOP,fill=X)
        
        #! Manage Frame
        Manage_Frame = Frame(self.root,bd=4,relief=RIDGE,bg='blue')
        Manage_Frame.place(x=20,y=100,width=450,height=675)
        
        #! Profile image
        self.image_frame = Label(Manage_Frame,bg='blue',bd=5,relief=GROOVE)
        self.defalt_img = Image.open('Image\Profile.png')
        self.defalt_img = self.defalt_img.resize((210,240),Image.ANTIALIAS) 
        self.profile = ImageTk.PhotoImage(self.defalt_img)
        self.image_frame.config(image=self.profile)
        self.image_frame.place(x=120,y=30,width=210,height=240)
        
        #! Label & Entry Name
        lblName = Label(Manage_Frame,text="Name:",bg="blue",fg="white",font=('times new roman',15,'bold'))
        lblName.place(x=5,y=300,width=125)
        entryName = Entry(Manage_Frame,font=('times new roman',15),textvariable=self.name_var)
        entryName.place(x=140,y=300,width=290)
        
        #! Label & Entry Phone
        lblPhone = Label(Manage_Frame,text="Phone Number:",bg="blue",fg="white",font=('times new roman',15,'bold'))
        lblPhone.place(x=5,y=350,width=125)
        entryPhone = Entry(Manage_Frame,font=('times new roman',15),textvariable=self.contact_var)
        entryPhone.place(x=140,y=350,width=290)

        #! Label & Entry & Buttton Photo
        lblPhoto = Label(Manage_Frame,text="Photo:",bg="blue",fg="white",font=('times new roman',15,'bold'))
        lblPhoto.place(x=5,y=400,width=125)
        self.photo_var.set('Image\Profile.png') 
        self.entryPhoto = Entry(Manage_Frame,font=('times new roman',15),textvariable=self.photo_var)
        self.entryPhoto.place(x=140,y=400,width=220)
        bPhoto = Button(Manage_Frame,text="Browse",bg="darkblue",fg="yellow",command=self.browsePhoto,font=('times new roman',12))
        bPhoto.place(x=370,y=400,height=25)
        

        #! Label & Entry Info
        lblMore = Label(Manage_Frame,text="More Info:",bg="blue",fg="white",font=('times new roman',15,'bold'))
        lblMore.place(x=5,y=450,width=125)
        entryMore = Entry(Manage_Frame,font=('times new roman',15),textvariable=self.info_var)
        entryMore.place(x=140,y=450,width=290)
        
        #! Button Frame
        Button_Frame = Frame(Manage_Frame,bd=4,relief=GROOVE,bg='blue')
        Button_Frame.place(x=5,y=500,width=430,height=155)
        
        #! Buttons
        add_btn = Button(Button_Frame,text='Add',width=55,bg="darkblue",fg="yellow",font=('times new roman',10),command=self.adding).grid(row=0,column=0,padx=15,pady=5)
        update_btn = Button(Button_Frame,text='Update',width=55,bg="darkblue",fg="yellow",font=('times new roman',10),command=self.updating).grid(row=1,column=0,padx=15,pady=5)
        delete_btn = Button(Button_Frame,text='Delete',width=55,bg="darkblue",fg="yellow",font=('times new roman',10),command=self.deleting).grid(row=2,column=0,padx=15,pady=5)
        clear_btn = Button(Button_Frame,text='Clear',width=55,bg="darkblue",fg="yellow",font=('times new roman',10),command=self.clear).grid(row=3,column=0,padx=15,pady=5)
        
        #! Detail Frame
        Detail_Frame = Frame(self.root,bd=4,relief=RIDGE,bg='blue')
        Detail_Frame.place(x=500,y=100,width=1015,height=675)
        
        #! Search label
        lbl_search = Label(Detail_Frame,text='Search By',font=('times new roman',20,'bold'),bg='blue',fg='white')
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky='w')
    
        #! Search dropdown 
        combo_search = ttk.Combobox(Detail_Frame,font=('times new roman',13,'bold'),state='readonly',width=10,textvariable=self.search_by)  
        combo_search['values'] = ('name','contacts','info')
        combo_search.current(0)
        combo_search.grid(row=0,column=1,pady=10,padx=20,sticky='w')
        
        #! Search text
        text_search = Entry(Detail_Frame,font=('times new roman',10,'bold'),bd=5,relief=GROOVE,width=25,textvariable=self.search_text)    
        text_search.grid(row=0,column=2,pady=10,padx=20,sticky='w')
        
        #! Search and Show all buttons
        search_btn = Button(Detail_Frame,text='Search',width=15,pady=5,bg='darkblue',fg='yellow',command=self.search_data).grid(row=0,column=3,padx=20,pady=5) 
        showAll_btn = Button(Detail_Frame,text='Show All',width=15,pady=5,bg='darkblue',fg='yellow',command=self.fetch_data).grid(row=0,column=4,padx=20,pady=5) 
        sort_btn = Button(Detail_Frame,text='Sort by name',width=15,pady=5,bg='darkblue',fg='yellow',command=self.sort_by_name).grid(row=0,column=5,padx=20,pady=5)
        
        #! Table Frame
        Table_Frame = Frame(Detail_Frame,bd=4,relief=RIDGE,bg='blue')
        Table_Frame.place(x=10,y=60,width=985,height=600)
        
        #! Table 
        scroll_x = Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame,orient=VERTICAL)
        self.Contact_table = ttk.Treeview(Table_Frame,columns=('id','name','contact','info','photo'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Contact_table.xview)
        scroll_y.config(command=self.Contact_table.yview)
        self.Contact_table.heading('id',text='Sr. no.')
        self.Contact_table.heading('name',text='Name')
        self.Contact_table.heading('contact',text='Contact')
        self.Contact_table.heading('info',text='More info')
        self.Contact_table.heading('photo',text='Photo Directory')
        self.Contact_table['show'] = "headings"
        self.Contact_table.column('id',width=100)
        self.Contact_table.column('name',width=100)
        self.Contact_table.column('contact',width=100)
        self.Contact_table.column('info',width=130)
        self.Contact_table.column('photo',width=130)
        self.Contact_table.pack(fill=BOTH,expand=True)
        self.Contact_table.bind('<ButtonRelease-1>',self.get_cursor)
        self.fetch_data()
        
        #! Info Keys log
        self.lblInstruction = Label(self.root,text="F11 - Toggle Fullscreen , Escape - Quit",bg="blue",fg="white",font=('times new roman',15,'bold'),bd=5,relief=GROOVE)
        self.lblInstruction.pack(side=BOTTOM,fill=X)

        #! Mainloop
        self.root.mainloop() 
        
    #! toggle FullScreen
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)
    
    #! Quit program
    def quit(self, event):
        self.root.quit()
        
    #! Browse photo directory
    def browsePhoto(self):
        self.filename = filedialog.askopenfilename(initialdir='/',title='Select File')
        self.photo_var.set(self.filename) 
        self.defalt_img = Image.open(self.photo_var.get())
        self.defalt_img = self.defalt_img.resize((210,240),Image.ANTIALIAS) 
        self.profile = ImageTk.PhotoImage(self.defalt_img)
        self.image_frame.config(image=self.profile)

    #! Create SQL
    def create_table(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS "Contacts" 
                    ("id"INTEGER,"name"TEXT,"contacts"TEXT,"info"TEXT,"photo"TEXT,PRIMARY KEY("id" AUTOINCREMENT))''')
        con.commit()
        con.close()

    #! Fetching data
    def fetch_data(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        self.create_table()
        cur.execute('''SELECT * FROM Contacts''')
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Contact_table.delete(*self.Contact_table.get_children())
            for row in rows:
                self.Contact_table.insert('',END,values=row)
            con.commit()
        con.close()
        
    #! Get cursor 
    def get_cursor(self,event):
        try:
            cursor_row = self.Contact_table.focus()
            content = self.Contact_table.item(cursor_row)
            row = content['values']
            self.id_var.set(row[0])
            self.name_var.set(row[1])
            self.contact_var.set(row[2])
            self.info_var.set(row[3])
            self.photo_var.set(row[4])
            self.defalt_img = Image.open(self.photo_var.get())
            self.defalt_img = self.defalt_img.resize((210,240),Image.ANTIALIAS) 
            self.profile = ImageTk.PhotoImage(self.defalt_img)
            self.image_frame.config(image=self.profile)
        except IndexError:
            pass

    #! Clear text area    
    def clear(self):
        self.name_var.set('')
        self.contact_var.set('')
        self.photo_var.set('Image\Profile.png') 
        self.info_var.set('')
        self.search_text.set('')
        self.defalt_img = Image.open(self.photo_var.get())
        self.defalt_img = self.defalt_img.resize((210,240),Image.ANTIALIAS) 
        self.profile = ImageTk.PhotoImage(self.defalt_img)
        self.image_frame.config(image=self.profile)
        self.lblInstruction.config(text='F11 - Toggle Fullscreen , Escape - Quit')
        
    #! Check for valid data
    def valid_contact(self,number):
        if len(number) == 10 and number.isdigit():
            return True
        return False
    
    #! Adding data 
    def adding(self):
        name = self.name_var.get()
        contact = self.contact_var.get()
        photo = self.photo_var.get()
        info = self.info_var.get()
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        
        if self.valid_contact(contact):
            select = cur.execute('''SELECT * FROM Contacts order by id desc''')
            select = list(select)
            id = 1
            if len(select) != 0:
                id = select[0][0] + 1
            img = Image.open(photo)
            rgb_img = img.convert('RGB')
            photo_dir = "Image/Profile_" + str(id) + ".jpg"
            rgb_img.save((photo_dir))
            data = (name,contact,info,photo_dir)
            cur.execute('''INSERT INTO Contacts (name,contacts,info,photo) VALUES (?,?,?,?);''',data)
            con.commit()
            con.close()
            self.fetch_data()
            self.clear()
            self.lblInstruction.config(text='Contact has been added')
        else:
            self.lblInstruction.config(text='Invalid contact number')
        
    #! Update data
    def updating(self):
        name = self.name_var.get()
        contact = self.contact_var.get()
        photo = self.photo_var.get()
        info = self.info_var.get()
        id = self.id_var.get()
        if self.valid_contact(contact):
            img = Image.open(photo)
            rgb_img = img.convert('RGB')
            photo_dir = "Image/Profile_" + str(id) + ".jpg"
            rgb_img.save((photo_dir))
            data = (name,contact,info,photo_dir,id)
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute('''UPDATE Contacts SET name = ?,contacts = ?,info = ?,photo= ? WHERE id = ?;''',data)
            con.commit()
            con.close()
            self.fetch_data()
            self.clear()
            self.lblInstruction.config(text='Contact has been updated')
        else:
            self.lblInstruction.config(text='Invalid contact number')
        
    #! Delete data
    def deleting(self):
        id = self.id_var.get()
        data = (id,)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('''DELETE FROM Contacts WHERE id = ?;''',data)
        con.commit()
        con.close()
        fname = "Image/Profile_" + str(id) + ".jpg"
        if os.path.isfile(fname): 
            os.remove(fname)
        self.fetch_data()
        self.clear()
        self.lblInstruction.config(text='Contact has been deleted')
    
    #! Search data
    def search_data(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        self.create_table()
        search_by = self.search_by.get()
        search_text = '%'+self.search_text.get()+'%'
        if search_by == 'contacts':
            query = '''SELECT * FROM Contacts WHERE contacts LIKE (?);'''
        elif search_by == 'info':
            query = '''SELECT * FROM Contacts WHERE info LIKE (?);'''
        else:
            query = '''SELECT * FROM Contacts WHERE name LIKE (?);'''
        cur.execute(query,(search_text,))
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Contact_table.delete(*self.Contact_table.get_children())
            for row in rows:
                self.Contact_table.insert('',END,values=row)
            con.commit()
        con.close()
        
    #! Sorting data by name
    def sort_by_name(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        self.create_table()
        cur.execute('''SELECT * FROM Contacts ORDER BY name''')
        rows = cur.fetchall()
        
        if len(rows) != 0:
            self.Contact_table.delete(*self.Contact_table.get_children())
            for row in rows:
                self.Contact_table.insert('',END,values=row)
            con.commit()
        con.close()

if __name__ == '__main__':
    app = App()  
