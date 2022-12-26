import sys
import smtplib
import re
import psycopg2
import base64
from getpass import getpass
from email.message import EmailMessage
from datetime import datetime

db_name = "birthday_manager"
db_user = "postgres"
password = base64.b64decode('c2hyZXlhMTIz')
db_pass = ""
for i in range(9):
    pass1 = chr(password[i])
    db_pass = db_pass+pass1
db_host = "localhost"

db = psycopg2.connect(dbname=db_name, user=db_user,
                      password=db_pass, host=db_host)
cur = db.cursor()


try:
    cmd = sys.argv[1]
except:
    print("to show all enteries: show_all\nto add entry:add\nto update record: update\nto delete entry: delete\nto send an invitation mail: invite_mail\nto send a birthday wish mail: wish_mail")
    sys.exit()


if cmd == "show_all":
    cur.execute('''SELECT * FROM friends''')
    all = cur.fetchall()
    print("['name','email','invitation_flag']")
    for i in range(len(all)):
        print(list(all[i]))
    sys.exit()


if cmd == "delete":
    def delete():
        del_name = input("Enter name: ")
        cur.execute('''SELECT * from friends''')
        all = cur.fetchall()
        c = 0
        for i in range(len(all)):
            if all[i][0] == del_name:
                del_data = f"DELETE FROM friends WHERE name='{del_name}'"
                cur.execute(del_data)
                db.commit()
                c = 1
        if c == 0:
            print("record not found")
        else:
            print("records updated")
        del_more = input("Do you want to delete more records [y/n]? ")
        if del_more == "y":
            delete()
        else:
            sys.exit()
    delete()


if cmd == "add":
    def add():
        pattern_name = "^[a-zA-Z]*$"
        pattern_email = "^[a-zA-Z][a-zA-Z0-9(._)]+@[a-zA-Z]+\."
        pattern_invitation_flag = "^[yn]$"
        pattern_birthdate="[0-9]{2}(-)[0-9]{2}(-)[0-9]{2}"

        try:
            name = input("Enter name: ")
            if re.search(pattern_name, name):
                add_name = name
            else:
                print("invalid input")
                sys.exit()

            email = input("Enter email: ")
            if re.search(pattern_email, email):
                add_email = email
            else:
                print("invalid input")
                sys.exit()

            flag = input("Enter invitation flag: ")
            if re.search(pattern_invitation_flag, flag):
                add_flag = flag
            else:
                print("invalid input")
                sys.exit()
            
            birthdate=input("Enter birthday date in DD-MM-YYYY format: ")
            if re.search(pattern_birthdate, birthdate):
                add_birthdate=birthdate
            else:
                print("invalid input")
                sys.exit()

            add_data = f"INSERT INTO friends(name,email,invitation_flag,birthdate) VALUES('{add_name}','{add_email}','{add_flag}','{add_birthdate}')"
            cur.execute(add_data)
            db.commit()
        except:
            print("Enter a unique name!")
            
        add_more = input("Do you want to add more record [y/n]? ")
        if add_more == "y":
            add()
        print("records updated")
        sys.exit()
    add()


if cmd == "invite_mail":
    sender = input("Enter Sender's name: ")
    username = input("Enter Sender's Email Address: ")
    password = getpass("Enter Password: ")
    sub = input("Enter Subject: ")
    message = input("Enter Message: ")
    func_date = input("Enter Event date: ")
    func_time = input("Enter Event time: ")
    func_venue = input("Enter Event venue: ")

    print("This is the sample message:\n ")
    print(f"Subject: {sub}\n\nDear invitee,\n\n{message}\n\nEvent Date: {func_date}\nEvent Time: {func_time}\nEvent Venue: {func_venue}\n\n\nRegards,\n{sender}")

    print("Please change your email settings to allow access by less safer apps to proceed successfully!")
    mail = input("Do you want to send this mail [y/n]? ")
    if mail == "n":
        print("mail not sent!")
        sys.exit()

    cur.execute('''SELECT * FROM friends''')
    all = cur.fetchall()
    for i in range(len(all)):
        if all[i][2] == "y":
            msg = EmailMessage()
            msg.set_content(
                f"Dear {all[i][0]},\n\n{message}\n\nEvent Date: {func_date}\nEvent Time: {func_time}\nEvent Venue: {func_venue}\n\n\nRegards,\n{sender}")
            msg['Subject'] = sub
            msg['From'] = username
            msg['To'] = all[i][1]
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(username, password)
            server.send_message(msg)
            server.quit()
    print("Mails sent successfully!")
    sys.exit()


if cmd == "wish_mail":
    today = datetime.today()
    day = today.day
    month = today.month

    cur.execute('''SELECT * from friends''')
    all=cur.fetchall()
    l=[]
    c=0
    for i in range(len(all)):
        row=list(all[i])
        if row[3].day==day:
            if row[3].month==month:
                l.append(row[0])
                c=1
    if c==0:
        print("No one")
        sys.exit()
    else:
        print("Your friends having birthday today: ")
        for i in range(len(l)):
            print(l[i])
    mail=input("Do you want to send all of them birthday wish mail[y/n]? ")
    if mail=="n":
        print("Mail not sent!")
        sys.exit()
    
    sender = input("Enter Sender's name: ")
    username = input("Enter Sender's Email Address: ")
    password = getpass("Enter Password: ")
    sub = input("Enter Subject: ")
    message = input("Enter Message: ")

    print("This is the sample message:\n ")
    print(
        f"Subject: {sub}\n\nDear friend,\n\n{message}\n\n\nRegards,\n{sender}")

    print("Please change your email settings to allow access by less safer apps to proceed successfully!")
    mail = input("Do you want to send this mail [y/n]? ")
    if mail == "n":
        print("mail not sent!")
        sys.exit()

    for i in range(len(all)):
        row=list(all[i])
        if row[0] in l:
            msg = EmailMessage()
            msg.set_content(
                f"Dear {row[0]},\n\n{message}\n\n\nRegards,\n{sender}")

            msg['Subject'] = sub
            msg['From'] = username
            msg['To'] = row[1]
			
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(username, password)
            server.send_message(msg)
            server.quit()

    print("Mails sent successfully!")
    sys.exit()


if cmd == "update":
    def update():
        update_record_name = input("Enter name of the person to update his/her records: ")
        field_to_be_updated=input("Enter name of the field to update its value[email/invitation_flag/birthdate]: ")
        new_value=input("Enter updated value: ")
        
        pattern_email = "^[a-zA-Z][a-zA-Z0-9(._)]+@[a-zA-Z]+\."
        pattern_invitation_flag = "^[yn]"
        pattern_birthdate="[0-9]{2}(-)[0-9]{2}(-)[0-9]{2}"

        if field_to_be_updated=="email":
            if re.search(pattern_email,new_value):
                updated_value=new_value
            else:
                print("invalid input")
                sys.exit()
        
        if field_to_be_updated=="invitation_flag":
            if re.search(pattern_invitation_flag,new_value):
                updated_value=new_value
            else:
                print("invalid input")
                sys.exit()
        
        if field_to_be_updated=="birthdate":
            if re.search(pattern_birthdate,new_value):
                updated_value=new_value
            else:
                print("invalid input")
                sys.exit()

        cur.execute('''SELECT * from friends''')
        all = cur.fetchall()
        c = 0
        for i in range(len(all)):
            if all[i][0] == update_record_name:
                update_data = f"UPDATE friends SET {field_to_be_updated}='{updated_value}' WHERE name='{update_record_name}'"
                cur.execute(update_data)
                db.commit()
                c = 1
        if c == 0:
            print("record not found")
        else:
            print("records updated")
        update_more = input("Do you want to update more records [y/n]? ")
        if update_more == "y":
            update()
        else:
            sys.exit()
    update()


