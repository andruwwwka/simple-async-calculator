import click
import uvicorn

from simple_async_calculator.api.handlers import app


@click.group()
def cli():
    """Группа cli-команд приложения"""


@cli.command()
@click.option("--debug", is_flag=True)
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=8000)
def serve(debug: bool, host: str, port: int):
    """Команда запкска сервиса разработки"""
    uvicorn.run(app, host=host, port=port, log_level="debug" if debug else "warning")


if __name__ == "__main__":
    cli()
