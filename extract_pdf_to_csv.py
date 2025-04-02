import pdfplumber
import pandas as pd
import zipfile
import os

# Criar a pasta 'downloads' se ela não existir
downloads_dir = "downloads"
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

pdf_path = "D:\\Teste-de-nivelamento\\teste-transformacao-de-dados\\arquivo-pdf\\Anexo_I.pdf"
csv_path = "downloads/Rol_Procedimentos.csv"
zip_path = "downloads/Teste_leonardo_jarussi.zip"

#Substituindo abreviações
substituicoes = {
    "OD": "Procedimentos Odontológicos",
    "AMB": "Procedimentos Ambulatoriais"
}

#Lista para armazenar os dados extraídos
dados = []

# Abrir o PDF e extrair tabelas
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_table()
        if tables:
            for row in tables:
                dados.append(row)

# Criar DataFrame e limpar os dados
df = pd.DataFrame(dados)
df = df.dropna().reset_index(drop=True) # Remove as linhas vazias

# Substituir abreviações
df.replace(substituicoes, inplace=True)

# Salvar em CSV
df.to_csv(csv_path, index=False, sep=';')

# Compactar o CSV em um ZIP
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path, os.path.basename(csv_path))

print(f"Transformação concluída! Arquivo salvo em: {zip_path}")