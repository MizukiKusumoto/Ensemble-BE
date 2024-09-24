from neomodel import db
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
from api.models.main import User
from api.utils.bert import get_user_vector

def find_similar_users_neo4j(target_user_name: str, top_k: int = 15) -> list:
    """
    Neo4jデータベースからユーザーベクトルを取得し、
    ターゲットユーザーに類似したユーザーを検索する。
    結果をJSON形式で返す。
    """

    query = "MATCH (u:User) RETURN u.name AS name, u.vector AS vector"
    results, meta = db.cypher_query(query)

    user_data = [{'name': row[0], 'vector': row[1]} for row in results]

    user_names = []
    user_vectors = []
    for user in user_data:
        user_names.append(user['name'])
        user_vectors.append(user['vector'])
    user_vectors = np.array(user_vectors)

    # ターゲットユーザーのベクトルを取得
    target_vector = None
    for i, name in enumerate(user_names):
        if name == target_user_name:
            target_vector = user_vectors[i]
            break

    if target_vector is None:
        raise HTTPException(status_code=404, detail=f"ターゲットユーザー {target_user_name} は見つかりませんでした。")


    # 近傍探索モデルの構築と検索
    knn = NearestNeighbors(n_neighbors=top_k, metric='cosine')
    knn.fit(user_vectors)
    _, indices = knn.kneighbors(target_vector.reshape(1, -1))
    similar_user_indices = indices[0]

    # 類似ユーザーの情報を辞書に格納
    similar_users = []
    for i in similar_user_indices:
        # ターゲットユーザー自身は除外
        if user_names[i] != target_user_name:
            similarity = cosine_similarity(target_vector.reshape(1, -1), user_vectors[i].reshape(1, -1))[0][0]
            similar_users.append({
                "name": user_names[i],
                "similarity": similarity
            })

    return similar_users