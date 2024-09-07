from api.models.main import User


def create_user(name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password=password).save()
    return user


def get_user_by_email(email: str) -> User:
    return User.nodes.get_or_none(email=email)
