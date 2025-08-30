# FastAPI Project

Uma estrutura base para desenvolvimento de APIs utilizando **FastAPI**, com **Alembic** para migrações, testes automatizados, padronização de código e formatação automática com **Ruff**.

---

## 📊 Tecnologias Utilizadas

* [Python 3.11+](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Alembic](https://alembic.sqlalchemy.org/)
* [Pytest](https://docs.pytest.org/)
* [Ruff](https://docs.astral.sh/ruff/)
* [Poetry](https://python-poetry.org/)

---

## 🔧 Pré-requisitos

Certifique-se de ter instalado:

* Python 3.11 ou superior
* [Poetry](https://python-poetry.org/docs/#installation)

---

## 🔄 Instalação

Clone o repositório:

```bash
  git clone https://github.com/iamDFSB/FastAPI_Project.git
  cd FastAPI_Project
```

Instale as dependências com **Poetry**:

```bash
  poetry install
```

---

## ▶ Como Rodar o Projeto

Ative o ambiente virtual do Poetry:

```bash
poetry shell
```

Inicie a aplicação via **Makefile**:

```bash
  make run-app
```

A API estará disponível em: [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 🗄 Migrações com Alembic

Para criar uma nova migração:

```bash
  alembic revision --autogenerate -m "mensagem_da_migracao"
```

Aplicar as migrações:

```bash
  alembic upgrade head
```

---

## 🧪 Como Rodar os Testes

```bash
  make test
```

Gerar relatório em HTML:

```bash
  make test-post
```

---

## 🧹 Padronização e Formatação com Ruff

Verificar problemas:

```bash
  make ruff-check-dir
```

Corrigir automaticamente:

```bash
  make ruff-check-fix
```

Formatar o código:

```bash
  make ruff-format
```

---

## 🔐 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.
