## Request Files

- You can define files to be uploaded by the client using File. To do this, you first need to install python-multipart.

- You need this because uploaded files are sent as form data.

- You can make a file optional by using standard type annotations and setting a default value of None.

### UploadFile

- Using UploadFile has several advantages over bytes. e.g you dont have to use File() in the default value of the parameter.

- It uses a "spooled" file. A spooled file is a file stored in memory up to a maximum size limit, and after passing this limit, it will be stored in disk.

- You can also add additional meta data to your file.


### Multiple File Uploads

- A user can upload multiple files, you can handle it this way

``` python

@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}

```

``` python

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

```

## Request Forms and Files

- You can declare files and forms together whenever you need to receive files and data at the same time.


## Handling Errors

- For cases of errors, you would normally return an HTTP status code in the range of 400 (from 400 to 499).

- To return HTTP responses with errors to the client, you raise an HTTPException. Since HTTPException is a regular python exception, it stops the execution of the code, and terminates, meaning all other tasks below that exception will not run, even if its not within its scope.


### Install custom exception handles

- In order to create your own custom exception handler, you have to use the @app.exception_handler decorator.

