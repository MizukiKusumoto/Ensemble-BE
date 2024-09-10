from api.models.main import User
from neomodel import db


@db.transaction
def create_user_func(name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password=password).save()
    return user


def get_user_by_email_func(email: str) -> User:
    return User.nodes.get_or_none(email=email)


def get_user_by_id_func(id: str) -> User:
    query = f"MATCH (n) WHERE elementId(n) = '{id}' RETURN n"
    results, meta = db.cypher_query(query)
    return User.inflate(results[0][0])
