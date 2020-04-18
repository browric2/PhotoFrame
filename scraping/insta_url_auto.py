import pyautogui
import pyperclip
import pickle as pkl

pyautogui.PAUSE=0.6

final_url ='https://instagram.com/p/B0YFNs0n7WS/'
urlfile = 'scraping/best3_urls'



def loc_click(tag):
    b = pyautogui.locateOnScreen(tag+'.png')
    clickpos = (b.left + int((b.width)/2),b.top + int(b.height/2))
    pyautogui.click(clickpos)

def one_img():
    loc_click('options')
    loc_click('copylink')
    urls.append(pyperclip.paste())
    loc_click('backbut')
    return pyperclip.paste()


urls = []


# one_img()
# pyautogui.moveRel(yOffset=100)
# pyautogui.scroll(-195)




# for m in range(20):
#     for i in range(100):
#         print(i)
#         #pyautogui.moveRel(yOffset=100)
#         if i % 2 == 0:
#             pyautogui.scroll(-194)
#         else:
#             pyautogui.scroll(-195)
#     pyautogui.scroll(-32)
box = pyautogui.locateOnScreen('backbut.png')
pyautogui.moveTo(box.left+(box.width/2),box.top+(box.height/2))
pyautogui.moveRel(yOffset=100)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=100)
pyautogui.moveRel(xOffset=300)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=100)
pyautogui.moveRel(xOffset=600)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=400)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=400)
pyautogui.moveRel(xOffset=300)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=400)
pyautogui.moveRel(xOffset=600)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=800)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=800)
pyautogui.moveRel(xOffset=300)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=800)
pyautogui.moveRel(xOffset=600)
pyautogui.click()
one_img()
pyautogui.moveRel(yOffset=800)
pyautogui.scroll(-195)

#first two rows:


u=0
while u != final_url:
    for m in range(20):
        if u!= final_url:
            for i in range(100):
                if u != final_url:
                    for shift in [0,300,600]:
                        if u != final_url:
                            pyautogui.moveRel(xOffset=shift)
                            pyautogui.click()
                            print(i)
                            u = one_img()
                            print(u)
                            pyautogui.moveRel(yOffset=800)
                    if i % 2 == 0:
                        pyautogui.scroll(-194)
                    else:
                        pyautogui.scroll(-195)
            pyautogui.scroll(-32)

pkl.dump(urls,open(urlfile+'.pkl','wb'))


#for i in range(100):
