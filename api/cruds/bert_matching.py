from neomodel import db
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
from neomodel import config
config.DATABASE_URL = "bolt://neo4j:0oFKulfd@localhost:7687"

def find_similar_users_neo4j(target_user_name: str, top_k: int = 15):
    """
    Neo4jデータベースからユーザーベクトルを取得し、
    ターゲットユーザーに類似したユーザーを検索する。
    """

    query = "MATCH (u:User) RETURN u.name AS name, u.vector AS vector"
    results, meta = db.cypher_query(query)

    # クエリ結果を辞書型のリストに変換
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
        print(f"ターゲットユーザー {target_user_name} は見つかりませんでした。")
        return []

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

if __name__ == "__main__":
    # ターゲットユーザーの指定 (本来は引数などから取得)
    target_user_name = "太陽"  

    # 類似ユーザーの検索
    similar_users = find_similar_users_neo4j(target_user_name, top_k=15)

    # 結果表示
    print(f"ターゲットユーザー: {target_user_name}")
    print("類似ユーザー:")
    for user in similar_users:
        print(f"- {user['name']}: {user['similarity']:.4f}")
