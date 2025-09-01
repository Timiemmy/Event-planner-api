from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Settings
from routes.users import user_router
from routes.events import event_router
import uvicorn

# register origins
origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = Settings()
    await settings.initialize_database()
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(user_router, prefix="/users")
app.include_router(event_router, prefix="/events")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def home():
    return RedirectResponse(url='/events/')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
