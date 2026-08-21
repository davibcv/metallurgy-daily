import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# METALLURGY DAILY
# COLLECTOR
# ============================================================


# ============================================================
# CONFIGURAÇÃO DAS FONTES
# ============================================================

SOURCES = [

    # --------------------------------------------------------
    # PESQUISA
    # --------------------------------------------------------

    {
        "name": "MIT News — Materials Science",
        "url": "https://news.mit.edu/rss/topic/materials-science-and-engineering",
        "category": "research",
        "mode": "rss"
    },

    {
        "name": "MIT News — Materials Processing",
        "url": "https://news.mit.edu/rss/topic/materials-processing",
        "category": "research",
        "mode": "rss"
    },

    {
        "name": "NIMS Japan",
        "url": "https://www.nims.go.jp/eng/siteinfo/rss-feed.html",
        "category": "research",
        "mode": "discover"
    },

    {
        "name": "Tohoku University — Materials",
        "url": "https://www.tohoku.ac.jp/en/news/research/index.html",
        "category": "research",
        "mode": "discover"
    },

    {
        "name": "AGH — JCME",
        "url": "https://journals.agh.edu.pl/jcme/gateway/plugin/WebFeedGatewayPlugin/rss2",
        "category": "research",
        "mode": "rss"
    },

    {
        "name": "Silesian University of Technology",
        "url": "https://www.polsl.pl/en/feed/",
        "category": "research",
        "mode": "rss"
    },


    # --------------------------------------------------------
    # INDÚSTRIA E MERCADO
    # --------------------------------------------------------

    {
        "name": "World Steel Association",
        "url": "https://worldsteel.org/feed/",
        "category": "industry",
        "mode": "rss"
    },

    {
        "name": "EUROMETAL",
        "url": "https://eurometal.net/feed/",
        "category": "industry",
        "mode": "rss"
    },

    {
        "name": "Instituto Aço Brasil",
        "url": "https://acobrasil.org.br/site/feed/",
        "category": "industry",
        "mode": "rss"
    },

    {
        "name": "SteelOnTheNet",
        "url": "https://www.steelonthenet.com/steel-industry-feeds.php",
        "category": "industry",
        "mode": "discover"
    },

    {
        "name": "EUROFER",
        "url": "https://www.eurofer.eu/",
        "category": "industry",
        "mode": "discover"
    },

    {
        "name": "European Commission — Trade",
        "url": "https://policy.trade.ec.europa.eu/",
        "category": "industry",
        "mode": "discover"
    }
]


# ============================================================
# TERMOS DE RELEVÂNCIA
# ============================================================

RELEVANCE_TERMS = {

    "aço": 10,
    "siderurgia": 10,
    "siderúrgica": 10,
    "ferro fundido": 10,
    "minério": 5,
    "sucata": 5,

    "steel": 10,
    "steels": 10,
    "steelmaking": 10,
    "steel mill": 10,
    "steelworks": 10,
    "steel production": 10,

    "cast iron": 10,
    "ductile iron": 10,
    "nodular iron": 10,
    "gray iron": 10,
    "grey iron": 10,
    "white iron": 10,
    "malleable iron": 10,

    "ferrous metallurgy": 8,
    "metallurgy": 8,
    "ironmaking": 8,
    "ferrous": 7,

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

    "creep": 7,
    "fatigue": 7,
    "fracture": 7,
    "embrittlement": 7,
    "wear": 7,
    "microstructure": 7,
    "corrosion": 6,

    "heat treatment": 6,
    "quenching": 6,
    "tempering": 6,
    "annealing": 6,
    "normalizing": 6,

    "stainless steel": 6,
    "alloy steel": 6,
    "low-alloy steel": 6,
    "high-alloy steel": 6,
    "tool steel": 6,
    "hsla": 6,
    "cr-mo": 6,
    "chromium steel": 5,
    "nickel steel": 5,

    "steel plant": 6,
    "steel production": 6,
    "steel capacity": 6,
    "scrap": 5,
    "iron ore": 5,
}


# ============================================================
# TERMOS NEGATIVOS
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
# LERO-LERO
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
# SERIEDADE
# ============================================================

SERIOUSNESS_TERMS = {

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
# NORMALIZAÇÃO
# ============================================================

def normalize(text):

    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


# ============================================================
# RELEVÂNCIA
# ============================================================

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


# ============================================================
# SERIEDADE
# ============================================================

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


# ============================================================
# ACESSO HTTP
# ============================================================

def fetch_url(url):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
                "Mozilla/5.0 "
                "(compatible; MetallurgyDaily/1.0; "
                "+https://github.com/davibcv/metallurgy-daily)"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=20
    ) as response:

        return response.read()


# ============================================================
# DESCOBERTA AUTOMÁTICA DE RSS / ATOM
# ============================================================

def discover_feeds(page_url):

    print("  Procurando feeds RSS/Atom na página oficial...")

    try:

        data = fetch_url(page_url)

        html = data.decode(
            "utf-8",
            errors="ignore"
        )

    except Exception as error:

        print(
            f"  ERRO ao acessar página de descoberta: {error}"
        )

        return []


    feeds = []


    # --------------------------------------------------------
    # Procura tags:
    #
    # <link rel="alternate"
    #       type="application/rss+xml"
    #       href="...">
    #
    # ou Atom
    # --------------------------------------------------------

    pattern = re.compile(
        r'<link[^>]+'
        r'(?:rel=["\']alternate["\'][^>]*'
        r'type=["\'](?:application/rss\+xml|application/atom\+xml)["\']'
        r'[^>]*|'
        r'type=["\'](?:application/rss\+xml|application/atom\+xml)["\']'
        r'[^>]*rel=["\']alternate["\'][^>]*)'
        r'[^>]*href=["\']([^"\']+)["\']',
        re.IGNORECASE
    )

    matches = pattern.findall(html)

    for href in matches:

        full_url = urllib.parse.urljoin(
            page_url,
            href
        )

        if full_url not in feeds:
            feeds.append(full_url)


    # --------------------------------------------------------
    # Fallback: procura URLs que parecem feeds
    # --------------------------------------------------------

    if not feeds:

        url_pattern = re.compile(
            r'href=["\']([^"\']*(?:rss|feed|atom)[^"\']*)["\']',
            re.IGNORECASE
        )

        matches = url_pattern.findall(html)

        for href in matches:

            full_url = urllib.parse.urljoin(
                page_url,
                href
            )

            if full_url not in feeds:
                feeds.append(full_url)


    print(
        f"  Feeds candidatos encontrados: {len(feeds)}"
    )

    for feed in feeds[:10]:
        print(f"    → {feed}")

    return feeds


# ============================================================
# OBTÉM O FEED
# ============================================================

def get_feed_data(source):

    if source["mode"] == "rss":

        print(
            "  Usando URL RSS configurada diretamente."
        )

        return fetch_url(source["url"])


    if source["mode"] == "discover":

        candidates = discover_feeds(
            source["url"]
        )

        if not candidates:

            raise Exception(
                "Nenhum feed RSS/Atom encontrado "
                "automaticamente."
            )


        # ----------------------------------------------------
        # Testa os candidatos até encontrar XML válido
        # ----------------------------------------------------

        for feed_url in candidates:

            try:

                print(
                    f"  Testando feed: {feed_url}"
                )

                data = fetch_url(feed_url)

                ET.fromstring(data)

                print(
                    f"  FEED VÁLIDO ENCONTRADO: "
                    f"{feed_url}"
                )

                return data

            except Exception as error:

                print(
                    f"  Feed rejeitado: {error}"
                )


        raise Exception(
            "Foram encontrados candidatos, "
            "mas nenhum retornou XML válido."
        )


    raise Exception(
        f"Modo desconhecido: {source['mode']}"
    )


# ============================================================
# EXTRAÇÃO DE TEXTO
# ============================================================

def get_text(element, names):

    for name in names:

        child = element.find(name)

        if child is not None and child.text:

            return child.text.strip()

    return ""


# ============================================================
# PARSER RSS / ATOM
# ============================================================

def parse_feed(data):

    root = ET.fromstring(data)

    articles = []


    # --------------------------------------------------------
    # RSS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # ATOM
    # --------------------------------------------------------

    atom_namespace = (
        "{http://www.w3.org/2005/Atom}"
    )


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

    print()
    print("=" * 70)
    print(f"FONTE: {source['name']}")
    print(f"CATEGORIA: {source['category']}")
    print(f"MODO: {source['mode']}")
    print(f"PÁGINA/URL: {source['url']}")
    print("-" * 70)


    # --------------------------------------------------------
    # ACESSO
    # --------------------------------------------------------

    try:

        data = get_feed_data(source)

        print(
            "STATUS: feed obtido com sucesso."
        )

    except Exception as error:

        print(
            "STATUS: FALHA AO OBTER FEED."
        )

        print(
            f"ERRO: {error}"
        )

        return []


    # --------------------------------------------------------
    # PARSING
    # --------------------------------------------------------

    try:

        raw_articles = parse_feed(data)

        print(
            "STATUS: parsing realizado com sucesso."
        )

        print(
            f"ARTIGOS ENCONTRADOS: "
            f"{len(raw_articles)}"
        )

    except Exception as error:

        print(
            "STATUS: FALHA AO INTERPRETAR FEED."
        )

        print(
            f"ERRO DE PARSING: {error}"
        )

        return []


    # --------------------------------------------------------
    # FILTRO
    # --------------------------------------------------------

    processed = []

    discarded = []


    for article in raw_articles:

        relevance = calculate_relevance(
            article["title"],
            article["summary"]
        )

        seriousness = calculate_seriousness(
            article["title"],
            article["summary"]
        )


        if relevance < 5:

            discarded.append({

                "title": article["title"],
                "relevance": relevance,
                "seriousness": seriousness

            })

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


    # --------------------------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------------------------

    print(
        f"MATÉRIAS APROVADAS: "
        f"{len(processed)}"
    )

    print(
        f"MATÉRIAS DESCARTADAS: "
        f"{len(discarded)}"
    )


    if discarded:

        discarded.sort(
            key=lambda article: (
                article["relevance"],
                article["seriousness"]
            ),
            reverse=True
        )


        print()
        print(
            "PRINCIPAIS MATÉRIAS DESCARTADAS:"
        )


        for index, article in enumerate(
            discarded[:10],
            start=1
        ):

            print(
                f"{index}. "
                f"[R:{article['relevance']} "
                f"S:{article['seriousness']}] "
                f"{article['title']}"
            )


    if processed:

        print()
        print(
            "EXEMPLOS DE MATÉRIAS APROVADAS:"
        )


        for index, article in enumerate(
            processed[:5],
            start=1
        ):

            print(
                f"{index}. "
                f"[R:{article['relevanceScore']} "
                f"S:{article['seriousnessScore']}] "
                f"{article['title']}"
            )


    return processed


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():

    print()
    print("=" * 70)
    print(
        "METALLURGY DAILY — COLETOR"
    )
    print("=" * 70)


    all_articles = []


    source_statistics = []


    # --------------------------------------------------------
    # CONSULTA TODAS AS FONTES
    # --------------------------------------------------------

    for source in SOURCES:

        articles = process_source(
            source
        )

        all_articles.extend(
            articles
        )

        source_statistics.append({

            "source": source["name"],
            "approved": len(articles)

        })


    # --------------------------------------------------------
    # REMOVE DUPLICATAS
    # --------------------------------------------------------

    unique = {}


    for article in all_articles:

        unique[article["url"]] = article


    all_articles = list(
        unique.values()
    )


    # --------------------------------------------------------
    # ORDENAÇÃO
    # --------------------------------------------------------

    all_articles.sort(

        key=lambda article: (

            article["relevanceScore"],
            article["seriousnessScore"]

        ),

        reverse=True

    )


    # --------------------------------------------------------
    # SEPARAÇÃO
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SAÍDA
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "RESUMO FINAL"
    )
    print("=" * 70)


    print(
        f"TOTAL APROVADO: "
        f"{len(all_articles)}"
    )

    print(
        f"PESQUISAS: "
        f"{len(research)}"
    )

    print(
        f"INDÚSTRIA: "
        f"{len(industry)}"
    )


    print()
    print(
        "APROVAÇÕES POR FONTE:"
    )

    print("-" * 70)


    for statistic in source_statistics:

        print(
            f"{statistic['source']}: "
            f"{statistic['approved']}"
        )


    print()
    print("=" * 70)
    print(
        "articles.json ATUALIZADO"
    )
    print("=" * 70)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
