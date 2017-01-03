import os
from pathlib import Path

import aiohttp_jinja2
import jinja2
import trafaret as t
from aiohttp import web
from aiohttp_jinja2 import APP_KEY as JINJA2_APP_KEY

from .views import index, thanks


THIS_DIR = Path(__file__).parent
BASE_DIR = THIS_DIR.parent
SETTINGS_FILE = BASE_DIR / 'settings.yml'

DEV_DICT = t.Dict()
DEV_DICT.allow_extra('*')

SETTINGS_STRUCTURE = t.Dict({
    # the "dev" dictionary contains information used by aiohttp-devtools to serve your app locally
    # you may wish to use it yourself,
    # eg. you might use dev.static_path in a management script to deploy static assets
    'dev': DEV_DICT,
})


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
    setup_routes(app)
    return app
