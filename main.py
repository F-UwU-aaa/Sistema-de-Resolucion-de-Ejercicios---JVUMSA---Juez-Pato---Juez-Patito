from bs4 import BeautifulSoup
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

def remove_html_tags(html_content):
    # Crear un objeto BeautifulSoup a partir del contenido HTML
    soup = BeautifulSoup(html_content, "html.parser")
    # Extraer solo el texto del contenido HTML
    clean_text = soup.get_text()
    codigo = f"""
    {clean_text}
    """
    # Eliminar los números al inicio de cada línea
    codigo_limpio = re.sub(r'^\d+', '', codigo, flags=re.MULTILINE)
    return codigo_limpio

df = pd.read_excel('datos.xlsx', engine='openpyxl')





nombre = df.iloc[0, 0]  
contraseña = df.iloc[0, 1]  
enlacee = str(df.iloc[0, 2]).strip()  
nombre_github = df.iloc[0, 3]  
github_contra = df.iloc[0, 4]  
if not enlacee.startswith(('http://', 'https://')):
    raise ValueError(f"La URL no es válida: {enlacee}")
sw = 1
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
driver.get("https://github.com/F-UwU-aaa/Sistema-de-Resolucion-de-Ejercicios---JVUMSA---Juez-Pato---Juez-Patito")

try:
    # Espera hasta que el botón sea clicable
    star_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-aria-prefix="Star this repository"]'))
    )
    # Hace clic en el botón
    star_button.click()

except Exception as e:
    print(f"Error al intentar hacer clic en el botón 'Star': {e}")

# Espera y hace clic en el botón que contiene data-testid="desktop"
try:
    # Espera hasta que uno de los botones sea visible
    desktop_button = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-testid*="desktop"]'))
    )
    
    # Si se encuentra el botón de escritorio, haz clic en él
    desktop_button.click()

except Exception:
    # Si no se encuentra el botón de escritorio, verifica el botón móvil
    try:
        mobile_button = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-testid*="mobile"]'))
        )
        # Haz clic en el botón móvil si está visible
        mobile_button.click()
    except Exception as e:
        print(f"Ningún botón encontrado: {e}")

# Espera y hace clic en el elemento con aria-keyshortcuts="a"
shortcut_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-keyshortcuts="a"]'))
)
shortcut_element.click()


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

for i in range(1, filas+1):
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
    print(code_inner_html)
    clean_code = remove_html_tags(code_inner_html)
    print("nuevo")
    print(clean_code)
    driver.get("https://jv.umsa.bo/admin/problems")
    time.sleep(1)

    #Nuevo codigo 
    driver.switch_to.window(gpt)
    if sw == 1:
        wait = WebDriverWait(driver, 20)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title*="ntro"]')))
        button.click()

        # Esperar hasta que el textarea con id "userInput" esté presente y luego enviar el texto
        textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[id="userInput"]')))
        textarea.send_keys("F")

        # Esperar hasta que el div contenedor del botón sea clicable y hacer clic
        div_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div div button')))
        div_button.click()

        # Esperar hasta que cualquier botón con un atributo 'title' esté clicable y hacer clic
        button_with_title = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title]')))
        button_with_title.click()
        sw = 0
    
    

    pyperclip.copy(clean_code + " Dame el mismo codigo que te estoy pasando sin agregar nada nuevo Entindes NADA DE AGREGAR COSAS NUEVAS, dame para copiar y pegar ")
    # Espera hasta que el textarea esté presente y luego envía el texto
    wait = WebDriverWait(driver, 20)
    textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[role="textbox"]')))

    # Asegúrate de que el textarea sea visible y clicable
    wait.until(EC.visibility_of(textarea))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea[role="textbox"]')))

    # Usa JavaScript para enfocar el textarea antes de pegar
    driver.execute_script("arguments[0].focus();", textarea)

    # Pega el contenido del portapapeles (Ctrl+V)
    textarea.send_keys(Keys.CONTROL, 'v')
    send_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Enviar mensaje"]')))
    send_button.click()

    time.sleep(30)
    copy_button = wait.until(EC.element_to_be_clickable((By.XPATH, '(//button[@title="Copiar código"])[last()]')))

    # Desplazarse hacia el botón
    driver.execute_script("arguments[0].scrollIntoView(true);", copy_button)

    # Esperar un poco para asegurar que el scroll se complete
    time.sleep(0.5)  # Ajusta el tiempo según sea necesario

    # Hacer clic en el botón
    copy_button.click()
    #Nuevo codigo 

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