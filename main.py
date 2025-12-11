from requests import *
from comtypes import CoInitialize, CoUninitialize
from time import *
from sys import *
import os
import win32clipboard
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from colorama import Fore
import threading
import pyperclip
import requests
import soundcard as sc
import soundfile as sf
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation
import json

CoInitialize()

class Bot:
    def __init__(self, headless: bool, autologin: bool, Browser: str = "2"): # همه کروم رو دارن 
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless') 
        try:
            requests.get("https://web.eitaa.com/") #چک کردن وضعیت سرویس ایتا
        except:
            print(Fore.RED+"Eitaa Is Down Or System Is Offline!"+Fore.WHITE)
            return
        print(Fore.CYAN+"Bip... Bip... Starting!"+Fore.WHITE)
        if str(Browser) == "1":
            self.driver = webdriver.Firefox(options=options)
        elif str(Browser) == "2":
            self.driver = webdriver.Chrome(options=options)

        try:
            self.driver.get("https://web.eitaa.com/")
        except:
            return "Error in go_eitaa_web"
        def login():
                while True:
                    try:
                        phone_input = self.driver.find_element(By.CSS_SELECTOR, "div.input-field:nth-child(2) > div:nth-child(1)")
                    except:
                        continue
                    else:
                        phone = input("What's your "+Fore.GREEN+"phone number"+Fore.WHITE+" for login in Eitaa? +")
                        phone_input.send_keys(Keys.CONTROL + 'a')
                        phone_input.send_keys(Keys.BACKSPACE)
                        phone_input.send_keys(str(phone))
                        self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary:nth-child(4)").click()
                        break
                while True:
                    try:
                        code_input = self.driver.find_element(By.CSS_SELECTOR, "input.input-field-input")
                    except:
                        continue
                    else:
                        Otp_code = input("What's The "+Fore.GREEN+"OTP Code"+Fore.WHITE+" Sent you in Eitaa or sms? ")
                        code_input.send_keys(str(Otp_code))
                        break
                while True:
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, '#main-search')
                    except:
                        status = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[3]/div/label/span")
                        if str(status.text) == "کد نامعتبر است":
                            Otp_code = input("OTP code is wrong try again!")
                            exit()
                        else:     
                            print("Waiting...", end="\r")
                            continue
                    else:
                        os.system('cls')
                        sleep(15.5)
                        print(Fore.GREEN+"Login Successfully! Welcome!"+Fore.WHITE)
                        flag = input("Should I Save your Account so you don't have to Login again? (y/n)")
                        if flag == "y":
                            data_auth = self.driver.execute_script("""
                                var items = {};
                                for (var i = 0; i < localStorage.length; i++) {
                                    var key = localStorage.key(i);
                                    items[key] = localStorage.getItem(key);
                                }
                                return items;
                            """)
                            self.data_account = data_auth  # data_auth یک دیکشنری است

                            eitaa_auth = self.data_account.get("eitaa_auth")
                            if eitaa_auth is None:
                                raise KeyError("'eitaa_auth' key not found in data_account")
                            
                            if isinstance(eitaa_auth, str):
                                try:
                                    eitaa_auth_dict = json.loads(eitaa_auth)
                                except json.JSONDecodeError as e:
                                    raise ValueError(f"Invalid JSON in eitaa_auth: {e}")
                            elif isinstance(eitaa_auth, dict):
                                eitaa_auth_dict = eitaa_auth
                            else:
                                raise TypeError(f"eitaa_auth must be dict or str, got {type(eitaa_auth)}")
                            
                            if "id" not in eitaa_auth_dict:
                                raise KeyError("'id' not found in eitaa_auth dictionary")
                            user_id = eitaa_auth_dict["id"]
                            
                            with open(f"login.json", "w") as file:
                                json.dump(self.data_account, file, indent=4)
                            print("Your Account Userid ==> "+str(user_id))
                        else:
                            pass
                        break
            
        if autologin:
            try:
                with open(f"login.json", "r") as file:
                    account_data = json.load(file)
                    script = ""
                    for key, value in account_data.items():
                        escaped_key = json.dumps(key)
                        escaped_value = json.dumps(value)
                        script += f"localStorage.setItem({escaped_key}, {escaped_value});"
                    self.driver.execute_script(script)
                    self.driver.refresh()
                    os.system('cls')
                    sleep(15.5)
            except:
                try:
                    requests.get("https://web.eitaa.com/")
                except:
                    print(Fore.RED+"Eitaa Is Down Or System Is Offline!"+Fore.WHITE)
                    return
                print(Fore.RED+"Login Data Not Found!"+Fore.WHITE+"\nLogin "+Fore.RED+"Without"+Fore.WHITE+" AutoLogin First!") #اتو لاگین اینجا مدیریت شده تا در صورت عدم وجود، لاگین بشه
                login()
        else:
            login()
    def list_active_sessions(self):
        
        sessions = AudioUtilities.GetAllSessions()
        active_sessions = [] 

        print("Programs currently playing sound:")
        for session in sessions:
            if session.Process:
                process_name = session.Process.name()
                pid = session.Process.pid
                try:
                    audio_meter = session._ctl.QueryInterface(IAudioMeterInformation)
                    peak = audio_meter.GetPeakValue()

                    if peak > 0:
                        print(f"Program: {process_name}, PID: {pid}, Peak Volume: {peak:.2f}")
                        active_sessions.append((session, process_name, pid))
                except Exception as e:
                    print(f"Could not retrieve audio info for {process_name}: {e}")

        return active_sessions

    def mute_sessions(self, active_sessions):
        for session, process_name, pid in active_sessions:
            try:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                print(f"Muting Program: {process_name}, PID: {pid}")
                volume.SetMasterVolume(0, None)
            except Exception as e:
                print(f"Could not mute {process_name}: {e}")

    def unmute_sessions(self, active_sessions):
        for session, process_name, pid in active_sessions:
            try:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                print(f"Unmuting Program: {process_name}, PID: {pid}")
                volume.SetMasterVolume(1, None)
            except Exception as e:
                print(f"Could not unmute {process_name}: {e}")
            

    def copy_to_clipboard(self, file_name):
        command = f"powershell Set-Clipboard -LiteralPath {file_name}"
        os.system(command)

    def save_audio(self, s):
        OUTPUT_FILE_NAME = "output.mp3"    # file name.
        SAMPLE_RATE = 48000              # [Hz]. sampling rate.
        RECORD_SEC = int(s)                  # [sec]. duration recording audio.

        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
            # record audio with loopback from default speaker.
            data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
            
            # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
            sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, window.scrollY + 30)")

    def send_to_clipboard(self, clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def isMessageNew(self, msg1, msg2):
        if str(msg1) == str(msg2):
            return False
        else:
            return True
    
    def canSendToUser(self, chat_id):
        r = self.driver.execute_script("return appUsersManager.canSendToUser("+str(chat_id)+");")
        if str(r) == "true":
            return True
        elif str(r) == "None":
            return "None"
        else:
            return False
    
    def isUserOnline(self, chat_id):
        r = self.driver.execute_script("return appUsersManager.isUserOnlineVisible("+str(chat_id)+");")
        if str(r) == "true":
            return True
        else:
            return False

    def myId(self):
        r = self.driver.execute_script("return appImManager.myId;")
        return str(r)

    def getContactList(self): 
        r = self.driver.execute_script("return appUsersManager.contactsList;")
        return str(r)

    def isContact(self, chat_id):
        r = self.driver.execute_script("return appUsersManager.isContact("+str(chat_id)+");")
        if str(r) == "true":
            return True
        else:
            return False
    
    def getPeerUsername(self, chat_id):
        r = self.driver.execute_script("return appPeersManager.getPeerUsername("+str(chat_id)+");")
        if str(r) == "true":
            return True
        else:
            return False

    def isAnyGroup(self, chat_id):
        r = self.driver.execute_script("return appPeersManager.isAnyGroup("+str(chat_id)+");")
        if str(r) == "true":
            return True
        else:
            return False
        
    def isUser(self, chat_id):
        if str(chat_id[0]) == "-":
            return False
        else:
            return True

    def getPeerSearchText(self, chat_id):
        r = self.driver.execute_script("return appPeersManager.getPeerSearchText("+str(chat_id)+");")
        return str(r)

    def getPeer(self, chat_id): 
        r = self.driver.execute_script("return appPeersManager.getPeer("+str(chat_id)+");")
        return str(r)

    def getDialogType(self, chat_id): 
        r = self.driver.execute_script("return appPeersManager.getDialogType("+str(chat_id)+");")
        return str(r)

    def canPinMessage(self, msg_id):
        r = self.driver.execute_script("return appPeersManager.canPinMessage("+str(msg_id)+");")
        if str(r) == "true":
            return True
        else:
            return False
        
    def canDeleteMessage(self, msg_id):
        r = self.driver.execute_script("return appMessagesManager.canDeleteMessage("+str(msg_id)+");")
        if str(r) == "true":
            return True
        else:
            return False

    def canEditMessage(self, msg_id):
        r = self.driver.execute_script("return appMessagesManager.canEditMessage("+str(msg_id)+");")
        if str(r) == "true":
            return True
        else:
            return False

    def canEditMessage(self, msg_id):
        r = self.driver.execute_script("return appMessagesManager.canForwardMessage("+str(msg_id)+");")
        if str(r) == "true":
            return True
        else:
            return False
        
    def back(self):
        self.driver.execute_script("appNavigationController.back()")

    def get_currentHash(self): 
        r = self.driver.execute_script("return appNavigationController.currentHash;")
        return str(r)

    def chat_id(self):
        chat = self.driver.find_element(By.CSS_SELECTOR, "div.user-title > span:nth-child(1)")
        chatid = chat.get_attribute("data-peer-id")
        return str(chatid)

    def send_message(self, chat_id, text):
        global message_sent
        message_sent = True
        text = str(text)
        text = text.replace('""', '')
        text = text.replace("\n", "\\n")
        text = text.replace("\"", '\\"')
        self.driver.execute_script(f'appMessagesManager.sendText({chat_id}, "{text}")')
        sleep(0.5)
        try:
            res, map = self.onchatupdate()
        except:
            return None
        else:
            return res, map
        
    def reply_to_message(self, text, chatid, msg_id):
        global message_sent
        message_sent = True
        text = str(text)
        text = text.replace('""', '')
        text = text.replace("\n", "\\n")
        text = text.replace("\"", '\\"')
        self.driver.execute_script('appMessagesManager.sendText('+str(chatid)+', "'+str(text)+'", { replyToMsgId: '+str(msg_id)+' });')
        try:
            res, map = self.onchatupdate()
        except:
            return None
        else:
            return res, map

    def edit_message(self, textnew, message):
        action = ActionChains(self.driver)
        action.context_click(on_element = message)
        sleep(1)
        action.perform()
        sleep(1)
        try:
            edit = self.driver.find_element(By.CSS_SELECTOR, 'div.tgico-edit > div:nth-child(1)')
        except:
            return "Error in find_edit"
        try:
            edit.click()
        except:
            return "Error in click_edit"
        try:
            map = self.driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
        except:
            return "Error in find_message_box"
        map.send_keys(Keys.CONTROL + 'a')
        map.send_keys(Keys.BACKSPACE)
        map.send_keys(textnew)
        map.send_keys(Keys.ENTER)

    def forward_message(self, target, message, quote):
        action = ActionChains(self.driver)
        action.context_click(on_element = message)
        sleep(1)
        action.perform()
        sleep(1)
        try:
            if quote == True:
                forward = self.driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(18)')
            elif quote == False:
                forward = self.driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(19)')
        except:
            return "Error in find_forward"
        try:
            forward.click()
        except:
            return "Error in click_forward"
        textBox = self.driver.find_element(By.CSS_SELECTOR, '.selector-search-input')
        textBox.send_keys(target)
        textBox.send_keys(Keys.ENTER)
        sleep(1)
        try:
            forwardtarget = self.driver.find_element(By.CSS_SELECTOR, '.selector > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1)')
        except:
            print("Not find a target")
            return
        forwardtarget.click()
        sleep(1)
        but = self.driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
        but.send_keys(Keys.ENTER)
        res, map = self.onchatupdate(self.driver)
        return res, map
    
    def pin_message(self, message):
        action = ActionChains(self.driver)
        action.context_click(on_element = message)
        sleep(1)
        action.perform()
        sleep(1)
        try:
            pinbox = self.driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(18) > div:nth-child(1)')
        except:
            return "Error in find_pin"
        try:
            pinbox.click()
        except:
            return "Error in click_pin"
        pin = self.driver.find_element(By.CSS_SELECTOR, 'button.btn:nth-child(1) > div:nth-child(1)')
        pin.click()
        sleep(2)

    def delete_message(self, message):
        action = ActionChains(self.driver)
        action.context_click(on_element = message)
        sleep(1)
        action.perform()
        sleep(1)
        try:
            deletebox = self.driver.find_element(By.CSS_SELECTOR, 'div.btn-menu-item:nth-child(26)')
        except:
            return "Error in find_delete"
        try:
            deletebox.click()
        except:
            return "Error in click_delete"
        delete = self.driver.find_element(By.CSS_SELECTOR, 'button.btn:nth-child(1) > div:nth-child(1)')
        delete.click()

    def search(self, x, text):
        search = self.driver.find_element(By.CSS_SELECTOR, '#main-search')
        sleep(3)
        search.click()
        button = self.driver.find_element(By.CSS_SELECTOR, "#search-container > div:nth-child(1) > div:nth-child(1) > nav:nth-child(1) > div:nth-child("+str(x)+")")
        button.click()
        searchbox = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input')
        sleep(4)
        searchbox.send_keys(text)
        sleep(1)
        tab = self.driver.find_element(By.CSS_SELECTOR, ".search-super-tabs > div:nth-child("+str(x)+")")
        tab.click()
        try:
            chat = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/div/div/div["+str(x)+"]/div/div[1]/ul/li[1]")
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

    def FindActiveFolderTabs(self):
        elements = self.driver.find_element(By.CSS_SELECTOR, '.menu-horizontal-div .menu-horizontal-div-item.rp')

        index = None
        for i, el in enumerate(elements):
            if 'active' in el.get_attribute('class'):
                index = i + 1
                break

        return int(index)

    def on_new_message(self, chat):
        try:
            chat = self.driver.find_element(By.CSS_SELECTOR, "li.chatlist-chat:nth-child("+str(chat)+")")
        except:
            return "not found chat"
        cp = chat.find_element(By.CLASS_NAME, "user-caption")
        sub = cp.find_element(By.CLASS_NAME, "dialog-subtitle")
        try:
            bubble = sub.find_element(By.CLASS_NAME, "dialog-subtitle-badge")
            bubbletext = str(bubble.get_attribute('innerHTML'))
        except:
            return None
        else:
            chatid = str(chat.get_attribute('data-peer-id'))
            chat.click()
            sleep(7.5)
            chat.click()
            sleep(1)
            response = {}
            for y in range(1, int(int(bubbletext)+1)):
                x = int(str("-"+str(y)))
                try:
                    bubble = self.driver.find_elements(By.CLASS_NAME, "bubble")[int(x)]
                except:
                    self.go_chat(chatid)
                    sleep(10)
                    try:
                       bubble = self.driver.find_elements(By.CLASS_NAME, "bubble")[int(x)]
                    except: 
                        break
                message_id = bubble.get_attribute("data-mid")
                chatbox = bubble.find_element(By.CLASS_NAME, "bubble-content-wrapper")
                day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
                try:
                    namebox = day.find_element(By.CLASS_NAME, "name")
                except:
                    is_from = False
                else:
                    is_from = True
                    try:
                        chatid_from = str(namebox.get_attribute('data-peer-id'))
                    except:
                        j = namebox.find_element(By.CLASS_NAME, "i18n").text
                        if "هدایت شده از " in str(j):
                            is_forward = True
                            peer_title = namebox.find_element(By.CLASS_NAME, "peer-title")
                            chatid_from = str(peer_title.get_attribute("data-peer-id"))
                            name_from = str(peer_title.text)
                        else:
                            is_forward = False
                    else:
                        is_forward = False
                        name_from = namebox.find_element(By.CLASS_NAME, "peer-title").text
                name = self.driver.find_element(By.CSS_SELECTOR, "div.user-title > span:nth-child(1)").text
                try:
                    map=day.find_element(By.CLASS_NAME, "message")
                except:
                    return "Error in find_message"
                try:
                    doc = map.find_element(By.CLASS_NAME, "document-container")
                except:
                    pass
                else:
                    action = ActionChains(self.driver)
                    action.context_click(on_element = map)
                    sleep(1)
                    action.perform()
                    sleep(1)
                    try:
                        tigo_link = self.driver.find_element(By.CSS_SELECTOR, "div.tgico-link:nth-child(12)")
                    except:
                        link = ""
                    else:
                        tigo_link.click()
                        sleep(0.1)
                        link = str(pyperclip.paste())
                    doc2 = doc.find_element(By.CLASS_NAME, "document-wrapper")
                    audio_element = doc2.find_element(By.TAG_NAME, "audio-element")
                    btn_play = audio_element.find_element(By.CLASS_NAME, "audio-toggle")
                    audio_time = audio_element.find_element(By.CLASS_NAME, "audio-time").text
                    audio_time = str(audio_time).split(":")
                    audio_time = (int(audio_time[0])*60)+int(audio_time[1])
                    active_sessions = self.list_active_sessions() 
                    self.mute_sessions(active_sessions)
                    btn_play.click()
                    self.save_audio(audio_time)
                    self.unmute_sessions(active_sessions)
                    audio = True
                try:
                    attachment = day.find_element(By.CLASS_NAME, "attachment")
                except:
                    media = False
                else:
                    try:
                        attachment.click()
                    except:
                        media = attachment.find_element(By.CLASS_NAME, "media-photo")
                        media = media.get_attribute("src")
                    else:
                        sleep(0.5)
                        media = self.driver.find_element(By.CSS_SELECTOR, ".media-viewer-aspecter > img:nth-child(1)")
                        media = media.get_attribute("src")
                        btn = self.driver.find_element(By.CLASS_NAME, "media-viewer-buttons")
                        btn.find_element(By.CLASS_NAME, "tgico-close").click()
                    try:
                        video_time = attachment.find_element(By.CLASS_NAME, "video-time")
                    except:
                        is_video = False
                    else:
                        is_video = True
                        video_time = str(video_time.text)
                try:
                    reply = day.find_element(By.CLASS_NAME, "reply")
                except:
                    reply = False
                else:
                    reply = reply.find_element(By.CLASS_NAME, "reply-content")
                    reply = reply.get_attribute("innerHTML")
                time_tgico = map.find_element(By.TAG_NAME, "span")
                time_inner = time_tgico.find_element(By.CLASS_NAME, "i18n").text
                if str(time_inner) == "":
                    is_from_me = False
                else:
                    is_from_me = True
                time = time_tgico.get_attribute("title")
                try:
                    view_message = time_tgico.find_element(By.CLASS_NAME, "post-views").text
                except:
                    view_message = False
                text = str(map.text)
                text = text.split("\n"+str(time_inner))[0]
                response2 = {
                    "result"+str(x):{
                        "message_id":str(message_id),
                        "link":str(link),
                        "chat":{
                            "id":str(chatid),
                            "title":str(name),
                            "username":str(self.getPeerUsername(chatid)),
                            "type":str(self.getDialogType(chatid))
                        },
                    }
                }
                if audio:
                    new_data = {
                        "audio":{
                            "output_file":"output.mp3",
                            "audio_time":int(audio_time)
                        }
                    }
                    response2["result"+str(x)].update(new_data)
                if media:
                    new_data = {
                        "media":{
                            "media-src": str(media)
                        }
                    }
                    response2["result"+str(x)].update(new_data)
                    if is_video:
                        new_data = {
                            "video":{
                                "video-time":str(video_time)
                            }
                        }
                        response2["result"+str(x)]["media"].update(new_data)
                if is_from:
                    new_data = {
                        "from":{
                            "is_forward":is_forward,
                            "id":str(chatid_from),
                            "name":str(name_from),
                            "username":str(self.getPeerUsername(chatid_from)),
                            "type":str(self.getDialogType(chatid_from))
                        }
                    }
                    response2["result"+str(x)].update(new_data)
                if reply:
                    new_data = {
                        "reply":{
                            "reply-content": str(reply)
                        }
                    }
                    response2["result"+str(x)].update(new_data)
                if view_message:
                    new_data = {
                        "date":str(time),
                        "text":str(text),
                        "view":str(view_message)
                    }
                else:
                    new_data = {
                        "date":str(time),
                        "text":str(text),
                        "is_from_me":is_from_me
                    }
                response2["result"+str(x)].update(new_data)
                response.update(response2)
            return response, map
        
    def on_all_message(self, chat):
        try:
            chat = self.driver.find_element(By.CSS_SELECTOR, "li.chatlist-chat:nth-child("+str(chat)+")")
        except:
            return "not found chat"
        cp = chat.find_element(By.CLASS_NAME, "user-caption")
        sub = cp.find_element(By.CLASS_NAME, "dialog-subtitle")
        try:
            bubble = sub.find_element(By.CLASS_NAME, "dialog-subtitle-badge")
            bubbletext = str(bubble.get_attribute('innerHTML'))
        except:
            pass
        chatid = str(chat.get_attribute('data-peer-id'))
        chat.click()
        sleep(7.5)
        chat.click()
        sleep(1)
        response = {}
        y = 0
        while True:
            y += 1
            x = int(str("-"+str(y)))
            try:
                bubble = self.driver.find_elements(By.CLASS_NAME, "bubble")[int(x)]
            except:
                self.go_chat(chatid)
                sleep(10)
                try:
                    bubble = self.driver.find_elements(By.CLASS_NAME, "bubble")[int(x)]
                except: 
                    break
            message_id = bubble.get_attribute("data-mid")
            try:
                chatbox = bubble.find_element(By.CLASS_NAME, "bubble-content-wrapper")
            except:
                continue
            day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
            try:
                namebox = day.find_element(By.CLASS_NAME, "name")
            except:
                is_from = False
            else:
                is_from = True
                try:
                    chatid_from = str(namebox.get_attribute('data-peer-id'))
                except:
                    j = namebox.find_element(By.CLASS_NAME, "i18n").text
                    if "هدایت شده از " in str(j):
                        is_forward = True
                        peer_title = namebox.find_element(By.CLASS_NAME, "peer-title")
                        chatid_from = str(peer_title.get_attribute("data-peer-id"))
                        name_from = str(peer_title.text)
                    else:
                        is_forward = False
                else:
                    is_forward = False
                    name_from = namebox.find_element(By.CLASS_NAME, "peer-title").text
            name = self.driver.find_element(By.CSS_SELECTOR, "div.user-title > span:nth-child(1)").text
            try:
                map=day.find_element(By.CLASS_NAME, "message")
            except:
                return "Error in find_message"
            try:
                    doc = map.find_element(By.CLASS_NAME, "document-container")
            except:
                pass
            else:
                action = ActionChains(self.driver)
                action.context_click(on_element = map)
                sleep(1)
                action.perform()
                sleep(1)
                try:
                    tigo_link = self.driver.find_element(By.CSS_SELECTOR, "div.tgico-link:nth-child(12)")
                except:
                    link = ""
                else:
                    tigo_link.click()
                    sleep(0.1)
                    link = str(pyperclip.paste())
                doc2 = doc.find_element(By.CLASS_NAME, "document-wrapper")
                audio_element = doc2.find_element(By.TAG_NAME, "audio-element")
                btn_play = audio_element.find_element(By.CLASS_NAME, "audio-toggle")
                audio_time = audio_element.find_element(By.CLASS_NAME, "audio-time").text
                audio_time = str(audio_time).split(":")
                audio_time = (int(audio_time[0])*60)+int(audio_time[1])
                active_sessions = self.list_active_sessions() 
                self.mute_sessions(active_sessions)
                btn_play.click()
                self.save_audio(audio_time)
                self.unmute_sessions(active_sessions)
                audio = True
            try:
                attachment = day.find_element(By.CLASS_NAME, "attachment")
            except:
                media = False
            else:
                media = attachment.find_element(By.CLASS_NAME, "media-photo")
                media = media.get_attribute("src")
                try:
                    video_time = attachment.find_element(By.CLASS_NAME, "video-time")
                except:
                    is_video = False
                else:
                    is_video = True
                    video_time = str(video_time.text)
            try:
                reply = day.find_element(By.CLASS_NAME, "reply")
            except:
                reply = False
            else:
                reply = reply.find_element(By.CLASS_NAME, "reply-content")
                reply = reply.get_attribute("innerHTML")
            time_tgico = map.find_element(By.TAG_NAME, "span")
            time_inner = time_tgico.find_element(By.CLASS_NAME, "inner").get_attribute("innerHTML").split("</span>")[1]
            if str(time_inner) == "":
                is_from_me = False
            else:
                is_from_me = True
            time = time_tgico.get_attribute("title")
            try:
                view_message = time_tgico.find_element(By.CLASS_NAME, "post-views").text
            except:
                view_message = False
            text = str(map.text)
            response2 = {
                "result"+str(x):{
                    "message_id":str(message_id),
                    "link":str(link),
                    "chat":{
                        "id":str(chatid),
                        "title":str(name),
                        "username":str(self.getPeerUsername(chatid)),
                        "type":str(self.getDialogType(chatid))
                    },
                }
            }
            if audio:
                new_data = {
                    "audio":{
                        "output_file":"output.mp3",
                        "audio_time":int(audio_time)
                    }
                }
                response2["result"+str(x)].update(new_data)
            if media:
                new_data = {
                    "media":{
                        "media-src": str(media)
                    }
                }
                response2["result"+str(x)].update(new_data)
                if is_video:
                    new_data = {
                        "video":{
                            "video-time":str(video_time)
                        }
                    }
                    response2["result"+str(x)]["media"].update(new_data)
            if is_from:
                new_data = {
                    "from":{
                        "is_forward":is_forward,
                        "is_from_me":is_from_me,
                        "id":str(chatid_from),
                        "name":str(name_from),
                        "username":str(self.getPeerUsername(chatid_from)),
                        "type":str(self.getDialogType(chatid_from))
                    }
                }
                response2["result"+str(x)].update(new_data)
            if reply:
                new_data = {
                    "reply":{
                        "reply-content": str(reply)
                    }
                }
                response2["result"+str(x)].update(new_data)
            if view_message:
                new_data = {
                    "date":str(time),
                    "text":str(text),
                    "view":str(view_message)
                }
            else:
                new_data = {
                    "date":str(time),
                    "text":str(text),
                    "is_from_me":is_from_me
                }
            if bubbletext:
                if int(bubbletext) >= int(y):
                    new_data = {
                        "unread":True,
                    }
                else:
                    new_data = {
                        "unread":False,
                    }
            response2["result"+str(x)].update(new_data)
            response.update(response2)
        return response, map

    def get_info(self, chat_id):
        s = self.driver.find_element(By.CSS_SELECTOR, "div.sidebar-header:nth-child(2)")
        s.click()
        sleep(1)
        try:
            username = self.driver.find_element(By.CSS_SELECTOR, ".tgico-username")
        except:
            username = False
        else:
            username = str(username.text)
        try:
            bio = self.driver.find_element(By.CSS_SELECTOR, ".tgico-info")
        except:
            bio = False
        else:
            bio = str(bio.text)
        name = self.driver.find_element(By.CSS_SELECTOR, ".profile-name > span:nth-child(1)")
        name = str(name.text)
        status = self.driver.find_element(By.CSS_SELECTOR, ".profile-subtitle > span:nth-child(1)")
        status = str(status.text)
        try: 
            phone = self.driver.find_element(By.CSS_SELECTOR, ".tgico-phone")
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
    
    def sendChatActionThread(self):
        global message_sent
        message_sent = False
        try:
                map = self.driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
        except:
            return "Error in find_message_box"
        while not message_sent:
            map.send_keys("s")
            map.send_keys(Keys.CONTROL + 'a')
            map.send_keys(Keys.BACKSPACE)

    def sendChatAction(self, chatid):
        self.go_chat(chatid)
        thread = threading.Thread(target=self.sendChatActionThread)
        thread.start()

    def getMe(api):
        req = get("https://eitaayar.ir/api/"+api+"/getMe")
        return str(req.text)

    def create_channel(self, name:str, bio:str):
        menu = self.driver.find_element(By.CSS_SELECTOR, "#new-menu")
        menu.click()
        newchannel = self.driver.find_element(By.CSS_SELECTOR, ".tgico-newchannel")
        newchannel.click()
        sleep(1)
        name_channel = self.driver.find_element(By.CSS_SELECTOR, "div.input-wrapper:nth-child(2) > div:nth-child(1) > div:nth-child(1)")
        name_channel.send_keys(name)
        bio_channel = self.driver.find_element(By.CSS_SELECTOR, "div.input-wrapper:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
        bio_channel.send_keys(bio)
        next = self.driver.find_element(By.CSS_SELECTOR, ".tgico-arrow_next")
        next.click()
        sleep(1)
        next2 = self.driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(1)")
        sleep(1)
        next2.click()
        self.send_message(self.driver, ".")
        chat_id = chat_id(False, True, self.driver)
        result = {
            'name':str(name),
            'bio':str(bio),
            'chat_id':str(chat_id),
        }
        return str(result)

    def folders_tabs(self, x):
        s = self.driver.find_element(By.CSS_SELECTOR, "#folders-tabs > div:nth-child("+str(x)+")")
        s.click()
        sleep(3.5)

    def contactMessage(self, map):
        try:
            c = map.find_element(By.CLASS_NAME, "contact")
        except:
            return False
        chat_id = c.get_attribute("data-peer-id")
        d = c.find_element(By.CLASS_NAME, "contact-details")
        name = d.find_element(By.CLASS_NAME, "contact-name")
        number = d.find_element(By.CLASS_NAME, "contact-number")
        return str(name.text), str(number.text), str(chat_id)

    def send_album(self, filepath, caption, Send_compressed):
        global message_sent
        message_sent = True
        n = 3
        for i in filepath:
            n += 1
            image = Image.open(i)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            self.send_to_clipboard(win32clipboard.CF_DIB, data)
            map = self.driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
            map.send_keys(Keys.CONTROL + 'v')
        sleep(1)
        btn = self.driver.find_element(By.XPATH, "//span[contains(., 'ارسال به صورت فشرده')]")
        title = self.driver.find_element(By.CSS_SELECTOR, ".popup-title > span:nth-child(1)")
        if Send_compressed:
            if str(title.text) == "ارسال عکس":
                pass
        else:
            if str(title.text) == "ارسال عکس":
                btn.click()
        try:
            caption2 = self.driver.find_element(By.CSS_SELECTOR, "div.input-field-input")
            caption2.click()
        except:
            caption2 = self.driver.find_element(By.CSS_SELECTOR, "div.input-field:nth-child("+str(n)+") > div:nth-child(1)")
            caption2.click()
        caption2.send_keys(caption)
        send = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary:nth-child(3)")
        send.click()

    def send_other(self, path, caption, Send_compressed):
        global message_sent 
        message_sent = True
        n = 3
        for i in path:
            self.copy_to_clipboard(str(i))
            map = self.driver.find_element(By.CSS_SELECTOR, 'div.input-message-input:nth-child(1)')
            map.send_keys(Keys.CONTROL + 'v')
            n += 1
        sleep(1)
        btn = self.driver.find_element(By.XPATH, "//span[contains(., 'ارسال به صورت فشرده')]")
        title = self.driver.find_element(By.CSS_SELECTOR, ".popup-title > span:nth-child(1)")
        if Send_compressed:
            if str(title.text) == "ارسال عکس":
                pass
        else:
            if str(title.text) == "ارسال عکس":
                btn.click()
        try:
            caption2 = self.driver.find_element(By.CSS_SELECTOR, "div.input-field-input")
            caption2.click()
        except:
            caption2 = self.driver.find_element(By.CSS_SELECTOR, "div.input-field:nth-child("+str(n)+") > div:nth-child(1)")
            caption2.click()
        caption2.send_keys(caption)
        send = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary:nth-child(3)")
        send.click()

    def onchatupdate(self):
        chatid = self.chat_id()
        try:
            bubble = self.driver.find_elements(By.CLASS_NAME, "bubble")[-1]
        except:
            self.go_chat(chatid)
            sleep(10)
            try:
               bubble = self.driver.find_elements(By.CLASS_NAME, "bubble")[-1]
            except: 
                return None
        message_id = bubble.get_attribute("data-mid")
        chatbox = bubble.find_element(By.CLASS_NAME, "bubble-content-wrapper")
        day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
        try:
            namebox = day.find_element(By.CLASS_NAME, "name")
        except:
            is_from = False
        else:
            is_from = True
            try:
                chatid_from = str(namebox.get_attribute('data-peer-id'))
            except:
                j = namebox.find_element(By.CLASS_NAME, "i18n").text
                if "هدایت شده از " in str(j):
                    is_forward = True
                    peer_title = namebox.find_element(By.CLASS_NAME, "peer-title")
                    chatid_from = str(peer_title.get_attribute("data-peer-id"))
                    name_from = str(peer_title.text)
                else:
                    is_forward = False
            else:
                is_forward = False
                name_from = namebox.find_element(By.CLASS_NAME, "peer-title").text
        name = self.driver.find_element(By.CSS_SELECTOR, "div.user-title > span:nth-child(1)").text
        try:
            map=day.find_element(By.CLASS_NAME, "message")
        except:
            return "Error in find_message"
        action = ActionChains(self.driver)
        action.context_click(on_element = map)
        sleep(1)
        action.perform()
        sleep(1)
        try:
            tigo_link = self.driver.find_element(By.CSS_SELECTOR, "div.tgico-link:nth-child(12)")
        except:
            link = ""
        else:
            tigo_link.click()
            sleep(0.1)
            link = str(pyperclip.paste())
        try:
            attachment = day.find_element(By.CLASS_NAME, "attachment")
        except:
            media = False
        else:
            media = attachment.find_element(By.CLASS_NAME, "media-photo")
            media = media.get_attribute("src")
            try:
                video_time = attachment.find_element(By.CLASS_NAME, "video-time")
            except:
                is_video = False
            else:
                is_video = True
                video_time = str(video_time.text)
        try:
            reply = day.find_element(By.CLASS_NAME, "reply")
        except:
            reply = False
        else:
            reply = reply.find_element(By.CLASS_NAME, "reply-content")
            reply = reply.get_attribute("innerHTML")
        time_tgico = map.find_element(By.TAG_NAME, "span")
        time_inner = time_tgico.find_element(By.CLASS_NAME, "i18n").text
        if str(time_inner) == "":
            is_from_me = False
        else:
            is_from_me = True
        time = time_tgico.get_attribute("title")
        try:
            view_message = time_tgico.find_element(By.CLASS_NAME, "post-views").text
        except:
            view_message = False
        text = str(map.text)
        text = text.split("\n"+str(time_inner))[0]
        response2 = {
            "result":{
                "message_id":str(message_id),
                "link":str(link),
                "chat":{
                    "id":str(chatid),
                    "title":str(name),
                    "username":str(self.getPeerUsername(chatid)),
                    "type":str(self.getDialogType(chatid))
                },
            }
        }
        if media:
            new_data = {
                "media":{
                    "media-src": str(media)
                }
            }
            response2["result"].update(new_data)
            if is_video:
                new_data = {
                    "video":{
                        "video-time":str(video_time)
                    }
                }
                response2["result"]["media"].update(new_data)
        if is_from:
            new_data = {
                "from":{
                    "is_forward":is_forward,
                    "id":str(chatid_from),
                    "name":str(name_from),
                    "username":str(self.getPeerUsername(chatid_from)),
                    "type":str(self.getDialogType(chatid_from))
                }
            }
            response2["result"].update(new_data)
        if reply:
            new_data = {
                "reply":{
                    "reply-content": str(reply)
                }
            }
            response2["result"].update(new_data)
        if view_message:
            new_data = {
                "date":str(time),
                "text":str(text),
                "is_from_me":is_from_me,
                "view":str(view_message)
        }
        else:
            new_data = {
                "date":str(time),
                "text":str(text),
                "is_from_me":is_from_me
            }
            response2["result"].update(new_data)
        return response2, map
        
    def driver_command(text, command):
        command = "//" + str(command)
        if str(text) == str(command):
            return True
        else:
            return False
        
    def get_user_photos(self):
        bar = self.driver.find_element(By.CSS_SELECTOR, "div.sidebar-header:nth-child(2)")
        bar.click()
        b = 0
        s = 0
        d = ""
        while b!=1:
            s = s + 1
            try:
                photo = self.driver.find_element(By.CSS_SELECTOR, "div.profile-avatars-avatar:nth-child("+str(s)+") > img:nth-child(1)")
            except:
                b=1
            l = photo.get_attribute('src')
            d = d + str(l) + ","
        return str(d)

    def ban_user(self):
        s = self.driver.find_element(By.CSS_SELECTOR, "div.btn-icon:nth-child(6)")
        s.click()
        b = self.driver.find_element(By.CSS_SELECTOR, ".tgico-lock")
        b.click()

    def add_user(self):
        s = self.driver.find_element(By.CSS_SELECTOR, "div.btn-icon:nth-child(6)")
        s.click()
        b = self.driver.find_element(By.CSS_SELECTOR, ".tgico-adduser")
        b.click()

    def delete_chat(self):
        s = self.driver.find_element(By.CSS_SELECTOR, "div.btn-icon:nth-child(6)")
        s.click()
        b = self.driver.find_element(By.CSS_SELECTOR, "div.tgico-delete:nth-child(12)")
        b.click()
        
    def edit_about(self, chat_id, text):
        self.driver.execute_script('appChatsManager.editAbout('+str(chat_id)+', "'+str(text)+'")')

    def onsubtitlechat(self, chat):
        chat = self.driver.find_element(By.CSS_SELECTOR, "li.chatlist-chat:nth-child("+str(chat)+")")
        chatid = chat.get_attribute("data-peer-id")
        cp = chat.find_element(By.CLASS_NAME, "user-caption")
        sub = cp.find_element(By.CLASS_NAME, "dialog-subtitle")
        dialog_title = cp.find_element(By.CLASS_NAME, "dialog-title")
        user_title = dialog_title.find_element(By.CLASS_NAME, "user-title")
        name = user_title.find_element(By.CLASS_NAME, "peer-title").text
        dialog_title_details = dialog_title.find_element(By.CLASS_NAME, "dialog-title-details")
        tigo = dialog_title_details.find_element(By.CLASS_NAME, "message-status").get_attribute("innerHTML")
        if str(tigo) == "":
            is_message_me = False
        else:
            is_message_me = True
        subtitle = sub.find_element(By.CLASS_NAME, "user-last-message").text
        message_time = dialog_title_details.find_element(By.CLASS_NAME, "message-time")
        time = message_time.find_element(By.CLASS_NAME, "i18n").text
        try:
            bubble = sub.find_element(By.CLASS_NAME, "dialog-subtitle-badge")
            bubbletext = str(bubble.get_attribute('innerHTML'))
        except:
            read = True
        else:
            read = False
        return str(subtitle), str(chatid), str(name), is_message_me, str(time), read

    def get_message(self, message_id):
        message = self.driver.find_element(By.XPATH, '//div[@data-mid="'+str(message_id)+'"]')
        chatbox = message.find_elements(By.CLASS_NAME, "bubble-content-wrapper")
        day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
        namebox = day.find_element(By.CLASS_NAME, "name")
        name = namebox.find_element(By.CLASS_NAME, "peer-title").text
        try:
            map=day.find_element(By.CLASS_NAME, "message")
        except:
            return "Error in find_message"
        text = str(map.text)
        return str(text), str(name), str(message_id), map

    def messageIdtoMap(self, message_id):
        message = self.driver.find_element(By.XPATH, '//div[@data-mid="'+str(message_id)+'"]')
        chatbox = message.find_elements(By.CLASS_NAME, "bubble-content-wrapper")
        day = chatbox.find_element(By.CLASS_NAME, "bubble-content")
        try:
            map=day.find_element(By.CLASS_NAME, "message")
        except:
            return "Error in find_message"
        else:
            return map
        
    def add_contact(self, num, name):
        menu = self.driver.find_element(By.CSS_SELECTOR, "#new-menu")
        menu.click()
        newchannel = self.driver.find_element(By.CSS_SELECTOR, ".tgico-newprivate")
        newchannel.click()
        sleep(1)
        bo2 = self.driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(3) > div:nth-child(1)")
        bo2.click()
        num = str(num)
        if num[0:3] == "098":
            num = num[1:]
        elif num[0] == "0":
            num = "98" + num[1:]
        elif num[0] == "+":
            num = num.replace("+", "")
        elif num[0:2] == "98":
            pass
        else:
            return
        bo2 = self.driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(3) > div:nth-child(1)")
        try:
            bo2.click()
        except:
            pass
        te = self.driver.find_element(By.CSS_SELECTOR, "div.input-field:nth-child(3) > div:nth-child(1)")
        te.send_keys(Keys.CONTROL + 'a')
        te.send_keys(Keys.BACKSPACE)
        te.send_keys(num)
        te1 = self.driver.find_element(By.CSS_SELECTOR, ".name-fields > div:nth-child(1) > div:nth-child(1)")
        te1.send_keys(Keys.CONTROL + 'a')
        te1.send_keys(Keys.BACKSPACE)
        te1.send_keys(name)
        bo3 = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary:nth-child(3)")
        bo3.click()
        sleep(1)
        try:
            rr = self.driver.find_element(By.CSS_SELECTOR, ".toast")
        except:
            te3 = self.driver.find_element(By.CSS_SELECTOR, "#contacts-container > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)")
            te3.send_keys(Keys.CONTROL + 'a')
            te3.send_keys(Keys.BACKSPACE)
            sleep(1)
            te3.send_keys(name)
            sleep(1)
            for i in range(10):
                try:
                    rr = self.driver.find_element(By.CSS_SELECTOR, "#contacts > li:nth-child("+str(i)+")")
                except:
                    return
                else:
                    rrr = self.driver.find_element(By.CSS_SELECTOR, "#contacts > li:nth-child("+str(i)+") > div:nth-child(3) > p:nth-child(1) > span:nth-child(1) > span:nth-child(2)").text
                    if str(name) == str(rrr):      
                        chatid = rr.get_attribute("data-peer-id")
                        return str(chatid)
                    else:
                        continue
            
    def go_chat(self, id):
        self.driver.get("https://web.eitaa.com/#"+str(id))
        sleep(3)

    def load_all_contacts(self, x):
        n = 1
        chatids = []
        for i in range(int(x)):
            try:
                contact = self.driver.find_element(By.CSS_SELECTOR, "#contacts > li:nth-child("+str(n)+")")
            except:
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                continue
            chatid = contact.get_attribute("data-peer-id")
            chatids.append(str(chatid))
            n += 1
        return chatids

    def go_settings(self):
        t = self.driver.find_element(By.CSS_SELECTOR, "div.btn-icon:nth-child(2)")
        t.click()
        t2 = self.driver.find_element(By.CSS_SELECTOR, ".tgico-settings")
        t2.click()
        sleep(1)

    def go_edit_chat(self):
        try:
            tigo_edit = self.driver.find_element(By.CSS_SELECTOR, "button.tgico-edit")
            tigo_edit.click()
        except:
            return
        sleep(1)
        
    def edit_my_about(self, text):
        sleep(0.2)
        try:
            t3 = self.driver.find_element(By.CSS_SELECTOR, "button.tgico-edit:nth-child(3)")
            t3.click()
        except:
            return
        sleep(1)

    def go_sidebar_chat(self):
        tab_bar = self.driver.find_element(By.CSS_SELECTOR, ".content")
        tab_bar.click()
        sleep(1)

    def go_members(self):
        t = self.driver.find_element(By.CSS_SELECTOR, "div.sidebar-slider-item:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)")
        t.click()
        sleep(1)

    def get_members(self, id, map):
        n = 1
        members = []

        while True:
            try:
                t2 = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/div[2]/div/div/ul/li["+str(n)+"]")
            except:
                if map:
                    return members, map
                else:
                    return members
            chatid = t2.get_attribute("data-peer-id")
            if id:
                if id == chatid:
                    map = t2
            members.append(str(chatid))
            n += 1

    def get_admins(self, id=None):
        n = 1
        admins = []

        while True:
            try:
                t2 = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div[3]/div[2]/div[2]/div/div/ul/li["+str(n)+"]")
            except:
                if map:
                    return admins, map
                else:
                    return admins
            chatid = t2.get_attribute("data-peer-id")
            if id:
                if id == chatid:
                    map = t2
            admins.append(str(chatid))
            n += 1

    def add_member(self, target):
        t2 = self.driver.find_element(By.CSS_SELECTOR, "button.is-visible")
        t2.click()
        sleep(1)

        for i in target:
            t3 = self.driver.find_element(By.CSS_SELECTOR, ".selector-search-input")
            t3.send_keys(str(i))
            sleep(1)

            t4 = self.driver.find_element(By.CSS_SELECTOR, "div.chatlist-container:nth-child(3) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1)")
            t4.click()
            sleep(1)

        t5 = self.driver.find_element(By.CSS_SELECTOR, "button.btn-circle:nth-child(1)")
        t5.click()
        sleep(1)

        t6 = self.driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(1)")
        t6.click()

    def promote_member(self, map, n):
        map.click()
        try:
            t = self.driver.find_element(By.CSS_SELECTOR, ".tgico-promote").click()
        except:
            return
        sleep(1)

        for i in n:
            i += 3
            t2 = self.driver.find_element(By.CSS_SELECTOR, "label.row:nth-child("+str(i)+") > div:nth-child(3) > div:nth-child(2) > label:nth-child(1) > div:nth-child(2)")
            if i < 10:
                t2.click().click()
            elif i == 10:
                t2.click()
            else:
                return
        t3 = self.driver.find_element(By.CSS_SELECTOR, "div.sidebar-slider-item:nth-child(4) > div:nth-child(1) > button:nth-child(1)")
        t3.click()
        sleep(1)

    def delete_member(self, map):
        map.click()
        try:
            t = self.driver.find_element(By.CSS_SELECTOR, "div.tgico-delete:nth-child(3)").click()
        except:
            return

    def edit_admin_rights(self, map, n):
        map.click()
        try:
            t = self.driver.find_element(By.CSS_SELECTOR, "div.tgico-admin:nth-child(2)").click()
        except:
            return
        sleep(1)

        for i in n:
            i += 3
            t2 = self.driver.find_element(By.CSS_SELECTOR, "label.row:nth-child("+str(i)+") > div:nth-child(3) > div:nth-child(2) > label:nth-child(1) > div:nth-child(2)")
            if i < 10:
                t2.click().click()
            elif i == 10:
                t2.click()
            else:
                return
        t3 = self.driver.find_element(By.CSS_SELECTOR, "div.sidebar-slider-item:nth-child(4) > div:nth-child(1) > button:nth-child(1)")
        t3.click()
        sleep(1)

    def go_administrators(self):
        t = self.driver.find_element(By.CSS_SELECTOR, "div.sidebar-slider-item:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
        t.click()
        sleep(1)

    def delete_admin(self, map):
        map.click()
        try:
            t = self.driver.find_element(By.CSS_SELECTOR, "div.tgico-admin:nth-child(2)").click()
        except:
            return
        
        t2 = self.driver.find_element(By.CSS_SELECTOR, "button.tgico-deleteuser")
        t2.click()

    def info_tabs(self):
        self.go_settings()
        self.driver.find_element(By.CSS_SELECTOR, "button.profile-button:nth-child(2)")
        sleep(0.2)
        response = {}
        for i in range(2, 12):
            tab = self.driver.find_element(By.CSS_SELECTOR, "div.sidebar-left-section-container:nth-child(5) > div:nth-child(1) > div:nth-child(2) > div:nth-child("+str(i)+")")
            subtitle = tab.find_element(By.CLASS_NAME, "row-subtitle").text
            title = tab.find_element(By.CLASS_NAME, "row-title").text
            data = {
                str(title):{
                    "subtitle":str(subtitle)
                }
            }
            data.update(data)
        return response
    
    def Reset_to_Defaults_Tabs(self):
        self.go_settings()
        self.driver.find_element(By.CSS_SELECTOR, "button.profile-button:nth-child(2)")
        sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-color-primary:nth-child(4)")

def cleanup():
    CoUninitialize()


threading.Thread(target=cleanup).start()
