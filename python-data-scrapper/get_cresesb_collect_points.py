import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

INTERVAL_POINTS_FILE = "sorocaba_interval_points.csv"
DATAFRAME = pd.read_csv(INTERVAL_POINTS_FILE, sep=';')
BASE_URL = "http://www.cresesb.cepel.br/index.php?section=sundata"

def getIntervals():
	mapValues = DATAFRAME[['latitude', 'longitude']]
	return mapValues.values.tolist()

def buildDriver():
	# -ignore-certificate-errors is used to access sites that dont have a SSL certificate
	# without getting an error
	chrome_options = Options()
	chrome_options.add_argument("-ignore-certificate-errors")
	s = Service(r"C:/Users/Sant/Github/solar-track/python-data-scrapper/chromedriver-win64/chromedriver.exe")
	return webdriver.Chrome(service=s, options=chrome_options)

def getCollectpoints(driver, interval_points):
    driver.get(BASE_URL)

    seen_rows = set()

    with open("cresesb_collect_points.csv", mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["latitude", "longitude", "cidade", "media_horizontal", "media_angulo_igual_altitude", "maior_media_anual", "maior_min_mensal"])
        for location in interval_points:
            #print(location[0], location[1])
            inputLatitude = driver.find_element(By.ID, "latitude_dec")
            inputLatitude.click()
            inputLatitude.clear()
            inputLatitude.send_keys(location[0])
            inputLongitude = driver.find_element(By.ID, "longitude_dec")
            inputLongitude.click()
            inputLongitude.clear()
            inputLongitude.send_keys(location[1])
            driver.find_element(By.ID, "submit_btn").click()
            for i in range(1, 4):
                latitude = driver.find_element(By.XPATH, f"/html/body/div[3]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/div/div[2]/table[1]/tbody/tr[{i}]/td[6]")
                latitude = latitude.text.replace(" ", "").replace(",", ".").replace("S", "").replace("°", "")
                longitude = driver.find_element(By.XPATH, f"/html/body/div[3]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/div/div[2]/table[1]/tbody/tr[{i}]/td[7]")
                longitude = longitude.text.replace(" ", "").replace(",", ".").replace("O", "").replace("°", "")
                cityName = driver.find_element(By.XPATH, f"/html/body/div[3]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/div/div[2]/table[1]/tbody/tr[{i}]/td[3]").text
                horizontalAverage = driver.find_element(By.XPATH, f"/html/body/div[3]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/div/div[2]/table[{i+1}]/tbody/tr[1]/td[16]/strong")
                horizontalAverage = horizontalAverage.text.replace(" ", "").replace(",", ".")
                angleEqualHeightAverage = driver.find_element(By.XPATH, f"/html/body/div[3]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/div/div[2]/table[{i+1}]/tbody/tr[2]/td[16]/strong")
                angleEqualHeightAverage = angleEqualHeightAverage.text.replace(" ", "").replace(",", ".")
                biggestAnualAverage = driver.find_element(By.XPATH, f"/html/body/div[3]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/div/div[2]/table[{i+1}]/tbody/tr[3]/td[16]/strong")
                biggestAnualAverage = biggestAnualAverage.text.replace(" ", "").replace(",", ".")
                lowestAnualAverage = driver.find_element(By.XPATH, f"/html/body/div[3]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[3]/div/div[2]/table[{i+1}]/tbody/tr[4]/td[16]/strong")
                lowestAnualAverage = lowestAnualAverage.text.replace(" ", "").replace(",", ".")
                row = (latitude, longitude, cityName, horizontalAverage, angleEqualHeightAverage, biggestAnualAverage, lowestAnualAverage)

                if row not in seen_rows:
                    seen_rows.add(row)
                    writer.writerow(row)
                    print(row)
                    
    driver.quit()

def main():
    interval_points = getIntervals()
    driver = buildDriver()
    getCollectpoints(driver, interval_points)

if __name__ == "__main__":
    main()