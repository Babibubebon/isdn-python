import json
import os
import time

import click
from requests.exceptions import HTTPError

from . import ISDN, __version__
from .client import ISDNClient


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo(f"isdn/{__version__}")


@cli.command("get", help="Get record from isdn.jp")
@click.argument("isdn")
@click.option("--format", "-f", type=click.Choice(["xml", "dict", "json"]), default="xml")
def get_isdn(isdn: str, format: str):
    c = ISDNClient()
    match format:
        case "xml":
            res = c.get_raw(isdn)
        case "dict":
            res = c.get(isdn).to_dict()
        case "json":
            res = json.dumps(c.get(isdn).to_dict(), ensure_ascii=False)
        case _:
            raise NotImplementedError
    click.echo(res)


@cli.command("list", help="List all ISDNs from isdn.jp")
def list_isdns():
    c = ISDNClient()
    for isdn in c.list():
        click.echo(isdn)


@cli.command(help="Download all xml record files from isdn.jp")
@click.argument("directory", type=click.Path(exists=True, file_okay=False, writable=True))
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
@click.option("--stop-on-error", is_flag=True, help="Overwrite existing files")
@click.option("--sleep-time", "-s", type=int, default=500, help="sleep interval for download (millisecond)")
def bulk_download(directory: str, force: bool, stop_on_error: bool, sleep_time: int):
    c = ISDNClient()
    with click.progressbar(list(c.list()), show_pos=True) as bar:
        for isdn in bar:
            path = os.path.join(directory, f"{isdn}.xml")
            if not force and os.path.exists(path):
                continue
            try:
                res = c.get_raw(isdn)
            except HTTPError as err:
                if stop_on_error:
                    raise err
                else:
                    continue
            with open(path, "wb") as out:
                out.write(res)
            time.sleep(sleep_time / 1000)


@cli.command(help="Validate ISDN code")
@click.argument("isdn")
def validate(isdn: str):
    try:
        click.echo(ISDN(isdn).validate(raise_error=True))
    except Exception as e:
        click.echo(e, err=True)
