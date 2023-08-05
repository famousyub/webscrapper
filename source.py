from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

# Creating a webdriver instance
driver = webdriver.Chrome()
# This instance will be used to log into LinkedIn

# Opening linkedIn's login page
#driver.get("https://linkedin.com/uas/login")
driver.get("https://www.linkedin.com")
# waiting for the page to load
time.sleep(5)

# entering username
username = driver.find_element  ( By.ID, "username")

# In case of an error, try changing the element
# tag used here.

# Enter Your Email Address
username.send_keys("email")

# entering password
pword = driver.find_element( By.ID,"password")
# In case of an error, try changing the element
# tag used here.

# Enter Your Password
pword.send_keys("password")		

# Clicking on the log in button
# Format (syntax) of writing XPath -->
# //tagname[@attribute='value']
driver.find_element(By.XPATH,"//button[@type='submit']").click()
# In case of an error, try changing the
# XPath used here.
start = time.time()

# will be used in the while loop
initialScroll = 0
finalScroll = 1000

while True:
	driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
	# this command scrolls the window starting from
	# the pixel value stored in the initialScroll
	# variable to the pixel value stored at the
	# finalScroll variable
	initialScroll = finalScroll
	finalScroll += 1000

	# we will stop the script for 3 seconds so that
	# the data can load
	time.sleep(3)
	# You can change it as per your needs and internet speed

	end = time.time()

	# We will scroll for 20 seconds.
	# You can change it as per your needs and internet speed
	if round(end - start) > 20:
		break

src = driver.page_source

# Now using beautiful soup
soup = BeautifulSoup(src, 'lxml')
# Extracting the HTML of the complete introduction box
# that contains the name, company name, and the location
intro = soup.find('div', {'class': 'scaffold-layout'})
    #scaffold-layout--breakpoint-md
    #scaffold-layout--sidebar-main-aside
    
    #scaffold-layout--reflow
    
   # '})

print(intro)
# In case of an error, try changing the tags used here.

name_loc = intro.find("h1")

# Extracting the Name
name = name_loc.get_text().strip()
# strip() is used to remove any extra blank spaces

works_at_loc = intro.find("div", {'class': 'scaffold-layout__row scaffold-layout__content'})

# this gives us the HTML of the tag in which the Company Name is present
# Extracting the Company Name
works_at = works_at_loc.get_text().strip()


location_loc = intro.find_all("span", {'class': 'text-body-small'})

# Ectracting the Location
# The 2nd element in the location_loc variable has the location
location = location_loc[1].get_text().strip()

print("Name -->", name,
	"\nWorks At -->", works_at,
	"\nLocation -->", location)
# Getting the HTML of the Experience section in the profile
experience = soup.find("section", {"id": "experience-section"}).find('ul')

print(experience)
# In case of an error, try changing the tags used here.

li_tags = experience.find('div')
a_tags = li_tags.find("a")
job_title = a_tags.find("h3").get_text().strip()

print(job_title)

company_name = a_tags.find_all("p")[1].get_text().strip()
print(company_name)

joining_date = a_tags.find_all("h4")[0].find_all("span")[1].get_text().strip()

employment_duration = a_tags.find_all("h4")[1].find_all(
	"span")[1].get_text().strip()

print(joining_date + ", " + employment_duration)
jobs = driver.find_element(By.XPATH,"//a[@data-link-to='jobs']/span")
# In case of an error, try changing the XPath.

jobs.click()
job_src = driver.page_source

soup = BeautifulSoup(job_src, 'lxml')
jobs_html = soup.find_all('a', {'class': 'job-card-list__title'})
# In case of an error, try changing the XPath.

job_titles = []

for title in jobs_html:
	job_titles.append(title.text.strip())

print(job_titles)
company_name_html = soup.find_all(
'div', {'class': 'job-card-container__company-name'})
company_names = []

for name in company_name_html:
	company_names.append(name.text.strip())

print(company_names)


import re # for removing the extra blank spaces

location_html = soup.find_all(
	'ul', {'class': 'job-card-container__metadata-wrapper'})

location_list = []

for loc in location_html:
	res = re.sub('\n\n +', ' ', loc.text.strip())

	location_list.append(res)

print(location_list)

