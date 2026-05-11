import json
import pathlib

PASTA_BASE = pathlib.Path(".")
INPUT = PASTA_BASE / "corpus_mestre.json"
OUTPUT = PASTA_BASE / "corpus_chunks.json"

CHUNK_SIZE = 1600
OVERLAP = 250


def criar_chunks_texto(texto, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Divide o texto em blocos com alguma sobreposição.
    Tenta cortar em fim de parágrafo ou fim de frase quando possível.
    """
    chunks = []
    inicio = 0
    tamanho = len(texto)

    while inicio < tamanho:
        fim = min(inicio + chunk_size, tamanho)
        fragmento = texto[inicio:fim]

        # tenta cortar no último parágrafo dentro do fragmento
        corte_paragrafo = fragmento.rfind("\n\n")
        corte_frase = max(
            fragmento.rfind(". "),
            fragmento.rfind("! "),
            fragmento.rfind("? ")
        )

        if fim < tamanho:
            if corte_paragrafo > chunk_size * 0.55:
                fim = inicio + corte_paragrafo
            elif corte_frase > chunk_size * 0.55:
                fim = inicio + corte_frase + 1

        fragmento = texto[inicio:fim].strip()

        if fragmento:
            chunks.append(fragmento)

        novo_inicio = fim - overlap

        if novo_inicio <= inicio:
            novo_inicio = fim

        inicio = novo_inicio

    return chunks


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Não encontrei: {INPUT}")

    corpus = json.loads(INPUT.read_text(encoding="utf-8"))

    todos_chunks = []

    for doc in corpus:
        texto = doc["texto"]
        fragmentos = criar_chunks_texto(texto)

        for i, fragmento in enumerate(fragmentos):
            chunk = {
                "chunk_id": f"{doc['id']}_{i:04d}",
                "doc_id": doc["id"],
                "chunk_index": i,
                "titulo": doc.get("titulo", ""),
                "data": doc.get("data", ""),
                "ano": doc.get("ano", ""),
                "fase": doc.get("fase", ""),
                "periodo_interpretativo": doc.get("periodo_interpretativo", ""),
                "genero": doc.get("genero", ""),
                "tema_principal": doc.get("tema_principal", ""),
                "temas": doc.get("temas", []),
                "fonte": doc.get("fonte", ""),
                "texto": fragmento,
                "caracteres": len(fragmento),
                "palavras_aprox": len(fragmento.split())
            }

            todos_chunks.append(chunk)

    OUTPUT.write_text(
        json.dumps(todos_chunks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Chunks criados.")
    print(f"Documentos processados: {len(corpus)}")
    print(f"Chunks totais: {len(todos_chunks)}")
    print(f"Ficheiro criado: {OUTPUT}")

    media_chars = sum(c["caracteres"] for c in todos_chunks) / len(todos_chunks)
    print(f"Tamanho médio dos chunks: {media_chars:.0f} caracteres")


if __name__ == "__main__":
    main()
