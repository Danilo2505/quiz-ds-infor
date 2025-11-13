// https://codepen.io/GemmaCroad/pen/RNWwGzG
class Notificacao {
  constructor(tipo, titulo, mensagem, icone) {
    // https://stackoverflow.com/questions/31342290/es6-classes-default-value
    this.tempoExpiracao = 5000;
    this.divNotificacao = document.createElement("div");

    divNotificacao.classList.add(
      "div-notification",
      `div-notification-${tipo}`
    );
  }

  mostrar() {}

  remover() {}

  sairAutomaticamente() {
    delay(this.tempoExpiracao);
  }
}
