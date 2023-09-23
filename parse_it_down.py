import requests
import re

def failover_criteria(response):
    print('Proxy authentication required')
    return response.status_code == requests.codes.proxy_authentication_required

# regex
base_re = re.compile(r'<div class="tc_content">\n<h5>((.|\n)*?)</div>')
link_name_re = re.compile(r'<a href="(.*?)</a>')
author_re = re.compile(r'<p>(.*?)</p>')

def page_load(url = None,start_page=0, end_page=0):       
    if url:
        with open("parsed.txt", "w") as f:
            f.write("page | name | author | link")
        
        for page in range(start_page,end_page+1):
            try:
                r = session.get(url+str(page))
                
            except BaseException as e:
                print(f'Due sending get request to {url+str(page)} an unexpected \
exception has been appeared:'+str(e))

            else:
                page_parser(r.text, page)
                
        return print('Parsing has been ended')

        
def page_parser(string, page):
    while True:
        content = re.search(base_re, string)
        
        if not content:
            return print(f'end of the page: {page}')
            
        string = string[:content.start()] + string[content.end():]
        content = content.groups()[0]
        link, name = link_name_re.search(content).groups()[0].split('">')
        author = author_re.search(content).groups()[0]
        line = f'\n{page} | {name} | {author} | {link}'
        with open("parsed.txt", "a", encoding="utf-8") as f:
            f.write(line)
    
if __name__=='__main__':
    ###
    start_page = 1
    end_page = 5
    ### You have to specify url with the page number excluded otherwise parser will run wrong ###
    url = 'https://vdoc.pub/explore/computers/'
    try:
        from pypac import PACSession, get_pac
        from pypac.parser import PACFile
        with open('proxy-ssl.js') as f:
            pac = PACaFile(f.read())
            
        session = PACSession(pac=pac, response_proxy_fail_filter=failover_criteria)
    except ModuleNotFoundError:
        print('Pypac module does not installed.')
        session = requests.Session()
        
    except FileNotFoundError:
        print('Specified PAC file does not located.')
        session = requests.Session()
        
    finally:
        page_load(url,start_page, end_page)
        
