import sys
import os
import time
import urllib
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


def main(driver, lista, path):
    for fasta in lista:
        main_tab = driver.current_window_handle
        elem = driver.find_element_by_name('uploadfile1')
        elem.send_keys(path + fasta)
        elem = driver.find_element_by_name('uploadfile2')
        elem.send_keys(path + fasta)
        sel_xpath = '//input[@type="button"]'
        buttons = driver.find_elements_by_xpath(sel_xpath)
        buttons[0].click()
        buttons[1].click()
        submit_xpath = '//input[@type="submit" and @value="run YASS"]'
        driver.find_element_by_xpath(submit_xpath).click()
        time.sleep(3)
        dotplot_a = driver.find_element_by_link_text('simple')
        dotplot_href = dotplot_a.get_attribute("href")
        dotplot_a.click()
        time.sleep(3)
        dotplot_url = "http://bioinfo.lifl.fr/yass/tmp/dp." + \
                      dotplot_href.split("=")[1].split("&")[0] + ".png"
        urllib.urlretrieve(dotplot_url, path + "dotplot." + fasta.split(".")[0] + ".png")
        time.sleep(3)
        driver.find_element_by_link_text('web server').click()

if __name__ == "__main__":
    path = os.getcwd() + "/"
    lista = [f for f in os.listdir(path) if isfile(join(path, f))]
    driver = webdriver.Chrome("~/chromedriver")
    driver.get("http://bioinfo.lifl.fr/yass/yass.php")
    element = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.NAME, "uploadfile1")))
    main(driver, lista, path)
