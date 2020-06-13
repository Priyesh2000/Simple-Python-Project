import sqlite3
from tkinter import *
from tkinter import messagebox
class DB:
    def __init__(self):
        self.con=sqlite3.connect("Employee.db")
        self.cursor=self.con.cursor()
        self.con.execute("CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY,name TEXT,department TEXT,employee_id INTEGER,Salary INTEGER)")
        
        self.con.commit()

    def __del__(self): #This is Distructor
        self.con.close() #close connection

#Get All Employees
    def employees(self):
        self.cursor.execute("SELECT * FROM EMPLOYEES")
        rows=self.cursor.fetchall() #get All Rows from database
        return rows
#Insert Data
    def insert(self,name,department,employee_id,Salary):
        self.cursor.execute("INSERT INTO employees VALUES(NULL,?,?,?,?)",(name,department,employee_id,Salary))
        self.con.commit()
#Search Into DATABASE
    def search(self,name="",department="",employee_id="", Salary=""):
        self.cursor.execute("SELECT * FROM employees WHERE name=? OR department=? OR employee_id=? OR Salary=?", (name,department,employee_id,Salary))
        found_rows=self.cursor.fetchall()
        return found_rows

#Delete From Database
    def delete(self,id):
        #print(id)
        self.cursor.execute("DELETE FROM employees where id=?",(id,))
        self.con.commit()


db=DB()  #Instantiate Our DB Class

    
def get_selected_row(event):
    global selected_tuple
    index=list1.curselection()[0]
    selected_tuple=list1.get(index)
    e1.delete(0,END)
    e1.insert(END,selected_tuple[1])
    e2.delete(0,END)
    e2.insert(END,selected_tuple[2])
    e3.delete(0,END)
    e3.insert(END,selected_tuple[3])
    e4.delete(0,END)
    e4.insert(END,selected_tuple[4])


def view_command():
    list1.delete(0,END)
    for row in db.employees():
        list1.insert(END,row)

def search_command():
    list1.delete(0,END)
    for row in db.search(name_text.get(),department_text.get(),employee_id_text.get(),Salary_text.get()):
        
        list1.insert(END,row)


def add_command():
    db.insert(name_text.get(),department_text.get(),employee_id_text.get(),Salary_text.get())
    list1.delete(0,END)
    list1.insert(END,(name_text.get(),department_text.get(),employee_id_text.get(),Salary_text.get()))



def delete_command():
    db.delete(selected_tuple[0])

    
window=Tk()
window.title("Employee Form")

def on_closing():
    dd=db
    
    if messagebox.askokcancel("Exit","Are you sure?"):
        window.destroy()
        del dd #DB destructor

window.protocol("WM_DELETE_WINDOW",on_closing)

l1=Label(window,text="Name")
l1.grid(row=0,column=0)

l2=Label(window,text="Department")
l2.grid(row=0,column=2)

l3=Label(window,text="ID")
l3.grid(row=1,column=0)

l4=Label(window,text="Salary")
l4.grid(row=1,column=2)

name_text=StringVar()
e1=Entry(window,textvariable=name_text)
e1.grid(row=0,column=1)

department_text=StringVar()
e2=Entry(window,textvariable=department_text)
e2.grid(row=0,column=3)

employee_id_text=StringVar()
e3=Entry(window,textvariable=employee_id_text)
e3.grid(row=1,column=1)

Salary_text=StringVar()
e4=Entry(window,textvariable=Salary_text)
e4.grid(row=1,column=3)

list1=Listbox(window,height=6,width=55)
list1.grid(row=2,column=0,rowspan=6,columnspan=2)

sb1=Scrollbar(window)
sb1.grid(row=2,column=2,rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>',get_selected_row)

b1=Button(window,text="View all",width=12,command=view_command)
b1.grid(row=2,column=3)

b2=Button(window,text="Search Entry",width=12,command=search_command)
b2.grid(row=3,column=3)

b3=Button(window,text="Add Entry",width=12,command=add_command)
b3.grid(row=4,column=3)



b5=Button(window,text="Delete Selected",width=12,command=delete_command)
b5.grid(row=6,column=3)

b6=Button(window,text="Close",width=12,command=window.destroy)
b6.grid(row=7,column=3)

window.mainloop()
