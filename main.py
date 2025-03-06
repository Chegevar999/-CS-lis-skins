from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent


url:str = "https://lis-skins.ru/market/"
url2 = "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"


def Create_driver():

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent={UserAgent().random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def Close_driver(driver):
    driver.close()
    driver.quit()

def Active_categories(driver,min_active = None,max_active = None,list_active=None):
    class_wepons = driver.find_elements(By.CLASS_NAME, "market__weapon-type")

    if(list_active):
        for i in list_active:
            knife = class_wepons[i]

            knife.click()
            knife_active = class_wepons[i].find_element(
                By.CLASS_NAME, "market__weapon-type-menu-inner-top")
            knife_active.click()
            time.sleep(1)
    else:
        for i in range(min_active,max_active):
            knife = class_wepons[i]

            knife.click()
            knife_active = class_wepons[i].find_element(
                By.CLASS_NAME, "market__weapon-type-menu-inner-top")
            knife_active.click()
            time.sleep(1)

def Change_price(url_old,min_price=None,max_price=None):
    string = ""

    if(min_price):
        string+=f"&price_from={min_price}"
    if(max_price):
        string+=f"&price_to={max_price}"
    new_url = url_old + string
    return new_url

def Parsing_skins(driver):
    result = []

    for i in range(1, 61):

        skin = driver.find_element(
            By.XPATH, f'//*[@id="skins-obj"]/div/div[{i}]')
        try:
            list_skin = skin.text.split("\n")
            if ("0." in list_skin[0].split(" ")[-1]):

                skin_float = float(list_skin[0].split(" ")[-1])
            else:
                skin_float = 0

            name = list_skin[1]


            price = float(list_skin[2].split('.cls')[0])
            sale = float(list_skin[2].split('.cls')[1].split(
                " ")[1].replace("%", "")) * (-1)


            dict_skin = {
                "float":skin_float,
                "name":name,
                "price":price,
                "sale":sale
            }
            if (dict_skin["sale"] > 40):
                result.append(dict_skin)


        except:
            continue

    return result


def main():
    driver = Create_driver()
    url = "https://lis-skins.ru/market/csgo/?"
    url = Change_price(url, 10, 100)


    driver.get(url= url)

    for page in range(1,50):
        driver.get(url=url+f"&page={page}")
        result = Parsing_skins(driver)
        print(result)

        time.sleep(1)

        #for i in result:
            #print(i)
        #print(result)
        #Active_categories(driver, list_active=[2, 6, 8])
    Close_driver(driver)


def collect_data(cat_type):
    driver = Create_driver()
    url = "https://lis-skins.ru/market/csgo/?"
    url = Change_price(url, 10, 100)

    driver.get(url=url)

    all_results = []

    for page in range(1, 50):
        driver.get(url=url + f"&page={page}")
        result = Parsing_skins(driver)
        all_results.extend(result)

        time.sleep(1)

    Close_driver(driver)

    # Сохраняем данные в JSON
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(all_results, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
