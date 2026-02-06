from app.domain.repositories.user_repository import UserRepository


def register_user(user_repo: UserRepository, email: str, password: str, hash_password) -> object:
    existing = user_repo.get_by_email(email)
    if existing:
        raise ValueError("E-mail já cadastrado")
    hashed_password = hash_password(password)
    return user_repo.create(email=email, hashed_password=hashed_password)
