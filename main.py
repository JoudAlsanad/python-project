from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, END as fd
import re
from random import randint
from datetime import date
from datetime import datetime


class Forms:
    generalvar = "00"

    def _init_(self):
        self.createDB()
        self.signupForm()

    def createDB(self):
        connection = sqlite3.connect('TSDatabase.db')

        c = connection.cursor()
        c.execute(''' Create table IF NOT EXISTS userinf(
                    user_id char(10) Primary Key,first_Name char(50),last_Name char(30), Password char(20),
                    Email char(30),mobile char(10)); ''')

        c.execute(''' Create table IF NOT EXISTS eventsinf(
                    event_id  Char(5) Primary Key , event_Name char(50),event_location char(40),capacity INT,
                    event_date  timestamp, event_time char(5)); ''')

        c.execute(''' Create table IF NOT EXISTS tickit(tickit_id Char(5) Primary Key,user_id char(10),event_id char(5),
                      FOREIGN KEY(user_id) REFERENCES userinf(userid) ,FOREIGN KEY(event_id) REFERENCES eventsinf(event_id)); ''')
        connection.commit()
        connection.close()
        print("hello again")
        return

    def signupForm(self):
        self.CreateSignupForm()
        return

    def signinForm(self):
        self.main_window.destroy()
        self.CreateLoginForm()
        return

    def eventsForm(self):
        self.main_window.destroy()
        self.CreateActivitiesForm()
        return

    def tickitForm(self):
        self.main_window.destroy()
        self.CreateBookingForm()
        return

    def logout(self):
        self.main_window.destroy()
        self.CreateLoginForm()
        return

    def CreateSignupForm(self):
        self.main_window = tk.Tk()
        self.main_window.geometry('600x200')
        self.main_window.title("Sign up")
        self.top_frame1 = ttk.Frame(self.main_window)
        self.top_frame2 = ttk.Frame(self.main_window)
        self.top_frame3 = ttk.Frame(self.main_window)
        self.bottom_frame = ttk.Frame(self.main_window)

        self.prompt_label1 = ttk.Label(self.top_frame1, text='      user id:')
        self.userid_entry = ttk.Entry(self.top_frame1, width=15)

        self.prompt_label2 = ttk.Label(self.top_frame2, text='First Name:')
        self.first_name_entry = ttk.Entry(self.top_frame2, width=20)

        self.prompt_label3 = ttk.Label(self.top_frame2, text='Last Name:')
        self.last_name_entry = ttk.Entry(self.top_frame2, width=20)

        self.prompt_label4 = ttk.Label(self.top_frame2, text='  Password:')
        self.password_entry = ttk.Entry(self.top_frame2, width=20)

        self.prompt_label5 = ttk.Label(self.top_frame3, text='        Emai:')
        self.email_entry = ttk.Entry(self.top_frame3, width=40)

        self.prompt_label6 = ttk.Label(self.top_frame3, text='Mobile Number:')
        self.mobile_entry = ttk.Entry(self.top_frame3, width=20)

        self.submit_button = ttk.Button(self.bottom_frame, text='Submit', command=self.saveUserInf)
        self.login_button = ttk.Button(self.bottom_frame, text='Login', command=self.signinForm)

        self.prompt_label1.pack(side='left')
        self.userid_entry.pack(side='left')

        self.prompt_label2.pack(side='left')
        self.first_name_entry.pack(side='left')

        self.prompt_label3.pack(side='left')
        self.last_name_entry.pack(side='left')

        self.prompt_label4.pack(side='left')
        self.password_entry.pack(side='left')

        self.prompt_label5.pack(side='left')
        self.email_entry.pack(side='left')

        self.prompt_label6.pack(side='left')
        self.mobile_entry.pack(side='left')

        self.submit_button.pack(side='left')
        self.login_button.pack(side='left')

        self.top_frame1.pack(anchor=W, padx=10, pady=10)
        self.top_frame2.pack(anchor=W, padx=10, pady=10)
        self.top_frame3.pack(anchor=W, padx=10, pady=10)

        self.bottom_frame.pack(padx=10, pady=10)

        tk.mainloop()

    def clearuserinfForm(self):
        self.userid_entry.delete(0, END)
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.mobile_entry.delete(0, END)

    def saveUserInf(self):
        try:
            connection = sqlite3.connect('TSDatabase.db')
            c = connection.cursor()

            userid = str(self.userid_entry.get())
            id = re.search(re.compile("^[0-9]{10}$"), userid)
            # validate user id
            if not id:
                messagebox.showinfo("input format", "user id should digits of 10th length")
                return
            # validate first name
            first_name = str(self.first_name_entry.get())
            if len(first_name) == 0:
                messagebox.showinfo("required input", "first name can not be null")
                return
            last_name = str(self.last_name_entry.get())
            if len(last_name) == 0:
                messagebox.showinfo("required input", "last name can not be null")
                return
            # validate password
            password = str(self.password_entry.get())
            passwd = re.search(re.compile("^[A-Za-z0-9]{6,20}$"), password)
            if not passwd:
                messagebox.showinfo("input format", "password should be length between 6 to 20")
                return

            # validate phone
            mobile = str(self.mobile_entry.get())
            mb = re.search(re.compile("^(05)[0-9]{8}$"), mobile)
            if not mb:
                messagebox.showinfo("input format", "phone Number should be in form of 05XXXXXXXX")
                return
            # validate email
            email = str(self.email_entry.get())
            em = re.search(re.compile("^([a-zA-Z0-9\._-]+){8}@ksu\.edu\.sa$"), email)
            if not em:
                messagebox.showinfo("input format", "Email formate should  be xxxxxxxx@ksu.edu.sa ")
                return
            # add user information to the database
            id = c.execute(f"SELECT user_id FROM userinf WHERE user_id = {userid}")
            if len(id.fetchall()) == 0:
                c.execute(
                    f"insert into userinf values('{userid}','{first_name}','{last_name}','{password}','{email}','{mobile}')")
                connection.commit()
                messagebox.showinfo("Success Message", "user information has been saved")
                self.clearuserinfForm()

            else:
                messagebox.showinfo("user id exist", "The input user id is exist")
            connection.close()
        except sqlite3.Error:
            messagebox.showinfo("connect fail", "can't execute the command")

        except:
            messagebox.showinfo("Error", "error")

        return

    # =========================================== login =================================
    def CreateLoginForm(self):
        self.main_window = tk.Tk()
        self.main_window.geometry('250x150')
        self.main_window.title("Login")
        self.top_frame1 = ttk.Frame(self.main_window)
        self.top_frame2 = ttk.Frame(self.main_window)

        self.bottom_frame = ttk.Frame(self.main_window)

        self.prompt_label1 = ttk.Label(self.top_frame1, text='       user id:')
        self.userid_entry = ttk.Entry(self.top_frame1, width=25)

        self.prompt_label2 = ttk.Label(self.top_frame2, text='  Password:')
        self.password_entry = ttk.Entry(self.top_frame2, width=25, show='*')

        self.login_button = ttk.Button(self.bottom_frame, text='Login', command=self.MatchUserInf)

        self.prompt_label1.pack(side='left')
        self.userid_entry.pack(side='left')

        self.prompt_label2.pack(side='left')
        self.password_entry.pack(side='left')

        self.login_button.pack(side='left')

        self.top_frame1.pack(anchor=W, padx=10, pady=10)
        self.top_frame2.pack(anchor=W, padx=10, pady=10)

        self.bottom_frame.pack(padx=10, pady=10)

        tk.mainloop()

    def clearloginForm(self):
        self.userid_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def MatchUserInf(self):
        try:
            connection = sqlite3.connect('TSDatabase.db')
            c = connection.cursor()

            userid = str(self.userid_entry.get())
            id = re.search(re.compile("^[0-9]{10}$"), userid)
            # validate user id
            if not id:
                messagebox.showinfo("input format", "user id should digits of 10th length")
                self.clearloginForm()
                return

            # add user information to the database
            id = c.execute(
                f"SELECT user_id FROM userinf WHERE user_id = {userid} and password={self.password_entry.get()}")
            if len(id.fetchall()) == 0:
                if userid == "0000000000" and self.password_entry.get() == "0000000000":
                    self.eventsForm()
                else:
                    messagebox.showinfo("Login fail", "incorrect user id or password ")
                    self.clearloginForm()

            else:
                self.generalvar = self.userid_entry.get()
                self.tickitForm()

            connection.close()
        except sqlite3.Error:
            messagebox.showinfo("connect fail", "can't execute the command")

        except:
            messagebox.showinfo("Error", "error")

        return

    # ============================= Create Activites ==============================
    def CreateActivitiesForm(self):
        self.main_window = tk.Tk()
        self.main_window.geometry('600x200')
        self.main_window.title("Activities Details")
        self.top_frame1 = ttk.Frame(self.main_window)
        self.top_frame2 = ttk.Frame(self.main_window)
        self.top_frame3 = ttk.Frame(self.main_window)
        self.bottom_frame = ttk.Frame(self.main_window)

        self.prompt_label1 = ttk.Label(self.top_frame1, text='    Event Name:')
        self.Event_Name_entry = ttk.Entry(self.top_frame1, width=35)

        self.prompt_label2 = ttk.Label(self.top_frame1, text='Event Location:')
        self.Event_Location_entry = ttk.Entry(self.top_frame1, width=30)

        self.prompt_label3 = ttk.Label(self.top_frame2, text='Event Capacity:')
        self.Event_Capacity_entry = ttk.Entry(self.top_frame2, width=20)

        self.prompt_label4 = ttk.Label(self.top_frame2, text='Event Date:')
        self.Event_Date_entry = ttk.Entry(self.top_frame2, width=20)

        self.prompt_label5 = ttk.Label(self.top_frame3, text='      Event Time:')
        self.Event_Time_entry = ttk.Entry(self.top_frame3, width=10)

        self.submit_button = ttk.Button(self.bottom_frame, text='Create', command=self.saveActivitiesInf)
        self.login_button = ttk.Button(self.bottom_frame, text='Logout', command=self.logout)

        self.prompt_label1.pack(side='left')
        self.Event_Name_entry.pack(side='left')

        self.prompt_label2.pack(side='left')
        self.Event_Location_entry.pack(side='left')

        self.prompt_label3.pack(side='left')
        self.Event_Capacity_entry.pack(side='left')

        self.prompt_label4.pack(side='left')
        self.Event_Date_entry.pack(side='left')

        self.prompt_label5.pack(side='left')
        self.Event_Time_entry.pack(side='left')

        self.submit_button.pack(side='left')
        self.login_button.pack(side='left')

        self.top_frame1.pack(anchor=W, padx=10, pady=10)
        self.top_frame2.pack(anchor=W, padx=10, pady=10)
        self.top_frame3.pack(anchor=W, padx=10, pady=10)

        self.bottom_frame.pack(padx=10, pady=10)

        tk.mainloop()

    def clearEventinfForm(self):
        self.Event_Name_entry.delete(0, END)
        self.Event_Location_entry.delete(0, END)
        self.Event_Capacity_entry.delete(0, END)
        self.Event_Date_entry.delete(0, END)
        self.Event_Time_entry.delete(0, END)

    def saveActivitiesInf(self):
        try:
            connection = sqlite3.connect('TSDatabase.db')
            c = connection.cursor()

            event_id = randint(10000, 99999)

            # validate Event Name
            event_name = self.Event_Name_entry.get()
            if len(event_name) == 0:
                messagebox.showinfo("required input", "Event Name can not be null")
                return
            event_location = self.Event_Location_entry.get()
            if len(event_location) == 0:
                messagebox.showinfo("required input", "Event Location can not be null")
                return
            # validate Event Capacity
            capacity = self.Event_Capacity_entry.get()
            if not capacity:
                messagebox.showinfo("required input", "Capacity can not be null")
                return
            cap = re.search(re.compile("^[0-9]*$"), str(capacity))

            if not cap:
                messagebox.showinfo("Data Formate Error", "Event capacity must be integer number")
                return
                # Validate Event Date
            event_date = self.Event_Date_entry.get()
            if not event_date:
                messagebox.showinfo("required input", "Event Date can not be null")
                return
            eventd = re.search(re.compile("^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$"), event_date)
            if not eventd:
                messagebox.showinfo("Date format Error", "Date formate not correct")
                return
                # Validate Event Time
            event_time = str(self.Event_Time_entry.get())
            eventtime = re.search(re.compile("^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"), event_time)
            if not eventtime:
                messagebox.showinfo("Time format Error", "Time formate not correct")
                return

            # check if the event id allready created
            id = c.execute(f"SELECT user_id FROM userinf WHERE user_id = {event_id}")
            if len(id.fetchall()) == 0:
                c.execute(
                    f"insert into eventsinf values('{event_id}','{event_name}','{event_location}','{capacity}','{event_date}','{event_time}')")
                connection.commit()
                messagebox.showinfo("Success Message", "Event information has been saved")
                self.clearEventinfForm()

            else:
                messagebox.showinfo("user id exist", "The input user id is exist")
            connection.close()
        except sqlite3.Error:
            messagebox.showinfo("connect fail", "can't execute the command")

        except:
            messagebox.showinfo("Error", "error")

        return

    # =================================== Booking Tickits =========================================
    def CreateBookingForm(self):
        self.main_window = tk.Tk()
        self.main_window.geometry('650x400')
        self.main_window.title("Activities Details")

        # create a notebook
        self.my_notebook = ttk.Notebook(self.main_window)
        self.my_notebook.pack(expand=1, fill=BOTH)

        # Create Tabs
        Book_Tickit_Tab = ttk.Frame(self.my_notebook)
        self.my_notebook.add(Book_Tickit_Tab, text="Book Tickit")
        My_tickits_Tab = ttk.Frame(self.my_notebook)
        self.my_notebook.add(My_tickits_Tab, text="my Tickits")

        # Book tickit details
        Label(Book_Tickit_Tab, text="Active Events", font=('Helvetica 20 bold')).grid(column=0, row=0, columnspan=4,
                                                                                      padx=10, pady=10)
        self.atcivites_treeView = ttk.Treeview(Book_Tickit_Tab, selectmode='browse')
        self.atcivites_treeView.grid(column=0, row=1, columnspan=4, padx=10, pady=10)

        # Defining number of columns
        self.atcivites_treeView["columns"] = ("1", "2", "3", "4", "5", "6")

        # Defining heading
        self.atcivites_treeView['show'] = 'headings'

        # Assigning the width and anchor to  the columns
        self.atcivites_treeView.column("1", width=50, anchor='c')
        self.atcivites_treeView.column("2", width=150, anchor='c')
        self.atcivites_treeView.column("3", width=150, anchor='c')
        self.atcivites_treeView.column("4", width=90, anchor='c')
        self.atcivites_treeView.column("5", width=90, anchor='c')
        self.atcivites_treeView.column("6", width=90, anchor='c')

        # Assigning the head names to the columns
        self.atcivites_treeView.heading("1", text="Event ID")
        self.atcivites_treeView.heading("2", text="Event Name")
        self.atcivites_treeView.heading("3", text="Lcation")
        self.atcivites_treeView.heading("4", text="Capacity")
        self.atcivites_treeView.heading("5", text="Date")
        self.atcivites_treeView.heading("6", text="Time")

        self.fillTreeviewActiveTic()
        self.book_button = ttk.Button(Book_Tickit_Tab, text='Create', command=self.saveBookingInf).grid(column=0, row=2,
                                                                                                        padx=10,
                                                                                                        pady=10,
                                                                                                        sticky=E,
                                                                                                        columnspan=2)
        self.logout_button2 = ttk.Button(Book_Tickit_Tab, text='Logout', command=self.logout).grid(column=2, row=2,
                                                                                                   sticky=W,
                                                                                                   columnspan=2)

        # second Tree view
        Label(My_tickits_Tab, text="My Tickits", font=('Helvetica 20 bold')).grid(column=0, row=0, columnspan=4,
                                                                                  padx=10, pady=10)

        self.myTickit_treeView = ttk.Treeview(My_tickits_Tab, selectmode='browse')
        self.myTickit_treeView.grid(column=0, row=1, columnspan=4, padx=10, pady=10)

        # Defining number of columns
        self.myTickit_treeView["columns"] = ("1", "2", "3", "4", "5", "6")

        # Defining heading
        self.myTickit_treeView['show'] = 'headings'

        # Assigning the width and anchor to  the columns
        self.myTickit_treeView.column("1", width=50, anchor='c')
        self.myTickit_treeView.column("2", width=150, anchor='c')
        self.myTickit_treeView.column("3", width=150, anchor='c')
        self.myTickit_treeView.column("4", width=90, anchor='c')
        self.myTickit_treeView.column("5", width=90, anchor='c')
        self.myTickit_treeView.column("6", width=90, anchor='c')

        # Assigning the head names to the columns
        self.myTickit_treeView.heading("1", text="Name")
        self.myTickit_treeView.heading("2", text="Tickit id")
        self.myTickit_treeView.heading("3", text="Event Name")
        self.myTickit_treeView.heading("4", text="Lcation")
        self.myTickit_treeView.heading("5", text="Date")
        self.myTickit_treeView.heading("6", text="Time")

        self.fillTreeviewActiveTic()
        self.submit_button = ttk.Button(My_tickits_Tab, text='Show', command=self.fillTreeviewMyTic).grid(column=0,
                                                                                                          row=2,
                                                                                                          padx=10,
                                                                                                          pady=10,
                                                                                                          sticky=E,
                                                                                                          columnspan=2)
        self.login_button = ttk.Button(My_tickits_Tab, text='Logout', command=self.logout).grid(column=2, row=2,
                                                                                                sticky=W, columnspan=2)

        tk.mainloop()

    def saveBookingInf(self):
        try:
            connection = sqlite3.connect('TSDatabase.db')
            c = connection.cursor()
            tickit_id = randint(10000, 99999)
            selectedActivity = self.atcivites_treeView.selection()[0]
            event_id = self.atcivites_treeView.item(selectedActivity)['values'][0]
            capacity = self.atcivites_treeView.item(selectedActivity)['values'][3]
            # check if this activity already bokked for the same user
            id = c.execute(f"select tickit_id from tickit where user_id= {self.generalvar} and event_id={event_id}")
            if len(id.fetchall()) == 0:
                if capacity == 0:
                    messagebox.showerror("Booking failuer", "sorry all seats Booked")
                else:
                    c.execute(f"insert into tickit values({tickit_id},{self.generalvar},{event_id}) ")
                    c.execute(f"update eventsinf set capacity = capacity-1 where  event_id={event_id}")
                    connection.commit()
                    self.fillTreeviewActiveTic()
                    messagebox.showinfo("Booking Done", "Your tickit issued with Tickit No(" + str(tickit_id) + ")")

            else:
                messagebox.showinfo("Booking failuer", "sorry You have booking for this event")
            connection.close()

        except sqlite3.Error:
            messagebox.showinfo("connect fail", "can't execute the command")

        except:
            messagebox.showinfo("Error", "error")

            return

    def fillTreeviewActiveTic(self):
        connection = sqlite3.connect('TSDatabase.db')
        cursor = connection.execute(
            f"SELECT event_id,event_Name,event_location,capacity,event_date,event_time from eventsinf where event_date > {date.today()}")
        count = 0
        for i in self.atcivites_treeView.get_children():
            self.atcivites_treeView.delete(i)
        for row in cursor:
            b = datetime.strptime(row[4], '%d/%m/%Y')
            if b >= datetime.now():
                self.atcivites_treeView.insert(parent='', index=count, text='',
                                               values=(row[0], row[1], row[2], row[3], row[4], row[5]))
                count += 1
            else:
                count += 1
        return

    def fillTreeviewMyTic(self):
        connection = sqlite3.connect('TSDatabase.db')
        cursor = connection.execute(
            f"select  first_Name,tickit.tickit_id,event_Name ,event_location,event_date,event_time  from userinf,eventsinf,tickit where userinf.user_id=tickit.user_id and eventsinf.event_id=tickit.event_id and tickit.user_id= {self.generalvar}")
        count = 0
        for i in self.myTickit_treeView.get_children():
            self.myTickit_treeView.delete(i)
        for row in cursor:
            self.myTickit_treeView.insert(parent='', index=count, text='',
                                          values=(row[0], row[1], row[2], row[3], row[4], row[5]))
            count += 1
        connection.close()
        return


myGUI = Forms()
