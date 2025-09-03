# tests/test_cli.py
"""Testes da CLI (hello e stats_cmd) alinhados com a sua interface atual:
'stats-cmd' recebe NUMEROS como ARGUMENTOS POSICIONAIS (sem --numeros).
Total: 20 testes (10 positivos + 10 negativos)."""

import re
from typer.testing import CliRunner
from meu_projeto.cli import app

runner = CliRunner()

# Remove códigos de cor ANSI do Rich para facilitar asserções de texto
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")

def clean(s: str) -> str:
    """Retorna o texto sem códigos ANSI."""
    return ANSI.sub("", s)


# ====================== POSITIVOS (10) ======================

# 1) `hello` sem nome usa o padrão "mundo" e imprime a saudação.
def test_hello_padrao():
    res = runner.invoke(app, ["hello"])
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Saudação" in out
    assert "Olá, mundo!" in out

# 2) `hello` com --name personaliza a saudação.
def test_hello_nome_custom():
    res = runner.invoke(app, ["hello", "--name", "Lucca"])
    assert res.exit_code == 0
    assert "Olá, Lucca!" in clean(res.stdout)

# 3) Cálculo básico com posicionais: 1 2 3 -> min=1, max=3, média=2.00, mediana=2.00, desvio=1.00.
def test_stats_cmd_basico_posicional():
    res = runner.invoke(app, ["stats-cmd", "1", "2", "3"])
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Estatísticas" in out
    assert "Quantidade" in out and "3" in out
    assert "Mínimo" in out and "1" in out
    assert "Máximo" in out and "3" in out
    assert "Média" in out and "2.00" in out
    assert "Mediana" in out and "2.00" in out
    assert "Desvio Padrão" in out and "1.00" in out

# 4) Caso par: 1 2 3 4 -> mediana 2.50.
def test_stats_cmd_par_com_mediana_quebrada():
    res = runner.invoke(app, ["stats-cmd", "1", "2", "3", "4"])
    assert res.exit_code == 0
    assert "2.50" in clean(res.stdout)

# 5) Decimais funcionam e saem com 2 casas.
def test_stats_cmd_decimais():
    res = runner.invoke(app, ["stats-cmd", "1.5", "2.5"])
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Média" in out and "2.00" in out
    assert "Mediana" in out and "2.00" in out

# 6) Todos iguais: desvio 0.00.
def test_stats_cmd_repetidos():
    res = runner.invoke(app, ["stats-cmd", "5", "5", "5"])
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Mínimo" in out and "5" in out
    assert "Máximo" in out and "5" in out
    assert "Média" in out and "5.00" in out
    assert "Mediana" in out and "5.00" in out
    assert "Desvio Padrão" in out and "0.00" in out

# 7) Ordem não importa: 9 1 5 -> mediana 5.00, min 1, max 9.
def test_stats_cmd_ordem_nao_importa():
    res = runner.invoke(app, ["stats-cmd", "9", "1", "5"])
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Quantidade" in out and "3" in out
    assert "Mínimo" in out and "1" in out
    assert "Máximo" in out and "9" in out
    assert "Mediana" in out and "5.00" in out

# 8) Mistura de negativos e decimais.
def test_stats_cmd_negativos_e_decimais():
    res = runner.invoke(app, ["stats-cmd", "--", "-2", "0", "3.5"])
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Mínimo" in out and "-2" in out
    assert "Máximo" in out and "3.5" in out
    assert "Média"  in out and "0.50" in out
    assert "Mediana" in out and "0.00" in out

# 9) Lista maior (1..10): média 5.50 e mediana 5.50.
def test_stats_cmd_lista_maior_media_mediana():
    args = ["stats-cmd"] + [str(i) for i in range(1, 11)]
    res = runner.invoke(app, args)
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Quantidade" in out and "10" in out
    assert "Média" in out and "5.50" in out
    assert "Mediana" in out and "5.50" in out

# 10) Unicode/acentos/emojis no nome do hello.
def test_hello_unicode():
    res = runner.invoke(app, ["hello", "--name", "Álvaro 😊"])
    assert res.exit_code == 0
    out = clean(res.stdout)
    assert "Olá, Álvaro 😊!" in out


# ====================== NEGATIVOS (10) ======================

# 1) Apenas um número: statistics.stdev exige >=2 dados -> deve falhar e mencionar "two data points".
def test_stats_cmd_um_numero_quebra_stdev():
    res = runner.invoke(app, ["stats-cmd", "42"])
   
    assert res.exit_code != 0
    assert "two data points" in (res.output + str(res.exception)).lower()

# 2) Sem nenhum número: Typer deve reclamar de argumento obrigatório.
def test_stats_cmd_sem_numeros_erro_de_argumento():
    res = runner.invoke(app, ["stats-cmd"])
    assert res.exit_code != 0
    assert "missing argument 'numeros'" in res.output.lower() or "missing argument 'num" in res.output.lower()

# 3) Valor não numérico como argumento posicional.
def test_stats_cmd_valor_invalido():
    res = runner.invoke(app, ["stats-cmd", "abc"])
    assert res.exit_code != 0
    o = res.output.lower()
    assert "invalid value" in o or "is not a valid float" in o

# 4) Opção desconhecida no hello.
def test_hello_opcao_desconhecida():
    res = runner.invoke(app, ["hello", "--nam", "X"])
    assert res.exit_code != 0
    assert "no such option" in res.output.lower()

# 5) Usar --numeros (que não existe na sua CLI atual) deve falhar.
def test_stats_cmd_opcao_inexistente_longa():
    res = runner.invoke(app, ["stats-cmd", "--numeros", "1"])
    assert res.exit_code != 0
    assert "no such option" in res.output.lower()

# 6) Comando escrito errado (stats) deve falhar.
def test_stats_cmd_comando_errado():
    res = runner.invoke(app, ["stats"])
    assert res.exit_code != 0
    assert "no such command" in res.output.lower()

# 7) Flag curta inexistente.
def test_stats_cmd_flag_curta_inexistente():
    res = runner.invoke(app, ["stats-cmd", "-n", "1"])
    assert res.exit_code != 0
    assert ("no such option" in res.output.lower()
            or "unknown option" in res.output.lower())

# 8) Misturando válido e inválido nos posicionais.
def test_stats_cmd_misto_valido_invalido():
    res = runner.invoke(app, ["stats-cmd", "1", "xyz", "3"])
    assert res.exit_code != 0
    o = res.output.lower()
    assert "invalid value" in o or "is not a valid float" in o

# 9) Passar argumento posicional em `hello` (sem --name) deve ser rejeitado.
def test_hello_argumento_posicional_sem_nome():
    res = runner.invoke(app, ["hello", "Lucca"])
    assert res.exit_code != 0
    assert ("unexpected extra" in res.output.lower()
            or "got unexpected extra argument" in res.output.lower())

# 10) Usar vírgula como separador decimal (ex.: 3,4) deve falhar (não é float válido).
def test_stats_cmd_valor_com_virgula_invalido():
    res = runner.invoke(app, ["stats-cmd", "3,4"])
    assert res.exit_code != 0
    o = res.output.lower()
    assert "invalid value" in o or "is not a valid float" in o
