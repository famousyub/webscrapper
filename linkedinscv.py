from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import variables
import parameters
query1 = variables.query

#change this with your favourite skills
query = "JAVA spring boot"


    



class ScrappingJobs():
    def __init__(self, country="Tunisia" , query="JAva spring boot"):
        self.location = country
        self.query = query
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        

    def jobfind(self):
       

        self.driver.implicitly_wait(10)

        self.driver.get('https://www.linkedin.com/login')

        email_input = self.driver.find_element(By.ID, 'username')
        password_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(parameters.username)
        password_input.send_keys(parameters.password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(10)

        for page_num in range(1, 3):
            url = f'https://www.linkedin.com/jobs/search/?keywords={query}&location={self.location}&start={25 * (page_num - 1)}'
            self.driver.get(url)
            last_height = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                new_height = self.driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                last_height = new_height

            time.sleep(20)  # Wait for 20 seconds
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            job_postings = soup.find_all('li', {'class': 'jobs-search-results__list-item'})

            # Extract relevant information from each job posting and store it in a list of dictionaries
            data = []
            for job_posting in job_postings:
                try:
                    job_title = job_posting.find('a', class_='job-card-list__title').get_text().strip()
                except AttributeError:
                    job_title = None

                try:
                    company_name = job_posting.find('a', class_='job-card-container__link').get_text().strip()
                except AttributeError:
                    company_name = None

                try:
                    location = job_posting.find('li', class_='job-card-container__metadata-item').get_text().strip()
                except AttributeError:
                    location = None

                data.append({
                    'Job Title': job_title,
                    'Company Name': company_name,
                    'Location': location
                })
                df = pd.DataFrame(data)
                df.to_csv(f'skillsjobs_{page_num}.csv', index=False)
        self.driver.quit()




