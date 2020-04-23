from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pickle as pkl
import urllib.request
from tqdm import tqdm
import time

urlfile = 'best2_urls'
dest_folder = 'best2_highres'


def get_img_url(driver, u):
    driver.get(u)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    title = html[html.find("<title>"):html.find("</title>")]

    # the beautiful line:
    return "https://"+html.split("display_url")[1].split(r'","display_resources')[0].split('https://')[1].replace('\\u0026', '&'), title



binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
#driver = webdriver.Firefox(firefox_binary=binary)
driver = webdriver.PhantomJS(r'C:\Users\Richard\Documents\Extracted\phantomjs-2.1.1-windows\bin\\phantomjs.exe')

urls = pkl.load(open(urlfile+'.pkl','rb'))

i=0

title_dict = {}

for u in tqdm(urls):
    driver.get(u)
    time.sleep(1)
    #urls = driver.find_element_by_partial_link_text('https:')
    #images = driver.find_elements_by_tag_name('img')
    #print(u)

    #OLD:

    # a = 0
    # while a == 0:
    #     try:
    #         imgList = driver.find_element_by_class_name("FFVAD")
    #         a = 1
    #     except:
    #         continue
    # img_link = None
    # while img_link == None:
    #     img_link = imgList.get_attribute('src')

    try:
        img_link, title = get_img_url(driver,u)

        title_dict['pic'+str(i)] = title

        urllib.request.urlretrieve(img_link, '../data/playlists/'+dest_folder+'/pic'+str(i)+'.jpg')
        i += 1
    except:
        pass

pkl.dump(title_dict,open('../data/playlists/'+dest_folder+'title_dict','wb'))

#html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

#the beautiful line:

#html.split("display_url")[1].split(r'","display_resources')[0].split('https://')[1].replace('\\u0026','&')