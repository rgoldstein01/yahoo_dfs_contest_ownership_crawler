from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

Y_EMAIL = ""
Y_PW = ""

CONTEST = ""

driver = webdriver.Chrome(ChromeDriverManager().install())


def authenticate(driver):
    # time.sleep(10)
    login = driver.find_element_by_id("login-username")
    login.click()
    login.send_keys(Y_EMAIL)

    e_button = driver.find_element_by_id("login-signin")

    time.sleep(10)

    e_button.click()

    time.sleep(15)

    pw = driver.find_element_by_id("login-passwd")
    pw.click()
    pw.send_keys(Y_PW)

    p_button = driver.find_element_by_id("login-signin")

    time.sleep(10)

    p_button.click()

    time.sleep(15)

    return driver

def get_lineup_exposures(driver, exposures_full):
    exposures = driver.find_elements_by_xpath("//span[@class='Fz-xs Cur-he C-inactive']")
    names = driver.find_elements_by_class_name("NoLinkColor")

    exposures_text = []
    counter = 0
    for e in exposures:
        if counter < 8:
            txt = e.text
            num_exposure = txt.split()[0]
            num_exposure_flt = num_exposure[:-1]
            exposures_text.append(float(num_exposure_flt))
        else:
            break
        counter += 1

    names_text = []
    counter = 0
    for n in names:
        if counter == 0:
            pass
        elif counter < 9:
            names_text.append(n.text)
        else:
            break
        counter += 1

    counter = 0
    while counter < len(exposures):
        curr_n = names_text[counter]
        curr_e = exposures_text[counter]
        exposures_full[curr_n] = curr_e
        counter += 1

    time.sleep(20)

    return driver, exposures_full

try:
    driver.get('https://login.yahoo.com/?specId=usernameReg&context=reg&src=dailyfantasy&intl=US&.lang=en-US&.done=https%3A%2F%2Fsports.yahoo.com%2Fdailyfantasy%2F%3Factivity%3Dquickmatch%26pspid%3D782206164')
    # driver.save_screenshot('screenie.png')

    driver = authenticate(driver)

    # now we are authenticated and can go wherever on the site
    driver.get('https://sports.yahoo.com/dailyfantasy/contest/' + CONTEST)

    time.sleep(10)

    # now let's get exposures for rest of players on the current page of LUs
    other_lineups = driver.find_elements_by_xpath("//a[@class='NoLinkColor P-2']")

    time.sleep(5)
    links = []
    for elem in other_lineups:
        links.append(elem.get_attribute("href"))

    time.sleep(20)

    # storing all final exposure values here
    exposures_full = {}
    counter = 1
    for l in links:
        print(l)
        driver.get(l)
        time.sleep(10)

        # get our own lineup we clicked on exposures
        driver, exposures_full = get_lineup_exposures(driver, exposures_full)

        print("Finished lineup " + str(counter))
        counter += 1

    d = dict(sorted(exposures_full.items(), key=lambda item: item[1]))
    for a in d.keys():
        print(a + " " + str(d[a]))
    driver.close()

except Exception as e:
    print(e)
    print('driver closing on error')
    driver.close()
