import os
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_jinja2 import APP_KEY as JINJA2_APP_KEY

from .views import index, thanks


THIS_DIR = Path(__file__).parent


def setup_routes(app):
    app.router.add_route('*', '/', index, name='index')
    app.router.add_get('/thanks', thanks, name='thanks')


def create_app(loop):
    app = web.Application(loop=loop)
    for env_var in ['USERNAME', 'API_KEY', 'ZONE_ID']:
        try:
            app[env_var.lower()] = os.environ[env_var]
        except KeyError:
            raise RuntimeError('"{}" environment variable not found'.format(env_var))

    app.update(
        name='cloudflare purge',
        site=os.getenv('SITE', 'unknown'),
    )

    jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / 'templates'))
    aiohttp_jinja2.setup(app, loader=jinja2_loader, app_key=JINJA2_APP_KEY)
    app.router.add_route('*', '/', index, name='index')
    app.router.add_get('/thanks', thanks, name='thanks')
    return app
