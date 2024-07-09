from src.create_app import create_application
import uvicorn

app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
