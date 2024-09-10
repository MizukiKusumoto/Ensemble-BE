from neomodel import db
from transformers import BertJapaneseTokenizer, BertModel
import numpy as np
from neo4j import GraphDatabase

from neomodel import config
config.DATABASE_URL = "bolt://neo4j:0oFKulfd@localhost:7687"

# BERTモデルの読み込み
model_name = 'cl-tohoku/bert-base-japanese-whole-word-masking'
tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def get_user_vector(attributes: list[str]) -> np.ndarray:
    """ユーザー属性のリストからベクトルを計算する。"""
    if isinstance(attributes, str):
        text = attributes
    elif isinstance(attributes, list):
        text = "、".join(attributes)
    else:  
        text = "" # attributesがリストでも文字列でもない場合の処理

    input_ids = tokenizer(text, return_tensors='pt')['input_ids']
    outputs = model(input_ids)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy().squeeze(0)

def read_all_users():
    """全ユーザーのnameとlabelを取得"""
    query = "MATCH (p:User) RETURN p.name AS name, p.label AS label"
    results, meta = db.cypher_query(query)
    
    # クエリ結果を辞書型のリストに変換
    users_data = [{'name': row[0], 'label': row[1]} for row in results]
    return users_data

def save_bert_vectors(users_data):
    """ユーザーデータのBERTベクトルを計算し、データベースの User.vector に格納する"""
    for user_data in users_data:
        user_name = user_data['name']
        attributes = user_data['label']  # labelはリスト形式で取得される
        
        # ベクトルを計算し、リストに変換
        vector = get_user_vector(attributes).tolist()  

        # ベクトルをデータベースに保存
        query = f"MATCH (u:User {{name: '{user_name}'}}) SET u.vector = {vector}"
        db.cypher_query(query)

if __name__ == "__main__":
    all_users = read_all_users()
    save_bert_vectors(all_users)
    print("BERTベクトルをデータベースに保存しました。")
    
# torch
# transformers
# fugashi
# ipadic