import socket
import smtplib
import mysql.connector

# ---------------------------- MYSQL CONNECTOR ------------------------------- #

mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               password='Rajeev@123',
                               database='dbms_project'
                               )
cursor = mydb.cursor()

website_count = {}
user = {}


# ---------------------------- MAIL CONNECTION ------------------------------- #

my_email = "passmanager365@gmail.com"
password_mail = "bflpdwygxcpuuxwf"

connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=my_email, password=password_mail)

# ---------------------------- FUNCTIONS ------------------------------- #


# Sign Up
def add_user(name, email, password, address):
    if name in user:
        msg = 'User Already Exists'
    else:
        msg = 'Done'
        user[name] = address
        code = "INSERT INTO user(username, emailId, password) VALUES(%s, %s, %s)"
        val = (name, email, password)
        cursor.execute(code, val)
        mydb.commit()

        code_temp = "SELECT user_id from user where username=(%s) and emailId=(%s)"
        val_temp = (name, email)
        cursor.execute(code_temp, val_temp)
        res = cursor.fetchall()
        userid = res[0][0]

        code_add = "INSERT INTO ip_address(user_id,Ip_Address) VALUES(%s, %s)"
        val_add = (userid, address[0])
        cursor.execute(code_add, val_add)
        mydb.commit()
    server_socket.sendto(msg.encode(FORMAT), address)


# Login
def check_user(name, password, address):
    code = "SELECT password FROM user WHERE username=(%s)"
    val = (name,)
    cursor.execute(code, val)
    res = cursor.fetchall()

    if res:
        # User found, check password
        if res[0][0] == password:
            message = "True"  # Correct password
        else:
            message = "Incorrect password"
    else:
        # User not found
        message = "User not found"

    # Get user ID
    code_temp = "SELECT user_id FROM user WHERE username=(%s)"
    cursor.execute(code_temp, val)
    res_1 = cursor.fetchall()
    if res_1:
        userid = res_1[0][0]
    else:
        # User not found
        server_socket.sendto(message.encode(FORMAT), address)
        return

    # Check IP address
    code_temp_1 = "SELECT Ip_Address FROM ip_address WHERE user_id=(%s)"
    val_temp_1 = (userid,)
    cursor.execute(code_temp_1, val_temp_1)
    res_2 = cursor.fetchall()
    config = res_2[0][0] if res_2 else None

    if config == address[0]:
        pass  # IP address matches, do nothing
    else:
        # IP address doesn't match, send email
        code_temp_2 = "SELECT emailId FROM user WHERE user_id=(%s) AND username=(%s)"
        val_temp_2 = (userid, name)
        cursor.execute(code_temp_2, val_temp_2)
        res_3 = cursor.fetchall()
        mail = res_3[0][0] if res_3 else None

        if mail:
            connection.sendmail(from_addr=my_email, to_addrs=mail,
                                msg="Subject:Logged In PassManager\n\nYou have logged in PassManager through an unknown device. If it's not you, then please change your password")

    server_socket.sendto(message.encode(FORMAT), address)
    return userid


# Main functions
def add(web, mail, password, uid):
    query = "SELECT website from website where website=(%s)"
    query_val = (web,)
    cursor.execute(query, query_val)
    result = cursor.fetchone()

    if result:
        code_temp = "UPDATE website set No_of_Pass=No_of_Pass+1 where website=(%s)"
        val = (web,)
        cursor.execute(code_temp, val)
        mydb.commit()

    else:
        x = 1
        code_temp = "INSERT INTO website(website, No_of_Pass) VALUES(%s, %s)"
        val = (web, x)
        cursor.execute(code_temp, val)
        mydb.commit()

    code = "INSERT INTO password(website, email, password, user_id) VALUES(%s, %s, %s, %s)"
    val = (web, mail, password, uid)
    cursor.execute(code, val)
    mydb.commit()


def update(website, email, password):
    code = "UPDATE password set password=(%s) where website=(%s) and email=(%s)"
    val = (password, website, email)
    cursor.execute(code, val)
    mydb.commit()


def search(website, mail, address):
    code = "SELECT password from password where website=(%s) and email=(%s)"
    val = (website.lower(), mail.lower())
    cursor.execute(code, val)
    res = cursor.fetchall()
    if res:
        res = res[0][0]
        message = f"{website},{mail},{res}"
    else:
        message = "Record not found"
    server_socket.sendto(message.encode(FORMAT), address)


# ---------------------------- SOCKET CONNECTION ------------------------------- #

SERVER = '192.168.250.141'
PORT = 12345
BUFFER_SIZE = 1024
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(ADDRESS)

print("Server is listening...")

while True:
    global userId
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    l1 = data.decode().split(',')
    print(client_address[0])

    if l1[-1].lower() == 'search':
        search(l1[0], l1[1], client_address)
    elif l1[-1].lower() == 'add_user':
        add_user(l1[0], l1[1], l1[2], client_address)
    elif l1[-1].lower() == 'check':
        global userId
        userId = check_user(l1[0], l1[1], client_address)
    elif l1[-1].lower() == 'add':
        add(l1[0], l1[1], l1[2], userId)
    elif l1[-1].lower() == 'update':
        update(l1[0], l1[1], l1[2])
