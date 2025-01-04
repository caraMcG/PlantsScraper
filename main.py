from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)  # or use the appropriate WebDriver for your browser
driver.get('https://www.rover.com/blog/poisonous-plants/')

# Wait for content to load
driver.implicitly_wait(5)


# extract plant info from page
def extract_plants():
    body_element = driver.find_element(By.TAG_NAME, 'body')
    html = body_element.get_attribute('innerHTML')

    soup = BeautifulSoup(html, 'html.parser')
    plants = soup.select('tr.tile.tile-plant')

    return plants


def formatSave(all_plants):
    #LIST VARIABLES FOR SAVING
    names = []
    science_names = []
    dogs = []
    cats = []
    ptype = []
    level = []
    symptom = []

    #Iterate through plants and print info
    for plant in all_plants:
        #finding data on web page
        plant_name = plant.find('h4', class_='tile-title').text
        plant_science = plant.find('div', class_='scientific-name').text
        plant_type = plant.find('td', class_='attribute type').text
        toxicity_level = plant.find('td', class_='attribute toxicity').text
        toxic_to_dog = [item['data-label'] for item in plant.find_all('td', class_='toxic_to_dogs', attrs={'data-label': True})]
        toxic_to_cat = [item['data-label'] for item in plant.find_all('td', class_='toxic_to_cats', attrs={'data-label': True})]
        symptoms = plant.find('ul', class_='symptom-list').find_all('li')

        # print(f'Plant Name: {plant_name}')
        # print(f'Scientific Name: {plant_science}')

        #TOXICITY TO ANIMALS, active = yes
        if toxic_to_dog.__contains__('active'):
            # print(f'Toxic to Dogs?: ' + ''.join(toxic_to_dog))
            dog_int = 1
        else:
            # print(f'Toxic to Dogs?: no')
            dog_int = 0

        if toxic_to_cat.__contains__('active'):
            # print(f'Toxic to Cats?: ' + ''.join(toxic_to_cat))
            cat_int = 1
        else:
            # print('Toxic to Cats?: no')
            cat_int = 0

        # print(f'Plant Type: {plant_type}')
        # print(f'Toxicity Level: {toxicity_level}')

        #SYMPTOMS
        # print('Symptoms: ' + ', '.join(symptom.get_text() for symptom in symptoms)+'\n')

        #APPENDING DATA TO LISTS
        names.append(plant_name)
        science_names.append(plant_science)
        dogs.append(dog_int)
        cats.append(cat_int)
        ptype.append(plant_type)
        level.append(toxicity_level)
        symptom.append(', '.join(symptom.get_text() for symptom in symptoms))

    # EXPORTING TO .CSV & EXCEL
    try:
        today = datetime.today().strftime('%Y-%m-%d')

        df = pd.DataFrame({'Plant Name': names, 'Scientific Name': science_names, 'Dogs': dogs, 'Cats': cats, 'Plant Type': ptype, 'Toxicity Level': level, 'Symptoms': symptom})
        df.to_csv(f'output/plantInfo_{today}.csv', index=False, encoding='utf-8')
        df.to_excel(f'output/PlantInfo_{today}.xlsx', index=False, encoding='utf-8')
        print(f"Save completed successfully: {today}")
    except Exception as e:
        print("Error occurred when saving to excel and/or csv: ", str(e))


# List to store all plant data
all_plants = []
page = 0

# Loop through pages
while True:
    # Extract plants from the current page
    plants = extract_plants()
    # Add the current page's plants to the list
    all_plants.extend(plants)
    # check for next button: id =poisonous-plants-list_next
    try:
        page += 1
        print("Page: ", page)
        # wait until next page button is loaded fully
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='paginate_button next']")))
        #find the next button
        next_button = driver.find_element(By.XPATH, "//a[@class='paginate_button next']")

        if next_button:
            #click button
            driver.execute_script("arguments[0].click();", next_button)
            # next_button.click()
            driver.implicitly_wait(5)
            print("Loading next page... ")
        else:
            break
    except Exception as e:
        errorString = str(e)
        if "Element not found" not in errorString:
            print("No more pages.")
            break
        else:
            print('Error: ', errorString)
    except:
        print("Total pages checked: ", page)
        break

# Close the browser
driver.quit()

#get variables from plant data
formatSave(all_plants)

print(f"Total rows saved: {len(all_plants)}")