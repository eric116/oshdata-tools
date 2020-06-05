import csv
from datetime import date
from urllib import request
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
    "Description", "Version", "Hardware License", "Software License", "Documentation License", "Documentation Link"])

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
    project_fields.append(project_page_soup.find('a', class_='documentation-link')['href']) #Documentation Link

    project_data.append(project_fields)
    print(project_fields[2] + " added")

with open('oshwa_scrape_' + str(date.today()) + '.csv', 'w') as f:
    writer = csv.writer(f)
    for row in project_data:
        writer.writerow(row)