import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.fall import fall_router
from routes.featured import featured_router
from routes.spring import spring_router
from routes.summer import summer_router
from routes.winter import winter_router

app = FastAPI(
    title="Parfums API",
    description="API de catálogos e CRUD de perfumes por estação.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(featured_router)
app.include_router(spring_router)
app.include_router(summer_router)
app.include_router(fall_router)
app.include_router(winter_router)


@app.get("/")
def back_status() -> dict[str, str]:
    return {"status": "A TODO VAPOR"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 5500))
    uvicorn.run(app, host="0.0.0.0", port=port)
