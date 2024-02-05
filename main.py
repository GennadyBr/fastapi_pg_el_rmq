from logging import getLogger
import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.v1.users_routers import users_router
from api.v1.login_routers import login_router
from api.v1.register_router import register_router
from api.v1.user_delete_routers import user_delete_router
from logging_setup import LoggerSetup

logger_setup = LoggerSetup()  # setup root logger
LOGGER = getLogger(__name__)

app = FastAPI(
    debug=True,
    version="0.0.1",
    docs_url=f"/docs",
    openapi_url=f"/openapi.json",
    title="FastAPI",
)

# Обработка ошибок HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    LOGGER.info(f"REQUEST METHOD {request.method} {request.url}")
    response = await call_next(request)
    return response

# Middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



main_api_router = APIRouter()

#    1. Регистрация пользователя:
main_api_router.include_router(
    register_router, prefix="/register", tags=["register"]
)

#    2. Аутентификация пользователя:
main_api_router.include_router(
    login_router, prefix="/login", tags=["login"]
)

#    3. Получение списка пользователей:
#    4. Поиск пользователей по полям:
main_api_router.include_router(
    users_router, prefix="/users", tags=["users"]
)

#    5. Удаление пользователя:
main_api_router.include_router(
    user_delete_router, prefix="/user_delete", tags=["user_delete"]
)


app.include_router(main_api_router)

@app.on_event("startup")
async def startup_event():
    LOGGER.info(""
                "--- Start up App ---")


@app.on_event("shutdown")
async def shutdown():
    LOGGER.info("--- Shutdown App ---")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)