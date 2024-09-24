from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import psycopg2 as pg

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/finance/quote/USD-BRL?sa=X&ved=2ahUKEwiNg7-xrfGEAxX9PbkGHao2CaUQmY0JegQIExAv")
valor_dolar = round(float((driver.find_element(By.CLASS_NAME,"fxKbKc").text).replace(",",".")),2)
data_cotacao = date.today()
hora_cotacao = ((((driver.find_element(By.CLASS_NAME,"ygUjEc").text).split(", "))[1]).split(" · "))[0]

hora_cotacao = hora_cotacao.split(" ")[0]
hora_cotacao_temp = (hora_cotacao.split(":"))[0]
if hora_cotacao_temp == "3":
    hora_cotacao_temp = "12"
elif int(hora_cotacao_temp) < 3:
    hora_cotacao_temp = str((int(hora_cotacao_temp) - 3) + 12)
else:
    hora_cotacao_temp = str(int(hora_cotacao_temp)-3)
hora_cotacao = hora_cotacao_temp+":"+(hora_cotacao.split(":"))[1]+":"+(((hora_cotacao.split(":"))[2]).split(" "))[0]

print(valor_dolar," | ",data_cotacao," | ",hora_cotacao)

conn = pg.connect(host="pg-11d01e0e-testepgsql.e.aivencloud.com", database="defaultdb", user="avnadmin", password="AVNS_69W0O2_65jEqbsCuztW", port="24931")
cur = conn.cursor()
cur.execute("CALL inserir_cotacao_dolar(%s, %s, %s);", (data_cotacao, hora_cotacao, valor_dolar))
conn.commit()
cur.close()
conn.close()
