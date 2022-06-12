from selenium import webdriver
from PIL import Image
import pytesseract
import sys, os
driver = webdriver.Firefox()
url = "http://wss.mahadiscom.in/wss/wss?uiActionName=getViewPayBill"


driver.get(url)

driver.maximize_window()
if len(sys.argv) > 1:
    consumer_no = sys.argv[1]
else:
    raise Exception("Consumer No. is missing: Usage: python3 main.py <consumer_no>")

# driver.find_element_by_id("consumerNo").send_keys(consumer_no)
driver.find_element(value="consumerNo").send_keys(consumer_no)
captcha_image = driver.find_element(value="captcha")
captcha_image.screenshot("_temp.png")

get_captcha = pytesseract.image_to_string(Image.open("_temp.png")).strip()
get_captcha = (lambda x: "".join(i for i in x if i.isdigit()))(get_captcha)
print("Captcha:", get_captcha)
os.remove("_temp.png")


driver.find_element(value="txtInput").send_keys(get_captcha)
driver.find_element(value="lblSubmit").click()
driver.find_element(value="Img1").click()
driver.find_element(value="lbllTitle").click()

driver.close()
driver.switch_to.window(driver.window_handles[0])
import time
while driver.execute_script('return document.readyState;') != "complete":
    time.sleep(0.1)

driver.execute_script("window.print();")
driver.quit()