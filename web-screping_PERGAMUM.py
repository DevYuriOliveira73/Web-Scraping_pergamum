# Coloque suas credenciais
matricula_ = '777777'
senha_ = '333333'

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("https://pergamum.ufc.br/pergamum/biblioteca_s/php/login_usu.php?flag=index.php")

    wait = WebDriverWait(driver, 10)
    
    matricula = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="id_login"]'))
    )
    matricula.send_keys(matricula_)

    senha = driver.find_element(By.XPATH, '//*[@id="id_senhaLogin"]')
    senha.send_keys(senha_)

    button_acessar = driver.find_element(By.XPATH, '//*[@id="button"]')
    button_acessar.click()

    html = driver.page_source
    html_parsed = BeautifulSoup(html, "html.parser")

    quantidade_livros = len(html_parsed.find_all(class_='txt_magenta')) + 1

except TimeoutException:
    print("O elemento não ficou clicável dentro do tempo especificado")

finally:
    try:
        for i in range(1, quantidade_livros):
            xpath_renovar = (f'//*[@id="botao_renovar{i}"]/center/input')
            
            # PARA RENOVAR O LIVRO
            button_renovar = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_renovar))
            )
            button_renovar.click()
            
            # PARA RECEBER O RECIBO POR EMAIL
            recibo = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))
            )
            recibo.click()
        
            # PARA VOLTAR
            voltar = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_gravar4"]'))
            )
            voltar.click()
            
    except TimeoutException:
        print('Demorando para responder!')

    finally:
        logout = driver.find_element(By.CSS_SELECTOR, '[title="Sair do Meu Pergamum"]')
        logout.click()
        driver.quit()
        print("RENOVAÇÃO CONCLUÍDA")
