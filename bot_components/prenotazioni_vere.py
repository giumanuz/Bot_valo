from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, CallbackQueryHandler, CallbackContext
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select


def prenota(update: Update, context: CallbackContext):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    time.sleep(2)
    driver.get("https://prodigit.uniroma1.it")
    time.sleep(2)
    driver.find_element(By.ID, "cookieChoiceDismiss").click()
    time.sleep(2)

    email_ob = driver.find_element(By.NAME, "Username")
    password_ob = driver.find_element(By.NAME, "Password")

    email_ob.click()
    email_ob.send_keys("1943520")
    password_ob.click()
    password_ob.send_keys("juhsut-rEhsy0-qy")

    password_ob.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.get("https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/prenotaposto-in-aula")
    time.sleep(5)

    Select(driver.find_element(By.ID, "codiceedificio")).select_by_visible_text('RM021')

    Select(driver.find_element(By.NAME, "aula")).select_by_visible_text("AULA 108 -- RM021-P01L008")

    Select(driver.find_element(By.NAME, "selezsettimana")).select_by_index(1)

    # lunedi
    Select(driver.find_element(By.NAME, "dalleore1")).select_by_visible_text("09:00")
    Select(driver.find_element(By.NAME, "alleore1")).select_by_visible_text("13:00")

    # martedì
    Select(driver.find_element(By.NAME, "dalleore2")).select_by_visible_text("09:00")
    Select(driver.find_element(By.NAME, "alleore2")).select_by_visible_text("11:00")

    # mercoledì
    Select(driver.find_element(By.NAME, "dalleore3")).select_by_visible_text("09:00")
    Select(driver.find_element(By.NAME, "alleore3")).select_by_visible_text("13:00")

    # giovedi
    Select(driver.find_element(By.NAME, "dalleore4")).select_by_visible_text("09:00")
    Select(driver.find_element(By.NAME, "alleore4")).select_by_visible_text("13:00")

    # venerdì
    Select(driver.find_element(By.NAME, "dalleore5")).select_by_visible_text("09:00")
    Select(driver.find_element(By.NAME, "alleore5")).select_by_visible_text("15:00")

    # dichiarazione covid
    driver.find_element(By.NAME, "dichiarazione").click()

    # pulsante prenota
    #driver.find_element(By.ID, "btnprenota").click()

    time.sleep(2)
    driver.get("https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/prenotaposto-in-aula")
    time.sleep(2)

    Select(driver.find_element(By.ID, "codiceedificio")).select_by_visible_text('RM021')

    Select(driver.find_element(By.NAME, "aula")).select_by_visible_text("AULA 204 -- RM021-P02L004")

    Select(driver.find_element(By.NAME, "selezsettimana")).select_by_index(1)

    # lunedi aula 204
    Select(driver.find_element(By.NAME, "dalleore1")).select_by_visible_text("13:00")
    Select(driver.find_element(By.NAME, "alleore1")).select_by_visible_text("15:00")
    # dichiarazione covid
    driver.find_element(By.NAME, "dichiarazione").click()
    # pulsante prenota
    #driver.find_element(By.ID, "btnprenota").click()
    time.sleep(2)

    driver.get("https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/prenotaposto-in-aula")
    time.sleep(4)

    Select(driver.find_element(By.ID, "codiceedificio")).select_by_visible_text('RM025')

    Select(driver.find_element(By.NAME, "aula")).select_by_visible_text("AULA INFORMATICA 15 -- RM025-E01PTEL024")

    Select(driver.find_element(By.NAME, "selezsettimana")).select_by_index(1)

    # martedì
    Select(driver.find_element(By.NAME, "dalleore2")).select_by_visible_text("11:00")
    Select(driver.find_element(By.NAME, "alleore2")).select_by_visible_text("15:00")
    # venerdì
    Select(driver.find_element(By.NAME, "dalleore5")).select_by_visible_text("15:00")
    Select(driver.find_element(By.NAME, "alleore5")).select_by_visible_text("19:00")

    # dichiarazione covid
    driver.find_element(By.NAME, "dichiarazione").click()

    # pulsante prenota
    #driver.find_element(By.ID, "btnprenota").click()
    time.sleep(2)

    print("tutto ok")
    driver.quit()

def init_prenotazioni_vere(dispatcher: Dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(
        prenota, "^prenotazione_vera$", run_async=True
    ))