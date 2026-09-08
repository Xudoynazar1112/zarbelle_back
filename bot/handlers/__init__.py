from aiogram import Router
from . import start, auth, customers, trash, search, stats, language


def register_all_handlers() -> Router:
    main_router = Router()
    main_router.include_router(start.router)
    main_router.include_router(auth.router)
    main_router.include_router(language.router)
    main_router.include_router(customers.router)
    main_router.include_router(trash.router)
    main_router.include_router(search.router)
    main_router.include_router(stats.router)
    return main_router
