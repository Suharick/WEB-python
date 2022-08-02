from aiohttp import web

async def hello(request):
    return web.HTTPFound('/new')
    # return web.Response(text="Hello, world")

async def new_page(request):
    return web.Response(text='Привет! Это новая страница!')

app = web.Application()

app.add_routes([
    web.get('/', hello),
    web.get('/new', new_page)
])

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8089)