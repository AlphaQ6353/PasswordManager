from tkinter import *
from tkinter import messagebox
import mysql.connector
from characters_file import *
from random import *
import pyperclip

# ---------------------------- MYSQL CONNECTOR ------------------------------- #

mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               password='Rajeev@123',
                               database='mini_project'
                               )
cursor = mydb.cursor()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_gen():
    pass_chr = [choice(list_char) for _ in range(randint(8, 10))]
    pass_num = [choice(list_num) for _ in range(randint(2, 4))]
    pass_sym = [choice(list_spl) for _ in range(randint(2, 4))]
    password_list = pass_sym + pass_chr + pass_num
    shuffle(password_list)
    password_str = "".join(password_list)
    password_ans.insert(0, password_str)
    pyperclip.copy(password_str)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_to_db():
    code = "INSERT INTO password(website, email, password) VALUES(%s, %s, %s)"
    val = (web_ans.get(), mail_ans.get(), password_ans.get())
    cursor.execute(code, val)
    mydb.commit()


def search():
    code = "SELECT password from password where website=(%s) and email=(%s)"
    website = web_ans.get()
    mail_id = mail_ans.get()
    val = (website, mail_id)
    cursor.execute(code, val)
    res = cursor.fetchall()
    res = res[0][0]
    messagebox.showinfo(title=f"{website}", message=f"Email: {mail_id}\nPassword: {res}")


# ---------------------------- UPDATE PASSWORD ------------------------------- #


def update_db():
    code = "UPDATE password set password=(%s) where website=(%s) and email=(%s)"
    password_res = password_ans.get()
    website = web_ans.get()
    email = mail_ans.get()
    val = (password_res, website, email)
    cursor.execute(code, val)
    mydb.commit()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password_Gen")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
bg_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=bg_img)
canvas.grid(row=0, column=1)

web = Label(text='Website:')
web.grid(row=1, column=0)

web_ans = Entry(width=21)
web_ans.grid(row=1, column=1)
web_ans.focus()

search_button = Button(text='Search', width=13, highlightthickness=0, command=search)
search_button.grid(row=1, column=2)

mail = Label(text='Email/Username:')
mail.grid(row=2, column=0)

mail_ans = Entry(width=46)
mail_ans.grid(row=2, column=1, columnspan=2)

password = Label(text='Password:')
password.grid(row=3, column=0)

password_ans = Entry(width=21)
password_ans.grid(row=3, column=1)

generate_button = Button(text='Generate Password', highlightthickness=0, command=password_gen)
generate_button.grid(row=3, column=2)

add_button = Button(text='Add', width=20, highlightthickness=0, command=add_to_db)
add_button.grid(row=4, column=1)

update_button = Button(text='Update', width=20, highlightthickness=0, command=update_db)
update_button.grid(row=4, column=2)

window.mainloop()
