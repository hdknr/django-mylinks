# https://pythonhosted.org/feedparser/
from django.conf import settings
from django.utils import html, timezone
from django.utils.translation import ugettext as _
import json
from datetime import datetime
from time import mktime
import feedparser
import pytz
import logging

logger = logging.getLogger('feeds')

def parse(url):
    return feedparser.parse(url)

def is_valid_feed(parsed):
    if hasattr(parsed.feed, 'bozo_exception'):
        msg = f'Feedreader poll_feeds found Malformed feed,  {parsed.feed.bozo_exception}'
        logger.warning(msg)
        return False

    for attr in ['title', 'title_detail', 'link']:
        if not hasattr(parsed.feed, attr):
            msg = f'Feedreader poll_feeds. Feed has no {attr}'
            logger.error(msg)
            return False

    return True


def get_published_datetime(source):
    published_time = source and datetime.fromtimestamp(mktime(source)) or timezone.now()

    try:
        published_time = pytz.timezone(settings.TIME_ZONE).localize(published_time, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        pytz_timezone = pytz.timezone(settings.TIME_ZONE)
        published_time = pytz_timezone.localize(published_time, is_dst=False)
    return published_time


def get_feed_published_time(parsed, last_published_at):
    published_time = get_published_datetime(parsed.feed.updated_parsed)
    if last_published_at and last_published_at >= published_time:
        return last_published_at
    return published_time


def get_feed_title(parsed):
    if parsed.feed.title_detail.type == 'text/plain':
        return html.escape(parsed.feed.title)
    return parsed.feed.title


def get_feed_description(parsed):
    return getattr(parsed.feed, 'description', '')


def is_valid_entry(entry):
    for attr in ['title', 'title_detail', 'link', 'description']:
        if not hasattr(entry, attr):
            msg = f'Feedreader poll_feeds. Entry "{entry.link}" has no {attr}'
            logger.error(msg)
            return False

    if entry.title == "":
        msg = f'Feedreader poll_feeds. Entry "{entry.link}" has a blank title'
        logger.warning(msg)
        return False

    return True


def get_entry_title(entry):
    if entry.title_detail.type == 'text/plain':
        return html.escape(entry.title)
    return entry.title


def get_entry_description(entry):
    return getattr(entry, 'description', '')


def get_entry_published_time(entry):
    dt = entry.get('published_parsed', entry.get('updated_parsed', None))

    now = timezone.now()
    published_time = dt and get_published_datetime(dt) or now
    return published_time <= now and published_time or now
