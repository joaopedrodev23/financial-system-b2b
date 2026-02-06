from app.domain.repositories.user_repository import UserRepository


def authenticate_user(user_repo: UserRepository, email: str, password: str, verify_password) -> object | None:
    user = user_repo.get_by_email(email)
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
