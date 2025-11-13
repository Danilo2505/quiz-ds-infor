// https://codepen.io/GemmaCroad/pen/RNWwGzG
class Notificacao {
  constructor(tipo, titulo, mensagem, icone) {
    const divNotificacao = document.createElement("div");

    divNotificacao.classList.add(
      "div-notification",
      `div-notification-${tipo}`
    );
  }

  mostrar() {}

  remover() {}

  sairAutomaticamente() {}
}
