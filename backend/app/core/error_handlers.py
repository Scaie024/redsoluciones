"""
Centralized error handling for the application.

This module provides middleware and exception handlers for consistent error handling
across the application.
"""
import logging
from typing import Callable, Dict, Any, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError

from app.models.base import ErrorResponse

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base exception class for application-specific errors."""
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "internal_server_error",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)

class ValidationError(AppError):
    """Raised when request validation fails."""
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="validation_error",
            details=details or {},
        )

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    def __init__(self, resource: str = "Resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="not_found",
            details=details or {},
        )

class UnauthorizedError(AppError):
    """Raised when authentication fails or credentials are invalid."""
    def __init__(self, message: str = "Not authenticated", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="unauthorized",
            details=details or {},
        )

class ForbiddenError(AppError):
    """Raised when a user doesn't have permission to access a resource."""
    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="forbidden",
            details=details or {},
        )

class ConflictError(AppError):
    """Raised when a resource conflict occurs."""
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="conflict",
            details=details or {},
        )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    error_response = ErrorResponse(
        success=False,
        error={
            "code": getattr(exc, "error_code", "http_error"),
            "message": str(exc.detail) if hasattr(exc, "detail") else str(exc),
            "details": getattr(exc, "details", {}) or {},
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])  # Skip 'body' in loc
        errors.append({
            "field": field or "request body",
            "message": error["msg"],
            "type": error["type"],
        })
    
    error_response = ErrorResponse(
        success=False,
        error={
            "code": "validation_error",
            "message": "Validation error",
            "details": {"errors": errors},
        },
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.dict(),
    )

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle application-specific errors."""
    error_response = ErrorResponse(
        success=False,
        error={
            "code": exc.error_code,
            "message": str(exc.message),
            "details": exc.details,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(),
    )

async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions."""
    logger.exception("Unhandled exception", exc_info=exc)
    
    error_response = ErrorResponse(
        success=False,
        error={
            "code": "internal_server_error",
            "message": "An unexpected error occurred",
            "details": {},
        },
    )
    
    # In production, don't expose internal error details
    if request.app.debug:
        error_response.error["details"] = {
            "type": exc.__class__.__name__,
            "message": str(exc),
        }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict(),
    )

def setup_error_handlers(app: FastAPI) -> None:
    """Register error handlers with the FastAPI application."""
    # Custom exception handlers
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    
    # Catch-all exception handler (must be last)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    
    # Add middleware for logging requests and responses
    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable):
        # Log request
        logger.info(
            "Request: %s %s",
            request.method,
            request.url.path,
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client": {"host": request.client.host if request.client else None},
            },
        )
        
        try:
            response = await call_next(request)
            
            # Log response
            logger.info(
                "Response: %s %s - %s",
                request.method,
                request.url.path,
                response.status_code,
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                },
            )
            
            return response
            
        except Exception as exc:
            # Log the error
            logger.exception(
                "Unhandled exception in request",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(exc),
                },
            )
            raise
