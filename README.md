# Python Web Scraper

## About
A simple project that pulls plant data from [Rover](https://www.rover.com/blog/poisonous-plants/) and saves to both an excel and csv file in an output folder. 
Used to create a local SQL Server database for future personal projects.


## Built With
![Python](https://img.shields.io/badge/Python-20232A?style=for-the-badge&logo=python&logoColor=#3776AB)
![Selenium](https://img.shields.io/badge/Selenium-20232A?style=for-the-badge&logo=selenium&logoColor=#43B02A)


## File Output
* ``Plant Name``
  * **Type:** String
  * **Description:** Common name of the plant
* ``Scientific Name``
  * **Type:** String
  * **Description:** Formal scientific name of the plant
* ``Dogs``
  * **Type:** Int
  * **Description:** Indicates whether the plant affects this animal (dog): 1 = Yes, 0 = No.
* ``Cats``
  * **Type:** Int
  * **Description:** Indicates whether the plant affects this animal (cat): 1 = Yes, 0 = No.
* ``Plant Type``
  * **Type:** String
  * **Description:** Describes the type of plant: House, Wild, Garden.
* ``Toxicity Level``
  * **Type:** String
  * **Description:** Indicates the severity of the plant to the animal: Mild-Moderate, Severe.
* ``Symptoms``
  * **Type:** String
  * **Description:** A comma delimited list of common symptoms of toxicity.
  