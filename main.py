from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time


def main():
    #config chrome web driver
    service = Service()
    #opciones navegador
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920, 1080")
    
    #instancia
    driver = Chrome(service=service, options=option)
    #pagina inicio sesion
    driver.get("http://127.0.0.1:5000/login")
    
    time.sleep(5)
    #Hacer login
    driver.find_element(By.NAME, "user_login").send_keys("Deiby")
    driver.find_element(By.NAME, "contraseña_login").send_keys("123456")
    driver.find_element(By.NAME, "btn-login").click()
    
    time.sleep(5)
    #Ver productos y precios de menu
    driver.find_element(By.LINK_TEXT, "Menú").click()
    
    time.sleep(3)
    
    product_names = driver.find_elements(By.TAG_NAME, "h3")
    precios = driver.find_elements(By.CLASS_NAME,"precio")
    
    names = [name.text for name in product_names]
    prices = [float(price.text.replace('$','')) for price in precios]
    
    df = pd.DataFrame({
        "Producto": names,
        "Precio ($)": prices
    })
    
    df.to_csv("productos.csv",index=False)
    print(df)
    
    time.sleep(5)
    
    #hacer un pedido
    driver.find_element(By.LINK_TEXT, "Pedir").click()
    
    driver.find_element(By.NAME, "nombre").send_keys("Don Juan")
    driver.find_element(By.NAME, "telefono").send_keys("12345678")

    elselect = driver.find_element(By.NAME, "plato_selected")
    
    select = Select(elselect)
    
    select.select_by_value("2")
    
    driver.find_element(By.NAME, "cantidad").send_keys("8")
    driver.find_element(By.ID, "pedir").click()

    

    time.sleep(10)
    driver.quit()
    
if __name__ == "__main__":
    main()
