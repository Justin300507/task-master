from fastapi import FastAPI
from app.database import Base, engine

# model imports
from app.models.lists import *  # noqa: F401
from app.models.list_members import *  # noqa: F401
from app.models.users import *  # noqa: F401
from app.models.tasks import *  # noqa: F401
from app.models.tags import *  # noqa: F401
from app.models.task_tags import *  # noqa: F401

# router imports
from app.routes.stats_routes import stats_router
from app.routes.user_routes import user_router
from app.routes.auth_routes import auth_router
from app.routes.seed_routes import seed_router
from app.routes.list_item_routes import list_item_router
from app.routes.list_member_routes import list_member_router
from app.routes.task_routes import task_router
from app.routes.tag_routes import tag_router

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# include routers
app.include_router(stats_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(seed_router)
app.include_router(list_item_router)
app.include_router(list_member_router)
app.include_router(task_router)
app.include_router(tag_router)

# CORS (required for frontend access)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint (required for deployment health checks)
@app.get("/health")
def health():
    return {"status": "ok"}
