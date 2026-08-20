/* =========================================================
   METALLURGY DAILY
   JAVASCRIPT PRINCIPAL
========================================================= */


/* =========================================================
   DADOS DE TESTE
========================================================= */

const researchArticles = [

    {
        category: "Pesquisa",
        source: "MIT",
        title: "Nova abordagem para compreender o comportamento de aços de baixa liga",
        date: "Hoje",
        description:
            "Pesquisadores investigam mecanismos relacionados ao comportamento mecânico e microestrutural de aços de baixa liga.",
        image: "Pesquisa MIT",
        body:
            "Esta é uma matéria de demonstração. Posteriormente, o conteúdo será substituído automaticamente por pesquisas reais provenientes das fontes selecionadas.",
        url: "https://news.mit.edu/"
    },


    {
        category: "Pesquisa",
        source: "University of Limerick",
        title: "Estudo analisa novas possibilidades para materiais metálicos estruturais",
        date: "Hoje",
        description:
            "Pesquisa recente relacionada ao desenvolvimento e caracterização de materiais metálicos.",
        image: "Pesquisa UL",
        body:
            "Conteúdo de demonstração do Metallurgy Daily. O sistema posteriormente buscará automaticamente pesquisas relevantes.",
        url: "https://www.ul.ie/"
    },


    {
        category: "Pesquisa",
        source: "Nagoya University",
        title: "Pesquisa investiga propriedades de materiais metálicos avançados",
        date: "Ontem",
        description:
            "Estudo envolvendo propriedades, processamento e desempenho de materiais metálicos.",
        image: "Pesquisa Nagoya",
        body:
            "Conteúdo de demonstração. Esta área será alimentada posteriormente por fontes reais.",
        url: "https://www.nagoya-u.ac.jp/en/"
    },


    {
        category: "Pesquisa",
        source: "Politehnica University of Bucharest",
        title: "Novo estudo sobre processamento e desempenho de ligas metálicas",
        date: "Ontem",
        description:
            "Pesquisa relacionada ao processamento de materiais metálicos.",
        image: "Pesquisa UPB",
        body:
            "Conteúdo provisório do sistema.",
        url: "https://upb.ro/"
    },


    {
        category: "Pesquisa",
        source: "Poland",
        title: "Investigação sobre microestrutura e propriedades de aços",
        date: "2 dias atrás",
        description:
            "Estudo sobre relações entre processamento, microestrutura e propriedades mecânicas.",
        image: "Pesquisa Polônia",
        body:
            "Conteúdo provisório.",
        url: "https://www.gov.pl/"
    }

];



const industryArticles = [

    {
        category: "Indústria",
        source: "World Steel Association",
        title: "Produção mundial de aço apresenta novas movimentações",
        date: "Hoje",
        description:
            "Informações recentes sobre produção e tendências da indústria siderúrgica mundial.",
        image: "Indústria do aço",
        body:
            "Conteúdo de demonstração. Posteriormente esta seção será alimentada automaticamente por portais especializados.",
        url: "https://worldsteel.org/"
    },


    {
        category: "Geopolítica",
        source: "Europa",
        title: "Novos movimentos comerciais afetam o mercado internacional do aço",
        date: "Hoje",
        description:
            "Mudanças regulatórias e comerciais podem alterar os fluxos internacionais de produtos siderúrgicos.",
        image: "Mercado do aço",
        body:
            "Conteúdo de demonstração.",
        url: "https://policy.trade.ec.europa.eu/"
    },


    {
        category: "Indústria",
        source: "Japão",
        title: "Mercado japonês de aço acompanha mudanças na demanda industrial",
        date: "Ontem",
        description:
            "O setor siderúrgico japonês observa mudanças em segmentos consumidores de aço.",
        image: "Aço no Japão",
        body:
            "Conteúdo provisório.",
        url: "https://www.jisf.or.jp/en/"
    },


    {
        category: "Mineração",
        source: "Global",
        title: "Mercado de minério de ferro influencia perspectivas para a siderurgia",
        date: "Ontem",
        description:
            "Movimentos no mercado de matérias-primas continuam influenciando os custos da produção de aço.",
        image: "Minério de ferro",
        body:
            "Conteúdo de demonstração.",
        url: "https://www.iea.org/"
    },


    {
        category: "Siderurgia",
        source: "Estados Unidos",
        title: "Empresas siderúrgicas anunciam novos investimentos industriais",
        date: "2 dias atrás",
        description:
            "Novos investimentos podem alterar capacidade produtiva e competitividade do setor.",
        image: "Siderurgia americana",
        body:
            "Conteúdo provisório.",
        url: "https://www.steel.org/"
    }

];



/* =========================================================
   ELEMENTOS
========================================================= */

const researchCarousel =
    document.getElementById("researchCarousel");

const industryCarousel =
    document.getElementById("industryCarousel");

const modal =
    document.getElementById("articleModal");

const modalTitle =
    document.getElementById("modalTitle");

const modalCategory =
    document.getElementById("modalCategory");

const modalSource =
    document.getElementById("modalSource");

const modalDescription =
    document.getElementById("modalDescription");

const modalClose =
    document.getElementById("modalClose");

const viewExternal =
    document.getElementById("viewExternal");

const viewBoard =
    document.getElementById("viewBoard");

const boardTitle =
    document.getElementById("boardTitle");

const readingBoard =
    document.getElementById("readingBoard");



/* =========================================================
   DATA ATUAL
========================================================= */

let selectedArticle = null;



/* =========================================================
   CRIAÇÃO DOS CARTÕES
========================================================= */

function createCard(article) {

    const card =
        document.createElement("article");

    card.className = "article-card";


    card.innerHTML = `

        <div class="card-image">

            ${article.image}

        </div>


        <div class="card-content">

            <div class="card-source">

                ${article.source}

            </div>


            <h3 class="card-title">

                ${article.title}

            </h3>


            <div class="card-date">

                ${article.date}

            </div>

        </div>

    `;


    card.addEventListener(
        "click",
        () => openModal(article)
    );


    return card;
}



/* =========================================================
   CARREGA OS CARTÕES
========================================================= */

function loadCarousel(
    carousel,
    articles
) {

    carousel.innerHTML = "";


    articles.forEach(
        article => {

            carousel.appendChild(
                createCard(article)
            );

        }
    );

}


loadCarousel(
    researchCarousel,
    researchArticles
);


loadCarousel(
    industryCarousel,
    industryArticles
);



/* =========================================================
   ABRIR MODAL
========================================================= */

function openModal(article) {

    selectedArticle = article;


    modalCategory.textContent =
        article.category;


    modalTitle.textContent =
        article.title;


    modalSource.textContent =
        article.source +
        " • " +
        article.date;


    modalDescription.textContent =
        article.description;


    modal.classList.add("active");

    modal.setAttribute(
        "aria-hidden",
        "false"
    );

}



/* =========================================================
   FECHAR MODAL
========================================================= */

function closeModal() {

    modal.classList.remove("active");

    modal.setAttribute(
        "aria-hidden",
        "true"
    );

}


modalClose.addEventListener(
    "click",
    closeModal
);


modal.addEventListener(
    "click",
    event => {

        if (
            event.target === modal
        ) {

            closeModal();

        }

    }
);


document.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Escape"
        ) {

            closeModal();

        }

    }
);



/* =========================================================
   VER NO SITE
========================================================= */

viewExternal.addEventListener(
    "click",
    () => {

        if (
            selectedArticle &&
            selectedArticle.url
        ) {

            window.open(
                selectedArticle.url,
                "_blank"
            );

        }

    }
);



/* =========================================================
   VER NO QUADRO
========================================================= */

viewBoard.addEventListener(
    "click",
    () => {

        if (!selectedArticle) {
            return;
        }


        displayOnBoard(
            selectedArticle
        );


        closeModal();


        document
            .getElementById(
                "readingBoard"
            )
            .scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

    }
);



/* =========================================================
   COLOCAR MATÉRIA NO QUADRO
========================================================= */

function displayOnBoard(article) {

    boardTitle.textContent =
        article.title;


    readingBoard.innerHTML = `

        <article class="board-article">


            <div class="article-category">

                ${article.category}

            </div>


            <h1>

                ${article.title}

            </h1>


            <div class="article-meta">

                ${article.source}
                •
                ${article.date}

            </div>


            <div class="article-image">

                ${article.image}

            </div>


            <div class="article-body">

                <p>

                    ${article.description}

                </p>


                <p>

                    ${article.body}

                </p>


                <p>

                    Esta versão do quadro é uma
                    representação local da matéria.
                    Quando o sistema estiver conectado
                    às fontes reais, este conteúdo será
                    preenchido automaticamente.

                </p>

            </div>

        </article>

    `;

}



/* =========================================================
   CONTROLES DOS CARROSSÉIS
========================================================= */

function setupCarouselControls(
    carousel,
    previousButton,
    nextButton
) {

    const amount = 380;


    previousButton.addEventListener(
        "click",
        () => {

            carousel.scrollBy({

                left: -amount,

                behavior: "smooth"

            });

        }
    );


    nextButton.addEventListener(
        "click",
        () => {

            carousel.scrollBy({

                left: amount,

                behavior: "smooth"

            });

        }
    );

}


setupCarouselControls(

    researchCarousel,

    document.getElementById(
        "researchPrev"
    ),

    document.getElementById(
        "researchNext"
    )

);


setupCarouselControls(

    industryCarousel,

    document.getElementById(
        "industryPrev"
    ),

    document.getElementById(
        "industryNext"
    )

);



/* =========================================================
   ROLAGEM AUTOMÁTICA
========================================================= */

function startAutoScroll(
    carousel
) {

    let direction = 1;


    setInterval(
        () => {

            const maxScroll =
                carousel.scrollWidth -
                carousel.clientWidth;


            if (
                maxScroll <= 0
            ) {

                return;

            }


            if (
                carousel.scrollLeft >=
                maxScroll - 5
            ) {

                direction = -1;

            }


            if (
                carousel.scrollLeft <= 5
            ) {

                direction = 1;

            }


            carousel.scrollBy({

                left:
                    direction * 1,

                behavior:
                    "auto"

            });

        },

        25

    );

}


startAutoScroll(
    researchCarousel
);


startAutoScroll(
    industryCarousel
);



/* =========================================================
   DATA DO CABEÇALHO
========================================================= */

function updateDate() {

    const element =
        document.getElementById(
            "currentDate"
        );


    const today =
        new Date();


    element.textContent =
        today.toLocaleDateString(
            "pt-BR",
            {
                day: "2-digit",
                month: "long",
                year: "numeric"
            }
        );

}


updateDate();
