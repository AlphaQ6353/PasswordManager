from tkinter import *
from tkinter import messagebox
import threading
from queue import Queue
from random import *
from characters_file import *
import pyperclip
import socket

# Windows ipconfig 'wireless LAN Wi-Fi for SERVER
SERVER_IP = '192.168.250.141'  # Server IP address
SERVER_PORT = 12345  # Server port number
BUFFER_SIZE = 1024

# Create a socket object
ADDRESS = (SERVER_IP, SERVER_PORT)
FORMAT = "utf-8"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message_queue = Queue()

# Create a threading event for message received
message_received_event = threading.Event()


# Sending and Receiving messages from Server
def receive_messages():
    while True:
        try:
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            temp = data.decode()

            # Put the received message into the queue
            message_queue.put(temp)

            # Set the event to signal that the message is received
            message_received_event.set()
        except socket.timeout:
            pass
        except ConnectionResetError:
            pass


def send_messages(message):
    try:
        client_socket.sendto(message.encode(), ADDRESS)
    except BrokenPipeError:
        print("Here")

message_temp = ''
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages, args=(message_temp,)).start()
message_lock = threading.Lock()


class Login:
    def __init__(self):
        self.login_window = Tk()
        self.login_window.title("PassManager")
        self.login_window.geometry('925x500+300+200')
        self.login_window.configure(bg='#fff')
        self.login_window.resizable(False, False)

        self.bg_img = PhotoImage(file='Images/frontImg.png')
        Label(self.login_window, image=self.bg_img, bg='white').place(x=50, y=50)

        self.frame = Frame(self.login_window, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)

        self.heading = Label(self.frame, text='Log In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 33,
                                                                                        'bold'))
        self.heading.place(x=100, y=5)
        self.user = Entry(self.frame, width=25, fg='black', border=0, bg='white', highlightthickness=0,
                          font=('Microsoft YaHei UI Light', 13))
        self.user.place(x=30, y=80)
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', self.on_enter)
        self.user.bind('<FocusOut>', self.on_leave)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.code = Entry(self.frame, width=25, fg='black', border=0, bg='white', highlightthickness=0,
                          font=('Microsoft YaHei UI Light', 13))
        self.code.place(x=30, y=150)
        self.code.insert(0, 'Password')
        self.code.bind('<FocusIn>', self.on_enter_1)
        self.code.bind('<FocusOut>', self.on_leave_1)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=177)

        self.Log = Button(self.frame, width=30, pady=7, text='Log In', bg='#57a1f8', fg='black', border=0,
                          command=self.log_in)
        self.Log.place(x=30, y=204)
        self.label = Label(self.frame, text="Don't have an account?", fg='black', bg='white',
                           font=('Microsoft YaHei UI Light', 13))
        self.label.place(x=75, y=270)

        self.sign_up = Button(self.frame, width=8, text='Sign Up', border=0, bg='white',
                              cursor='hand2', fg='#57a1f8',
                              highlightthickness=0, highlightbackground='white', command=self.sign)
        self.sign_up.place(x=224, y=270)

        self.login_window.mainloop()

    def on_enter(self, e):
        self.user.delete(0, 'end')

    def on_leave(self, e):
        name = self.user.get()
        if name == '':
            self.user.insert(0, 'Username')

    def on_enter_1(self, e):
        self.code.delete(0, 'end')

    def on_leave_1(self, e):
        name = self.code.get()
        if name == '':
            self.code.insert(0, 'Password')

    def log_in(self):
        name = self.user.get()
        password = self.code.get()
        msg = f"{name},{password},check"
        send_messages(msg)

        client_socket.settimeout(15)

        try:
            message_received_event.wait()

            received_message = message_queue.get()

            if received_message.lower() == 'true':
                self.login_window.destroy()
                PassManager()
            else:
                messagebox.showinfo(title="Not Found",
                                    message=f"The Username and/or Password you specified are not correct...")
        except socket.timeout:
            messagebox.showinfo(title="Not Found",
                                message=f"The Username and/or Password you specified are not correct...")

    def sign(self):
        self.login_window.destroy()
        SignUp()


class SignUp:
    def __init__(self):
        self.sign_up = Tk()
        self.sign_up.title("SignUp")
        self.sign_up.geometry('925x500+300+200')
        self.sign_up.configure(bg='#fff')
        self.sign_up.resizable(False, False)

        self.img = PhotoImage(file='Images/sign_frontImg.png')
        Label(self.sign_up, image=self.img, border=0, bg='white').place(x=50, y=90)

        self.frame = Frame(self.sign_up, width=350, height=390, bg='#fff')
        self.frame.place(x=480, y=50)

        self.heading = Label(self.frame, text='Sign Up', fg='#57a1f8', bg='white',
                             font=('Microsoft YaHei UI Light', 33, 'bold'))
        self.heading.place(x=100, y=5)

        self.user = Entry(self.frame, width=25, fg='black', border=0, bg='white',
                          highlightthickness=0, font=('Microsoft YaHei UI Light', 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, 'Username')

        self.user.bind("<FocusIn>", self.on_enter)
        self.user.bind("<FocusOut>", self.on_leave)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.code = Entry(self.frame, width=25, fg='black', border=0, bg='white',
                          highlightthickness=0, font=('Microsoft YaHei UI Light', 11))
        self.code.place(x=30, y=150)
        self.code.insert(0, 'EmailId')

        self.code.bind("<FocusIn>", self.on_enter_1)
        self.code.bind("<FocusOut>", self.on_leave_1)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=177)

        self.passw = Entry(self.frame, width=25, fg='black', border=0, bg='white',
                          highlightthickness=0, font=('Microsoft YaHei UI Light', 11))
        self.passw.place(x=30, y=220)
        self.passw.insert(0, 'Password')

        self.passw.bind("<FocusIn>", self.on_enter_2)
        self.passw.bind("<FocusOut>", self.on_leave_2)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=247)

        self.button = Button(self.frame, width=30, pady=7, text='Sign Up', bg='#57a1f8',
                             fg='black', border=0, command=self.gomain)
        self.button.place(x=35, y=280)

        self.label = Label(self.frame, text='I have an account', fg='black', bg='white',
                           font=('Microsoft YaHei UI Light', 13))
        self.label.place(x=90, y=340)

        self.signin = Button(self.frame, width=6, text='Login', border=0, bg='black', cursor='hand2', fg='#57a1f8',
                             highlightthickness=0, highlightbackground='white', command=self.login)
        self.signin.place(x=200, y=340)

        self.sign_up.mainloop()

    def on_enter(self, e):
        self.user.delete(0, 'end')

    def on_leave(self, e):
        name = self.user.get()
        if name == '':
            self.user.insert(0, 'Username')

    def on_enter_1(self, e):
        self.code.delete(0, 'end')

    def on_leave_1(self, e):
        name = self.code.get()
        if name == '':
            self.code.insert(0, 'EmailId')

    def on_enter_2(self, e):
        self.passw.delete(0, 'end')

    def on_leave_2(self, e):
        name = self.passw.get()
        if name == '':
            self.passw.insert(0, 'Password')

    def gomain(self):
        name = self.user.get()
        email = self.code.get()
        password = self.passw.get()
        msg = f"{name},{email},{password},add_user"
        send_messages(msg)

        try:
            message_received_event.wait()

            received_message = message_queue.get()

            if received_message.lower() == "user already exists":
                messagebox.showinfo(title="Already Taken",
                                    message=f"The Username you are asking for is already taken by others...")
            else:
                self.sign_up.destroy()
                PassManager()
        except socket.timeout:
            messagebox.showinfo(title="Time Out",
                                message=f"Server unexpectedly shutdown...")

    def login(self):
        self.sign_up.destroy()
        Login()


class PassManager:
    def __init__(self):
        self.window = Tk()
        self.window.title("Password_Gen")
        self.window.geometry('670x450')
        self.window.resizable(False, False)
        self.window.config(padx=50, pady=50)

        self.canvas = Canvas(self.window, width=200, height=200)
        self.bg_img = PhotoImage(file='Images/logo.png')
        self.canvas.create_image(100, 100, image=self.bg_img)
        self.canvas.grid(row=0, column=1)

        self.web_label = Label(self.window, text='Website:')
        self.web_label.grid(row=1, column=0)

        self.web_ans = Entry(self.window, width=21)
        self.web_ans.grid(row=1, column=1)
        self.web_ans.focus()

        self.search_button = Button(self.window, text='Search', width=13, highlightthickness=0, command=self.search)
        self.search_button.grid(row=1, column=2)

        self.mail_label = Label(self.window, text='Email/Username:')
        self.mail_label.grid(row=2, column=0)

        self.mail_ans = Entry(self.window, width=30)
        self.mail_ans.grid(row=2, column=1)

        self.password_label = Label(self.window, text='Password:')
        self.password_label.grid(row=3, column=0)

        self.password_ans = Entry(self.window, width=21)
        self.password_ans.grid(row=3, column=1)

        self.generate_button = Button(self.window, text='Generate Password', highlightthickness=0,
                                      command=self.password_gen)
        self.generate_button.grid(row=3, column=2)

        self.add_button = Button(self.window, text='Add', width=20, highlightthickness=0, command=self.add_to_db)
        self.add_button.grid(row=4, column=1)

        self.update_button = Button(self.window, text='Update', width=20, highlightthickness=0, command=self.update_db)
        self.update_button.grid(row=4, column=2)

        self.window.mainloop()

    def search(self):
        web_data = self.web_ans.get()
        mail_id = self.mail_ans.get()
        message = f"{web_data},{mail_id},search"
        send_messages(message)

        client_socket.settimeout(15)

        try:
            message_received_event.wait()

            received_message = message_queue.get()

            if received_message == "Record not found":
                messagebox.showinfo(title="Not Found",
                                    message=f"The password for the website:{web_data} doesn't exist in Database...")
            else:
                l1 = received_message.split(',')
                messagebox.showinfo(title=f"{l1[0]}", message=f"Email: {l1[1]}\nPassword: {l1[2]}")
        except socket.timeout:
            messagebox.showinfo(title="Not Found",
                                message=f"The password for the website:{web_data} doesn't exist in Database...")

    def password_gen(self):
        pass_chr = [choice(list_char) for _ in range(randint(8, 10))]
        pass_num = [choice(list_num) for _ in range(randint(2, 4))]
        pass_sym = [choice(list_spl) for _ in range(randint(2, 4))]
        password_list = pass_sym + pass_chr + pass_num
        shuffle(password_list)
        password_str = "".join(password_list)
        self.password_ans.insert(0, password_str)
        pyperclip.copy(password_str)

    def add_to_db(self):
        web_data = self.web_ans.get()
        mail_data = self.mail_ans.get()
        password_data = self.password_ans.get()
        message = f"{web_data},{mail_data},{password_data},add"
        send_messages(message)

    def update_db(self):
        password_res = self.password_ans.get()
        website = self.web_ans.get()
        email = self.mail_ans.get()
        message = f"{website},{email},{password_res},update"
        send_messages(message)
