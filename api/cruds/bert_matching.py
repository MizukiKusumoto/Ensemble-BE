from neomodel import db
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
from api.models.main import User
from api.utils.bert import get_user_vector
from fastapi import HTTPException
import numpy as np
# from sklearn.decomposition import PCA

# def reduce_dimensions(vectors, target_dim):
#   """ベクトルの次元数をtarget_dimに削減する"""
#   pca = PCA(n_components=target_dim)
#   reduced_vectors = pca.fit_transform(vectors)
#   return reduced_vectors

import numpy as np

def pad_vectors(vectors, target_dim):
  """ベクトルの次元数をtarget_dimに揃える"""
  padded_vectors = []
  for vector in vectors:
    # 要素がリストでない場合はリストに変換
    if not isinstance(vector, list):
        vector = vector.tolist() 

    if len(vector) < target_dim:
      padding = np.zeros(target_dim - len(vector))
      padded_vector = np.concatenate([vector, padding])
    else:
      padded_vector = vector[:target_dim]  # 次元数が大きい場合は切り詰める
    padded_vectors.append(padded_vector)
  return padded_vectors

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
    
    user_vectors = [v for v in user_vectors if v is not None]
    user_names = [user_names[i] for i, v in enumerate(user_vectors) if v is not None] # 対応するユーザー名も除外
    
    user_vectors = pad_vectors(user_vectors, target_dim=768)  # 次元数を768に揃える
    user_vectors = np.array(user_vectors) # 修正後のベクトルを変換

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