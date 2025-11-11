const buttonPreviousCard = document.querySelector("#button-previous-card");
const buttonNextCard = document.querySelector("#button-next-card");

function escolherAlternativa(idPergunta, idAlternativa) {
  const ulAlternativas = document.querySelector(
    `.div-card-pergunta[id_pergunta="${idPergunta}"] .ul-alternativas`
  );

  // Retira a alternativa selecionada de todas as alternativas
  ulAlternativas
    .querySelectorAll(".alternativa-selecionada")
    .forEach((liAlternativa) => {
      liAlternativa.classList.remove("alternativa-selecionada");
    });

  // Define a nova alternativa selecionada
  ulAlternativas
    .querySelector(`.li-alternativa[id_alternativa="${idAlternativa}"]`)
    .classList.add("alternativa-selecionada");
}

function enviarRespostas() {
  // Procura algum Card Sem Resposta
  const cardSemResposta = document.querySelector(
    `.div-card-pergunta[id_pergunta]:not(:has(.alternativa-selecionada))`
  );
  if (cardSemResposta) {
    cardSemResposta.scrollIntoView();
    return;
  }

  // Pega as Alternativas Selecionadas e guarda junto ao ID da Pergunta
  let perguntasERespostas = [];
  const alternativasSelecionadas = document.querySelectorAll(
    `.alternativa-selecionada`
  );
  alternativasSelecionadas.forEach((alternativa) => {
    const idPergunta =
      alternativa.parentElement.parentElement.getAttribute("id_pergunta");
    const idAlternativa = alternativa.getAttribute("id_alternativa");
    perguntasERespostas = [...perguntasERespostas, [idPergunta, idAlternativa]];
  });

  console.log(perguntasERespostas);
}

async function verificarRespostas(idPergunta) {
  const pergunta = await pegarDadosDoFlask(`api/perguntas?id=${idPergunta}`);
  const idResposta = pergunta[0]["id_resposta"];
}

function voltarParaPrimeiraPergunta() {
  const divCardsPerguntas = document.querySelector("#div-cards-perguntas");
  const divCardBox = document.querySelector(".div-card-box");

  divCardsPerguntas.scrollTo({ top: 0 });
}

function proximaAnterior() {
  const divCardsPerguntas = document.querySelector("#div-cards-perguntas");
  const divCardBox = document.querySelector(".div-card-box");

  const maxScrollCards = divCardsPerguntas.scrollTop;
  const alturaCardBox = divCardBox.clientHeight;

  divCardsPerguntas.scrollBy(0, -alturaCardBox);
}

function proximaPergunta() {
  const divCardsPerguntas = document.querySelector("#div-cards-perguntas");
  const divCardBox = document.querySelector(".div-card-box");

  const maxScrollCards = divCardsPerguntas.scrollTop;
  const alturaCardBox = divCardBox.clientHeight;

  divCardsPerguntas.scrollBy(0, alturaCardBox);
}

buttonPreviousCard.addEventListener("click", proximaAnterior);

buttonNextCard.addEventListener("click", proximaPergunta);
