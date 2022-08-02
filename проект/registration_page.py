from multiprocessing import context
import aiohttp_jinja2
import jinja2
from aiohttp import web

from flask import redirect, request
import re
import os
from urllib import response
import time


users = []
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') # шаблон для проверки почты
allowed_ext= {'png', 'jpg', 'jpeg'}

user_status = 'guest'
number_of_user = -1

# параметры входа для администратора сайта
admin_login = 'admin'
admin_password = 'Qwerty'


# Создаем домашнюю страницу
async def home(request):
    return aiohttp_jinja2.render_template('home_page.html', request, {})


# Создаем страницу регистрации
async def reg(request):
    global users
    global regex
    global allowed_ext
    context = {'error_password' : '', # одинаковые ли пароли (пароль + проверка)
                'result' : '', # сбщ об успешной регистрации
                'len_password' : '', # проверка длины пароля (длина > 4)
                'len_phone' : '', # проверки длины номера телефона (длина = 11)
                're_email' : '', # проверка имейла по шаблону
                'image_ext' : ''} #проверка на расширение изображение
    error = [0, 0, 0, 0, 0]

    if request.method == 'POST':
        data = await request.post()

        s_name = data['surname']
        name = data['name']
        e_mail = data['email']
        phone_number = data['phone_number']
        nick = data['nick']
        password = data['password']
        password_again = data['password_again']
        file_photo = data['photo']
        

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
            if re.fullmatch(regex, e_mail):
                context['re_email'] = ''
                error[3] = 0
            else:
                context['re_email'] = 'Неверно введен email'
                error[3] = 1

        
        if file_photo:
            if file_photo.filename.rsplit('.', 1)[1].lower() in allowed_ext:
                context['image_ext'] = ''
                file_content = file_photo.file.read()
                filename = file_photo.filename
                error[4] = 0
            else:
                context['image_ext'] = 'Неверный формат файла'
                error[4] = 1



        if s_name and name and e_mail and phone_number and nick and password and password_again and (sum(error) == 0):
            users.append([[e_mail, phone_number, password], s_name, name, nick])
            context['result'] = 'Регистрация прошла успешно'
            print(context['result'], users)
            return web.HTTPFound('/enter')
            # return aiohttp_jinja2.render_template('enter_page.html', request, {})
        else:
            context['result'] = 'Были заполнены не все поля или некоторые поля заполнены с ошибкой'
    return aiohttp_jinja2.render_template('registrarion.html', request, context)


# Создаем страницу входа на сайт
async def enter(request):
    global user_status
    global users
    global number_of_user
    global admin_login
    global admin_password
    context = {'error_enter' : ''}
    error = 1
    j = 0

    if request.method == 'POST':
        data = await request.post()

        login = data['telephone_or_email']
        p_word = data['p_word']

        if login and p_word:
            for i in users:
                if (login == i[0][0] or login == i[0][1]) and p_word == i[0][2]:
                    error = 0
                    number_of_user = j
                    response=web.Response()
                    response.set_cookie('number_of_user', number_of_user)
                else:
                    context['error_enter'] = 'Несовпадение логина или пароля'
                j += 1     

        if login and p_word and error == 0:
            user_status = 'user'
            # response.set_cookie('user_status', user_status)
            number_of_user = request.cookies.get(number_of_user, 0)
            print(request.cookies.get(number_of_user, 0))
            return aiohttp_jinja2.render_template('welcome.html', request, {'coma' : ',', 'name' : users[number_of_user][2], 's_name' : users[number_of_user][1]})
        elif login == admin_login and p_word == admin_password:
            user_status = 'admin'
            # response.set_cookie('user_status', user_status)
            number_of_user = request.cookies.get(number_of_user, 0)
            print(request.cookies.get(number_of_user, 0))
            return aiohttp_jinja2.render_template('welcome.html', request, {'coma' : '', 'name' : 'домой, хозяин', 's_name' : ''})
        else:
            context['error_enter'] = 'Несовпадение логина или пароля'
    return aiohttp_jinja2.render_template('enter_page.html', request, context)



app = web.Application()
app.add_routes([web.get('/', home),
                web.post('/registration', reg),
                web.get('/registration', reg),
                web.post('/enter', enter),
                web.get('/enter', enter)])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(''))

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8089)