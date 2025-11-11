// ----- Consultas de API -----
// Faz uma consulta de API e retorna o resultado
async function pegarDadosDoFlask(link) {
  try {
    const response = await fetch(link);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    // console.log("Data from Flask:", data);
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Adiciona um item a uma tabela via API.
async function adicionarDadoFlask(tabela, valores) {
  const dados = { tabela, valores };

  const opcoes = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dados),
  };

  try {
    const resposta = await fetch("/api/adicionar", opcoes);

    // O fetch não lança erro para status como 400 ou 500, então verificamos manualmente.
    if (!resposta.ok) {
      // Analisa a resposta JSON para obter a mensagem de erro do servidor.
      const erroData = await resposta.json();
      throw new Error(
        `Erro do servidor: ${resposta.status} - ${erroData.mensagem}`
      );
    }

    return await resposta.json(); // Retorna os dados da resposta em caso de sucesso.
  } catch (erro) {
    console.error("Erro na requisição:", erro);
    throw erro; // Propaga o erro para o código que chamou a função.
  }
}

// Lista os dados de uma tabela via API.
async function listarDadosFlask(tabela, filtros = {}) {
  const dados = { tabela, filtros };

  const opcoes = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  };

  try {
    const resposta = await fetch("/api/listar", opcoes);

    // Verifica manualmente se houve erro
    if (!resposta.ok) {
      const erroData = await resposta.json();
      throw new Error(
        `Erro do servidor (${resposta.status}): ${erroData.mensagem}`
      );
    }

    const json = await resposta.json();
    return json.dados; // retorna apenas os dados úteis
  } catch (erro) {
    console.error("Erro na requisição:", erro.message);
    throw erro;
  }
}

// Atualiza um item a uma tabela via API.
async function atualizarDadoFlask(tabela, valores, condicao, params = []) {
  // Monta o JSON esperado pelo Flask
  const dados = { tabela, valores, condicao, params };

  const opcoes = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dados),
  };

  try {
    const resposta = await fetch("/api/atualizar", opcoes);

    if (!resposta.ok) {
      const erroData = await resposta.json();
      throw new Error(
        `Erro do servidor: ${resposta.status} - ${erroData.mensagem}`
      );
    }

    return await resposta.json(); // Sucesso
  } catch (erro) {
    console.error("Erro na requisição:", erro);
    throw erro;
  }
}

// Exclui um item de uma tabela via API.
async function excluirDadoFlask(tabela, condicao, params = []) {
  const dados = { tabela, condicao, params };

  const opcoes = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  };

  try {
    const resposta = await fetch("/api/excluir", opcoes);

    if (!resposta.ok) {
      const erroData = await resposta.json();
      throw new Error(
        `Erro do servidor: ${resposta.status} - ${erroData.mensagem}`
      );
    }

    return await resposta.json(); // Sucesso
  } catch (erro) {
    console.error("Erro na requisição:", erro);
    throw erro;
  }
}
