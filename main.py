from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request


from exceptions.custom_exceptions import CustomException

import os

import shutil
from typing import Annotated


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# first way of returning html content.
@app.get('/', response_class=HTMLResponse)
async def index():
    content = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1>Hello</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=content, status_code=200) 


# using templating engine
@app.get('/another', response_class=HTMLResponse)
async def get_html_template(request: Request, id: str):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})


# file upload
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

# using fileupload, instead of file gives you meta data about the file.
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    save_path = f"uploads/{file.filename}"

    os.makedirs("uploads", exist_ok=True)

    #writing to that file
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "message": "File saved successfully"}


@app.delete("/delete-file/{filename}/")
async def delete_file(filename: str):
    main_dir = os.getcwd()
    file_directory = os.path.join(main_dir, 'uploads')
    sep = os.sep
    try:
        os.remove(file_directory + sep + filename)
    except FileNotFoundError:
        raise HTTPException(status_code=422, detail="file not found")
    return {"message": "Operation completed successfully"}


# file upload with lots of meta data
# async def create_upload_file(file: Annotated[UploadFile, File(description='A file read as UploadFile')]):
#  ...
# or
# async def create_upload_file(file: Annotated[bytes, File(description='A file read as bytes')]):


@app.post("/v2/uploadfile-lock")
async def uploadfile_and_token(
    file: Annotated[UploadFile, File()], 
    token: Annotated[str, Form()]
):
    return {
        "file_size": file.size,
        "token": token,
        "file_content_type": file.content_type,
    }


# custom exception handler

@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something."}
)


@app.get("/custom-exception/{name}")
async def read_name(name: str):
    if name == 'pete':
        raise CustomException(name=name)
    return {"your_name": name}