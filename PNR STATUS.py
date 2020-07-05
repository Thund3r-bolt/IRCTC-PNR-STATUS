from selenium import webdriver
from PIL import Image
import pytesseract
import io
import numpy as np
import cv2
import time
import tkinter   
from tkinter import ttk

window = tkinter.Tk()
name = tkinter.StringVar()
def click():
    global inputpnrnumber
    inputpnrnumber = str(name.get()) 
    if (inputpnrnumber.isnumeric()) and ( len(inputpnrnumber) == 10 ) :
        window.destroy()
def GUI() :
    window.title("PNR STATUS")
    lbl = ttk.Label(window, text = "                         ").grid(column = 0, row = 0) 
    lbl = ttk.Label(window, text = "    Enter PNR Number:    ").grid(column = 0, row = 1)
    nameEntered = ttk.Entry(window, width = 12, textvariable = name).grid(column = 1, row = 1)
    lbl = ttk.Label(window, text = "            ").grid(column = 2, row = 1)
    lbl = ttk.Label(window, text = "                        ").grid(column = 1, row = 2) 
    button = ttk.Button(window, text = "Submit", command = click).grid(column = 1, row = 3)
    lbl = ttk.Label(window, text = "                         ").grid(column = 1, row = 4) 
    window.mainloop() 
url="http://www.indianrail.gov.in/enquiry/PNR/PnrEnquiry.html?locale=en"
GUI()
browser = webdriver.Firefox(executable_path= r"C:\Users\Thunder-bolt\Documents\Web scraper\PNR_STATUS\geckodriver.exe")     #paste the location of geckodriver here
browser.get(url)
pnrnumber = browser.find_element_by_id('inputPnrNo')
pnrnumber.send_keys(inputpnrnumber)
close = browser.find_element_by_id('corover-close-btn')
close.click()
submitbutton = browser.find_element_by_id('modal1')
submitbutton.click()
captchascreenshot = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[3]/div/div/div/div[2]/div[2]/div/div[2]")
time.sleep(2)  
screenshotimagebinary = captchascreenshot.screenshot_as_png
img_array = np.array(bytearray(screenshotimagebinary), dtype=np.uint8)
img = cv2.imdecode(img_array, 0)
(thresh, blackAndWhiteImage) = cv2.threshold(img, 120,255, cv2.THRESH_BINARY)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'   # paste the location of tesseract ocr here Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
problem = pytesseract.image_to_string(blackAndWhiteImage) 
problem = problem.replace('=', ' ')
problem = problem.replace('?', ' ')
add = problem.find('+')
subract = problem.find('-')
if add != -1 :
    k=1
    problem = problem.replace('+', ' ')
if subract != -1 :
    k=2
    problem = problem.replace('-', ' ')
j = 0
while j < len(problem):
    q = problem[j]
    if not(q.isdigit()):
        problem = problem.replace(problem[j], ' ')
    j+=1
    
i = problem.split(" ", 1)
print(problem)
num1=int(i[0])
num2=int(i[1])
if k == 1 :
    sol=num1+num2
if k == 2 :
    sol=num1-num2
print(str(sol))
ans = browser.find_element_by_id('inputCaptcha')
ans.send_keys(str(sol))
time.sleep(1)  
submitbutton1 = browser.find_element_by_id('submitPnrNo')
submitbutton1.click()
time.sleep(3)

screenshot = browser.find_element_by_xpath("//html/body/div[2]/div[2]/div[2]")
screenshotimagebin = screenshot.screenshot_as_png
imgarray = np.array(bytearray(screenshotimagebin), dtype=np.uint8)
img1 = cv2.imdecode(imgarray, cv2.IMREAD_COLOR)
cv2.imshow("PNR STATUS",img1)
cv2.imwrite("PNRSTATUS.png", img1)











