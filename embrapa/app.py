from fastapi import FastAPI
from embrapa.routers import apis, import_csv, auth


app = FastAPI()
app.include_router(import_csv.router)
app.include_router(apis.router)
app.include_router(auth.router)
# app.mount('/mkdocs', StaticFiles(directory='site', html=True), name='mkdocs')
