import djclick as click
from mimetypes import guess_type
from ... import models
import sys
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
@click.option('--outfile', '-o', default=None)
@click.pass_context
def get_oembed(ctx, url, outfile):
    ''' create oembed'''
    from mylinks.oembed import get_oembed 
    res = get_oembed(url)
    t = (outfile and guess_type(outfile)[0] or 'application/text').split('/')[1]
    output = outfile and open(outfile, 'w') or sys.stdout 
    if t == 'text':
        output.write(str(res))
    elif t == 'json':
        output.write(res.Schema().dumps(res, indent=2, ensure_ascii=False))

@main.command()
@click.option('--id', '-i', default=None)
@click.option('--url', '-u', default=None)
@click.pass_context
def poll(ctx, id, url):
    feeds = None 
    if id:
        feeds = models.Feed.objects.filter(id=id)
    elif url:
        feeds = [models.Feed.objects.get_or_create(url=url)]
    else:
        feeds = models.Feed.objects.all()

    for feed in feeds:
        models.FeedEntry.objects.poll_for(feed)
