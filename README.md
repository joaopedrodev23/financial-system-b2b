# Sistema Financeiro para Pequenas Empresas (Brasil)

Sistema web simples, profissional e pronto para produção, focado em controle financeiro operacional para pequenas empresas e MEIs.

## Visão Geral
- **Backend**: FastAPI + PostgreSQL
- **Frontend**: React (Vite)
- **Autenticação**: JWT
- **Arquitetura**: Clean Architecture
- **Idiomas**: português (Brasil)
- **Exportação**: CSV

## Funcionalidades
- Autenticação com e-mail e senha (JWT)
- Lançamentos de entrada e saída
- Categorias configuráveis
- Filtros por período e tipo
- Dashboard com resumo financeiro
- Exportação de dados em CSV

## Estrutura do Projeto
```
backend/
  app/
    core/           # configuração e settings
    domain/         # entidades e contratos
    application/    # casos de uso e schemas
    infrastructure/ # banco, repos, segurança
    presentation/   # rotas e controllers
  requirements.txt
  Dockerfile
  .env.example
frontend/
  src/
    api/            # chamadas HTTP
    components/     # UI reutilizável
    pages/          # páginas principais
    hooks/          # auth
    styles/         # estilos
  Dockerfile
  nginx.conf
  .env.example
docker-compose.yml
```

## Requisitos
- Docker + Docker Compose (recomendado)
- Ou: Python 3.11+, Node 20+, PostgreSQL 14+

## Setup com Docker (recomendado)
1. Copie o `.env.example` do backend:
```
cp backend/.env.example backend/.env
```
2. Ajuste as variáveis em `backend/.env`.
3. Suba os containers:
```
docker compose up --build
```
4. Acesse:
- API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## Setup Local (dev)
### Backend
```
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
### Ajuste importante
No ambiente local, altere `POSTGRES_HOST` para `localhost` no arquivo `backend/.env`.

### Frontend
```
cd frontend
npm install
copy .env.example .env
npm run dev
```

## Endpoints Principais
Base URL: `http://localhost:8000/api/v1`

### Autenticação
**Registro**
```
POST /auth/register
{
  "email": "empresa@exemplo.com",
  "password": "123456"
}
```

**Login**
```
POST /auth/login
{
  "email": "empresa@exemplo.com",
  "password": "123456"
}
```

**Resposta**
```
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Categorias
**Criar**
```
POST /categories
Authorization: Bearer <jwt>
{
  "name": "Vendas",
  "type": "income"
}
```

**Listar**
```
GET /categories
Authorization: Bearer <jwt>
```

### Lançamentos
**Criar**
```
POST /transactions
Authorization: Bearer <jwt>
{
  "category_id": "<uuid>",
  "type": "income",
  "amount": 1500.00,
  "description": "Pagamento cliente",
  "date": "2026-02-06"
}
```

**Listar com filtros**
```
GET /transactions?start_date=2026-02-01&end_date=2026-02-28&type=income
Authorization: Bearer <jwt>
```

**Exportar CSV**
```
GET /transactions/export?start_date=2026-02-01&end_date=2026-02-28
Authorization: Bearer <jwt>
```

### Dashboard
```
GET /dashboard/summary?start_date=2026-02-01&end_date=2026-02-28
Authorization: Bearer <jwt>
```

## Observações Importantes
- O backend cria as tabelas automaticamente no primeiro start (ideal para MVP). Para produção, recomenda-se incluir migrações com Alembic.
- As senhas são armazenadas com hash seguro (bcrypt).
- JWT expira em 24h por padrão (configurável em `.env`).

## Sugestões de Melhorias Futuras
1. Multi-empresa com permissões por usuário
2. Centro de custos e rateios
3. Recorrência de lançamentos
4. Conciliação bancária e importação OFX
5. Relatórios avançados e gráficos
6. Trilhas de auditoria e logs de acesso
7. Recuperação de senha e MFA
8. Integração com Pix e boletos

## Licença
Uso interno ou comercial conforme necessidade do projeto.
