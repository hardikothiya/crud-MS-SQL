import pyodbc

server = 'LAPTOP-BLSHEGRH'
database = 'demo'
username = ''
password = ''
cxnn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cxnn.cursor()

