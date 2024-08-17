from selenium import webdriver
from selenium.webdriver.common.by import By
from time import *

driver = webdriver.Firefox()
driver.get("https://deepai.org/chat")

def send_message_to_bot(text):

    textarea = driver.find_elements(By.CLASS_NAME, "chatbox")[-1]
    textarea.send_keys(text)

    sleep(0.5)
    SubmitButton = driver.find_element(By.CSS_SELECTOR, "#chatSubmitButton")
    try:
        SubmitButton.click()
    except:
        while True:
            try:
                SubmitButton.click()
            except:
                driver.execute_script("window.scrollTo(0, window.scrollY + 10)")
                continue
            else:
                break

    while True:
        if str(SubmitButton.text) == "Go":
            sleep(1)
            outputbox = driver.find_elements(By.CLASS_NAME, "outputBox")[-1]
            sleep(int(len(text)/3))
            t = outputbox.find_element(By.CLASS_NAME, "markdownContainer")
            result = t.find_element(By.CLASS_NAME, "markdownContainer").text
            return str(result)
        