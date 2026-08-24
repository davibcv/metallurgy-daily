/* =========================================================
   METALLURGY DAILY
   JAVASCRIPT PRINCIPAL
========================================================= */


/* =========================================================
   ELEMENTOS
========================================================= */

const researchCarousel = document.getElementById("researchCarousel");
const industryCarousel = document.getElementById("industryCarousel");

const boardTitle = document.getElementById("boardTitle");
const readingBoard = document.getElementById("readingBoard");


/* =========================================================
   CONTROLE DO QUADRO
========================================================= */

let selectedArticle = null;


/* =========================================================
   BUSCA DOS DADOS REAIS
========================================================= */

async function fetchArticles() {

    try {

        // Busca o arquivo JSON gerado pelo GitHub Actions
        const response = await fetch("data/articles.json");

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();


        // Carrega os carrosséis com os dados reais
        loadCarousel(
            researchCarousel,
            data.research || []
        );

        loadCarousel(
            industryCarousel,
            data.industry || []
        );


    } catch (error) {

        console.error(
            "Falha ao carregar as notícias:",
            error
        );


        researchCarousel.innerHTML =
            "<p style='padding: 20px;'>Não foi possível carregar as pesquisas.</p>";


        industryCarousel.innerHTML =
            "<p style='padding: 20px;'>Não foi possível carregar as notícias.</p>";

    }

}


/* =========================================================
   CRIAÇÃO DOS CARTÕES
========================================================= */

function createCard(article) {

    const card = document.createElement("article");

    card.className = "article-card";


    /* =====================================================
       FORMATAÇÃO DA DATA
    ===================================================== */

    let displayDate = article.date;


    if (
        displayDate &&
        displayDate.length > 15
    ) {

        const d = new Date(displayDate);


        if (!isNaN(d)) {

            displayDate =
                d.toLocaleDateString(
                    "pt-BR",
                    {
                        day: "2-digit",
                        month: "short",
                        year: "numeric"
                    }
                );

        }

    }


    /* =====================================================
       LOGO DA FONTE
    ===================================================== */

    let logoHTML = "";


    /*
       O coletor deverá futuramente inserir no JSON
       algo como:

       "logo": "https://.../logo.png"

       Se existir uma logo, ela será exibida.
    */

    if (article.logo) {

        logoHTML = `
            <img
                class="source-logo"
                src="${article.logo}"
                alt="Logo ${article.source}"
                loading="lazy"
            >
        `;

    }


    /* =====================================================
       ESTRUTURA DO CARD
    ===================================================== */

    card.innerHTML = `

        <div class="card-image">

            ${logoHTML}

        </div>


        <div class="card-content">

            <div class="card-source">
                ${article.source}
            </div>


            <h3 class="card-title">
                ${article.title}
            </h3>


            <div class="card-date">
                ${displayDate}
            </div>

        </div>

    `;


    /*
       Agora o cartão vai diretamente para o quadro.
       Não existe mais janela intermediária.
    */

    card.addEventListener(
        "click",
        () => {

            displayOnBoard(article);

            document
                .getElementById("readingBoard")
                .scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

        }
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


    if (articles.length === 0) {

        carousel.innerHTML =
            "<p style='padding: 20px; color: var(--text-secondary);'>Nenhuma matéria recente encontrada com os critérios atuais.</p>";

        return;

    }


    articles.forEach(
        article => {

            carousel.appendChild(
                createCard(article)
            );

        }
    );

}


/* =========================================================
   COLOCAR MATÉRIA NO QUADRO
========================================================= */

function displayOnBoard(article) {

    selectedArticle = article;


    boardTitle.textContent =
        article.title;


    let displayDate =
        article.date;


    const d =
        new Date(displayDate);


    if (!isNaN(d)) {

        displayDate =
            d.toLocaleDateString(
                "pt-BR",
                {
                    day: "2-digit",
                    month: "short",
                    year: "numeric"
                }
            );

    }


    const categoryLabel =
        article.category === "research"
            ? "PESQUISA"
            : "INDÚSTRIA";


    readingBoard.innerHTML = `

        <article class="board-article">


            <div class="board-article-top">

                <div class="article-category">

                    ${categoryLabel}

                </div>


                <button
                    class="board-external-button"
                    id="boardExternalButton"
                    type="button">

                    Mostrar no site ↗

                </button>

            </div>


            <h1>
                ${article.title}
            </h1>


            <div class="article-meta">

                ${article.source}
                •
                ${displayDate}

            </div>


            <div class="article-body">

                <p>

                    <strong>Resumo:</strong>

                    ${
                        article.summary ||
                        "Nenhum resumo fornecido pela fonte."
                    }

                </p>


                <br>


                <p>

                    <em>
                        Para consultar o conteúdo completo,
                        utilize o botão
                        "Mostrar no site".
                    </em>

                </p>

            </div>


        </article>

    `;


    /*
       Botão "Mostrar no site"
    */

    const boardExternalButton =
        document.getElementById(
            "boardExternalButton"
        );


    if (
        boardExternalButton &&
        article.url
    ) {

        boardExternalButton.addEventListener(
            "click",
            () => {

                window.open(
                    article.url,
                    "_blank"
                );

            }
        );

    }

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


    /*
       Controle da rolagem automática.
    */

    let autoScrollPausedUntil = 0;


    function pauseAutoScroll() {

        autoScrollPausedUntil =
            Date.now() + 5000;

    }


    previousButton.addEventListener(
        "click",
        () => {

            pauseAutoScroll();


            carousel.scrollBy({

                left: -amount,

                behavior: "smooth"

            });

        }
    );


    nextButton.addEventListener(
        "click",
        () => {

            pauseAutoScroll();


            carousel.scrollBy({

                left: amount,

                behavior: "smooth"

            });

        }
    );


    return {

        isAutoScrollPaused() {

            return (
                Date.now() <
                autoScrollPausedUntil
            );

        }

    };

}


/* =========================================================
   CONFIGURAÇÃO DOS CONTROLES
========================================================= */

const researchAutoControl =
    setupCarouselControls(
        researchCarousel,
        document.getElementById(
            "researchPrev"
        ),
        document.getElementById(
            "researchNext"
        )
    );


const industryAutoControl =
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
    carousel,
    autoControl
) {

    let direction = 1;


    setInterval(
        () => {


            /*
               Se o usuário acabou de usar
               uma das setas, aguardamos.
            */

            if (
                autoControl &&
                autoControl.isAutoScrollPaused()
            ) {

                return;

            }


            const maxScroll =
                carousel.scrollWidth -
                carousel.clientWidth;


            /*
               Se não existe conteúdo suficiente
               para rolar, não fazemos nada.
            */

            if (maxScroll <= 0) {

                return;

            }


            /*
               Quando chega ao final,
               muda de direção.
            */

            if (
                carousel.scrollLeft >=
                maxScroll - 2
            ) {

                direction = -1;

            }


            /*
               Quando chega ao começo,
               volta a avançar.
            */

            if (
                carousel.scrollLeft <= 2
            ) {

                direction = 1;

            }


            carousel.scrollBy({

                left: direction,

                behavior: "auto"

            });


        },

        140

    );

}


/* =========================================================
   INICIA A ROLAGEM AUTOMÁTICA
========================================================= */

startAutoScroll(
    researchCarousel,
    researchAutoControl
);


startAutoScroll(
    industryCarousel,
    industryAutoControl
);


/* =========================================================
   DATA ATUAL
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


/* =========================================================
   INICIALIZAÇÃO
========================================================= */

updateDate();

fetchArticles();
