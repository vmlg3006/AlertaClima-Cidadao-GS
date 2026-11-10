# AlertaClima Cidadão — GS Coding for Security

Protótipo CitizenTech para acompanhar temperatura por região. **Versão MongoDB Atlas**.

## Requisitos
- Windows com Python 3.10+ e internet
- Cluster MongoDB Atlas ativo (plano Free serve)
- Usuário do banco com papel **readWrite** no banco `alertaclima` (não use conta Atlas admin na entrega)
- IP público do computador autorizado em Atlas > Network Access

## Instalação no PowerShell
Abra o PowerShell dentro desta pasta e execute, um comando de cada vez:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

No `.env`, substitua `SEU_USUARIO`, `SUA_SENHA` e `SEU_CLUSTER` pelos dados obtidos em Atlas > Cluster0 > Connect > Drivers > Python. **Não compartilhe o `.env`**. Senhas com `@`, `#`, `:`, `/` etc. precisam ser codificadas para URL; alternativa: crie senha alfanumérica forte. `MONGO_DB=alertaclima` deve permanecer. Não inclua os sinais `< >` ao substituir valores. Não use a senha da conta de login do site Atlas.

```powershell
python run.py
```

Acesse `http://127.0.0.1:5000`. Na primeira execução, o app cria o índice `id` no banco. O MongoDB cria coleções conforme o uso.

## Teste da interface
Cadastre bairro `Pinheiros`, cidade `São Paulo`, latitude `-23.5614`, longitude `-46.6916`, limite `35`. Clique em **Ver temperatura** (consulta Open-Meteo), depois **Editar** e **Excluir**. Confirme os dados no Atlas > Browse Collections > banco `alertaclima` > coleção `alertas`.

## Testes automatizados
```powershell
python -m pytest -q
```
Os testes usam mocks e não precisam de acesso real ao Atlas. Eles não substituem o teste manual da integração.

## Socket TCP
Em outro PowerShell, com ambiente virtual ativo:
```powershell
python run.py --tcp
```
Em um terceiro PowerShell:
```powershell
python -c "import socket; s=socket.create_connection(('127.0.0.1',5051)); s.sendall(b'STATUS'); print(s.recv(1024).decode()); s.close()"
```

## API
- GET `/api/alertas` — 200
- POST `/api/alertas` — 201
- PUT `/api/alertas/<id>` — 200 ou 404
- DELETE `/api/alertas/<id>` — 204 ou 404
- GET `/api/alertas/<id>/clima` — consulta Open-Meteo

JSON do POST/PUT: `{"bairro":"Pinheiros","cidade":"São Paulo","latitude":-23.5614,"longitude":-46.6916,"limite_calor":35}`.

## Segurança e limitações
Credenciais em `.env` (ignorado pelo Git); validação de entradas; mensagens genéricas de erro; banco com acesso restrito; logs em `logs/acoes.log`; sem coleta de nome, telefone ou CPF. O MongoDB usa filtros e operadores do driver, sem concatenação de consultas SQL. Este protótipo não tem autenticação de usuários, não deve ser publicado diretamente na internet e **não emite alertas oficiais**. Se o Atlas estiver pausado ou seu IP mudar, a conexão poderá falhar.

## Entrega
Envie o ZIP com o código, `.env.example`, `requirements.txt`, README e PDF. **Nunca inclua seu `.env` com senha**. Confirme com a professora se GitHub também é obrigatório, pois consta no enunciado. Declare a ajuda de IA e entenda os códigos para a arguição.
