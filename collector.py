import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from collections import defaultdict
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO GERAL
# ============================================================

# Quantas publicações MAIS RECENTES de cada fonte serão analisadas.
#
# Isso evita recalcular relevância/seriedade de dezenas de matérias
# antigas de fontes que publicam com pouca frequência.
#
# Para alterar no futuro, basta mudar este número.
MAX_ARTICLES_PER_SOURCE = 5


# ============================================================
# CONFIGURAÇÃO DAS FONTES (PURIFICADA E BLINDADA)
# ============================================================

SOURCES = [

    # ========================================================
    # PESQUISA
    # ========================================================

    {
        "name": "MIT News — Materials Science",
        "url": "https://news.mit.edu/rss/topic/materials-science-and-engineering",
        "category": "research",
        "country": "us"
    },

    {
        "name": "MIT News — Materials Processing",
        "url": "https://news.mit.edu/rss/topic/materials-processing",
        "category": "research",
        "country": "us"
    },

    {
        "name": "AGH — JCME",
        "url": "https://journals.agh.edu.pl/jcme/gateway/plugin/WebFeedGatewayPlugin/rss2",
        "category": "research",
        "country": "pl"
    },

    {
        "name": "Silesian University of Technology",
        "url": "https://www.polsl.pl/en/feed/",
        "category": "research",
        "country": "pl"
    },

    {
        "name": "MDPI — Metals",
        "url": "https://www.mdpi.com/rss/journal/metals",
        "category": "research",
        "country": "ch"
    },

    {
        "name": "MDPI — Materials",
        "url": "https://www.mdpi.com/rss/journal/materials",
        "category": "research",
        "country": "ch"
    },

    {
        "name": "SciELO — Materials Research",
        "url": "https://www.scielo.br/rss.php?pid=1516-1439&lang=en",
        "category": "research",
        "country": "br"
    },

    {
        "name": "Nature — Materials",
        "url": "https://www.nature.com/nmat.rss",
        "category": "research",
        "country": "gb"
    },

    {
        "name": "ScienceDaily — Materials Science",
        "url": "https://www.sciencedaily.com/rss/matter_energy/materials_science.xml",
        "category": "research",
        "country": "us"
    },

    {
        "name": "Springer — Metallurgical",
        "url": "https://link.springer.com/journal/11661.rss",
        "category": "research",
        "country": "de"
    },


    # ========================================================
    # INDÚSTRIA E MERCADO — FONTES ATUAIS
    # ========================================================

    {
        "name": "World Steel Association",
        "url": "https://worldsteel.org/feed/",
        "category": "industry",
        "country": "be"
    },

    {
        "name": "Instituto Aço Brasil",
        "url": "https://acobrasil.org.br/site/feed/",
        "category": "industry",
        "country": "br"
    },

    {
        "name": "Mining.com — Iron Ore",
        "url": "https://www.mining.com/commodity/iron-ore/feed/",
        "category": "industry",
        "country": "ca"
    },

    {
        "name": "MetalMiner",
        "url": "https://agmetalminer.com/feed/",
        "category": "industry",
        "country": "us"
    },

    {
        "name": "Hellenic Shipping News",
        "url": "https://www.hellenicshippingnews.com/category/commodities/steel-iron/feed/",
        "category": "industry",
        "country": "gr"
    },

    {
        "name": "UK Gov — Business & Trade",
        "url": "https://www.gov.uk/search/news-and-communications.atom?organisations[]=department-for-business-and-trade",
        "category": "industry",
        "country": "gb"
    },

    {
        "name": "US Department of Commerce",
        "url": "https://www.commerce.gov/rss.xml",
        "category": "industry",
        "country": "us"
    },

    {
        "name": "US International Trade Commission",
        "url": "https://www.usitc.gov/press_room/news_release.xml",
        "category": "industry",
        "country": "us"
    },

    {
        "name": "World Economic Forum",
        "url": "https://www.weforum.org/agenda/trade-and-investment/feed",
        "category": "industry",
        "country": "ch"
    },

    {
        "name": "Bnamericas — Mineração e Metais",
        "url": "https://www.bnamericas.com/rss/mining.xml",
        "category": "industry",
        "country": "cl"
    },


    # ========================================================
    # GOVERNOS E INSTITUIÇÕES
    # GEOPOLÍTICA, COMÉRCIO E POLÍTICA INDUSTRIAL
    # ========================================================

    {
        "name": "EU Council — Press Releases",
        "url": "https://www.consilium.europa.eu/en/press/press-releases/rss",
        "category": "industry",
        "country": "eu"
    },

    {
        "name": "EU Commission — Economy & Finance",
        "url": "https://ec.europa.eu/commission/presscorner/api/rss?language=en&theme=Economy%20and%20Finance",
        "category": "industry",
        "country": "eu"
    },

    {
        "name": "France Ministère de l'Économie",
        "url": "https://www.economie.gouv.fr/flux-rss/presse",
        "category": "industry",
        "country": "fr"
    },

    {
        "name": "Italy MIMIT (Ministério da Indústria)",
        "url": "https://www.mimit.gov.it/it/notizie-stampa?format=feed&type=rss",
        "category": "industry",
        "country": "it"
    },

    {
        "name": "Sweden Government Offices",
        "url": "https://www.government.se/rss.xml",
        "category": "industry",
        "country": "se"
    },

    {
        "name": "Brasil MDIC",
        "url": "https://www.gov.br/mdic/pt-br/assuntos/noticias/RSS",
        "category": "industry",
        "country": "br"
    },

    {
        "name": "Australia Dept of Industry",
        "url": "https://www.industry.gov.au/rss.xml",
        "category": "industry",
        "country": "au"
    },

    {
        "name": "OECD Newsroom",
        "url": "https://www.oecd.org/en/rss/newsroom.xml",
        "category": "industry",
        "country": "fr"
    },


    # ========================================================
    # GIGANTES SIDERÚRGICAS
    # IMPACTO CORPORATIVO E INDUSTRIAL
    # ========================================================

    {
        "name": "ArcelorMittal",
        "url": "https://corporate.arcelormittal.com/media/press-releases/rss",
        "category": "industry",
        "country": "lu"
    },

    {
        "name": "voestalpine",
        "url": "https://www.voestalpine.com/blog/en/feed/",
        "category": "industry",
        "country": "at"
    },

    {
        "name": "Gerdau (RI)",
        "url": "https://ri.gerdau.com/rss/",
        "category": "industry",
        "country": "br"
    },

    {
        "name": "POSCO",
        "url": "https://newsroom.posco.com/en/feed/",
        "category": "industry",
        "country": "kr"
    },

    {
        "name": "Baowu Group",
        "url": "https://www.baowugroup.com/en/feed",
        "category": "industry",
        "country": "cn"
    },


    # ========================================================
    # MERCADO GLOBAL PESADO
    # COMMODITIES, PREÇOS E COMÉRCIO
    # ========================================================

    {
        "name": "S&P Global Platts — Metals",
        "url": "https://www.spglobal.com/commodityinsights/en/rss/metals",
        "category": "industry",
        "country": "us"
    },

    {
        "name": "Kallanish Iron & Steel",
        "url": "https://www.kallanish.com/en/news/steel/feed/",
        "category": "industry",
        "country": "gb"
    }

]


# ============================================================
# TERMOS DE RELEVÂNCIA
# ============================================================

RELEVANCE_TERMS = {

    # Aço / ferro
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

    # Propriedades / fenômenos
    "creep": 7,
    "fatigue": 7,
    "fracture": 7,
    "embrittlement": 7,
    "wear": 7,
    "microstructure": 7,
    "corrosion": 6,

    # Tratamentos térmicos
    "heat treatment": 6,
    "quenching": 6,
    "tempering": 6,
    "annealing": 6,
    "normalizing": 6,

    # Aços específicos
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
# TERMOS DE BAIXA SERIEDADE
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

    # Escala / dinheiro
    "million": 5,
    "billion": 6,
    "tonnes": 5,
    "tons": 5,
    "mt": 5,

    # Produção / capacidade
    "investment": 6,
    "capacity": 6,
    "production": 5,

    # Comércio
    "export": 5,
    "exports": 5,
    "import": 5,
    "imports": 5,
    "price": 5,
    "prices": 5,
    "tariff": 6,
    "tariffs": 6,
    "tax": 5,

    # Matérias-primas / siderurgia
    "ore": 5,
    "scrap": 5,
    "furnace": 5,
    "plant": 5,
    "steelworks": 6,
    "installed capacity": 6,
    "commercial production": 6,

    # Negócios
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
# FUNÇÕES DE PROCESSAMENTO E CONVERSÃO DE DATAS
# ============================================================

def normalize(text):

    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip().lower()


def calculate_relevance(title, summary):

    text = normalize(
        title + " " + summary
    )

    score = sum(
        points
        for term, points in RELEVANCE_TERMS.items()
        if term in text
    )

    score += sum(
        points
        for term, points in NEGATIVE_TERMS.items()
        if term in text
    )

    return score


def calculate_seriousness(title, summary):

    text = normalize(
        title + " " + summary
    )

    score = 50

    score += sum(
        points
        for term, points in SERIOUSNESS_TERMS.items()
        if term in text
    )

    score += sum(
        points
        for term, points in LOW_SERIOUSNESS_TERMS.items()
        if term in text
    )

    return max(
        0,
        min(score, 100)
    )


def parse_date(date_str):
    """
    Converte o texto da data do RSS/Atom
    para um objeto datetime.
    """

    if not date_str:
        return datetime.min.replace(
            tzinfo=timezone.utc
        )

    # RSS / RFC 2822
    try:

        parsed = parsedate_to_datetime(
            date_str
        )

        if parsed.tzinfo is None:

            parsed = parsed.replace(
                tzinfo=timezone.utc
            )

        return parsed

    except Exception:
        pass

    # Atom / ISO 8601
    try:

        clean_date = date_str.replace(
            "Z",
            "+00:00"
        )

        parsed = datetime.fromisoformat(
            clean_date
        )

        if parsed.tzinfo is None:

            parsed = parsed.replace(
                tzinfo=timezone.utc
            )

        return parsed

    except Exception:
        pass

    return datetime.min.replace(
        tzinfo=timezone.utc
    )


# ============================================================
# OBTENÇÃO DOS FEEDS (COM DISFARCE ANTIBOT)
# ============================================================

def fetch_feed(url):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept":
                "application/rss+xml, application/xml, text/xml, */*"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=20
    ) as response:

        return response.read()


# ============================================================
# LEITURA DOS CAMPOS XML
# ============================================================

def get_text(element, names):

    for name in names:

        child = element.find(name)

        if (
            child is not None
            and child.text
        ):

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

            articles.append(
                {
                    "title": title,
                    "url": link,
                    "summary": summary,
                    "date": date
                }
            )


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
            if (
                title_element is not None
                and title_element.text
            )
            else ""
        )

        summary = (
            summary_element.text.strip()
            if (
                summary_element is not None
                and summary_element.text
            )
            else ""
        )

        date = (
            updated_element.text.strip()
            if (
                updated_element is not None
                and updated_element.text
            )
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

            articles.append(
                {
                    "title": title,
                    "url": link,
                    "summary": summary,
                    "date": date
                }
            )

    return articles


# ============================================================
# SELEÇÃO DAS PUBLICAÇÕES MAIS RECENTES
# ============================================================

def get_latest_articles(articles, limit):
    """
    Mantém somente as publicações mais recentes
    de uma fonte antes de calcular relevância e seriedade.

    Isso evita processar dezenas de matérias antigas
    de fontes que publicam com baixa frequência.
    """

    if not articles:
        return []

    # Ordena pelas datas reais.
    # O sort é estável, portanto, se alguma fonte não
    # fornecer datas válidas, a ordem original do feed
    # continua sendo preservada entre essas matérias.
    articles.sort(
        key=lambda article: parse_date(
            article["date"]
        ),
        reverse=True
    )

    return articles[:limit]


# ============================================================
# PROCESSAMENTO DE CADA FONTE
# ============================================================

def process_source(source):

    print(
        "\n======================================================================"
    )

    print(
        f"FONTE: {source['name']}"
    )

    print(
        f"URL: {source['url']}"
    )

    print(
        f"LIMITANDO ANÁLISE ÀS "
        f"{MAX_ARTICLES_PER_SOURCE} PUBLICAÇÕES MAIS RECENTES"
    )

    try:

        data = fetch_feed(
            source["url"]
        )

        raw_articles = parse_feed(
            data
        )

    except Exception as error:

        print(
            f"STATUS: FALHA AO ACESSAR O FEED. "
            f"Erro: {error}"
        )

        return []


    print(
        f"PUBLICAÇÕES ENCONTRADAS NO FEED: "
        f"{len(raw_articles)}"
    )


    # --------------------------------------------------------
    # NOVA OTIMIZAÇÃO:
    # somente as 5 mais recentes entram no filtro
    # --------------------------------------------------------

    latest_articles = get_latest_articles(
        raw_articles,
        MAX_ARTICLES_PER_SOURCE
    )


    print(
        f"PUBLICAÇÕES ANALISADAS: "
        f"{len(latest_articles)}"
    )


    processed = []

    for article in latest_articles:

        relevance = calculate_relevance(
            article["title"],
            article["summary"]
        )

        seriousness = calculate_seriousness(
            article["title"],
            article["summary"]
        )


        # ----------------------------------------------------
        # FILTRO DE RELEVÂNCIA
        # ----------------------------------------------------

        if relevance < 5:

            continue


        processed.append(
            {
                "title": article["title"],
                "source": source["name"],
                "date": article["date"],
                "url": article["url"],
                "summary": article["summary"],
                "category": source["category"],
                "country": source.get(
                    "country",
                    ""
                ),
                "relevanceScore": relevance,
                "seriousnessScore": seriousness
            }
        )


    print(
        f"MATÉRIAS APROVADAS PELO FILTRO: "
        f"{len(processed)}"
    )

    return processed


# ============================================================
# ALGORITMO DE DISTRIBUIÇÃO E DIVERSIDADE
# ============================================================

def distribute_articles(
    articles_list,
    max_per_source=2
):

    if not articles_list:
        return []


    # --------------------------------------------------------
    # 1. Cria campo de data real
    # --------------------------------------------------------

    for article in articles_list:

        article["_parsed_date"] = parse_date(
            article["date"]
        )


    # --------------------------------------------------------
    # 2. Ordem temporal
    #
    # Data é o critério principal.
    # Relevância e seriedade servem como desempate.
    # --------------------------------------------------------

    articles_list.sort(
        key=lambda x: (
            x["_parsed_date"],
            x["relevanceScore"],
            x["seriousnessScore"]
        ),
        reverse=True
    )


    # --------------------------------------------------------
    # 3. Agrupa por fonte
    # --------------------------------------------------------

    grouped = defaultdict(list)

    for article in articles_list:

        grouped[
            article["source"]
        ].append(article)


    # --------------------------------------------------------
    # 4. Fonte com matéria mais nova começa
    # --------------------------------------------------------

    ordered_sources = sorted(
        grouped.keys(),
        key=lambda source:
            grouped[source][0]["_parsed_date"],
        reverse=True
    )


    distributed = []


    # --------------------------------------------------------
    # 5. Round-Robin
    #
    # Cada fonte fornece no máximo 2 matérias
    # antes de passar a vez para as demais.
    # --------------------------------------------------------

    while ordered_sources:

        next_round_sources = []

        for source in ordered_sources:

            chunk = grouped[source][
                :max_per_source
            ]

            grouped[source] = grouped[source][
                max_per_source:
            ]

            distributed.extend(
                chunk
            )

            if grouped[source]:

                next_round_sources.append(
                    source
                )

        ordered_sources = (
            next_round_sources
        )


    # --------------------------------------------------------
    # Remove campo temporário
    # --------------------------------------------------------

    for article in distributed:

        del article["_parsed_date"]


    return distributed


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():

    all_articles = []


    # --------------------------------------------------------
    # Processa todas as fontes
    # --------------------------------------------------------

    for source in SOURCES:

        articles = process_source(
            source
        )

        all_articles.extend(
            articles
        )


    # --------------------------------------------------------
    # Remove duplicatas exatas de URL
    # --------------------------------------------------------

    unique = {
        article["url"]: article
        for article in all_articles
    }

    all_articles = list(
        unique.values()
    )


    print(
        "\n======================================================================"
    )

    print(
        f"TOTAL DE MATÉRIAS APROVADAS "
        f"ANTES DA DISTRIBUIÇÃO: "
        f"{len(all_articles)}"
    )


    # --------------------------------------------------------
    # Separa pesquisa e indústria
    # --------------------------------------------------------

    research_raw = [
        article
        for article in all_articles
        if article["category"] == "research"
    ]

    industry_raw = [
        article
        for article in all_articles
        if article["category"] == "industry"
    ]


    # --------------------------------------------------------
    # Distribuição cronológica + diversidade
    # --------------------------------------------------------

    research = distribute_articles(
        research_raw,
        max_per_source=2
    )

    industry = distribute_articles(
        industry_raw,
        max_per_source=2
    )


    # --------------------------------------------------------
    # Saída final
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


    # --------------------------------------------------------
    # Grava articles.json
    # --------------------------------------------------------

    output_path = Path(
        "data/articles.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
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
    # Resumo final
    # --------------------------------------------------------

    print(
        "\n======================================================================"
    )

    print(
        "CONCLUÍDO."
    )

    print(
        f"Enviadas "
        f"{len(output['research'])} pesquisas "
        f"e "
        f"{len(output['industry'])} notícias estruturadas."
    )

    print(
        f"Limite analisado por fonte: "
        f"{MAX_ARTICLES_PER_SOURCE} publicações."
    )

    print(
        "======================================================================"
    )


# ============================================================
# INÍCIO
# ============================================================

if __name__ == "__main__":

    main()
