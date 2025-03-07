import base64
import logging
import random
import string
import time
from threading import Thread

from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

allowed_values = {
    "Катя",
    "Маша",
    "Алёна",
    "Милана",
    "Полина Б.",
    "Полина С.",
    "Настя"
}
second_task_code = "1234567890"
second_task_name = "анатолий"

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def submit_form(value: str = Form(...)):
    if value in allowed_values:
        encoded_value = base64.b64encode(value.encode('utf-8')).decode('utf-8')
        response = RedirectResponse(url=f"/guesswho?code=%20&name=%20", status_code=303)
        response.set_cookie(key="user_value", value=encoded_value)

        return response
    else:
        return RedirectResponse(url="/", status_code=303)


@app.get("/guesswho")
async def guess_who(request: Request):
    code = request.query_params.get("code")
    name = request.query_params.get("name")

    logging.info(f"Code from query: {code}, Name from query: {name}")

    encoded_value = request.cookies.get("user_value")
    if not encoded_value:
        return RedirectResponse(url="/", status_code=303)

    user_value = base64.b64decode(encoded_value).decode('utf-8')
    if user_value not in allowed_values:
        return RedirectResponse(url="/", status_code=303)

    if code == second_task_code and name == second_task_name:
        return RedirectResponse(url="/authors", status_code=303)

    return templates.TemplateResponse("guesswho.html", {"request": request, "user_value": user_value})


@app.get("/authors")
async def authors(request: Request):
    return templates.TemplateResponse("authors.html", {"request": request})


@app.get("/youneedtobefaster")
async def youneedtobefaster(request: Request):
    return templates.TemplateResponse("youneedtobefaster.html", {"request": request})


temp_password = ""
time_left = 3  # Время до обновления пароля в секундах


def generate_temp_password():
    global temp_password, time_left
    while True:
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        time_left = 3  # После обновления пароля обнуляем счетчик

        # Уменьшаем счетчик времени до обновления
        for _ in range(3):
            time.sleep(1)
            time_left -= 1


@app.on_event("startup")
def start_password_generation():
    # Запускаем генерацию пароля в отдельном потоке
    password_thread = Thread(target=generate_temp_password)
    password_thread.daemon = True
    password_thread.start()


@app.get("/tmp_key")
def get_temp_password():
    return {
        "tmp_key": temp_password,
        "time_left": time_left
    }


@app.get("/sendme")
def get_temp_password(key: str):
    if key and len(key) > 0 and temp_password != '' and key == temp_password:
        return {
            'new_link': '/must_have_to_know'
        }
    else:
        return {
            "error": 'Попытка не пытка'
        }


count_tries = 1


@app.get("/guess_who")
def get_temp_password(surname: str, code: str):
    global count_tries

    if 'новак' == surname.lower() and "427003_166136574" == code:
        return {
            'new_link': '/authors'
        }
    else:
        if count_tries >= 3:
            count_tries = 0
            return {
                'error': '"Отчислен" - Макаров А.В.'
            }
        else:
            count_tries += 1

            return {
                'error': 'Ошибка'
            }

# @app.post("/lowercase")
# async def lowercase(request: Request):
#     data = await request.json()

#     return {"message": data["data"].lower()}
