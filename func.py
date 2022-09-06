import pyodbc 

# Conexão com o banco
server = 'nome do servidor' 
database = 'nome do banco' 
username = '' 
password = '' 
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#QUERYS
sqlTitular = "SELECT P.CPF, P.NOME, F.CHAPA, 0 NRODEPEND FROM PPESSOA P join PFUNC F on p.CODIGO = f.CODPESSOA join ( SELECT CODCOLIGADA, CHAPA, CODBENEFICIO FROM VBENEFFUNC (NOLOCK) WHERE CODBENEFICIO = 8 ) v on f.CODCOLIGADA = v.CODCOLIGADA and f.CHAPA = v.CHAPA where f.CODCOLIGADA = 1 and f.CODSITUACAO not in ('D','I','U','L') AND P.CPF = ?" 
sqlDependente = "SELECT D.CPF, D.NOME, F.CHAPA, D.NRODEPEND FROM PFUNC F join PFDEPEND d on f.CODCOLIGADA = d.CODCOLIGADA AND F.CHAPA = D.CHAPA join ( SELECT CODCOLIGADA, CHAPA, CODBENEFICIO, NRODEPEND FROM VBENEFDEPEND (NOLOCK) WHERE CODBENEFICIO = 8 ) v on D.CODCOLIGADA = V.CODCOLIGADA and D.CHAPA = v.CHAPA AND D.NRODEPEND = V.NRODEPEND where f.CODCOLIGADA = 1 and f.CODSITUACAO not in ('D','I','U','L') AND D.CPF = ?"


