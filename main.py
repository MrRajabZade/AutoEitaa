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

def start(nameBrowser):
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

def start_wet(nameBrowser):
    nameBrowser = nameBrowser.lower()
    if str(nameBrowser) == "firefox":
        wet = webdriver.Firefox()
    elif str(nameBrowser) == "chrome":
        wet = webdriver.Chrome()

    try:
        wet.get("https://old.eitaa.com/")
    except:
        return "Error in get_eitaa_wet"
    error = 0
    status = 0
    while(status==0):
        try:
            search = wet.find_element(By.CSS_SELECTOR, 'input.form-control')
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
    return wet

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

def chat_id(text, im, driver):
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

def send_Message(driver, text):
    messagebox = driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
    messagebox.send_keys(text)
    messagebox.send_keys(Keys.ENTER)

def reply_Message(driver, textnew, Message):
    action = ActionChains(driver)
    action.context_click(on_element = Message)
    try:
        k = driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(4)")
        k.click()
    except:
        f = 0
    else:
        sleep(2.5)
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
    messagebox.send_keys(textnew)
    messagebox.send_keys(Keys.ENTER)

def edit_Message(driver, textnew, Message):
    action = ActionChains(driver)
    action.context_click(on_element = Message)
    try:
        k = driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(4)")
        k.click()
    except:
        f = 0
    else:
        sleep(2.5)
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

def forward_Message(driver, target, Message):
    action = ActionChains(driver)
    action.context_click(on_element = Message)
    try:
        k = driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(4)")
        k.click()
    except:
        f = 0
    else:
        sleep(2.5)
    sleep(1)
    action.perform()
    sleep(1)
    try:
        forward = driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(18) > div:nth-child(1)')
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

def pin_Message(driver, Message):
    action = ActionChains(driver)
    action.context_click(on_element = Message)
    try:
        k = driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(4)")
        k.click()
    except:
        f = 0
    else:
        sleep(2.5)
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

def delete_Message(driver, Message):
    action = ActionChains(driver)
    try:
        k = driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(4)")
        k.click()
    except:
        f = 0
    else:
        sleep(2.5)
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

def Search(driver, text, textmessage, Message):
    search = driver.find_element(By.CSS_SELECTOR, '#main-search')
    search.click()
    searchbox = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input')
    sleep(4)
    searchbox.send_keys(text)
    sleep(1)
    channel = driver.find_element(By.CSS_SELECTOR, '.search-group > ul:nth-child(1) > li:nth-child(1)')
    channel.click()
    sleep(2)
    if Message == True:
        searchbutton = driver.find_element(By.CSS_SELECTOR, "button.tgico-search:nth-child(5) > div:nth-child(1)")
        searchbutton.click()
        sleep(2)
        searchbox2 = driver.find_element(By.CSS_SELECTOR, "#search-private-container > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)")
        sleep(2)
        searchbox2.send_keys(textmessage)
        sleep(4)
        Messagebox = driver.find_element(By.CSS_SELECTOR, ".search-group-messages > ul:nth-child(2) > li:nth-child(1)")
        Messagebox.click()
        Messageh_id = Messagebox.get_attribute("data-mid")
        Message = driver.find_element(By.XPATH, """//div[@data-mid=""""+str(Messageh_id)""""]""")
        return Message
    return "done"

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
        namebox = chat.find_element(By.CLASS_NAME, "peer-title")
        name = str(namebox.text)
        chat.click()
        sleep(3)
        s = ""
        for y in range(1, int(int(bubbletext)+1)):
            chatbox = driver.find_element(By.CLASS_NAME, "bubble-content-wrapper")
            day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
            x = int(str("-"+str(y)))
            chatbox = driver.find_elements(By.CLASS_NAME, "bubble-content-wrapper")[int(x)]
            day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
            try:
                messagebox=day.find_element(By.CLASS_NAME, "message")
            except:
                return "Error in find_message"
            message = str(messagebox.get_attribute("innerHTML"))
            message = str(message)
            message = message.replace('\u200c',' ')
            db = str(message)
            bd = db.split('<span class="time tgico"')
            text = str(bd[0])
            text = str(text)
            Codelanguage = detect_language(text)
            datatext = {
        'name' : str(name),
        'text' : str(text),
        'chat_id' : str(chat_id),
        'language_code' : str(Codelanguage),
        'message_box':str(messagebox),
}
            s = str(str(datatext)+"\n"+str(s))
        return str(s)

def get_info(driver, chat_id):
    driver.get("https://web.eitaa.com/#"+str(chat_id))
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
    send_Message(driver, ".")
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

def get_phone(driver):
    try:
        phone = driver.find_element(By.CSS_SELECTOR, ".contact-number")
    except:
        return "invalid"
    else:
        phone = str(phone.text)
        return str(phone)
    
def Search_wet(wet, text):
    s = wet.find_element(By.CSS_SELECTOR, "input.form-control")
    s.click()
    s.send_keys(text)
    sleep(4)
    try:
        chat = wet.find_element(By.CSS_SELECTOR, ".im_dialog")
    except:
        return "Error in find_chat"
    chat.click()
    sleep(3)
    
def delete_member(name, wet):
    s = wet.find_element(By.CSS_SELECTOR, ".tg_head_peer_info")
    s.click()
    sleep(1.5)
    try:
        wet.find_element(By.CSS_SELECTOR, "a.md_modal_action:nth-child(2)")
    except:
        return "Error in is_admin"
    sleep(2)
    s = 1
    while True:
        s = s + 1
        try:
            user = wet.find_element(By.CSS_SELECTOR, "div.md_modal_list_peer_wrap:nth-child("+str(s)+") > div:nth-child(3) > a:nth-child(1)")
        except:
            return "Error in find_user"
        name_user = str(user.text)
        if str(name_user) == str(name):
            delete = wet.find_element(By.CSS_SELECTOR, "div.md_modal_list_peer_wrap:nth-child("+str(s)+") > a:nth-child(1)")
            delete.click()
            return "done"
        else:
            continue

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
    caption2 = driver.find_element(By.CSS_SELECTOR, "div.input-field:nth-child(5) > div:nth-child(1)")
    caption2.send_keys(caption)
    send = driver.find_element(By.CSS_SELECTOR, "button.btn-primary:nth-child(3)")
    send.click()

