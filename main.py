from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging
import base64

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

# @app.post("/lowercase")
# async def lowercase(request: Request):
#     data = await request.json()

#     return {"message": data["data"].lower()}
