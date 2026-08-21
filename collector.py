import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DAS FONTES
# ============================================================

SOURCES = [
    # --- PESQUISA ---
    {
        "name": "MIT News — Materials Science",
        "url": "https://news.mit.edu/rss/topic/materials-science-and-engineering",
        "category": "research"
    },
    {
        "name": "MIT News — Materials Processing",
        "url": "https://news.mit.edu/rss/topic/materials-processing",
        "category": "research"
    },
    {
        "name": "NIMS Japan",
        "url": "https://www.nims.go.jp/eng/news/atom.xml",
        "category": "research"
    },
    {
        "name": "Tohoku University — Materials",
        "url": "https://www.tohoku.ac.jp/en/news/research/rss.xml",
        "category": "research"
    },
    {
        "name": "AGH — JCME",
        "url": "https://journals.agh.edu.pl/jcme/gateway/plugin/WebFeedGatewayPlugin/rss2",
        "category": "research"
    },
    {
        "name": "Silesian University of Technology",
        "url": "https://www.polsl.pl/en/feed/",
        "category": "research"
    },

    # --- INDÚSTRIA E MERCADO ---
    {
        "name": "World Steel Association",
        "url": "https://worldsteel.org/feed/",
        "category": "industry"
    },
    {
        "name": "EUROMETAL",
        "url": "https://eurometal.net/feed/",
        "category": "industry"
    },
    {
        "name": "Instituto Aço Brasil",
        "url": "https://acobrasil.org.br/site/feed/",
        "category": "industry"
    },
    {
        "name": "SteelOnTheNet",
        "url": "https://www.steelonthenet.com/feed/",
        "category": "industry"
    },
    {
        "name": "EUROFER",
        "url": "https://www.eurofer.eu/news/rss/",
        "category": "industry"
    },
    {
        "name": "European Commission — Trade",
        "url": "https://ec.europa.eu/trade/rss/",
        "category": "industry"
    }
]


# ============================================================
# TERMOS DE RELEVÂNCIA
# ============================================================

RELEVANCE_TERMS = {
    # Português
    "aço": 10,
    "siderurgia": 10,
    "siderúrgica": 10,
    "ferro fundido": 10,
    "minério": 5,
    "sucata": 5,

    # Aço
    "steel": 10,
    "steels": 10,
    "steelmaking": 10,
    "steel mill": 10,
    "steelworks": 10,
    "steel production": 10,

    # Ferro fundido
    "cast iron": 10,
    "ductile iron": 10,
    "nodular iron": 10,
    "gray iron": 10,
    "grey iron": 10,
    "white iron": 10,
    "malleable iron": 10,

    # Metalurgia
    "ferrous metallurgy": 8,
    "metallurgy": 8,
    "ironmaking": 8,
    "ferrous": 7,

    # Processos
    "blast furnace": 7,
    "electric arc furnace": 7,
    "eaf": 7,
    "bof": 7,
    "basic oxygen furnace": 7,
    "dri": 7,
    "hbi": 7,
    "rolling": 7,
    "casting": 7,
    "forging": 7,

    # Comportamento
    "creep": 7,
    "fatigue": 7,
    "fracture": 7,
    "embrittlement": 7,
    "wear": 7,
    "microstructure": 7,
    "corrosion": 6,

    # Tratamentos
    "heat treatment": 6,
    "quenching": 6,
    "tempering": 6,
    "annealing": 6,
    "normalizing": 6,

    # Ligas
    "stainless steel": 6,
    "alloy steel": 6,
    "low-alloy steel": 6,
    "high-alloy steel": 6,
    "tool steel": 6,
    "hsla": 6,
    "cr-mo": 6,
    "chromium steel": 5,
    "nickel steel": 5,

    # Indústria
    "steel plant": 6,
    "steel production": 6,
    "steel capacity": 6,
    "scrap": 5,
    "iron ore": 5,
}


# ============================================================
# TERMOS QUE REDUZEM A RELEVÂNCIA
# ============================================================

NEGATIVE_TERMS = {
    "ceramic": -10,
    "ceramics": -10,
    "polymer": -10,
    "polymers": -10,
    "plastic": -10,
    "plastics": -10,
    "composite": -10,
    "composites": -10,

    "biomaterial": -8,
    "biomaterials": -8,
    "tissue engineering": -8,
    "drug delivery": -8,

    "semiconductor": -8,
    "semiconductors": -8,
    "transistor": -8,
    "quantum computing": -8,

    "battery": -7,
    "batteries": -7,
    "lithium-ion": -7,
    "electrode": -7,
}


# ============================================================
# TERMOS DE "LERO-LERO"
# ============================================================

LOW_SERIOUSNESS_TERMS = {
    "award": -7,
    "prize": -7,
    "congratulations": -7,
    "celebrates": -6,
    "celebration": -6,
    "appointed": -6,
    "joins": -5,
    "graduation": -7,
    "students": -4,
    "scholarship": -5,
    "campus": -4,
    "alumni": -4,
    "professor receives": -7,
    "faculty award": -7,
    "new dean": -7,
    "commencement": -7,
}


# ============================================================
# TERMOS DE SERIEDADE
# ============================================================

SERIOUSNESS_TERMS = {
    # Inglês
    "million": 5,
    "billion": 6,
    "tonnes": 5,
    "tons": 5,
    "mt": 5,
    "investment": 6,
    "capacity": 6,
    "production": 5,
    "export": 5,
    "exports": 5,
    "import": 5,
    "imports": 5,
    "price": 5,
    "prices": 5,
    "tariff": 6,
    "tariffs": 6,
    "tax": 5,
    "ore": 5,
    "scrap": 5,
    "furnace": 5,
    "plant": 5,
    "steelworks": 6,
    "installed capacity": 6,
    "commercial production": 6,
    "contract": 5,
    "acquisition": 6,
    "merger": 6,
    "closure": 6,
    "expansion": 6,
    "construction": 5,
    "project": 4,
    "agreement": 4,
    "trade": 5,
    "market": 4,

    # Português
    "toneladas": 5,
    "investimento": 6,
    "produção": 5,
    "exportação": 5,
    "importação": 5,
    "preço": 5,
    "tarifa": 6,
    "imposto": 5,
    "usina": 5,
    "aquisição": 6,
    "fusão": 6,
    "expansão": 6,
    "construção": 5,
    "mercado": 4,
}


# ============================================================
# FUNÇÕES
# ============================================================

def normalize(text):
    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


def calculate_relevance(title, summary):
    text = normalize(title + " " + summary)

    score = 0

    for term, points in RELEVANCE_TERMS.items():
        if term in text:
            score += points

    for term, points in NEGATIVE_TERMS.items():
        if term in text:
            score += points

    return score


def calculate_seriousness(title, summary):
    text = normalize(title + " " + summary)

    score = 50

    for term, points in SERIOUSNESS_TERMS.items():
        if term in text:
            score += points

    for term, points in LOW_SERIOUSNESS_TERMS.items():
        if term in text:
            score += points

    return max(0, min(score, 100))


def fetch_feed(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Pagina-Inicial-News-Aggregator/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def get_text(element, names):
    for name in names:
        child = element.find(name)

        if child is not None and child.text:
            return child.text.strip()

    return ""


def parse_feed(data):
    root = ET.fromstring(data)

    articles = []

    # ========================================================
    # RSS
    # ========================================================

    for item in root.findall(".//item"):

        title = get_text(
            item,
            ["title"]
        )

        link = get_text(
            item,
            ["link"]
        )

        summary = get_text(
            item,
            [
                "description",
                "{http://purl.org/rss/1.0/modules/content/}encoded"
            ]
        )

        date = get_text(
            item,
            [
                "pubDate",
                "{http://purl.org/dc/elements/1.1/}date"
            ]
        )

        if title and link:

            articles.append({
                "title": title,
                "url": link,
                "summary": summary,
                "date": date
            })


    # ========================================================
    # ATOM
    # ========================================================

    atom_namespace = "{http://www.w3.org/2005/Atom}"

    for entry in root.findall(
        f".//{atom_namespace}entry"
    ):

        title_element = entry.find(
            f"{atom_namespace}title"
        )

        summary_element = entry.find(
            f"{atom_namespace}summary"
        )

        updated_element = entry.find(
            f"{atom_namespace}updated"
        )

        title = (
            title_element.text.strip()
            if title_element is not None
            and title_element.text
            else ""
        )

        summary = (
            summary_element.text.strip()
            if summary_element is not None
            and summary_element.text
            else ""
        )

        date = (
            updated_element.text.strip()
            if updated_element is not None
            and updated_element.text
            else ""
        )

        link = ""

        link_element = entry.find(
            f"{atom_namespace}link"
        )

        if link_element is not None:

            link = link_element.attrib.get(
                "href",
                ""
            )

        if title and link:

            articles.append({
                "title": title,
                "url": link,
                "summary": summary,
                "date": date
            })

    return articles


# ============================================================
# PROCESSAMENTO DA FONTE
# ============================================================

def process_source(source):

    print("")
    print("=" * 70)
    print(f"FONTE: {source['name']}")
    print(f"CATEGORIA: {source['category']}")
    print(f"URL: {source['url']}")
    print("-" * 70)

    try:

        data = fetch_feed(
            source["url"]
        )

        print("STATUS: acesso ao feed realizado com sucesso.")

    except Exception as error:

        print("STATUS: FALHA AO ACESSAR O FEED.")
        print(f"ERRO: {error}")

        return []


    try:

        raw_articles = parse_feed(data)

        print(
            f"ARTIGOS ENCONTRADOS NO FEED: "
            f"{len(raw_articles)}"
        )

    except Exception as error:

        print("STATUS: FALHA AO INTERPRETAR O FEED.")
        print(f"ERRO DE PARSING: {error}")

        return []


    processed = []

    discarded_relevance = 0

    # ========================================================
    # ANÁLISE DAS MATÉRIAS
    # ========================================================

    for article in raw_articles:

        relevance = calculate_relevance(
            article["title"],
            article["summary"]
        )

        seriousness = calculate_seriousness(
            article["title"],
            article["summary"]
        )

        # ----------------------------------------------------
        # FILTRO ATUAL
        # ----------------------------------------------------

        if relevance < 5:

            discarded_relevance += 1

            continue


        processed.append({

            "title": article["title"],

            "source": source["name"],

            "date": article["date"],

            "url": article["url"],

            "summary": article["summary"],

            "category": source["category"],

            "relevanceScore": relevance,

            "seriousnessScore": seriousness

        })


    # ========================================================
    # RESULTADO DO FILTRO
    # ========================================================

    print(
        f"MATÉRIAS APROVADAS: "
        f"{len(processed)}"
    )

    print(
        f"MATÉRIAS DESCARTADAS POR RELEVÂNCIA: "
        f"{discarded_relevance}"
    )

    # ========================================================
    # MOSTRA ALGUNS EXEMPLOS
    # ========================================================

    if processed:

        print("")
        print("EXEMPLOS DE MATÉRIAS APROVADAS:")

        # Mostra no máximo 5 para não poluir o log
        examples = sorted(
            processed,
            key=lambda article: (
                article["relevanceScore"],
                article["seriousnessScore"]
            ),
            reverse=True
        )[:5]

        for index, article in enumerate(
            examples,
            start=1
        ):

            print(
                f"{index}. "
                f"[R:{article['relevanceScore']} "
                f"S:{article['seriousnessScore']}] "
                f"{article['title']}"
            )

    elif raw_articles:

        print("")
        print(
            "ATENÇÃO: O feed possui matérias, "
            "mas TODAS foram descartadas pelo filtro."
        )

    else:

        print("")
        print(
            "ATENÇÃO: O feed foi acessado, "
            "mas nenhum artigo foi encontrado."
        )


    return processed


# ============================================================
# EXECUÇÃO
# ============================================================

def main():

    print("")
    print("=" * 70)
    print("METALLURGY DAILY — DIAGNÓSTICO DO COLETOR")
    print("=" * 70)
    print("")

    all_articles = []

    # --------------------------------------------------------
    # ESTATÍSTICAS POR FONTE
    # --------------------------------------------------------

    source_statistics = []

    # ========================================================
    # CONSULTA TODAS AS FONTES
    # ========================================================

    for source in SOURCES:

        articles = process_source(
            source
        )

        all_articles.extend(
            articles
        )

        source_statistics.append({

            "source": source["name"],

            "category": source["category"],

            "approved": len(articles)

        })


    # ========================================================
    # REMOVE DUPLICATAS
    # ========================================================

    unique = {}

    for article in all_articles:

        unique[article["url"]] = article


    all_articles = list(
        unique.values()
    )


    # ========================================================
    # ORDENAÇÃO
    # ========================================================

    all_articles.sort(

        key=lambda article: (

            article["relevanceScore"],

            article["seriousnessScore"]

        ),

        reverse=True

    )


    # ========================================================
    # SEPARAÇÃO POR CATEGORIA
    # ========================================================

    research = [

        article

        for article in all_articles

        if article["category"] == "research"

    ]


    industry = [

        article

        for article in all_articles

        if article["category"] == "industry"

    ]


    # ========================================================
    # RESUMO FINAL DO DIAGNÓSTICO
    # ========================================================

    print("")
    print("")
    print("=" * 70)
    print("RESUMO GERAL")
    print("=" * 70)

    print(
        f"TOTAL DE MATÉRIAS APROVADAS: "
        f"{len(all_articles)}"
    )

    print(
        f"PESQUISAS APROVADAS: "
        f"{len(research)}"
    )

    print(
        f"NOTÍCIAS DE INDÚSTRIA APROVADAS: "
        f"{len(industry)}"
    )

    print("")
    print("APROVAÇÕES POR FONTE:")
    print("-" * 70)


    # ========================================================
    # MOSTRA QUANTAS CADA FONTE FORNECEU
    # ========================================================

    for statistic in source_statistics:

        print(

            f"{statistic['source']}: "
            f"{statistic['approved']} "
            f"matérias aprovadas"

        )


    # ========================================================
    # DADOS PARA O SITE
    # ========================================================

    output = {

        "updatedAt":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "research":
            research[:30],

        "industry":
            industry[:30]

    }


    # ========================================================
    # SALVA ARTICLES.JSON
    # ========================================================

    output_path = Path(
        "data/articles.json"
    )

    output_path.write_text(

        json.dumps(
            output,
            ensure_ascii=False,
            indent=2
        ),

        encoding="utf-8"

    )


    # ========================================================
    # RESULTADO FINAL
    # ========================================================

    print("")
    print("=" * 70)
    print("ARQUIVO articles.json ATUALIZADO")
    print("=" * 70)

    print(
        f"Enviadas para o site: "
        f"{len(research[:30])} pesquisas e "
        f"{len(industry[:30])} notícias."
    )

    print("")
    print("DIAGNÓSTICO CONCLUÍDO.")
    print("=" * 70)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":
    main()
