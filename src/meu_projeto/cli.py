import typer
from rich.console import Console
from rich.table import Table
import statistics as stats

app = typer.Typer(help="Ferramenta de exemplo com Typer e Rich")
console = Console()

@app.command()
def hello(name: str = "mundo"):
    """Exibe uma saudação estilosa."""
    console.rule("[bold green]Saudação[/bold green]")
    console.print(f"Olá, {name}! 👋", style="bold green")

@app.command()
def stats_cmd(numeros: list[float]):
    """Calcula estatísticas simples."""
    t = Table(title="Estatísticas")
    t.add_column("Métrica", style="cyan")
    t.add_column("Valor", style="magenta")

    t.add_row("Quantidade", str(len(numeros)))
    t.add_row("Mínimo", str(min(numeros)))
    t.add_row("Máximo", str(max(numeros)))
    t.add_row("Média", f"{stats.mean(numeros):.2f}")
    t.add_row("Mediana", f"{stats.median(numeros):.2f}")
    t.add_row("Desvio Padrão", f"{stats.stdev(numeros):.2f}")

    console.print(t)

if __name__ == "__main__":
    app()
