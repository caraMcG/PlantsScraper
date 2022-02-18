from bs4 import BeautifulSoup
import requests
import pandas as pd

#DOGS AND CATS, count=191
html = requests.get('https://www.rover.com/blog/poisonous-plants/').text

soup = BeautifulSoup(html, 'lxml')

#Find all plants
plants = soup.find_all('tr', class_='tile tile-plant')
counter = 0

#LIST VARIABLES FOR SAVING
names = []
science_names = []
dogs = []
cats = []
ptype = []
level = []
symptom = []

#Iterate through plants and print info
for plant in plants:
    #finding data on web page
    plant_name = plant.find('h4', class_='tile-title').text
    plant_science = plant.find('div', class_='scientific-name').text
    plant_type = plant.find('td', class_='attribute type').text
    toxicity_level = plant.find('td', class_='attribute toxicity').text
    toxic_to_dog = [item['data-label'] for item in plant.find_all('td', class_='toxic_to_dogs', attrs={'data-label': True})]
    toxic_to_cat = [item['data-label'] for item in plant.find_all('td', class_='toxic_to_cats', attrs={'data-label': True})]
    symptoms = plant.find('ul', class_='symptom-list').find_all('li')

    #keep count of plants
    counter += 1

    print(f'Plant ID:  {counter}')
    print(f'Plant Name: {plant_name}')
    print(f'Scientific Name: {plant_science}')

    #TOXICITY TO ANIMALS, active = yes
    if toxic_to_dog.__contains__('active'):
        print(f'Toxic to Dogs?: ' + ''.join(toxic_to_dog))
        dog_int = 1
    else:
        print(f'Toxic to Dogs?: no')
        dog_int = 0

    if toxic_to_cat.__contains__('active'):
        print(f'Toxic to Cats?: ' + ''.join(toxic_to_cat))
        cat_int = 1
    else:
        print('Toxic to Cats?: no')
        cat_int = 0

    print(f'Plant Type: {plant_type}')
    print(f'Toxicity Level: {toxicity_level}')

    #SYMPTOMS
    print('Symptoms: ' + ', '.join(symptom.get_text() for symptom in symptoms)+'\n')

    #APPENDING DATA TO LISTS
    names.append(plant_name)
    science_names.append(plant_science)
    dogs.append(dog_int)
    cats.append(cat_int)
    ptype.append(plant_type)
    level.append(toxicity_level)
    symptom.append(', '.join(symptom.get_text() for symptom in symptoms))

print(f'Total Plants: {counter}')

#EXPORTING TO .CSV & EXCEL
df = pd.DataFrame({'Plant Name': names, 'Scientific Name': science_names, 'Dogs': dogs, 'Cats': cats, 'Plant Type': ptype, 'Toxicity Level': level, 'Symptoms': symptom})
df.to_csv('plantInfo_Updated.csv', index=False, encoding='utf-8-sig')
df.to_excel('PlantInfo_EXCEL.xlsx', index=False, encoding='utf-8')
