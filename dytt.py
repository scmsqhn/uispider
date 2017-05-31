#coding:utf-8
#encoding:utf-8
#获取电影天堂全站电影资源的迅雷下载地址
#获取的迅雷地址，暂时无法解码成base64 -d
#使用迅雷批量下载
import base64
import os
from subprocess import call
from selenium import webdriver  
import urllib
import re
import sys
import subprocess
import chardet


DEBUG=True
FABU=False

base_url=('http://www.runoob.com')
index_url=('http://www.dytt8.net/index.htm')
#base_url=r'http://www.dytt8.net/html/gndy/dyzz/20170305/53401.html'
  
def get_driver(url):
    print('get_driver')
    driver = webdriver.PhantomJS()
    print('webdriver')
    driver.get(url)
    print('get_url')
    return driver


def search_html(driver, html):
   # fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')
    fhtml=open(r'./html_txt.txt', 'a+')
    print('search_html') 
    restrs = ('href="(.*?)">')
    resurl = ('href="(.*?).html"')
    html = str(html)
    lines = html.split('</a>')
    for line in lines:
            fhtml.writelines(line+'\n')
            #print(line+'\n')
#        try:
            results = re.search(restrs, line.strip())
            if results is None:
                continue
            for result in results.groups():
                if ('tutorial' in result and 'www' in result):
                    result = "http://"+result[2:]
                    print("result= %s" % result)
                    outmsg = subprocess.getoutput("wget -i %s"% result)
                    print("wget==>%s" % result)
                    driver = get_driver(result)
                    html2 = driver.page_source
                    html2 = str(html2)
                    lines2 = html2.split('</a>')
                    for line in lines2:
                        results = re.search(resurl, line.strip())
                        if results is None:
                            continue
                        for result in results.groups():
                            result = base_url+result+".html"
                            print("======2 level======")
                            print(result)
                            outmsg = subprocess.getoutput("wget -i %s"% result)
                            print("wget==>%s" % result)
                            driver = get_driver(result)
                            html3 = driver.page_source
                            html3 = str(html3)
                            lines3 = html3.split('</a>')
                            for line in lines3:
                                results = re.search(resurl, line.strip())
                                if results is None:
                                    continue
                                for result in results.groups():
                                    print("======3 level======")
                                    result = base_url+result+".html"
                                    outmsg = subprocess.getoutput("wget -i %s"% result)
                                    print("wget==>%s" % result)
    fhtml.close()
                #print (chardet.detect(result.encode(encoding='utf-8')))
                #urls = re.search(resurl, result.strip())
                #if urls is None:
                #    continue
                #for url in urls.groups():
                #     print(url)
                #     url = '/html%shtml\n' % url
                #     if repeatcheck(url, fout):
                #         fout.write(url)
                #         prepare_data(base_url+url)
#        except:
#            pass
#        try:
#            driver.close()
#        except:
#            pass

def repeatcheck(url, file):
    file.seek(0)
    #print url 
    #print file
    lines=file.readlines()
    for line in lines:
        #print line 
        #print url 
        if url.strip()==line.strip():
            #print 'REPEAT'
            return False
    print ('UNREPEAT')
    print (url) 
    return True 


def prepare_data(url):
#    fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')
    print('main') 
    driver = get_driver(url)
 #   time.sleep(10)
    html = driver.page_source
    search_html(driver, html)
    driver.quit()
 #   fout.flush()
  #  fout.close()

def download_data():
    xpath = ('//*[@id="Zoom"]/span/table/tbody/tr/td/a')
    print('download_data') 
    fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'r')
    fsave=open(r'/scrapyredis/selephan/dytt_mv_url_save.txt', 'a+')
    print('open data') 
    lines = fout.readlines()
    print(lines) 
    for line in lines:
        url = base_url+line
        if 'index' in url:
            continue
        driver = get_driver(url)
        elements = driver.find_elements_by_xpath(xpath)
        if elements is not None:
            for element in elements:
                try:
                    strsele = str(element)
                    print ('call[]')
                    thunder = element.get_attribute('wmwalovz')
                    href    = element.get_attribute('href')
#                    call("echo | %s | base64 -d | echo" % thunder, shell=True)
#                    call("echo | %s | base64 -d | echo" % href, shell=True)
                    text = element.text
                    print ('text=%s' % text)
                    print ('thunder=%s' % thunder)
                    print ('href=%s' % href)
                except:
                    print ('except: ')
                    pass
    fout.close()
    fsave.close()

def download_data_2():
    print('download_data') 
    fout=open(r'/scrapyredis/selephan/temp_url.txt', 'r')
    fsave=open(r'/scrapyredis/selephan/temp_thunder.txt', 'a+')
    print('open data') 
    lines = fout.readlines()
    print(lines) 
    pat=('thunder://(.*?)">')
    for line in lines:
       try:
          url = base_url+line
          if 'index' in url:
              continue
          print ('downurl='+url)
          driver = get_driver(url)
          html = driver.page_source
          driver.quit()
          lines = html.split('\n')
          for line in lines:
              #print ('line='+line)
              urls = re.search(pat, line, flags=0)
              if urls is not None:
                  try:
                      for url in urls.groups():
                          fsave.write('thunder://'+url+'\n')
                          print ('thunder://'+url+'\n')
                  except:
                      print('except 9')
                      pass
       except:
          print('except key')
          pass
    fout.close()
    fsave.close()
    
def get_all_html_addr():   
    global fout
    fout=open(r'./html_url.txt', 'a+')
    prepare_data(base_url)
#    download_data_2()
    fout.flush()
    fout.close()

def get_all_thunder_addr():   
    prepare_data(base_url)
    download_data_2()

def get_all_rar_cont():
    print('get_all_rar_cont')
    fsave=open(r'/scrapyredis/selephan/dytt_mv_url_save.txt', 'r')
    lines=fsave.readlines()
    for line in lines:
        line = line[10:-1]
        b64c = base64.b64decode(line)
        b64c = b64c[2:-2]
        print (b64c)
        b64c = commands.getoutput(r'axel %s' % b64c)
        print (b64c)

if __name__=="__main__":
#get the www.runoob.com all course
    get_all_html_addr()
#    get_all_rar_cont()
#    try:
#        get_all_html_addr()
#        download_data_2()
#    except: 
#        print ('except')
#        pass

