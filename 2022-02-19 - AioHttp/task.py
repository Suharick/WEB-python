# Создать приложение, позволяющее сложить/вычесть/перемножить/поделить 2 числа. 
# Вернуться со страницы результата на ввод новых значений. 
# Сохранять последние 3 операции и их результат для текущего пользователя.

from aiohttp import web
import aiohttp_jinja2
import jinja2

last3 = []

async def input_ab(request):
    global last3 
    a = request.rel_url.query.get('a')
    b = request.rel_url.query.get('b')

    context = {'title': 'Калькулятор',
                'res' : '',
                'lst3' : ''}
                
    oper = request.rel_url.query.get('operation')
    if a and b:
        a = int(a)
        b = int(b)
        if oper == "add":
            last3.append(a+b)
            last3 = last3[-3:]
            context['res'] = a + b
            context['lst3'] = f'Последние 3 результата: {last3}'
        elif oper == "sub":
            last3.append(a-b)
            last3 = last3[-3:]
            context['res'] = a - b
            context['lst3'] = f'Последние 3 результата: {last3}'
        elif oper == "mul":
            last3.append(a*b)
            last3 = last3[-3:]
            context['res'] = a * b
            context['lst3'] = f'Последние 3 результата: {last3}'
        elif oper == "div":
            last3.append(a/b)
            last3 = last3[-3:]
            context['res'] = a / b
            context['lst3'] = f'Последние 3 результата: {last3}'

    return aiohttp_jinja2.render_template('input.html', request, context)

app = web.Application()
app.add_routes([web.get('/', input_ab)])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(''))

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8089)