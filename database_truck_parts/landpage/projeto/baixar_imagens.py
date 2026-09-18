import os
import re
import requests
from PIL import Image
from io import BytesIO

# =========================================================
# CONFIGURAÇÕES
# =========================================================

API_KEY = "COLOQUE_SUA_CHAVE_DA_API_AQUI"

URL_API = "https://api.bing.microsoft.com/v7.0/images/search"

PASTA_IMAGENS = os.path.join("static", "imagens")

os.makedirs(PASTA_IMAGENS, exist_ok=True)


# =========================================================
# LISTA DAS 100 PEÇAS
# =========================================================

PECAS = [
    "Bomba D'Água",
    "Bomba de Óleo",
    "Bomba de Combustível",
    "Bomba Hidráulica",
    "Radiador",
    "Intercooler",
    "Ventoinha do Radiador",
    "Reservatório de Expansão",
    "Válvula Termostática",
    "Junta do Cabeçote",

    "Junta do Cárter",
    "Cárter do Motor",
    "Cabeçote do Motor",
    "Pistão do Motor",
    "Anel de Pistão",
    "Biela do Motor",
    "Virabrequim",
    "Comando de Válvulas",
    "Válvula de Admissão",
    "Válvula de Escape",

    "Correia do Motor",
    "Tensor da Correia",
    "Polia do Motor",
    "Compressor de Ar",
    "Filtro de Óleo",
    "Filtro de Ar",
    "Filtro de Combustível",
    "Filtro Separador de Água",
    "Filtro de Cabine",
    "Filtro Hidráulico",

    "Kit de Embreagem",
    "Disco de Embreagem",
    "Platô de Embreagem",
    "Rolamento de Embreagem",
    "Cilindro Mestre da Embreagem",
    "Cilindro Auxiliar da Embreagem",
    "Garfo da Embreagem",
    "Volante do Motor",
    "Retentor do Volante",
    "Atuador da Embreagem",

    "Pastilha de Freio",
    "Disco de Freio",
    "Tambor de Freio",
    "Lona de Freio",
    "Cilindro de Roda",
    "Válvula de Freio",
    "Câmara de Freio",
    "Compressor de Freio",
    "Válvula Reguladora",
    "Sensor ABS",

    "Amortecedor Dianteiro",
    "Amortecedor Traseiro",
    "Mola da Suspensão",
    "Bucha da Suspensão",
    "Pino de Mola",
    "Cubo de Roda",
    "Manga de Eixo",
    "Barra Estabilizadora",
    "Bucha da Barra Estabilizadora",
    "Suporte do Amortecedor",

    "Cruzeta do Cardan",
    "Eixo Cardan",
    "Rolamento do Cardan",
    "Flange do Cardan",
    "Diferencial",
    "Coroa e Pinhão",
    "Engrenagem do Câmbio",
    "Kit de Reparo do Câmbio",
    "Retentor do Câmbio",
    "Garfo de Câmbio",

    "Alternador",
    "Motor de Partida",
    "Bateria",
    "Sensor de Rotação",
    "Sensor de Temperatura",
    "Sensor de Pressão",
    "Relé Automotivo",
    "Chicote Elétrico",
    "Fusível",
    "Módulo Eletrônico",

    "Farol Principal",
    "Lanterna Traseira",
    "Farol de Neblina",
    "Lâmpada do Farol",
    "Lâmpada da Lanterna",
    "Luz de Posição",
    "Luz de Freio",
    "Refletor Lateral",
    "Soquete de Lâmpada",
    "Lente do Farol",

    "Retrovisor Externo",
    "Maçaneta da Porta",
    "Fechadura da Porta",
    "Dobradiça da Porta",
    "Vidro da Porta",
    "Máquina do Vidro",
    "Palheta do Limpador",
    "Braço do Limpador",
    "Grade Dianteira",
    "Para-choque Dianteiro"
]


# =========================================================
# TRANSFORMA O NOME DA PEÇA EM NOME DE ARQUIVO
# =========================================================

def nome_arquivo(nome):
    nome = nome.lower()

    substituicoes = {
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "é": "e",
        "ê": "e",
        "í": "i",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ú": "u",
        "ç": "c"
    }

    for antigo, novo in substituicoes.items():
        nome = nome.replace(antigo, novo)

    nome = re.sub(r"[^a-z0-9]+", "_", nome)

    return nome.strip("_") + ".jpg"


# =========================================================
# PESQUISA A IMAGEM
# =========================================================

def pesquisar_imagem(peca):

    consulta = f"{peca} Scania truck peça"

    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY
    }

    parametros = {
        "q": consulta,
        "count": 5,
        "safeSearch": "Strict",
        "imageType": "Photo"
    }

    try:

        resposta = requests.get(
            URL_API,
            headers=headers,
            params=parametros,
            timeout=15
        )

        resposta.raise_for_status()

        dados = resposta.json()

        resultados = dados.get("value", [])

        if not resultados:
            print(f"❌ Nenhuma imagem encontrada: {peca}")
            return None

        # Tenta as imagens até encontrar uma que funcione
        for resultado in resultados:

            url = resultado.get("contentUrl")

            if not url:
                continue

            try:

                imagem = requests.get(
                    url,
                    timeout=15,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                if imagem.status_code != 200:
                    continue

                return imagem.content

            except Exception:
                continue

        return None

    except Exception as erro:

        print(f"❌ Erro na pesquisa de {peca}: {erro}")

        return None


# =========================================================
# SALVA A IMAGEM
# =========================================================

def salvar_imagem(peca, dados):

    arquivo = nome_arquivo(peca)

    caminho = os.path.join(
        PASTA_IMAGENS,
        arquivo
    )

    try:

        imagem = Image.open(
            BytesIO(dados)
        )

        # Converte para RGB
        if imagem.mode != "RGB":
            imagem = imagem.convert("RGB")

        # Redimensiona para manter o catálogo leve
        imagem.thumbnail((1000, 1000))

        imagem.save(
            caminho,
            "JPEG",
            quality=90
        )

        print(f"✅ {peca} → {arquivo}")

        return caminho

    except Exception as erro:

        print(
            f"❌ Não foi possível salvar {peca}: {erro}"
        )

        return None


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

def main():

    print("=" * 60)
    print("TRUCK PARTS - DOWNLOAD AUTOMÁTICO DE IMAGENS")
    print("=" * 60)

    print(f"\nTotal de peças: {len(PECAS)}")
    print(f"Pasta: {PASTA_IMAGENS}\n")

    sucessos = 0
    erros = []

    for numero, peca in enumerate(PECAS, start=1):

        arquivo = nome_arquivo(peca)

        caminho = os.path.join(
            PASTA_IMAGENS,
            arquivo
        )

        # Não baixa novamente
        if os.path.exists(caminho):

            print(
                f"[{numero}/100] ⏭️ Já existe: {arquivo}"
            )

            sucessos += 1
            continue

        print(
            f"\n[{numero}/100] 🔎 Procurando: {peca}"
        )

        dados = pesquisar_imagem(peca)

        if dados:

            resultado = salvar_imagem(
                peca,
                dados
            )

            if resultado:
                sucessos += 1
            else:
                erros.append(peca)

        else:

            erros.append(peca)

    print("\n" + "=" * 60)
    print("FINALIZADO")
    print("=" * 60)

    print(f"Imagens salvas: {sucessos}")
    print(f"Erros: {len(erros)}")

    if erros:

        print("\nPeças que não tiveram imagem:")

        for peca in erros:
            print(f"- {peca}")


if __name__ == "__main__":
    main()