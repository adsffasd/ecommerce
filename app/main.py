from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.api import category

# Tạo tất cả bảng trong database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# Đăng ký routers
app.include_router(category.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}
