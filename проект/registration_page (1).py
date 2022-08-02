# Создаем страницу регистрации

import aiohttp_jinja2
from flask import redirect
import jinja2
from aiohttp import web
import re
import os

users = []
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') # шаблон для проверки почты
upload_folder = ''
allowed_ext= {'png', 'jpg', 'jpeg'}

async def reg(request):
    global users
    global regex
    global upload_folder
    global allowed_ext
    context = {'error_password' : '', # одинаковые ли пароли (пароль + проверка)
                'result' : '', # сбщ об успешной регистрации
                'len_password' : '', # проверка длины пароля (длина > 4)
                'len_phone' : '', # проверки длины номера телефона (длина = 11)
                're_email' : '', # проверка имейла по шаблону
                'image_ext' : ''} #проверка на расширение изображение
    error = [0, 0, 0, 0, 0]

    s_name = request.rel_url.query.get('surname')
    name = request.rel_url.query.get('name')
    e_mail = request.rel_url.query.get('email')
    phone_number = request.rel_url.query.get('phone_number')
    nick = request.rel_url.query.get('nick')
    password = request.rel_url.query.get('password')
    password_again = request.rel_url.query.get('password_again')
    file = request.files('file')

    if password and password_again:
        if password != password_again:
            context['error_password'] = 'Введите одинаковый пароль в оба поля'
            error[0] = 1
        else:
            context['error_password'] = ''
            error[0] = 0

    if password:
        if len(str(password)) <= 4:
            context['len_password'] = 'Слишком короткий пароль'
            error[1] = 1
        else:
            context['len_password'] = ''
            error[1] = 0

    if phone_number:
        if len(str(phone_number)) != 11:
            context['phone_number'] = 'Неверно задан номер телефона. Запись должна начинаться с 89...'
            error[2] = 1
        else:
            context['phone_number'] = ''
            error[2] = 0
    
    if e_mail:
        if e_mail:
            if re.fullmatch(regex, e_mail):
                context['re_email'] = ''
                error[3] = 0
            else:
                context['re_email'] = 'Неверно введен email'
                error[3] = 1

    if file.filename.rsplit(., 1)[1].lower() in allowed_ext:
        context['image_ext'] = ''
        filename = file.filename
        file.save(os.path.join(upload_folder, filename))
        error[4] = 0
    else:
        context['image_ext'] = 'Неверный формат файла'
        error[4] = 1

    if s_name and name and e_mail and phone_number and nick and password and password_again and (sum(error) == 0):
        users.append([[e_mail, phone_number, password], s_name, name, nick, filename])
        context['result'] = 'Регистрация прошла успешно'
        print(users)
    return aiohttp_jinja2.render_template('registrarion.html', request, context)

app = web.Application()
app.add_routes([web.get('/', reg)])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(''))

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8089)