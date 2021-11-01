from lxml import html
import requests
import timeit
import time
import threading
import string
import random
import csv
import os
import os.path
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from random import randint
import names

# import country name and country code from PVA_country.txt


def read_countryname():
    path = "mailbot.conf"
    file = open(path, "r")
    fullname = file.read()
    list_countries = []
    PVA_code = str(fullname.split("\n")[0]).split(":")[1]
    for _ in range(len(fullname.split("\n"))):
        if _ == 0:
            continue
        list_countries.append(str(fullname.split("\n")[_]))
    
    return list_countries,PVA_code

# Export Created data to names.csv
def save_all_data(userid, firstname, lastname,  password, phone_number, birth_day, birth_year, birth_month,status):
    # is_first = False
    # if str(path.exists('names.csv')):
    #     is_first = True
    with open('names.csv', 'w', newline='') as csvfile:
        fieldnames = ['id','first_name', 'last_name','password','phone','day','month','year','result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # if is_first:
        writer.writeheader()
        writer.writerow({'id' : userid,'first_name': firstname, 'last_name':lastname,'password':password,'phone':phone_number,'day':birth_day,'year':birth_month,'month':birth_year,'result' : status})

# save log file
def export_logfile(data):
    with open("Log.txt","a") as f:
        f.write(" \n\n\n @@ : " + time.ctime())
        f.write("\n")
        f.write(data)
        f.write("\n")

# Create driver
def create_Driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=default')
    options.add_argument('--incognito')
    options.add_argument('--disable-plugin-discovery')
    options.add_argument('--start-maximized')
    # prefs = {
	# "profile.managed_default_content_settings.images":2,
	# "--disable-bundled-ppapi-flash":1
	# }
    # options = Options()
    # options.add_argument('--disable-logging')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_experimental_option("prefs", prefs)
    print("start_driver")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options = options)
    print("started driver")
    return driver


    # Page 1
def start_creating_page_1(driver,name):
    
    driver.get("https://accounts.google.com/signup")
    upgrade_status("Getting page finished.")
    upgrade_progress(5)
    time.sleep(2)

    input_FirstName = driver.find_element_by_xpath( '//input[@type="text" and @id="firstName"]' )
    input_LastName = driver.find_element_by_xpath( '//input[@type="text" and @id="lastName"]' )
    input_UserName = driver.find_element_by_xpath( '//input[@type="text" and @id="username"]' )
    input_Password = driver.find_element_by_xpath( '//input[@type="password" and @name="Passwd"]' )
    input_Confirm = driver.find_element_by_xpath( '//input[@type="password" and @name="ConfirmPasswd"]' )
    btn_next_1 = driver.find_element_by_xpath( '//div[@id="accountDetailsNext"]' )
    upgrade_status("Getting Elements finished.")
    upgrade_progress(10)
    global Username,F_name,L_name,Password
    Username = name
    F_name = names.get_first_name(gender='male')
    L_name = names.get_last_name()
    input_FirstName.send_keys(F_name)
    input_LastName.send_keys(L_name)
    input_UserName.send_keys(name)
    Password = randomString(10)
    upgrade_status("First Name :%s \nLast Name :%s \nPassword :%s" %(F_name, L_name,Password))
    print(Password)
    input_Password.send_keys(Password)
    input_Confirm.send_keys(Password)
    
    btn_next_1.click()
    time.sleep(3)
    try:
        btn_next_1 = driver.find_element_by_xpath( '//div[@id="accountDetailsNext"]' )
        upgrade_status("The id is already taken, Try another.")
        save_all_data(name,"","","","","","","","The id is already taken, Try another.")
        return
    except:
        upgrade_status("Page 1 Completed!")
        upgrade_progress(20)
        print("input user info-1 finished")
        start_creating_page_2(driver)
        
    # Page 2 Input Phone Number
def start_creating_page_2(driver):
    time.sleep(3)
    try:
        input_phone = driver.find_element_by_xpath( '//input[@type="tel" and @id="phoneNumberId"]' )
    except:
        upgrade_status("You can't create Gmail now, please try again later")
        save_all_data(Username,"","","","","","","","You can't create Gmail now, please try again later")
        return
    global Phonenumber
    Phonenumber = get_phone_number(Entry_PVA.get())
    try:
        if(int(Phonenumber) > 0):
            print(Phonenumber)
    except:
        upgrade_status("Generate phone number failed")
        save_all_data(Username,"","","","","","","","Generate phone number failed")
        return
    
    prefix = get_country_code()
    print(prefix)
    upgrade_status("Phone number %s%s generated" %(prefix,Phonenumber))
    input_phone.send_keys(prefix + Phonenumber)
    return
    btn_next_2 = driver.find_element_by_xpath( '//div[@id="gradsIdvPhoneNext"]')
    btn_next_2.click()
    time.sleep(4)
    
    try:
        btn_next_2 = driver.find_element_by_xpath( '//div[@id="gradsIdvPhoneNext"]')
        upgrade_status("This number cannot be used to verify ID.")
        save_all_data(Username,"","","","","","","","This number cannot be used to verify ID.")
        return
    except:
        upgrade_status("Sending verify code! \n Page 2 Completed!")
        upgrade_progress(40)
    time.sleep(3)

    start_creating_page_3(driver)

    # Page 3 Verify code
def start_creating_page_3(driver):
    input_verif_code = driver.find_element_by_xpath('//input[@type="tel" and @id="code"]')
    verification_key = get_verification_code(Phonenumber)
    print(verification_key)
    if verification_key == "Failed":
        upgrade_status("getting verification code failed")
        save_all_data(Username,"","","","","","","","getting verification code failed.")
        return
    input_verif_code.send_keys(verification_key)
    btn_verify = driver.find_element_by_xpath('//div[@id ="gradsIdvVerifyNext"]')
    btn_verify.click()
    time.sleep(2)
    
    try:
        btn_verify = driver.find_element_by_xpath('//div[@id ="gradsIdvVerifyNext"]')
        upgrade_status("Verify Failed. Wrong Verification code.")
        save_all_data(Username,"","","","","","","","Verify Failed. Wrong Verification code.")
        return
    except:
        upgrade_status("Verify completed!")
        upgrade_progress(60)
    time.sleep(3)
    start_creating_page_4(driver)


    # Page 4 Input User Info
def start_creating_page_4(driver):

    selector_month = Select(driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div[3]/div[1]/div/div/div[2]/select"))
    birth_month = randint(1,12)

    selector_month.select_by_value(str(birth_month))
    input_day = driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div[3]/div[2]/div/div/div[1]/div/div[1]/input")
    birth_day = randint(1,28)
    input_day.send_keys(str(birth_day))
    input_year = driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div[3]/div[3]/div/div/div[1]/div/div[1]/input")
    birth_year = randint(1980, 1997)
    input_year.send_keys(str(birth_year))
    global Birthday
    Birthday = birth_day + "/" + birth_month + "/" +birth_year
    selector_gender = Select(driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div[4]/div[1]/div/div[2]/select"))
    selector_gender.select_by_value('1')
    time.sleep(3)
    btn_next_3 = driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div[5]/div[1]/div")
    btn_next_3.click()
    upgrade_progress(80)
    time.sleep(3)
    btn_next_4 = driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div[2]/div[1]/div[1]")
    btn_next_4.click()
    time.sleep(3)
    btn_scroll = driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/div[1]/div/div")
    
    for _ in range(5):
        try:
            btn_scroll.click()
            time.sleep(1)
        except:
            print("end scroll")
            break
 
    time.sleep(2)
    # Agree term of policy
    btn_agree = driver.find_element_by_xpath(".//html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/div[2]/div/div[1]/div")
    btn_agree.click()
    upgrade_progress(100)
    birth_day = Birthday.split("/")[0]
    birth_month = Birthday.split("/")[1]
    birth_year = Birthday.split("/")[2]
    # Save all data to CSV file
    save_all_data(Username,F_name, L_name, Password, Phonenumber, birth_day, birth_year, birth_month, "success!" )

def get_country_code():
    country_code = "+"
    if country.get().split("+")[0][:-1] == "USA" or country.get().split("+")[0][:-1] == "USA 1":
        country_code += country.get().split("+")[1]
    return country_code

def get_verification_code(number):
    for _ in range(5):
        url_country = str(country.get()).split("+")[0][:-1].upper()
        url_app = "GMAIL"
        if url_country == "USA":
            url_app = "GMAIL USA"
        url = "http://pvacodes.com/user/api/get_sms.php?customer=%s&number=%s&country=%s&app=%s"%(Entry_PVA.get(),number,url_country,url_app)
        page = requests.get(url)
        page_byte = page.content.decode("utf-8","ignore")
        try:
            if int(page_byte[2:]) > 0:
                upgrade_status(page_byte)
                return(page_byte[2:])
        except:
            upgrade_status("invalid Verification Code")
        time.sleep(3)
    return "Failed"

    # Generate Password
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
    

def get_phone_number(pva_code):
    upgrade_status("Getting Phone number")

    # return "9123961570"
    url_country = country.get().split(" +")[0].upper()
    url_app = "GMAIL"
    if url_country == "USA":
        url_app = "GMAIL USA"
    url = "http://pvacodes.com/user/api/get_number.php?customer=%s&app=%s&country=%s"%(pva_code,url_app,url_country)
    print(url)
    page = requests.get(url)
    number = page.content.decode("utf-8","ignore")
    upgrade_status("Http response: "+number)
    return number

def refresh():
        root.update()
        root.after(1000,refresh)

def start():
    threading.Thread(target=main_loop).start()

def main_loop():
    refresh()
    API_key = Entry_PVA.get()
    print("+" + country.get().split("+")[1])
    print(API_key)
    progress = 0

    if API_key == "":
        print("Empty PVA")
        messagebox.showerror("Error", "PVA Customre ID is required!")
        upgrade_status("Error empty PVA id")
        return
    if Entry_username1.get() == "" and Entry_username2.get() == "" and Entry_username3.get() == "":
        messagebox.showerror("Error", "At least one username is required!")
        upgrade_status("Error empty username")
        return
    if(country.get().split("+")[0].upper() == "UK 2"):
        messagebox.showerror("Error", "You can't get Verification code with this country")
        upgrade_status("Error invalid Country")
    
    list_names = []
    list_names.append(Entry_username1.get())
    list_names.append(Entry_username2.get())
    list_names.append(Entry_username3.get())
    driver = create_Driver()
    for _ in range(len(list_names)):
        if(str(list_names[_]) != ""):
            upgrade_status("Start Creating! \n PVA id : %s \n Username is %s"%(API_key,list_names[_]) )
            progress +=1
            upgrade_progress(progress)
            global old_progress
            old_progress = 0
            start_creating_page_1(driver,list_names[_])
    file_directory = os.path.dirname(os.path.abspath(__file__))
    export_logfile(T.get('1.0', END))
    upgrade_status("********All task Finished******** \n result data saved in %s/names.csv"%file_directory)        

    
    # Update progress bar
def upgrade_progress(value):
    new_progress = value
    global old_progress
    current = old_progress
    for _ in range(new_progress - current):
        BarVolSyringe1["value"] = current + _
        root.update_idletasks()
        time.sleep(0.1)
    old_progress = new_progress

    # Update status
def upgrade_status(status):
    T.insert(END, status +  "\n")
    T.see("end")
    root.update_idletasks()

if __name__ == '__main__':
    root = Tk() 
    root.geometry("800x250")
    root.title("Gmail Creator")
    root.grid_columnconfigure(0, weight = 1)
    root.grid_columnconfigure(1, weight = 3)
    root.grid_columnconfigure(2, weight = 1)
    root.grid_columnconfigure(3, weight = 2)
    #PVA id
    Label_PVA =  Label(root, text="PVA Customer ID", width = 20)
    Label_PVA.grid(row = 1, column = 0 , sticky = E)
    Entry_PVA =  Entry(root, bd =5, width = 70)
    Entry_PVA.grid(row = 1, column = 1)
    space1 = Frame(root, width=10, height=2)
    space1.grid(row = 2,sticky = E)
    #Country
    Label_country =  Label(root, text="Select Country  ", width = 20)
    Label_country.grid(row = 3, column = 0 , sticky = E)
    variable = StringVar(root)
    variable.set("USA +1")
    country_list,default_pva = read_countryname()
    Entry_PVA.insert(0,default_pva)
    country = ttk.Combobox(root, state="readonly", textvariable=variable, values = country_list, width = 70)
    country.grid(row = 3, column = 1, sticky = E)
    space2 = Frame(root, width=10, height=10)
    space2.grid(row = 4,sticky = E)
    #username 1
    Label_username1 =  Label(root, text="Username 1 ", width = 20)
    Label_username1.grid(row = 5, column = 0 , sticky = E)
    Entry_username1 =  Entry(root, bd =5, width = 70)
    Entry_username1.grid(row = 5, column = 1)
    space1 = Frame(root, width=10, height=2)
    space1.grid(row = 6,sticky = E)
    #username 2
    Label_username2 =  Label(root, text="Username 2 ", width = 20)
    Label_username2.grid(row = 7, column = 0 , sticky = E)
    Entry_username2 =  Entry(root, bd =5, width = 70)
    Entry_username2.grid(row = 7, column = 1)
    space1 = Frame(root, width=10, height=2)
    space1.grid(row = 8,sticky = E)
    #username 3
    Label_username3 =  Label(root, text="Username 3 ", width = 20)
    Label_username3.grid(row = 9, column = 0 , sticky = E)
    Entry_username3 =  Entry(root, bd =5, width = 70)
    Entry_username3.grid(row = 9, column = 1)
    space1 = Frame(root, width=10, height=2)
    space1.grid(row = 10,sticky = E)
    #margin
    margin = Frame(root,width = 50,height = 250)
    margin.grid(column = 2, row = 0,rowspan = 13, sticky = W+E)
    #result area
    output_status = Frame(root,width = 400,height = 10, background = "pink")
    output_status.grid(column = 3, row = 0,rowspan = 8, sticky = W)
    S = Scrollbar(output_status)
    T = Text(output_status, height=10, width=50)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=TOP, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    #Start Button
    buttonstart = Button(root, width = 20, text = "Start", command = lambda: start() )
    buttonstart.grid( row = 9, column = 3, sticky = W + E)
    #progress bar
    BarVolSyringe1 = ttk.Progressbar(root, orient='horizontal',length = 300, mode='determinate', value = 0)
    BarVolSyringe1.grid(row = 12, columnspan = 4,sticky = W + E)
    old_progress = 0
    Username = ""
    F_name = ""
    L_name = ""
    Password = ""
    Phonenumber = ""
    Birtyday = ""

    root.mainloop()

