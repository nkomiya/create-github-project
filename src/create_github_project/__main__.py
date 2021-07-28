import click

from create_github_project.commands import build


@click.group(help='Command line tool to create templated Git project.')
def cli() -> None:
    """CLI のエントリーポイント。
    """
    pass


def main():
    build(cli)
    cli()


if __name__ == "__main__":
    main()
