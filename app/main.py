from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze_repo


def create_app() -> FastAPI:

    app = FastAPI(
        title="GitHub repository Reader",
        description="RESTful API service that takes a GitHub repository URL and returns a human-readable summary of the project",
        version="0.0.1"

    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API routes
    app.include_router(analyze_repo.router)

    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello, from GitHub repo reader!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
