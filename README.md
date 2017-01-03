# Purge CloudFlare

Heroku app to allow anyone with the link to purge the cache for a cloudflare site.

You need to set the following environment variables in Heroku:

* **USERNAME** Your username for cloudflare
* **API_KEY** Your api key for cloudflare
* **ZONE_ID** the zone ID for the site you wish to purge
* **SITE** (optional) the url of the site being purged
