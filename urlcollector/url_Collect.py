from selenium import webdriver 
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxOptions
from urllib.parse import urlparse
from datetime import datetime
from pydantic import BaseModel

import time
import re



class UrlsModel(BaseModel):
    urls: list[str]=[]
    len: int
    # internal_urls: list[str] = []
    # advertisement_urls: list[str] = []
    # cdn_urls: list[str] = []
    # external_urls: list[str] = []

class UrlExtractor():

    COMMAND='http://172.19.0.1:4444/wd/hub'
    
    def __init__(self,url) -> None:
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.result = UrlsModel
        self.result.urls=[]
        self.driver = webdriver.Remote(command_executor=self.COMMAND,options=opts)
        start_process = datetime.now()
        self.driver.get(url=url)
        
        process_duration = datetime.now() - start_process
        print(f"{process_duration=}")


        
    def get_all_urls(self):
        js_href = 'return [...document.querySelectorAll("[href]")].map(e=>e.href)'
        js_src = 'return [...document.querySelectorAll("[src]")].map(e=>e.src)'
        js_background = 'return [...document.querySelectorAll("[background]")].map(e=>e.background)'
        js_action = 'return [...document.querySelectorAll("[action]")].map(e=>e.action)'
        js_cite = 'return [...document.querySelectorAll("[cite]")].map(e=>e.cite)'
        js_classid = 'return [...document.querySelectorAll("[classid]")].map(e=>e.classid)'
        js_codebase = 'return [...document.querySelectorAll("[codebase]")].map(e=>e.codebase)'
        js_data = 'return [...document.querySelectorAll("[data]")].map(e=>e.data)'
        js_longdesc = 'return [...document.querySelectorAll("[longdesc]")].map(e=>e.longdesc)'
        js_profile = 'return [...document.querySelectorAll("[profile]")].map(e=>e.profile)'
        js_usemap = 'return [...document.querySelectorAll("[usemap]")].map(e=>e.usemap)'
        js_formaction = 'return [...document.querySelectorAll("[formaction]")].map(e=>e.formaction)'
        js_icon = 'return [...document.querySelectorAll("[icon]")].map(e=>e.icon)'
        js_manifest = 'return [...document.querySelectorAll("[manifest]")].map(e=>e.manifest)'
        js_poster = 'return [...document.querySelectorAll("[poster]")].map(e=>e.poster)'
        js_srcset = 'return [...document.querySelectorAll("[srcset]")].map(e=>e.srcset)'
        js_archive = 'return [...document.querySelectorAll("[archive]")].map(e=>e.archive)'
        js_xmlns = 'return [...document.querySelectorAll("[xmlns]")].map(e=>e.xmlns)'
        js_imagesrcset = 'return [...document.querySelectorAll("[imagesrcset]")].map(e=>e.imagesrcset)'
        jses=[js_href,js_src,js_background,js_action,js_cite,js_classid,js_codebase,js_data,js_classid,js_longdesc,js_profile,js_usemap,js_formaction,js_icon,
           js_manifest,js_poster,js_srcset,js_archive,js_xmlns,js_imagesrcset]
        # wait until ...
        time.sleep(2)
        for js in jses:
            print(js)
            link_lists = self.driver.execute_script(js)
            print(link_lists)
            self.result.urls.extend(list(link_lists))
        self.result.len=len(self.result.urls)


    def check_is_redirect_link(self,url):
        driver=self.driver
        driver.switch_to.new_window(type_hint='tab')
        print("start")
        driver.get(url)
        tab=driver.window_handles
        
        a=False
        print("here")
        
        if(driver.current_url.split('/')[2] == url.split('/')[2]):
            a= True
        # print("after if")
        driver.close()
        driver.switch_to.window(window_name=tab[0])
        # print("done")
        return a

    def check_class_name(self,element,n):
        class_name=element.get_attribute("class")
        parent = element.find_element(By.XPATH,"..")
        
        if(parent == None):
            return False
        
        # print("tag name: ",element.tag_name)
        # print("class name: ",class_name)
        # print("parent: ",parent)
        # print("n:  ", n)
        if element.tag_name == "body":
            return False
        # erro ecure when get root element
        if(n>4):
            return False
        if re.search(".*.gif$|^ad*|^ads$|advertise|yn|bnr|banner|yektanet|redirect|GoogleActiveViewElement", str(class_name)):
            return True
        else:
            return self.check_class_name(parent,n+1)



    def check_image_tag(self,element):
        children= element.find_elements(By.XPATH,"*")
        # print("children: ",children)
        if(children == None):
            return 0
        for child in children:
            # print("child: ",child)
            if child.tag_name =="img" or child.tag_name =="iframe" :
                if re.search("cdn|CDN",str(child.get_attribute('src'))):
                    return 2
                if re.search(".*.gif$|ad|yn|bnr|banner|yektanet|redirect|GoogleActiveViewElement", str(child.get_attribute('src'))) :
                    return 1
            else:
                return self.check_image_tag(child)    
        return 0


    def check_href(self,href):
        if "click" in href or "banner" in href or "redirect/ad" in href :
            return True
        return False

    def get_urls_and_extract(self):
    
        driver=self.driver        
        # print('hello')
        # time.sleep(3)
        aTags = driver.find_elements(By.TAG_NAME,"a")
        

        for element in aTags:
            
            try:
                # print("element: ",element)
                href = element.get_attribute("href")
                link=urlparse(href)
                url=urlparse(self.url_address)
                print("link: ",link)
                print("url: ",url)
                # print("herf: ",href)
                
                # if re.search("cdn|CDN",str(href)):
                #     self.cdn_urls.append(href)


                if link.netloc in url.netloc or "#" in href:
                    # print("first: ",href)
                    self.internal_urls.append(href)
                else:
                    if self.check_href(href):
                        self.internal_urls.append(href)
                    check = self.check_image_tag(element)
                    if check==2 :
                        # print("2:  ",href)
                        self.cdn_urls.append(href)
                    if check >0 or self.check_class_name(element,0):
                        # print(">0:  ", href)
                        self.advertisement_urls.append(href)
                    elif self.url_address.replace("https://www.","") in href:
                    #     if(self.check_is_redirect_link(href)):
                    #         print("iner href",href)
                        self.internal_urls.append(href)
                    #     else:
                    #         print("adver link",href)
                    #         self.advertisement_urls.append(href)
                    else: 
                        # print("ext: ",href)
                        self.external_urls.append(href)
            except exceptions.StaleElementReferenceException:
                print("Error: ",exceptions.StaleElementReferenceException)
            except Exception as e:
                print("Error: ",e)

            
                
        driver.close()
        

# if __name__ == '__main__':
#         a=UrlExtractor(url="https://www.varzesh3.com/")
#         print("hello")
#         a.get_all_urls()
#         a.show_urls()
