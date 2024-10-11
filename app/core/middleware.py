from fastapi import Request

async def security_middleware(request: Request, call_next):
    response = await call_next(request)
    
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    if "session_id" in request.cookies:
        response.set_cookie(
            key="session_id",
            value=request.cookies["session_id"],
            httponly=True,
            # secure=True,
            samesite="Lax",
        )
        
    return response