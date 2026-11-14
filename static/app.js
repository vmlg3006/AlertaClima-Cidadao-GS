const form = document.querySelector('#formulario');
const mensagem = document.querySelector('#mensagem');
let registros = [];

async function api(caminho, opcoes = {}) {
  const resposta = await fetch(caminho, opcoes);
  if (resposta.status === 204) return null;
  const dados = await resposta.json();
  if (!resposta.ok) throw new Error(dados.erro || 'Falha na operação.');
  return dados;
}

function avisar(texto) { mensagem.textContent = texto; }

function elemento(tag, texto, classe) {
  const item = document.createElement(tag);
  item.textContent = texto;
  if (classe) item.className = classe;
  return item;
}

function botao(rotulo, acao, classe) {
  const item = elemento('button', rotulo, classe);
  item.type = 'button'; item.addEventListener('click', acao);
  return item;
}

async function carregar() {
  try {
    registros = await api('/api/alertas');
    const area = document.querySelector('#regioes');
    area.replaceChildren();
    if (!registros.length) area.append(elemento('p', 'Nenhuma região cadastrada.'));
    for (const reg of registros) {
      const cartao = elemento('article', '', 'cartao');
      cartao.append(elemento('h3', `${reg.bairro} — ${reg.cidade}`));
      cartao.append(elemento('p', `Limite: ${reg.limite_calor} °C`));
      const clima = elemento('p', 'Clima ainda não consultado.');
      cartao.append(clima);
      const acoes = elemento('div', '', 'acoes');
      acoes.append(botao('Ver temperatura', async () => {
        try {
          const dado = await api(`/api/alertas/${reg.id}/clima`);
          clima.textContent = `${dado.temperatura} °C — ${dado.aviso} (${dado.horario})`;
        } catch (erro) { avisar(erro.message); }
      }));
      acoes.append(botao('Editar', () => {
        for (const chave of ['id', 'bairro', 'cidade', 'latitude', 'longitude', 'limite_calor'])
          document.getElementById(chave).value = reg[chave];
        window.scrollTo({top: 0, behavior: 'smooth'});
      }, 'secundario'));
      acoes.append(botao('Excluir', async () => {
        if (!confirm('Excluir esta região?')) return;
        try { await api(`/api/alertas/${reg.id}`, {method:'DELETE'}); avisar('Região excluída.'); await carregar(); }
        catch (erro) { avisar(erro.message); }
      }, 'perigo'));
      cartao.append(acoes); area.append(cartao);
    }
  } catch (erro) { avisar(erro.message); }
}

form.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  const id = document.querySelector('#id').value;
  const dados = Object.fromEntries(['bairro','cidade','latitude','longitude','limite_calor'].map(chave => [chave, document.getElementById(chave).value]));
  try {
    await api(id ? `/api/alertas/${id}` : '/api/alertas', {
      method: id ? 'PUT' : 'POST', headers: {'Content-Type':'application/json'}, body:JSON.stringify(dados)
    });
    form.reset(); document.querySelector('#id').value = '';
    avisar(id ? 'Região atualizada.' : 'Região cadastrada.'); await carregar();
  } catch (erro) { avisar(erro.message); }
});
document.querySelector('#cancelar').addEventListener('click', () => { form.reset(); document.querySelector('#id').value=''; });
carregar();
