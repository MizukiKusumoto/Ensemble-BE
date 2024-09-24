from api.models.main import User
from neomodel import db


# BERT関連のインポート（渡邊追加分）
from transformers import BertJapaneseTokenizer, BertModel
import numpy as np
from neo4j import GraphDatabase
from neomodel import config

# BERTモデルの読み込み（渡邊追加分）
model_name = "cl-tohoku/bert-base-japanese-whole-word-masking"
tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)


# ベクトル計算の関数（渡邊T追加分）
def get_user_vector(attributes: list[str]) -> np.ndarray:
    """ユーザー属性のリストからベクトルを計算する。"""
    if isinstance(attributes, str):
        text = attributes
    elif isinstance(attributes, list):
        text = "、".join(attributes)
    else:
        text = ""
    input_ids = tokenizer(text, return_tensors="pt")["input_ids"]
    outputs = model(input_ids)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy().squeeze(0)


# ユーザ属性の更新（渡邊T追加分）
def update_user_labels_func(user_id: str, labels: list) -> User:
    """ユーザーの属性を更新する"""
    try:
        user = User.nodes.get(element_id=user_id)
        user.labels = labels
        user.vector = get_user_vector(labels).tolist()  # BERTベクトルを再計算して更新
        user.save()
        return user
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")


@db.transaction
def create_user_func(name: str, email: str, password: str, labels: list) -> User:

    # labels を結合してBERTでベクトル化（渡邊追加分）
    vector = get_user_vector(labels).tolist()

    user = User(name=name, email=email, password=password, vector=vector).save()
    return user


def get_user_by_email_or_id_func(email: str | None, id: str | None) -> User:
    if email:
        return User.nodes.get_or_none(email=email)
    if id:
        query = f"MATCH (n) WHERE elementId(n) = '{id}' RETURN n"
        results, meta = db.cypher_query(query)
        return User.inflate(results[0][0])
    return None
