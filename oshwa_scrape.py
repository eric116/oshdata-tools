import argparse #for debugging
import csv
from datetime import date
from urllib import request
from urllib.error import HTTPError, URLError
import ssl
import socket
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser(description='Create CSV of OSHWA Certified projects.')
parser.add_argument('--debug', action='store_true', help='enable debugging of the documentation status check') #debugging switch
parser.add_argument('--doccheck', action='store_true', help='return HTTP status codes for documentation links') #documentation check switch
args = parser.parse_args()
global debug_enable
if args.debug:
    print ('Debugging Enabled')
    debug_enable = True
else:
    print ('Debugging Disabled')
    debug_enable = False

oshwa_domain = 'https://certification.oshwa.org'

project_list_page = request.urlopen(oshwa_domain + '/list.html')
project_list_soup = bs(project_list_page, "html.parser")
project_list = project_list_soup.find_all('tr', class_="project")

project_page_urls = []

for project in project_list:
    project_page_urls.append(oshwa_domain + project.a['href'])

project_data = []
project_data.append([
    "UID", "Certification Date", "Project Name", "Website", "Creator", "Country", "Project Types",
    "Description", "Version", "Hardware License", "Software License", "Documentation License", "Documentation Link", "Documentation Status"])

def sanitizeURL(doc_url): #Define how to clean up doc_url so request.urlopen doesn't complain
    #global doc_url
    if '://' not in doc_url:
        doc_url="http://"+doc_url
        if debug_enable is True:
            print ('Scheme added')
        else:
            pass
    else:
        if debug_enable is True:
            print ('Scheme exists')
        else:
            pass
    if ' ' in doc_url:
        doc_url = doc_url.replace(" ", "%20")
        if debug_enable is True:
            print ('Spaces replaced: New URL is ' + doc_url)
        else:
            pass
    else:
        if debug_enable is True:
            print ('No spaces to replace')
        else:
            pass
    return (doc_url)

def getResponseCode(doc_url): #Define how to probe the URL and handle errors
    sani_doc_url = sanitizeURL(doc_url)
    if debug_enable is True:
        print ('Probing ' + sani_doc_url)
    else:
        pass
    try:
        conn = request.urlopen(sani_doc_url, timeout=5, context=ssl._create_unverified_context())
        return conn.getcode()
    except HTTPError as e1:
        return e1.code
    except URLError as e2:
        return e2.reason
    except ssl.SSLError as e3:
        return e3.reason
    except socket.timeout as e4:
        return 'Timed Out'

for url in project_page_urls:
    project_fields = []
    project_page = request.urlopen(url)
    project_page_soup = bs(project_page, "html.parser").find('section', class_='page-section')
    project_fields.append(project_page_soup.find('span', class_="id").text) #UID
    project_fields.append(project_page_soup.find('h3', text="Certification Date").next_sibling.text) #Certification Date
    project_fields.append(project_page_soup.h1.text) #Project Name
    if debug_enable is True:
        print ('Adding ' + project_fields[2] + '...')
    else:
        pass
    project_fields.append(project_page_soup.find('a', text="Project Website")['href']) #Website
    project_fields.append(project_page_soup.h2.contents[0]) #Creator
    project_fields.append(project_page_soup('h3', text="Country")[0].next_sibling.text) #Country

    project_types = ''
    for type in project_page_soup('div', class_='project__type'):
        project_types += type.text + ', '
    project_fields.append(project_types[:len(project_types)-2]) #Project Types

    project_fields.append(project_page_soup('div', class_="row")[1]('div', class_='column')[1].text) #Description
    project_fields.append(project_page_soup.find('span', class_='version').text) #Version
    project_fields.append(project_page_soup.find('h6', text='Hardware').next_sibling.text) #Hardware License
    project_fields.append(project_page_soup.find('h6', text='Software').next_sibling.text) #Software License
    project_fields.append(project_page_soup.find('h6', text='Documentation').next_sibling.text) #Documentation License
    doc_url = project_page_soup.find('a', class_='documentation-link')['href']
    project_fields.append(doc_url) #Documentation Link

    if args.doccheck:
        project_fields.append(getResponseCode(doc_url)) #Documentation Status
    else:
        project_fields.append('Not Checked') 

    project_data.append(project_fields)
    if debug_enable is True:
        print(project_fields[2] + " added" + " | Doc Status = " + str(project_fields[13]))
    else:
        print(project_fields[2] + " added")


with open('oshwa_scrape_' + str(date.today()) + '.csv', 'w') as f:
    writer = csv.writer(f)
    for row in project_data:
        writer.writerow(row)
