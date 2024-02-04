import uvicorn
from fastapi import FastAPI, APIRouter

from api.v1.users_routers import users_router
from api.v1.login_routers import login_router
from api.v1.register_router import register_router


app = FastAPI(
    debug=True,
    version="0.0.1",
    docs_url=f"/docs",
    openapi_url=f"/openapi.json",
    title="FastAPI",
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


# @app.get("/users")
# async def users():
#     return {"message": "Hello World"}

app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)