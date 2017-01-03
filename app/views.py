import json
from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPFound
from aiohttp.hdrs import METH_POST
from aiohttp_jinja2 import template

BASE_URL = 'https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache'

async def purge_site(app):
    url = BASE_URL.format(zone_id=app['zone_id'])
    headers = {
        'X-Auth-Email': app['username'],
        'X-Auth-Key': app['api_key'],
        'Content-Type': 'application/json',
    }
    data = '{"purge_everything":true}'
    async with ClientSession(loop=app.loop) as client:
        async with client.delete(url, data=data, headers=headers) as r:
            data = await r.json()
            if r.status != 200 or data.get('success') is not True:
                return r.status, json.dumps(data, indent=2)


@template('index.jinja')
async def index(request):
    d = {
        'title': 'Purge cache for {app[site]}'.format(app=request.app),
    }
    if request.method == METH_POST:
        error = await purge_site(request.app)
        if error:
            d['error_status'], d['error_response'] = error
        else:
            raise HTTPFound(request.app.router['thanks'].url())
    return d


@template('thanks.jinja')
async def thanks(request):
    return {
        'title': 'Purge Complete',
    }

