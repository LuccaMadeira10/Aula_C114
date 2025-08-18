# EstatisticaLucca

Este projeto tem como objetivo fornecer ferramentas e exemplos para o estudo de estatística utilizando Python. Ele está organizado para facilitar o aprendizado e a execução de exercícios práticos.

## Estrutura do Projeto

```
EstatisticaLucca/
├── exercicio_aula/
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── src/
│       └── meu_projeto/
│           ├── cli.py
│           └── __pycache__/
├── README.md
└── .gitignore
```

- **exercicio_aula/**: Pasta principal dos exercícios e código fonte.
  - **pyproject.toml** e **poetry.lock**: Gerenciamento de dependências com Poetry.
  - **src/meu_projeto/**: Código fonte do projeto, incluindo o arquivo `cli.py` para execução via linha de comando.

## Como instalar as dependências

O projeto utiliza o [Poetry](https://python-poetry.org/) para gerenciar as dependências. Para instalar, siga os passos abaixo:

1. Instale o Poetry (caso não tenha):
	```powershell
	(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
	```
2. Navegue até a pasta `exercicio_aula`:
	```powershell
	cd exercicio_aula
	```
3. Instale as dependências:
	```powershell
	poetry install
	```

## Como executar o projeto

Para rodar o projeto, utilize o comando abaixo dentro da pasta `exercicio_aula`:

```powershell
poetry run python src/meu_projeto/cli.py
```

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests com sugestões, correções ou novas funcionalidades.

## Licença

Este projeto está sob a licença MIT.
# Aula_C114