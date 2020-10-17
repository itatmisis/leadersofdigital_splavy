from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

import database.database
import database.entities.user

SECRET = "SECRET"

Database = database.database.Database

fastapi_users = None
jwt_authentication = None


def setup_routers(app):
    global fastapi_users, jwt_authentication

    user_db = Database.get_user_database()

    jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

    fastapi_users = FastAPIUsers(
        user_db,
        [jwt_authentication],
        database.entities.user.User,
        database.entities.user.UserCreate,
        database.entities.user.UserUpdate,
        database.entities.user.UserDB,
    )

    def on_after_register(user: database.entities.user.UserDB, request: Request):
        print(f"User {user.id} has registered.")

    def on_after_forgot_password(user: database.entities.user.UserDB, token: str, request: Request):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    app.include_router(
        fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_reset_password_router(
            SECRET, after_forgot_password=on_after_forgot_password
        ),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
