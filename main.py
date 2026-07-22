"""Main FastAPI application entry point."""

import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.database import Base, engine
from app.operations import add, divide, multiply, subtract
from app.routers.calculations import router as calculations_router
from app.routers.users import router as users_router

# Import the models so SQLAlchemy registers their tables.
from app.models.calculation import Calculation  # noqa: F401
from app.models.user import User  # noqa: F401


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create database tables that do not already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Module 12 User and Calculation API",
    description=(
        "FastAPI application providing user registration, login, "
        "and calculation BREAD operations."
    ),
    version="1.0.0",
)


# Register Module 12 routers.
app.include_router(users_router)
app.include_router(calculations_router)


templates = Jinja2Templates(directory="templates")


class OperationRequest(BaseModel):
    """Validate input for the original calculator routes."""

    a: float = Field(
        ...,
        description="The first number",
    )
    b: float = Field(
        ...,
        description="The second number",
    )


class OperationResponse(BaseModel):
    """Represent a successful arithmetic response."""

    result: float = Field(
        ...,
        description="The result of the operation",
    )


class ErrorResponse(BaseModel):
    """Represent an arithmetic error response."""

    error: str = Field(
        ...,
        description="Error message",
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Return application HTTP errors in a consistent format."""

    logger.error(
        "HTTPException on %s: %s",
        request.url.path,
        exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.get("/")
async def read_root(request: Request):
    """Display the original calculator page."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the health status of the API."""

    return {"status": "healthy"}


@app.post(
    "/add",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def add_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Add two numbers."""

    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as error:
        logger.error("Add operation error: %s", error)

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/subtract",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def subtract_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Subtract the second number from the first."""

    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as error:
        logger.error("Subtract operation error: %s", error)

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/multiply",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def multiply_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Multiply two numbers."""

    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as error:
        logger.error("Multiply operation error: %s", error)

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/divide",
    response_model=OperationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def divide_route(
    operation: OperationRequest,
) -> OperationResponse:
    """Divide the first number by the second."""

    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)

    except ValueError as error:
        logger.error("Divide operation error: %s", error)

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        logger.exception(
            "Unexpected divide operation error: %s",
            error,
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        ) from error


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )