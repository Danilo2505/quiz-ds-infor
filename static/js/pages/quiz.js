const buttonPreviousCard = document.querySelector("#button-previous-card");
const buttonNextCard = document.querySelector("#button-next-card");

async function enviarAlternativa(idPergunta, idAlternativa) {
  const pergunta = await pegarDadosDoFlask(`api/perguntas?id=${idPergunta}`);
  const idResposta = pergunta[0]["id_resposta"];
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
