import click
import uvicorn


@click.group()
def cli():
    """Группа cli-команд приложения"""


@cli.command()
@click.option("--debug", is_flag=True)
@click.option("--host", type=str, default="127.0.0.1")
@click.option("--port", type=int, default=8000)
def serve(debug: bool, host: str, port: int) -> None:
    """Команда запкска сервиса разработки"""
    uvicorn.run(
        "simple_async_calculator.api.handlers:app",
        host=host,
        port=port,
        log_level="debug" if debug else "warning",
        reload=debug,
    )


if __name__ == "__main__":
    cli()
