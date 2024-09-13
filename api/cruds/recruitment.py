# 渡邊T追加分
from api.models.main import User
from neomodel import db

def create_recruitment(title: str, description: str, image_urls: list, deadline: str):
    """Neo4j上にRecruitmentノードを作成する"""
    query = "MERGE (r:Recruitment { title: $title, description: $description, image_urls: $image_urls, deadline: $deadline }) RETURN r"
    results, meta = db.cypher_query(
        query, 
        {'title': title, 'description': description, 'image_urls': image_urls, 'deadline': deadline}
    )
    return results



# フォーマットの参考よう
# def get_user_by_id_func(id: str) -> User:
#     query = f"MATCH (n) WHERE elementId(n) = '{id}' RETURN n"
#     results, meta = db.cypher_query(query)
#     return User.inflate(results[0][0])