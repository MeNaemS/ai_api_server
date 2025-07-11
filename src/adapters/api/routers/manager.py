from fastapi import APIRouter, Request, Header
from dishka.integrations.fastapi import FromDishka, DishkaRoute

manager_router: APIRouter = APIRouter(prefix="/api", tags=["api", "manage"], route_class=DishkaRoute)


@manager_router.get("/current_key")
async def get_api_key(
    request: Request,
    token: str = Header(...),
):
    pass


@manager_router.get("/keys")
async def get_api_keys(
    request: Request,
    token: str = Header(...),
):
    pass


@manager_router.post("/key")
# ToDo: name and limit in params
async def create_api_key(
    request: Request,
    token: str = Header(...),
):
    pass


@manager_router.get("/{hash}")
async def get_api_key_by_hash(
    request: Request,
    hash: str,
    token: str = Header(...)
):
    pass


@manager_router.delete("/{hash}")
async def delete_api_key_by_hash(
    request: Request,
    hash: str,
    token: str = Header(...)
):
    pass


@manager_router.patch("/{hash}")
# ToDo: name, disabled and limit in params
async def update_api_key_by_hash(
    request: Request,
    hash: str,
    token: str = Header(...)
):
    pass
