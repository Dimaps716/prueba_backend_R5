import uvicorn
from fastapi import FastAPI

from controllers import users, registry
from settings import Settings

settings = Settings()

app = FastAPI(
    title="Api",
    description="API for a technology shop",
    version="1.0.1",
    root_path=settings.ROOT_PATH,
)
# routers users
app.include_router(users.user_router)
app.include_router(registry.registry_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
