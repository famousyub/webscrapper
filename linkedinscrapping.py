from linkedin_scraper import Person, actions,JobSearch
from selenium import webdriver
driver = webdriver.Chrome()
import parameters
email = parameters.username
password = parameters.password
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal

username = input("enter your name")
person = Person(f"https://www.linkedin.com/in/{username}", driver=driver)

print(type(Person))
job_search = JobSearch(driver=driver, close_on_complete=False, scrape=False)

job_listings = job_search.search("Machine Learning Engineer")



print(job_listings)


