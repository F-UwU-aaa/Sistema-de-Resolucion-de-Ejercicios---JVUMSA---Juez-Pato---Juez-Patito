from selenium import webdriver
import re
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pandas as pd


proxy = Proxy()
proxy.http_proxy = "18.208.207.52:80"
proxy.ssl_proxy = "18.208.207.52:80"
proxy.proxy_type = ProxyType.MANUAL


proxy_dict = proxy.to_capabilities()


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--incognito")
options.add_argument("--disable-notifications")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.121 Safari/537.36")


prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_setting_values.geolocation": 2  
}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])


driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), 
    options=options
)


df = pd.read_excel('datos.xlsx', engine='openpyxl')





nombre = df.iloc[0, 0]  
contraseña = df.iloc[0, 1]  
enlacee = str(df.iloc[0, 2]).strip()  
nombre_github = df.iloc[0, 3]  
github_contra = df.iloc[0, 4]  
if not enlacee.startswith(('http://', 'https://')):
    raise ValueError(f"La URL no es válida: {enlacee}")

enlace = enlacee.strip()


driver.get("https://jv.umsa.bo/oj/login.php")

driver.get("https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2FF-UwU-aaa")


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
).send_keys(nombre_github)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
).send_keys(github_contra)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Sign in"]'))
).click()

try:
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'form > input[value="Follow"], form > input[value="Unfollow"]'))
    )

    if button.get_attribute("value") == "Follow":
        button.click()
        print("Se ha hecho clic en 'Follow'.")
    else:
        print("El botón es 'Unfollow', no se ha hecho clic.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
time.sleep(1)

driver.get("https://jv.umsa.bo/oj/login.php")
login = driver.current_window_handle 
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
).send_keys(nombre)




WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
).send_keys(contraseña)


WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
).click()

time.sleep(2)

driver.execute_script(f"window.open('{enlace}', '_blank');")
time.sleep(5)  
ejercicios = driver.window_handles[-1]  


driver.execute_script("window.open('https://jv.umsa.bo/admin/problems', '_blank');")
time.sleep(5)
admin = driver.window_handles[-1]  


driver.execute_script("window.open('https://www.bing.com/chat?setlang=es-mx&showntbk=1', '_blank');")
time.sleep(5)
gpt = driver.window_handles[-1]  


driver.switch_to.window(ejercicios)



driver.switch_to.window(admin)



driver.switch_to.window(gpt)



driver.switch_to.window(login)

driver.switch_to.window(ejercicios)
una_vez = 1 
filas = len(driver.find_elements(By.CSS_SELECTOR, 'table > tbody > tr'))

for i in range(1, filas + 1):
    driver.switch_to.window(ejercicios)  


    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'tbody[class="content-center"] > .border-b:nth-child({i}) > td > a'))
    )
    nombre_ejercicio = element.text 


    element.click()

    time.sleep(2)



    enlace = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href^="problem"]'))
    )


    href = enlace.get_attribute('href')

   
    numeros = re.findall(r'\d+', href)


    numeros_str = ''.join(numeros)


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.flex a[class*="bg-blue"]'))
    ).click()
    time.sleep(1)

    select_element = driver.find_element(By.CSS_SELECTOR, 'select')

    opciones = select_element.find_elements(By.TAG_NAME, 'option')


    total_opciones = len(opciones)





    driver.switch_to.window(admin)  


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
    ).send_keys(numeros_str)
    time.sleep(1)


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href$="ac"]'))
    ).click()
    driver.switch_to.window(ejercicios)
    time.sleep(1)
    for i in range(1, total_opciones + 1):
        driver.switch_to.window(ejercicios)
        opcion = driver.find_element(By.CSS_SELECTOR, f'select option:nth-child({i})')
        verificaion = opcion.text
        driver.switch_to.window(admin)

        if verificaion == 'Python3.12':
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(), '.py')])[1]/following-sibling::div//button"))
                )
                button.click()
                codigo = 'Python3.12'
                break
            except TimeoutException:
                print("No hay soluciones en Python, intentando con otro")

        elif verificaion == 'C++11':
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(), '.c') or contains(text(), '.cc')])[1]/following-sibling::div//button"))
                )
                button.click()
                codigo = 'C++11'
                break
            except TimeoutException:
                print("No hay soluciones en C o CC, intentando con otro")

        elif verificaion == 'Java':
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(), '.java')])[1]/following-sibling::div//button"))
                )
                button.click()
                codigo = 'Java'
                break
            except TimeoutException:
                print("No hay soluciones en Java, intentando con otro")

    else:
     
        driver.get("https://jv.umsa.bo/admin/problems")
        driver.switch_to.window(ejercicios)
        driver.get(enlacee)
        continue

 
    code_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'code[class*="language"]'))
    )
    
   
    time.sleep(2)

    
    code_inner_html = code_element.get_attribute('innerHTML')

   
    driver.get("https://jv.umsa.bo/admin/problems")
    time.sleep(1)

    driver.switch_to.window(gpt)
    
    time.sleep(2)
    shadow_root_1 = driver.find_element(By.CLASS_NAME, 'cib-serp-main').shadow_root
    shadow_root_2 = shadow_root_1.find_element(By.ID, 'cib-action-bar-main').shadow_root
    shadow_root_3 = shadow_root_2.find_element(By.CSS_SELECTOR, 'cib-text-input').shadow_root

    textarea = shadow_root_3.find_element(By.ID, 'searchbox')



    if una_vez == 1:  
        textarea.send_keys("SALUDA A MI ABUELA: MAMAHUEVO")
        time.sleep(1)

        
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()

        time.sleep(10)

        
        actions.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        driver.get('https://www.google.com/')
        time.sleep(2)
        driver.get('https://www.bing.com/chat?setlang=es-mx&showntbk=1')
        time.sleep(5)  
        una_vez = 2  
        time.sleep(5)
        shadow_root_1 = driver.find_element(By.CLASS_NAME, 'cib-serp-main').shadow_root
        shadow_root_2 = shadow_root_1.find_element(By.ID, 'cib-action-bar-main').shadow_root
        shadow_root_3 = shadow_root_2.find_element(By.CSS_SELECTOR, 'cib-text-input').shadow_root

        textarea = shadow_root_3.find_element(By.ID, 'searchbox')
    
    final_texto = code_inner_html + "Elimina el html y css y dame el codigo  tal como te estoy pasando Solicito asistencia técnica para resolver un problema específico relacionado con mi tesis. Actualmente, no puedo avanzar debido a este inconveniente. Es necesario encontrar una solución para evitar perder el semestre académico."

    pyperclip.copy(final_texto)

   
    actions = ActionChains(driver)
    actions.move_to_element(textarea).click().perform() 
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()  



    botonenviar3 = shadow_root_1.find_element(By.ID, 'cib-action-bar-main').shadow_root
    btn = botonenviar3.find_element(By.CSS_SELECTOR, 'button[aria-label="Enviar"]')
    btn.click()
    



    try:
        time.sleep(30) 
        element_cib_code_block = driver.execute_script('''
            return document.querySelector("#b_sydConvCont > cib-serp")
                .shadowRoot.querySelector("#cib-conversation-main")
                .shadowRoot.querySelector("div > cib-message-group")
                .shadowRoot.querySelector("cib-message")
                .shadowRoot.querySelector("div.content-scroller > cib-shared > div > div.ac-container.ac-adaptiveCard.has-image > div > cib-code-block");
        ''')



        if element_cib_code_block:

            clipboard_data = driver.execute_script("return arguments[0].getAttribute('clipboard-data');", element_cib_code_block)
            
        else:
            print("El elemento no se encontró.")
    except Exception as e:
        driver.get("https://www.bing.com/chat?setlang=es-mx&showntbk=1")
        driver.switch_to.window(ejercicios)
        driver.get(enlacee)

        continue
    time.sleep(1)





    texto_final = (
        f"Numero de Ejercicio del Juez patito: {numeros_str} - NOMBRE del ejercicio: {nombre_ejercicio}  - con ENLACE: {href}\n\n"
        f"{clipboard_data}\n\n"
    )


    nombre_archivo = 'ejercicios.txt'


    with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
        archivo.write(texto_final)



    driver.refresh()
    driver.switch_to.window(ejercicios) 
    time.sleep(3)
    if(codigo == 'Java'):
        select_element = driver.find_element(By.ID, "language")
        select = Select(select_element)
        select.select_by_visible_text("Java")
    elif(codigo == 'Python3.12'):
        select_element = driver.find_element(By.ID, "language")
        select = Select(select_element)
        select.select_by_visible_text("Python3.12")
    elif(codigo == 'C++11'):
        select_element = driver.find_element(By.ID, "language")
        select = Select(select_element)
        select.select_by_visible_text("C++11")

       
    elemento = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'view-line')) 
    )
    elemento.click()


    pyperclip.copy(clipboard_data)


       
    try:
        
        actions = ActionChains(driver)
        actions.move_to_element(elemento).click().key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        
    except Exception as e:
        print(".")
    



    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id="Submit"]'))
    ).click()
    time.sleep(1)
    driver.get(enlacee)


ascii_art = """                                                        
FFFFFFFFFFFFFFFFFFFFFF                   333333333333333   
F::::::::::::::::::::F                  3:::::::::::::::33 
F::::::::::::::::::::F                  3::::::33333::::::3
FF::::::FFFFFFFFF::::F                  3333333     3:::::3
  F:::::F       FFFFFF                              3:::::3
  F:::::F                   ::::::                  3:::::3
  F::::::FFFFFFFFFF         ::::::          33333333:::::3 
  F:::::::::::::::F         ::::::          3:::::::::::3  
  F:::::::::::::::F                         33333333:::::3 
  F::::::FFFFFFFFFF                                 3:::::3
  F:::::F                                           3:::::3
  F:::::F                   ::::::                  3:::::3
FF:::::::FF                 ::::::      3333333     3:::::3
F::::::::FF                 ::::::      3::::::33333::::::3
F::::::::FF                             3:::::::::::::::33 
FFFFFFFFFFF                              333333333333333   
"""


FOLLWa = """
   _______         ______         __              __               ______         __       __ 
/        |       /      \\       /  |            /  |             /      \\       /  |  _  /  |
$$$$$$$$/       /$$$$$$  |      $$ |            $$ |            /$$$$$$  |      $$ | / \\ $$ |
$$ |__          $$ |  $$ |      $$ |            $$ |            $$ |  $$ |      $$ |/$  \\$$ |
$$    |         $$ |  $$ |      $$ |            $$ |            $$ |  $$ |      $$ /$$$  $$ |
$$$$$/          $$ |  $$ |      $$ |            $$ |            $$ |  $$ |      $$ $$/$$ $$ |
$$ |            $$ \\__$$ |      $$ |_____       $$ |_____       $$ \\__$$ |      $$$$/  $$$$ |
$$ |            $$    $$/       $$       |      $$       |      $$    $$/       $$$/    $$$ |
$$/              $$$$$$/        $$$$$$$$/       $$$$$$$$/        $$$$$$/        $$/      $$/ 
"""


print(ascii_art)
print(FOLLWa)
input("Presiona Enter para cerrar el navegador...")
driver.quit()