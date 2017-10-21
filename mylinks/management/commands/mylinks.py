# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
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
def add_page(ctx, url):
    ''' Add a Page'''
    models.Page.objects.create(url=url).update_content()
