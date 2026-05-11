import pathlib
import re

FICHEIRO = pathlib.Path("corpus_frases_alfabetico.txt")

texto = FICHEIRO.read_text(encoding="utf-8")

caracteres_com_espacos = len(texto)
caracteres_sem_espacos = len(re.sub(r"\s+", "", texto))

palavras = re.findall(r"\b[\wÀ-ÿ]+(?:[-'][\wÀ-ÿ]+)?\b", texto, flags=re.UNICODE)
numero_palavras = len(palavras)

linhas = [l for l in texto.splitlines() if l.strip()]
numero_linhas = len(linhas)

print(f"Ficheiro: {FICHEIRO}")
print(f"Linhas/frases: {numero_linhas}")
print(f"Caracteres com espaços: {caracteres_com_espacos:,}".replace(",", " "))
print(f"Caracteres sem espaços: {caracteres_sem_espacos:,}".replace(",", " "))
print(f"Palavras aproximadas: {numero_palavras:,}".replace(",", " "))

# Estimativa grosseira de tokens
tokens_estimativa = int(caracteres_com_espacos / 4)
print(f"Tokens estimados grosseiramente: {tokens_estimativa:,}".replace(",", " "))

# Se tiveres tiktoken instalado, conta tokens de forma mais realista
try:
    import tiktoken

    enc = tiktoken.get_encoding("cl100k_base")
    tokens = len(enc.encode(texto))
    print(f"Tokens cl100k_base: {tokens:,}".replace(",", " "))
except ImportError:
    print("tiktoken não instalado. Para instalar: py -m pip install tiktoken")
