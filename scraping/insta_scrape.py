from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pickle as pkl
import urllib.request
from tqdm import tqdm
import time

urlfile = 'best3_urls'
dest_folder = 'best3'



binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
#driver = webdriver.Firefox(firefox_binary=binary)
driver = webdriver.PhantomJS()

urls = pkl.load(open(urlfile+'.pkl','rb'))

i=0
for u in tqdm(urls):
    driver.get(u)
    #time.sleep(1)
    #urls = driver.find_element_by_partial_link_text('https:')
    #images = driver.find_elements_by_tag_name('img')
    #print(u)
    a = 0
    while a == 0:
        try:
            imgList = driver.find_element_by_class_name("FFVAD")
            a = 1
        except:
            continue
    img_link = None
    while img_link == None:
        img_link = imgList.get_attribute('src')

    #print(img_link)
    urllib.request.urlretrieve(img_link, 'data/playlists/'+dest_folder+'/pic'+str(i)+'.jpg')
    i+=1