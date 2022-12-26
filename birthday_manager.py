import sys
import csv
import smtplib
import re
from datetime import datetime
from getpass import getpass
from email.message import EmailMessage


try:
    cmd = sys.argv[1]
except:
    print("to show all enteries: show_all\nto add entry:add\nto update a record: update\nto delete entry: delete\nto send an invitation mail: invite_mail\nto send a birthday wish mail: wish_mail")
    sys.exit()


if cmd == "show_all":
    f = open("friends.csv", "r")
    csv_reader = csv.reader(f)
    for row in csv_reader:
        print(row)
    sys.exit()


if cmd == "add":
    while True:
        l = []
        pattern_name = "^[a-zA-Z]"
        name = input("Enter name: ")
        if re.search(pattern_name, name):
            l.append(name)
        else:
            print("invalid input")
            break
        pattern_email = "^[a-zA-Z][a-zA-Z0-9(._)]+@[a-zA-Z]+\."
        email = input("Enter email: ")
        if re.search(pattern_email, email):
            l.append(email)
        else:
            print("invalid input")
            break
        invitation_flag = input("Do you want to invite this recipient[y/n]?")
        pattern_flag = "^[yn]{1}$"
        if re.search(pattern_flag, invitation_flag):
            l.append(invitation_flag)
        else:
            print("invalid input")
            break
        birthdate = input("Enter birthdate in DD-MM-YYYY format: ")
        pattern_birthdate = "^[0-9]{2}(-)[0-9]{2}(-)[0-9]{4}"
        if re.search(pattern_birthdate, birthdate):
            l.append(birthdate)
        else:
            print("invalid input")
            break
        f = open("friends.csv", "a", newline="")
        csv_writer = csv.writer(f)
        csv_writer.writerow(l)
        a = input("do u want to enter more records?[y/n]")
        if a == "n":
            print("records updated")
            break
        f.close()
    sys.exit()


if cmd == "delete":
    n = input("enter name to delete the record: ")
    l = []
    f = open("friends.csv", "r", newline="")
    csv_reader = csv.reader(f)
    found = False
    for row in csv_reader:
        if row[0] == n:
            found = True
            pass
        else:
            l.append(row)
    f.close()
    if found == False:
        print("record not found")
    else:
        f = open("friends.csv", "w", newline="")
        csv_writer = csv.writer(f)
        csv_writer.writerows(l)
        f.close()
        print("records updated")
    sys.exit()


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

    f = open("friends.csv", "r", newline="")
    csv_reader = csv.reader(f)
    next(csv_reader)
    for line in csv_reader:
        if line[2] == "y":
            msg = EmailMessage()
            msg.set_content(
                f"Dear {line[0]},\n\n{message}\n\nEvent Date: {func_date}\nEvent Time: {func_time}\nEvent Venue: {func_venue}\n\n\nRegards,\n{sender}")

            msg['Subject'] = sub
            msg['From'] = username
            msg['To'] = line[1]

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

    f = open("friends.csv", "r", newline="")
    csv_reader = csv.reader(f)
    next(csv_reader)
    c = 0
    l = []
    for row in csv_reader:
        birth_date = row[3]
        if int(birth_date[0:2]) == day:
            if int(birth_date[3:5]) == month:
                print("Your friends having birthday today: ")
                l.append(row[0])
                print(row[0])
                c = 1
    f.close()
    if c == 0:
        print("No one")
        sys.exit()
    mail = input(
        "Do you want to send all of them the birthday wish mail[y/n]? ")
    if mail == "n":
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

    f = open("friends.csv", "r", newline="")
    csv_reader = csv.reader(f)
    next(csv_reader)
    for row in csv_reader:
        if row[0] in l:
            msg = EmailMessage()
            msg.set_content(
                f"Dear {row[0]},\n\n{message}\n\n\nRegards,\n{sender}")

            msg['Subject'] = sub
            msg['From'] = username
            msg['To'] = row[1]; print(row[1])
			
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(username, password)
            server.send_message(msg)
            server.quit()

    print("Mails sent successfully!")
    sys.exit()


if cmd == "update":
    def update():
        update_record_name = input("Enter name of the person to update his/her records: ")

        f=open("friends.csv","r",newline="")
        csv_reader=csv.reader(f)
        unchanged_record=[]
        for row in csv_reader:
            if row[0]==update_record_name:
                c=1
                record_data=row
                pass
            else:
                unchanged_record.append(row)
        if c==0:
            print("Record not found!")
            sys.exit()

        field_to_be_updated=input("Enter name of the field to update its value[email/invitation_flag/birthdate]: ")
        updated_value=input("Enter updated value: ")
        
        pattern_email = "^[a-zA-Z][a-zA-Z0-9(._)]+@[a-zA-Z]+\."
        pattern_invitation_flag = "^[yn]{1}$"
        pattern_birthdate="[0-9]{2}(-)[0-9]{2}(-)[0-9]{2}"

        if field_to_be_updated=="email":
            if re.search(pattern_email,updated_value):
                record_data[1]=updated_value
            else:
                print("invalid input")
                sys.exit()
        
        if field_to_be_updated=="invitation_flag":
            if re.search(pattern_invitation_flag,updated_value):
                record_data[2]=updated_value
            else:
                print("invalid input")
                sys.exit()
        
        if field_to_be_updated=="birthdate":
            if re.search(pattern_birthdate,updated_value):
                record_data[3]=updated_value
            else:
                print("invalid input")
                sys.exit()

        f=open("friends.csv","w",newline="")
        csv_writer=csv.writer(f)

        for i in range(len(unchanged_record)):
            csv_writer.writerow(unchanged_record[i])

        csv_writer.writerow(record_data)

        print("records updated")

        update_more = input("Do you want to update more records [y/n]? ")
        if update_more == "y":
            update()
        else:
            sys.exit()
    update()
