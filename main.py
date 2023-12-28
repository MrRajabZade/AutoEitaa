from requests import *
from bs4 import BeautifulSoup
from time import *
import json
from sys import *
import os
import json
import datetime
from langdetect import detect
from io import BytesIO
import win32clipboard
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

def StartBot(nameBrowser):
    nameBrowser = nameBrowser.lower()
    if str(nameBrowser) == "firefox":
        driver = webdriver.Firefox()
    elif str(nameBrowser) == "chrome":
        driver = webdriver.Chrome()

    try:
        driver.get("https://web.eitaa.com/")
    except:
        return "Error in get_eitaa_web"
    error = 0
    status = 0
    while(status==0):
        try:
            search = driver.find_element(By.CSS_SELECTOR, '#main-search')
        except:
            if int(error) == 0:
                print("Waiting for login...")
                error = 1
            else:
                pass
        else:
            status = 1
            os.system('cls')
    sleep(15.5)
    return driver

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Unable to detect the language."
    
def canSendToUser(driver, chat_id):
    r = driver.execute_script("appUsersManager.canSendToUser("+str(chat_id)+")")
    if str(r) == "True":
        return True
    else:
        return False
    
def isUserOnline(driver, chat_id):
    r = driver.execute_script("appUsersManager.isUserOnlineVisible("+str(chat_id)+")")
    if str(r) == "True":
        return True
    else:
        return False

def getChat(driver):
    r = driver.execute_script("appChatsManager.chats")
    return str(r)

def isContact(driver, chat_id):
    r = driver.execute_script("appUsersManager.isContact("+str(chat_id)+")")
    if str(r) == "True":
        return True
    else:
        return False

def chat_id(im, text, driver):
    if im == True:
        chat = driver.find_element(By.CSS_SELECTOR, "div.user-title > span:nth-child(1)")
        chat_id = chat.get_attribute("data-peer-id")
        return str(chat_id)
    else:
        search = driver.find_element(By.CSS_SELECTOR, '#main-search')
        search.click()
        searchbox = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input')
        sleep(4)
        searchbox.send_keys(text)
        sleep(1)
        channel = driver.find_element(By.CSS_SELECTOR, '.search-group > ul:nth-child(1) > li:nth-child(1)')
        channel.click()
        chat = driver.find_element(By.CSS_SELECTOR, ".search-group > ul:nth-child(1) > li:nth-child(1)")
        chat_id = chat.get_attribute("data-peer-id")
        return str(chat_id)

def send_message(driver, chat_id, text):
    r = canSendToUser(driver, chat_id)
    if r == True:
        driver.execute_script('appMessagesManager.sendText('+str(chat_id)+', "'+str(text)+'")')
    else:
        return False
    try:
        text2, name, Codelanguage, message_id, messagebox = onchatupdate(driver)
    except:
        return None
    else:
        return text2, name, Codelanguage, message_id, messagebox
    
def reply_message(driver, text, message):
    action = ActionChains(driver)
    action.context_click(on_element = message)
    sleep(1)
    action.perform()
    sleep(1)
    try:
        reply = driver.find_element(By.CSS_SELECTOR, 'div.tgico-reply > div:nth-child(1)')
    except:
        return "Error in find_reply"
    try:
        reply.click()
    except:
        return "Error in click_reply"
    try:
        messagebox = driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
    except:
        return "Error in find_message_box"
    messagebox.send_keys(text)
    messagebox.send_keys(Keys.ENTER)
    text2, name, Codelanguage, message_id, messagebox2 = onchatupdate(driver)
    return text2, name, Codelanguage, message_id, messagebox2

def edit_message(driver, textnew, message):
    action = ActionChains(driver)
    action.context_click(on_element = message)
    sleep(1)
    action.perform()
    sleep(1)
    try:
        edit = driver.find_element(By.CSS_SELECTOR, 'div.tgico-edit > div:nth-child(1)')
    except:
        return "Error in find_edit"
    try:
        edit.click()
    except:
        return "Error in click_edit"
    try:
        messagebox = driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
    except:
        return "Error in find_message_box"
    messagebox.send_keys(Keys.CONTROL + 'a')
    messagebox.send_keys(Keys.BACKSPACE)
    messagebox.send_keys(textnew)
    messagebox.send_keys(Keys.ENTER)

def forward_message(driver, target, message, quote):
    action = ActionChains(driver)
    action.context_click(on_element = message)
    sleep(1)
    action.perform()
    sleep(1)
    try:
        if quote == True:
            forward = driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(18)')
        elif quote == False:
            forward = driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(19)')
    except:
        return "Error in find_forward"
    try:
        forward.click()
    except:
        return "Error in click_forward"
    textBox = driver.find_element(By.CSS_SELECTOR, '.selector-search-input')
    textBox.send_keys(target)
    textBox.send_keys(Keys.ENTER)
    sleep(1)
    forwardtarget = driver.find_element(By.CSS_SELECTOR, '.selector > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1)')
    forwardtarget.click()
    sleep(1)
    messagebox = driver.find_element(By.CSS_SELECTOR, 'div.chat:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(2) > div:nth-child(1)')
    messagebox.send_keys(Keys.ENTER)
    text2, name, Codelanguage, message_id, messagebox2 = onchatupdate(driver)
    return text2, name, Codelanguage, message_id, messagebox2

def pin_message(driver, message):
    action = ActionChains(driver)
    action.context_click(on_element = message)
    sleep(1)
    action.perform()
    sleep(1)
    try:
        pinbox = driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(18) > div:nth-child(1)')
    except:
        return "Error in find_pin"
    try:
        pinbox.click()
    except:
        return "Error in click_pin"
    pin = driver.find_element(By.CSS_SELECTOR, 'button.btn:nth-child(1) > div:nth-child(1)')
    pin.click()
    sleep(2)

def delete_message(driver, message):
    action = ActionChains(driver)
    action.context_click(on_element = message)
    sleep(1)
    action.perform()
    sleep(1)
    try:
        deletebox = driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(25) > div:nth-child(1)')
    except:
        return "Error in find_delete"
    try:
        deletebox.click()
    except:
        return "Error in click_delete"
    delete = driver.find_element(By.CSS_SELECTOR, 'button.btn:nth-child(1) > div:nth-child(1)')
    delete.click()

def Search(driver, x, text):
    search = driver.find_element(By.CSS_SELECTOR, '#main-search')
    sleep(3)
    search.click()
    button = driver.find_element(By.CSS_SELECTOR, "#search-container > div:nth-child(1) > div:nth-child(1) > nav:nth-child(1) > div:nth-child("+str(x)+")")
    button.click()
    searchbox = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input')
    sleep(4)
    searchbox.send_keys(text)
    sleep(1)
    tab = driver.find_element(By.CSS_SELECTOR, ".search-super-tabs > div:nth-child("+str(x)+")")
    tab.click()
    try:
        chat = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/div/div/div["+str(x)+"]/div/div[1]/ul/li[1]")
    except:
        return "Not Found !"
    else:
        try:
            message_id = chat.get_attribute("data-mid")
        except:
            chat.click()
        else:
            chat.click()
            return message_id

def on_message(driver):
    try:
        chat = driver.find_element(By.CSS_SELECTOR, "div.chatlist-parts:nth-child(1) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1)")
    except:
        try:
            chat = driver.find_element(By.CSS_SELECTOR, "div.chatlist-parts:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1)")
        except:
            try:
                chat = driver.find_element(By.CSS_SELECTOR, "div.chatlist-parts:nth-child(3) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1)")
            except:
                try:
                    chat = driver.find_element(By.CSS_SELECTOR, "div.chatlist-parts:nth-child(4) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1)")
                except:
                    try:
                        chat = driver.find_element(By.CSS_SELECTOR, "div.chatlist-parts:nth-child(5) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1)")
                    except:
                        try:
                            chat = driver.find_element(By.CSS_SELECTOR, "div.chatlist-parts:nth-child(6) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1)")
                        except:
                            return "Error in find_chat"
    cp = chat.find_element(By.CLASS_NAME, "user-caption")
    sub = cp.find_element(By.CLASS_NAME, "dialog-subtitle")
    try:
        bubble = sub.find_element(By.CLASS_NAME, "dialog-subtitle-badge")
        bubbletext = str(bubble.get_attribute('innerHTML'))
    except:
        return
    else:
        chat_id = str(chat.get_attribute('data-peer-id'))
        chat.click()
        sleep(3)
        for y in range(1, int(int(bubbletext)+1)):
            x = int(str("-"+str(y)))
            bubble = driver.find_element(By.CLASS_NAME, "bubble")[int(x)]
            message_id = bubble.get_attribute("data-mid")
            chatbox = bubble.find_elements(By.CLASS_NAME, "bubble-content-wrapper")
            day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
            namebox = day.find_element(By.CLASS_NAME, "name")
            name = namebox.find_element(By.CLASS_NAME, "peer-title").text
            try:
                messagebox=day.find_element(By.CLASS_NAME, "message")
            except:
                return "Error in find_message"
            # message = messagebox.get_attribute("innerHTML")
            # message = str(message)
            # message = message.replace('\u200c',' ')
            # db = str(message)
            # bd = db.split('<span class="time tgico"')
            # text = str(bd[0])
            text = str(messagebox.text)
            Codelanguage = detect_language(text)
            return str(text), str(name), str(Codelanguage), str(message_id), messagebox

def get_info(driver, chat_id):
    driver.get("https://web.eitaa.com/#"+str(chat_id))
    sleep(3.5)
    s = driver.find_element(By.CSS_SELECTOR, "div.sidebar-header:nth-child(2)")
    s.click()
    sleep(1)
    try:
        username = driver.find_element(By.CSS_SELECTOR, ".tgico-username")
    except:
        username = False
    else:
        username = str(username.text)
    try:
        bio = driver.find_element(By.CSS_SELECTOR, ".tgico-info")
    except:
        bio = False
    else:
        bio = str(bio.text)
    name = driver.find_element(By.CSS_SELECTOR, ".profile-name > span:nth-child(1)")
    name = str(name.text)
    status = driver.find_element(By.CSS_SELECTOR, ".profile-subtitle > span:nth-child(1)")
    status = str(status.text)
    try: 
        phone = driver.find_element(By.CSS_SELECTOR, ".tgico-phone")
    except:
        phone = False
    else:
        phone = str(phone.text)
    result = {
    'name':str(name),
    'status':str(status),
    'bio':str(bio),
    'phone':str(phone),
    'username':str(username),
    'chat_id':str(chat_id),
}
    return str(result)

def getMe(api):
    req = get("https://eitaayar.ir/api/"+api+"/getMe")
    return str(req.text)

def create_channel(driver, name, bio):
    menu = driver.find_element(By.CSS_SELECTOR, "#new-menu")
    menu.click()
    newchannel = driver.find_element(By.CSS_SELECTOR, ".tgico-newchannel")
    newchannel.click()
    sleep(1)
    name_channel = driver.find_element(By.CSS_SELECTOR, "div.input-wrapper:nth-child(2) > div:nth-child(1) > div:nth-child(1)")
    name_channel.send_keys(name)
    bio_channel = driver.find_element(By.CSS_SELECTOR, "div.input-wrapper:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
    bio_channel.send_keys(bio)
    next = driver.find_element(By.CSS_SELECTOR, ".tgico-arrow_next")
    next.click()
    sleep(1)
    next2 = driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(1)")
    sleep(1)
    next2.click()
    send_message(driver, ".")
    chatid = chat_id(False, True, driver)
    result = {
        'name':str(name),
        'bio':str(bio),
        'chat_id':str(chatid),
    }
    return str(result)

def folders_tabs(driver, x):
    s = driver.find_element(By.CSS_SELECTOR, "#folders-tabs > div:nth-child("+str(x)+")")
    s.click()
    sleep(3.5)

def contactMessage(driver, messagebox):
    try:
        c = messagebox.find_element(By.CLASS_NAME, "contact")
    except:
        return False
    chat_id = c.get_attribute("data-peer-id")
    d = c.find_element(By.CLASS_NAME, "contact-details")
    name = d.find_element(By.CLASS_NAME, "contact-name")
    number = d.find_element(By.CLASS_NAME, "contact-number")
    return str(name), str(number), str(chat_id)

def send_file(driver, filepath, caption):
    for i in filepath:
        image = Image.open(i)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        send_to_clipboard(win32clipboard.CF_DIB, data)
        messagebox = driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
        messagebox.send_keys(Keys.CONTROL + 'v')
    sleep(1)
    caption2 = driver.find_element(By.CSS_SELECTOR, "div.input-field-input")
    caption2.click()
    caption2.send_keys(caption)
    send = driver.find_element(By.CSS_SELECTOR, "button.btn-primary:nth-child(3)")
    send.click()

def onchatupdate(driver):
    bubble = driver.find_element(By.CLASS_NAME, "bubble")[-1]
    message_id = bubble.get_attribute("data-mid")
    chatbox = bubble.find_elements(By.CLASS_NAME, "bubble-content-wrapper")
    day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
    try:
        messagebox=day.find_element(By.CLASS_NAME, "message")
    except:
        return False
    else:
        # message = messagebox.get_attribute("innerHTML")
        # message = str(message)
        # message = message.replace('\u200c',' ')
        # db = str(message)
        # bd = db.split('<span class="time tgico"')
        # text = str(bd[0])
        text = str(messagebox.text)
        namebox = day.find_element(By.CLASS_NAME, "name")
        name = namebox.find_element(By.CLASS_NAME, "peer-title").text
        Codelanguage = detect_language(text)
        return str(text), str(name), str(Codelanguage), str(message_id), messagebox

def bot_command(text, command):
    command = "//" + str(command)
    if str(text) == str(command):
        return True
    else:
        return False
    
def get_user_photos(driver):
    bar = driver.find_element(By.CSS_SELECTOR, "div.sidebar-header:nth-child(2)")
    bar.click()
    b = 0
    s = 0
    d = ""
    while b!=1:
        s = s + 1
        try:
            photo = driver.find_element(By.CSS_SELECTOR, "div.profile-avatars-avatar:nth-child("+str(s)+") > img:nth-child(1)")
        except:
            b=1
        l = photo.get_attribute('src')
        d = d + str(l) + ","
    return str(d)

def ban_user(driver):
    s = driver.find_element(By.CSS_SELECTOR, "div.btn-icon:nth-child(6)")
    s.click()
    b = driver.find_element(By.CSS_SELECTOR, ".tgico-lock")
    b.click()

def add_user(driver):
    s = driver.find_element(By.CSS_SELECTOR, "div.btn-icon:nth-child(6)")
    s.click()
    b = driver.find_element(By.CSS_SELECTOR, ".tgico-adduser")
    b.click()

def delete_chat(driver):
    s = driver.find_element(By.CSS_SELECTOR, "div.btn-icon:nth-child(6)")
    s.click()
    b = driver.find_element(By.CSS_SELECTOR, "div.tgico-delete:nth-child(12)")
    b.click()

def isMessageNew(messagebox_old, messagebox_new):
    if str(messagebox_old) == str(messagebox_new):
        return False
    else:
        return True
    

def editAbout(driver, chat_id, text):
    driver.execute_script('appChatsManager.editAbout('+str(chat_id)+', "'+str(text)+'")')

