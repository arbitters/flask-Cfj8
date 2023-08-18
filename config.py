from urllib import parse

TOKEN = 'MTE0MDc0MDE0NjA5OTEzODY0MA.GFePjF.fYbgE7W4-pHIIjIqrL7QgEn2m_vWk3PQw6TbGY'
CLIENT_SECRET = 'SnwhkeIUwg3AIKZ7aSpUUQGUbbQc8Qlo'
REDIRECT_URL = 'http://localhost:5000/oauth/callback'
REDIRECT_URL_LEAGUE = 'https://matches.arbiters.io/oauth/callback/league'
REDIRECT_URL_COUNTER = 'https://matches.arbiters.io/oauth/callback/counter'
OAUTH_URL = f'https://discord.com/api/oauth2/authorize?client_id=1140740146099138640&redirect_uri={parse.quote(REDIRECT_URL)}&response_type=code&scope=identify'
OAUTH_URL_LEAGUE = f'https://discord.com/api/oauth2/authorize?client_id=1140740146099138640&redirect_uri={parse.quote(REDIRECT_URL_LEAGUE)}&response_type=code&scope=identify'
OAUTH_URL_COUNTER = f'https://discord.com/api/oauth2/authorize?client_id=1140740146099138640&redirect_uri={parse.quote(REDIRECT_URL_COUNTER)}&response_type=code&scope=identify'