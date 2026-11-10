# Guia rápido — arguição

**Problema:** calor intenso pode afetar a saúde de moradores urbanos. **Cidadão:** moradores, especialmente grupos vulneráveis. **ODS:** 3, 11 e 13. **Inspiração:** monitoramento de eventos climáticos extremos/ondas de calor, a confirmar na página do Experience FIAP.

**Flask:** `api.py` implementa GET, POST, PUT, DELETE e rota de consulta meteorológica. **MongoDB:** `database.py` usa `pymongo` diretamente, sem ORM, com coleção `alertas` e contador para IDs numéricos. **Validação:** `validacao.py` verifica os cinco campos. **Clima:** `clima.py` consulta a API pública Open-Meteo com `requests` e JSON. **Logs:** `logs.py` registra horário, ação e resultado. **TCP:** `tcp_status.py` responde `STATUS` na porta local 5051.

**Segurança:** `.env` mantém a string de conexão fora do código; permissão `readWrite` apenas no banco `alertaclima`; validação; não exibir detalhes de falhas internas; mínimo de dados pessoais. **Ameaças:** vazamento de credenciais, entradas maliciosas, indisponibilidade do Atlas/API.

**Demonstração:** iniciar `python run.py`, abrir `http://127.0.0.1:5000`, cadastrar região, consultar clima, editar, excluir, mostrar logs e testar socket TCP. Executar `python -m pytest -q`. Não afirmar que os testes passaram sem executar.

**IA:** foi usada para auxiliar na elaboração, organização e revisão do código/documentação; o aluno deve compreender e validar o projeto.
