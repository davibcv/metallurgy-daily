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

let selectedArticle = null;

/* =========================================================
   BUSCA DOS DADOS REAIS
========================================================= */
async function fetchArticles() {
    try {
        // Busca o arquivo JSON gerado pelo GitHub Actions
        const response = await fetch('data/articles.json');

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();

        // Carrega os carrosséis com os dados reais
        loadCarousel(researchCarousel, data.research || []);
        loadCarousel(industryCarousel, data.industry || []);

    } catch (error) {
        console.error("Falha ao carregar as notícias:", error);

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

    // Formatação de data simplificada
    let displayDate = article.date;

    if (displayDate && displayDate.length > 15) {
        const d = new Date(displayDate);

        if (!isNaN(d)) {
            displayDate = d.toLocaleDateString("pt-BR", {
                day: "2-digit",
                month: "short",
                year: "numeric"
            });
        }
    }

    card.innerHTML = `
        <div class="card-image">
            ${article.category === 'research' ? 'PESQUISA' : 'INDÚSTRIA'}
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
     * Ao clicar no cartão, a matéria vai diretamente
     * para o quadro de leitura.
     */
    card.addEventListener("click", () => {

        displayOnBoard(article);

        document.getElementById("readingBoard").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    });

    return card;
}

/* =========================================================
   CARREGA OS CARTÕES
========================================================= */
function loadCarousel(carousel, articles) {

    carousel.innerHTML = "";

    if (articles.length === 0) {

        carousel.innerHTML =
            "<p style='padding: 20px; color: var(--text-secondary);'>Nenhuma matéria recente encontrada com os critérios atuais.</p>";

        return;
    }

    articles.forEach(article => {
        carousel.appendChild(createCard(article));
    });
}

/* =========================================================
   COLOCAR MATÉRIA NO QUADRO
========================================================= */
function displayOnBoard(article) {

    selectedArticle = article;

    boardTitle.textContent = article.title;

    let displayDate = article.date;

    const d = new Date(displayDate);

    if (!isNaN(d)) {

        displayDate = d.toLocaleDateString("pt-BR", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        });

    }

    const categoryLabel =
        article.category === 'research'
            ? 'PESQUISA'
            : 'INDÚSTRIA';

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
                ${article.source} • ${displayDate}
            </div>


            <div class="article-body">

                <p>
                    <strong>Resumo:</strong>
                    ${article.summary || "Nenhum resumo fornecido pela fonte."}
                </p>

                <br>

                <p>
                    <em>
                        Este é um resumo da matéria original.
                        Para acessar o conteúdo completo, utilize o botão
                        "Mostrar no site".
                    </em>
                </p>

            </div>

        </article>
    `;


    /* =====================================================
       BOTÃO — MOSTRAR NO SITE
    ===================================================== */

    const boardExternalButton =
        document.getElementById("boardExternalButton");

    boardExternalButton.addEventListener("click", () => {

        if (selectedArticle && selectedArticle.url) {

            window.open(
                selectedArticle.url,
                "_blank",
                "noopener,noreferrer"
            );

        }

    });

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

    previousButton.addEventListener("click", () => {

        carousel.scrollBy({
            left: -amount,
            behavior: "smooth"
        });

    });

    nextButton.addEventListener("click", () => {

        carousel.scrollBy({
            left: amount,
            behavior: "smooth"
        });

    });

}

setupCarouselControls(
    researchCarousel,
    document.getElementById("researchPrev"),
    document.getElementById("researchNext")
);

setupCarouselControls(
    industryCarousel,
    document.getElementById("industryPrev"),
    document.getElementById("industryNext")
);

/* =========================================================
   ROLAGEM AUTOMÁTICA
========================================================= */
function startAutoScroll(carousel) {

    let direction = 1;

    setInterval(() => {

        const maxScroll =
            carousel.scrollWidth - carousel.clientWidth;

        if (maxScroll <= 0) return;

        if (carousel.scrollLeft >= maxScroll - 5) {
            direction = -1;
        }

        if (carousel.scrollLeft <= 5) {
            direction = 1;
        }

        carousel.scrollBy({
            left: direction * 1,
            behavior: "auto"
        });

    }, 35);

}

startAutoScroll(researchCarousel);
startAutoScroll(industryCarousel);

/* =========================================================
   DATA ATUAL
========================================================= */
function updateDate() {

    const element =
        document.getElementById("currentDate");

    const today = new Date();

    element.textContent =
        today.toLocaleDateString("pt-BR", {
            day: "2-digit",
            month: "long",
            year: "numeric"
        });

}

updateDate();

/* =========================================================
   INICIALIZAÇÃO
========================================================= */

fetchArticles();
