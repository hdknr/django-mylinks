import djclick as click
from ... import models
from logging import getLogger
logger = getLogger()


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.argument('url')
@click.pass_context
def create_entry(ctx, url):
    ''' create a Link'''
    models.create_entry(url=url)


@main.command()
@click.argument('url')
@click.pass_context
def get_oembed(ctx, url):
    ''' create oembed'''
    from mylinks.oembed import get_oembed 
    res = get_oembed(url)
    print(res['url'])
    print(res['html'])
    print(res['source'])
    print(res['data'])
