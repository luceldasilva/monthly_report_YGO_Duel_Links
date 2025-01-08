import click
from buscar_urls_yugioh_api import url_cropped, card_list_archetype


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Buscar los avatares de los arquetipos en la terminal."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument('archetype', type=str)
def arquetipo(archetype):
    """Todas las cartas de un arquetipo dado."""
    card_list_archetype(archetype=archetype)


@cli.command()
@click.argument('name_card', type=str)
def carta(name_card):
    """La URL de la imagen formato cropped de la carta."""
    url_cropped(name_card=name_card)


if __name__ == "__main__":
    cli()
