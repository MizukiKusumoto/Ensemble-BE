from transformers import BertJapaneseTokenizer, BertModel
import numpy as np

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
        text = ""
    input_ids = tokenizer(text, return_tensors='pt')['input_ids']
    outputs = model(input_ids)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy().squeeze(0)