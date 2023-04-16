from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

time.sleep(60)
website = 'https://www.theclimatepledge.com/us/en/Signatories'
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_experimental_option("detach", True)

extracted_signitories = pd.read_csv('signatories.csv')
loaded_links = list(extracted_signitories['sign_link'].values)

def accept_cookies(driver_object):
    print('accept_cookies')
    """
    locates and presses the accept cookies button
    """
    time.sleep(10) # wait for the site to fully load
    accept_cookies_button = driver_object.find_element(By.XPATH, '//button[@class="cta accept-cookie     "]')
    accept_cookies_button.click()



def extract_individual_links(driver_object):
    print('extract_individual_links')
    xpath = '//div[@class="scrollable-grid-wrapper"]/div/div[@class="row"]'
    rows = driver_object.find_elements(By.XPATH, xpath)
    print(f'There are {len(rows)} row wrappers')
    all_signitory_anchors = []
    print('got rows')
    for row in rows:
        signitory_anchors = row.find_elements(By.XPATH, './a[@data-component="m07-signatory"]')
        print(f'{len(signitory_anchors)} signitories')
        all_signitory_anchors+=signitory_anchors
    
    href_links = [tag.get_attribute('href') for tag in all_signitory_anchors]
    link_list = [link for link in href_links  if 'amazonclimatepledge' in link]
    return [l for l in link_list if l not in loaded_links]

def main():
    try:
        website_driver = webdriver.Chrome(
            service=Service(
            ChromeDriverManager().install()
            ),
            options=options
        )
        website_driver.get(website)
    except:
        website_driver.quit()
        time.sleep(60)
        website_driver = webdriver.Chrome(
            service=Service(
            ChromeDriverManager().install()
            ),
            options=options
        )
        website_driver.get(website)
    accept_cookies(website_driver)
    all_links = extract_individual_links(website_driver)
    website_driver.quit()
    print(f'Signitory links are {len(all_links)}')
    signatory_names = []
    join_dates = []
    signatory_descriptions = []
    signatory_sites = []
    i = 0
    for signitory_link in all_links:
        i+=1
        print(f'log: Extracting signatory {i}')
        try:
            signitory_driver = webdriver.Chrome(
                service=Service(
                ChromeDriverManager().install()
                ),
                options=options
                )
            signitory_driver.get(signitory_link)
        except:
            try:
                signitory_driver.quit()
                time.sleep(60)
                signitory_driver = webdriver.Chrome(
                    service=Service(
                    ChromeDriverManager().install()
                    ),
                    options=options
                    )
                signitory_driver.get(signitory_link)
            except:
                try:
                    signitory_driver.quit()
                    time.sleep(180)
                    signitory_driver = webdriver.Chrome(
                        service=Service(
                        ChromeDriverManager().install()
                        ),
                        options=options
                        )
                    signitory_driver.get(signitory_link)
                except:
                    signitory_driver.quit()
                    time.sleep(600)
                    signitory_driver = webdriver.Chrome(
                        service=Service(
                        ChromeDriverManager().install()
                        ),
                        options=options
                        )
                    signitory_driver.get(signitory_link)
        accept_cookies(signitory_driver)
        signatory_name = signitory_driver.find_element(By.XPATH, '//p[@class="heading-2 signatory-name mobile"]').text
        signatory_name = signatory_name.replace(",", " ").replace("\n", " ")
        signatory_names.append(signatory_name)
        join_date = signitory_driver.find_element(By.XPATH, '//p[@class="heading-3 date"]').text
        join_date = join_date.replace(",", " ").replace("\n", " ")
        join_dates.append(join_date)
        signatory_description = signitory_driver.find_element(By.XPATH, '//p[@class="body-regular description rich-text-content"]').text
        signatory_description = signatory_description.replace(",", " ").replace("\n", " ")
        signatory_descriptions.append(signatory_description)
        signatory_site = signitory_driver.find_element(By.XPATH, '//a[@class="secondary-button   with-icon   "]').get_attribute('href')
        signatory_site = signatory_site.replace(",", " ").replace("\n", " ")
        signatory_sites.append(signatory_site)
        signitory_driver.quit()
        signitory_link = signitory_link.replace(",", " ").replace("\n", " ")

        with open('signatories.csv', 'a') as f:
            f.write(f"""{signatory_name},{join_date},{signatory_description},{signatory_site},{signitory_link}\n""")
    
    data = {
        'signatory_names': signatory_names,
        'join_dates': join_dates,
        'signatory_descriptions': signatory_descriptions,
        'signatory_sites': signatory_sites
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv('signatories.csv', index=False)

if __name__=='__main__':
    main()