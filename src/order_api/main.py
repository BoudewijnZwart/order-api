from fastapi import FastAPI

from order_api.routes import router

app = FastAPI()
app.include_router(router)


def main() -> None:
    """Start the order api."""
    import uvicorn  # noqa: PLC0415

    uvicorn.run(
        "order_api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
