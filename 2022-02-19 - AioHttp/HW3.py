# Приложение состоит из 2 страниц:
# 1. Главная страница - список статей и кнопка добавить новую.
# 2. Создание статьи - страница с формой создания.
# (статьи хранить в глобальной переменной)

# Задания:
# 1. На главной странице вывести список статей (сортировка от новых к
# старым). Для каждой статьи должны быть: заголовок, дата создания, 
# текст, теги.
# Если статей больше 5, должна быть постраничная навигация с шагом в 5 
# страниц.
# 2. На странице с формой создания статьи: 
# a. Добавить ввод названия, текста, списка тегов. Теги вводятся через
# запятую или пробел.
# b. После создания статьи необходимо перенаправить пользователя на
# главную страницу.
# c. Если не заполнены какие то из полей, вывести соответствующую
# ошибку.

import aiohttp_jinja2
from flask import redirect
import jinja2
from aiohttp import web

articles = []
count5 = 0

async def redirect(request):
    return web.HTTPFound('/p1')

async def page1(request):
    global articles
    context = {'items' : articles}
    return aiohttp_jinja2.render_template('p1.html', request, context)

async def page2(request):
    global count5
    global articles
    context = {'error' : ''}

    name = request.rel_url.query.get('name')
    date = request.rel_url.query.get('date')
    text = request.rel_url.query.get('text')
    tags = request.rel_url.query.get('tags')
    if name and date and text and tags:
        articles.append([name, date, text, tags])
        count5 += 1
        if count5 == 5:
            articles.append([])
            count5 = 0
        return web.HTTPFound('/p1')
    return aiohttp_jinja2.render_template('p2.html', request, context)

app = web.Application()
app.add_routes([web.get('/p1', page1),
                web.get('/p2', page2),
                web.get('/', redirect)])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(''))

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8089)