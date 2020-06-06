import csv
from datetime import date
from urllib import request
from urllib.error import HTTPError, URLError
import ssl
from bs4 import BeautifulSoup as bs

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

for url in project_page_urls:
    project_fields = []
    project_page = request.urlopen(url)
    project_page_soup = bs(project_page, "html.parser").find('section', class_='page-section')
    project_fields.append(project_page_soup.find('span', class_="id").text) #UID
    project_fields.append(project_page_soup.find('h3', text="Certification Date").next_sibling.text) #Certification Date
    project_fields.append(project_page_soup.h1.text) #Project Name
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
    
    def sanitizeURL(doc_url):
        #global doc_url
        if '://' not in doc_url:
            doc_url="http://"+doc_url
            print ('Scheme added')
        else:
            print ('Scheme exists')
        if ' ' in doc_url:
            doc_url = doc_url.replace(" ", "%20")
            print ('Spaces replaced: New URL is ' + doc_url)
        else:
            print ('No spaces to replace')
        return (doc_url)
    
    def getResponseCode(doc_url):
        mod_doc_url = sanitizeURL(doc_url)
        print ('Probing ' + mod_doc_url)
        try:
            conn = request.urlopen(mod_doc_url, context=ssl._create_unverified_context())
            return conn.getcode()
        except HTTPError as e1:
            return e1.code
        except URLError as e2:
            return e2.reason
        except ssl.SSLError as e3:
            return e3.reason

    project_fields.append(getResponseCode(doc_url)) #Documentation Status

    project_data.append(project_fields)
    print(project_fields[2] + " added" + " | Doc Status = " + str(project_fields[13]))

with open('oshwa_scrape_' + str(date.today()) + '.csv', 'w') as f:
    writer = csv.writer(f)
    for row in project_data:
        writer.writerow(row)
