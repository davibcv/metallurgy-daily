=========================================================

   METALLURGY DAILY

   JAVASCRIPT PRINCIPAL

========================================================= */



const researchCarousel = document.getElementById("researchCarousel");

const industryCarousel = document.getElementById("industryCarousel");

const boardTitle = document.getElementById("boardTitle");

const readingBoard = document.getElementById("readingBoard");



let selectedArticle = null;



async function fetchArticles() {

    try {

        const response = await fetch("data/articles.json");

        if (!response.ok) {

            throw new Error(`Erro HTTP: ${response.status}`);

        }

        const data = await response.json();



        loadCarousel(researchCarousel, data.research || []);

        loadCarousel(industryCarousel, data.industry || []);

    } catch (error) {

        console.error("Falha ao carregar as notícias:", error);

        researchCarousel.innerHTML = "<p style='padding: 20px;'>Não foi possível carregar as pesquisas.</p>";

        industryCarousel.innerHTML = "<p style='padding: 20px;'>Não foi possível carregar as notícias.</p>";

    }

}



function createCard(article) {

    const card = document.createElement("article");

    card.className = "article-card";



    let displayDate = article.date;

    if (displayDate && displayDate.length > 15) {

        const d = new Date(displayDate);

        if (!isNaN(d)) {

            displayDate = d.toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" });

        }

    }



    let domain = "";

    try {

        if (article.url) {

            domain = new URL(article.url).hostname;

        }

    } catch (e) {

        console.error("URL inválida:", article.url);

    }



    // Busca a logo

    let logoHTML = "";

    if (domain) {

        const logoUrl = `https://s2.googleusercontent.com/s2/favicons?domain=${domain}&sz=128`;

        logoHTML = `

            <img

                class="source-logo"

                src="${logoUrl}"

                alt="Logo"

                loading="lazy"

                style="width: 45px; height: 45px; border-radius: 8px; background: white; padding: 4px; object-fit: contain;"

            >

        `;

    }



    // Busca a bandeira mapeada pelo coletor Python

    let flagHTML = "";

    if (article.country) {

        const flagUrl = `https://flagcdn.com/24x18/${article.country}.png`;

        flagHTML = `

            <img 

                src="${flagUrl}" 

                alt="País" 

                style="width: 20px; height: 15px; border-radius: 2px; box-shadow: 0 0 0 1px rgba(255,255,255,0.15);"

            >

        `;

    }



    // Isola o nome principal da fonte, cortando tudo após um traço

    let shortSource = article.source.split(/[-—]/)[0].trim();

    if (shortSource.toUpperCase() === "MIT NEWS") {

        shortSource = "MIT";

    }



    // Estrutura visual: Logo e bandeira em bloco horizontal; nome empurrado para a linha de baixo

    card.innerHTML = `

        <div class="card-image" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 15px;">

            

            <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px;">

                ${logoHTML}

                ${flagHTML}

            </div>



            <span style="display: block; font-size: 0.75rem; letter-spacing: 1px; color: rgba(255,255,255,0.9); font-weight: bold; text-transform: uppercase; margin-top: 8px;">

                ${shortSource}

            </span>

            

        </div>

        <div class="card-content">

            <h3 class="card-title">${article.title}</h3>

            <div class="card-date">${displayDate || ""}</div>

        </div>

    `;



    card.addEventListener("click", () => {

        displayOnBoard(article);

        document.getElementById("readingBoard").scrollIntoView({ behavior: "smooth", block: "start" });

    });



    return card;

}



function loadCarousel(carousel, articles) {

    carousel.innerHTML = "";

    if (articles.length === 0) {

        carousel.innerHTML = "<p style='padding: 20px; color: var(--text-secondary);'>Nenhuma matéria recente encontrada com os critérios atuais.</p>";

        return;

    }

    articles.forEach(article => {

        carousel.appendChild(createCard(article));

    });

}



function displayOnBoard(article) {

    selectedArticle = article;

    boardTitle.textContent = article.title;



    let displayDate = article.date;

    const d = new Date(displayDate);

    if (!isNaN(d)) {

        displayDate = d.toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" });

    }



    const categoryLabel = article.category === "research" ? "PESQUISA" : "INDÚSTRIA";



    readingBoard.innerHTML = `

        <article class="board-article">

            <div class="board-article-top">

                <div class="article-category">${categoryLabel}</div>

                <button class="board-external-button" id="boardExternalButton" type="button">

                    Mostrar no site ↗

                </button>

            </div>

            <h1>${article.title}</h1>

            <div class="article-meta">

                ${article.source} • ${displayDate || ""}

            </div>

            <div class="article-body">

                <p><strong>Resumo:</strong> ${article.summary || "Nenhum resumo fornecido pela fonte."}</p>

                <br>

                <p><em>Para consultar o conteúdo completo, utilize o botão "Mostrar no site".</em></p>

            </div>

        </article>

    `;



    const boardExternalButton = document.getElementById("boardExternalButton");

    if (boardExternalButton && article.url) {

        boardExternalButton.addEventListener("click", () => {

            window.open(article.url, "_blank");

        });

    }

}



function setupCarouselControls(carousel, previousButton, nextButton) {

    const amount = 380;

    let autoScrollPausedUntil = 0;



    function pauseAutoScroll() {

        autoScrollPausedUntil = Date.now() + 5000;

    }



    previousButton.addEventListener("click", () => {

        pauseAutoScroll();

        carousel.scrollBy({ left: -amount, behavior: "smooth" });

    });



    nextButton.addEventListener("click", () => {

        pauseAutoScroll();

        carousel.scrollBy({ left: amount, behavior: "smooth" });

    });



    return {

        isAutoScrollPaused() {

            return Date.now() < autoScrollPausedUntil;

        }

    };

}



const researchAutoControl = setupCarouselControls(researchCarousel, document.getElementById("researchPrev"), document.getElementById("researchNext"));

const industryAutoControl = setupCarouselControls(industryCarousel, document.getElementById("industryPrev"), document.getElementById("industryNext"));



function startAutoScroll(carousel, autoControl) {

    let direction = 1;

    setInterval(() => {

        if (autoControl && autoControl.isAutoScrollPaused()) return;

        const maxScroll = carousel.scrollWidth - carousel.clientWidth;

        if (maxScroll <= 0) return;

        

        if (carousel.scrollLeft >= maxScroll - 2) direction = -1;

        if (carousel.scrollLeft <= 2) direction = 1;

        

        carousel.scrollBy({ left: direction, behavior: "auto" });

    }, 140);

}



startAutoScroll(researchCarousel, researchAutoControl);

startAutoScroll(industryCarousel, industryAutoControl);



function updateDate() {

    const element = document.getElementById("currentDate");

    const today = new Date();

    element.textContent = today.toLocaleDateString("pt-BR", { day: "2-digit", month: "long", year: "numeric" });

}



updateDate();

fetchArticles(); 

