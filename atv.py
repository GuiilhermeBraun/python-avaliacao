from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
import pyautogui as py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configurações do navegador
opts = ChromeOptions()
opts.add_experimental_option('detach', True)
nav = webdriver.Chrome(options=opts)

# Dicionário de sites com seus localizadores
sites = {
    'https://www.kabum.com.br/': {
        'search_locator': (By.CLASS_NAME, "id_search_input"),
        'price_xpath': '/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div/div[2]/div[1]/main/div/article/a/div/div[2]/div[2]/span'
    },
    'https://www.dell.com/pt-br': {
        'search_locator': (By.CLASS_NAME, "mh-search-input"),
        'price_xpath': '/html/body/main/div/div[2]/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/div/div/article[1]/section[2]/div[1]/div[1]'
    },
    'https://www.magazineluiza.com.br/': {
        'search_locator': (By.ID, 'input-search'),
        'price_xpath': '/html/body/div[2]/div/main/section[4]/div[4]/div/ul/li[1]/a/div[3]/div[3]/div/div/p'
    }
}

# Dicionário para armazenar preços
precos = {}

# Loop para pesquisa
for site, locators in sites.items():
    nav.get(site)
    sleep(5)

    try:
        # Localiza o campo de pesquisa
        search_by, search_value = locators['search_locator']
        pesquisa = nav.find_element(search_by, search_value)
        pesquisa.send_keys('Notebook Gamer Dell Intel Core i5-13450HX, 8GB RAM, GeForce RTX 3050 6GB')
        py.press('enter')

        # Resultados e busca o elemento de preço usando o XPath
        sleep(5)
        preco_element = nav.find_element(By.XPATH, locators['price_xpath'])

        # Adiciona o preço ao dicionário
        precos[site] = preco_element.text
        sleep(5)

    except Exception as e:
        print(f'Erro ao coletar dados no site {site}: {e}')

# Fecha o navegador
nav.quit()

# Salva os preços em um arquivo de texto
with open('precos_notebook.txt', 'w') as arquivo:
    for site, preco in precos.items():
        arquivo.write(f'{site}: {preco}\n')

print("Preços salvos em 'precos_notebook.txt'")

# Configurações do e-mail
sender_email = 'guilherme.taschetto@duque.g12.br'   # Meu e-mail
receiver_email = 'antonio.alves@duque.g12.br'       # E-mail de destino
password = 'veio rnah bjku ggrx '                   # Senha de e-mail
smtp_server = 'smtp.gmail.com'                      # Servidor SMTP do seu provedor de e-mail
smtp_port = 587                                     # Porta SMTP

# Configura a mensagem do e-mail
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'Preços do Notebook Dell G15'

# Corpo do e-mail
body = 'Arquivo com os preços do Notebook Dell G15.'
message.attach(MIMEText(body, 'plain'))

# Anexa o arquivo de preços
filename = 'precos_notebook.txt'
with open(filename, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())

# Codifica o arquivo em Base64 e adiciona ao e-mail
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename= {filename}')
message.attach(part)

# Envia o e-mail
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Inicializa a conexão TLS
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    print('E-mail enviado com sucesso!')
except Exception as e:
    print(f'Erro ao enviar e-mail: {e}')
finally:
    server.quit()
