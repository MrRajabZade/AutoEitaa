# Eitaabot
Eitaabot toolkit for making bot in Eitaa

## Features
- [x] Send Message
- [x] Send File
- [x] Reply Message
- [x] Edit Message
- [x] Forward Message
- [x] Pin Message
- [x] delete Message
- [x] Search
- [x] On Message
- [x] Create Channel
- [x] delete Member 
- [x] Folders Tabs 
- [x] Get Phone
- [x] Get Eitaa_ID
- [x] Get info
- [x] Get info Me             

## Basic
```py
from main import *

driver = start(namebrowser="Firefox")
wet = start_wet(namebrowser="Firefox")
```
## Send Message
Example :
```py
text = "salam"
send_Message(driver, text)
```
**Note**: You need to be in the chat to send a message
## Send File
Example :
```py
filepath = [r"C:\Users\hp\Documents\Eitaabot\img.png", r"C:\Users\hp\Documents\Eitaabot\img.jpg"]
caption = "salam"
send_file(driver, filepath, caption
```
**Note**: 
- You need to be in the chat to send a message

- To send a gif, send the desired file with the .gif extension.

- To send a sticker, you must send the desired file with the .webp extension
## Reply Message
Example :
```py
Message = "<selenium.webdriver.remote.webelement.WebElement (session="d79fe6d7-1db5-45de-a9d1-4df4881dc92b", element="bb9c6560-411c-444a-acbf-2bb311b8823e")>"
text = "salam"
reply_Message(driver, text, Message)
```
**Note**: You need to be in the chat to send a message

```

