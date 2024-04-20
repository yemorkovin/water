from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext

import db
from db import *
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'))
app.add_middleware(SessionMiddleware, secret_key="lasmfklwejfl25l23klrjsgkl")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    #print(request.session['login'])
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/reg', response_class=HTMLResponse)
def reg(request: Request):
    return templates.TemplateResponse('reg.html', {'request': request})

@app.post('/reg', response_class=HTMLResponse)
def register(request: Request, login: str = Form(...), password: str = Form(...), password_rep: str = Form(...)):
    p = pwd_context.hash(password)
    message = ''
    if password == password_rep:
        if not getLoginUser(login):
            registration(login, p)
            message += 'Вы успешно зарегистрированы'
        else:
            message += 'Такой логин существует'
    else:
        message += 'Пароли не совпадают'
    return templates.TemplateResponse('reg.html', {'request': request, 'message': message})


@app.get('/auth', response_class=HTMLResponse)
def auth(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})

@app.post('/auth',  response_class=HTMLResponse)
async def auth(request: Request, login: str = Form(...), password: str = Form(...)):
    #print(login)
    user = getUser(login)
    if not user or not pwd_context.verify(password, user[2]):
        return templates.TemplateResponse('auth.html', {'request': request, 'message': 'Invalid login or password'})
    request.session['login'] = login

    return RedirectResponse(url='/panel', status_code=303)


@app.get('/logout', response_class=HTMLResponse)
def logout(request: Request):
    if 'login' in request.session:
        del request.session['login']
    return RedirectResponse(url='/')

@app.get('/panel', response_class=HTMLResponse)
def panel(request: Request):
    return templates.TemplateResponse('panel.html', {'request': request})


@app.post('/panel', response_class=HTMLResponse)
def panel(request: Request, old_password: str = Form(...), new_password: str = Form(...)):
    user = getUser(request.session['login'])
    errors = ''
    if not pwd_context.verify(old_password, user[2]):
        errors = 'Error old password'
    else:
        p = pwd_context.hash(new_password)
        db.updatePassword(p, request.session['login'])
    return templates.TemplateResponse('panel.html', {'request': request, 'errors': errors})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8001)

'''
TCP - синхронное (клиент -> сервер)  (сервер -> клиент) -> соединение -> оправка пакета
UDP - пакет клиент -> сервер
'''
