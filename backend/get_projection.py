import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
from transformers import AutoTokenizer, AutoModel
import torch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
import nltk

nltk.download('stopwords')
nltk.download('punkt')

df = pd.read_csv("../filtered_df.csv")
def get_sentence_embedding(sentence, model, tokenizer):
    # Tokenize input sentence
    tokens = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)

    # Get the transformer model output
    with torch.no_grad():
        outputs = model(**tokens)

    # Extract the output embeddings (CLS token)
    embeddings = outputs.last_hidden_state[:, 0, :]

    return embeddings.numpy()

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def preprocess(doc):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    processed_docs = []
    words = [ps.stem(word.lower()) for word in word_tokenize(doc) if word.isalpha() and word.lower() not in stop_words]
    return words

def calculate_term_frequency(documents):
    term_frequency = Counter()
    for doc in documents:
        term_frequency.update(doc)
    return term_frequency

subset["preprocessed"] = subset["Reviews"].apply(preprocess)
tf_group = [calculate_term_frequency(subset["preprocessed"][subset["cluster"] == i]) for i in range(3)]
terms_group_more = [{term: tf_group[i][term] for term in tf_group[i] if tf_group[i][term] > tf_group[(i+1)%3][term] 
                        and tf_group[i][term] > tf_group[(i+2)%3][term]} for i in range(3)]
terms_group_more = [sorted(cnt.items(), key=lambda x: x[1], reverse=True) for cnt in terms_group_more]

def get_projection(mobile_name):
    subset = df[df["Product Name"] == mobile_name]
    subset["embedding"] = subset["Reviews"].apply(get_sentence_embedding, args = (model, tokenizer))
    pca = PCA(n_components=3)
    embed = np.vstack(subset["embedding"].to_numpy())
    project = pca.fit_transform(embed)
    kmeans = KMeans(n_clusters=3)
    clusters = kmeans.fit_predict(embed)
    subset["cluster"] = clusters
    subset["x"] = project[:,0]
    subset["y"] = project[:,1]
    subset["z"] = project[:,2]

    subset["preprocessed"] = subset["Reviews"].apply(preprocess)
    tf_group = [calculate_term_frequency(subset["preprocessed"][subset["cluster"] == i]) for i in range(3)]
    terms_group_more = [{term: tf_group[i][term] for term in tf_group[i] if tf_group[i][term] > tf_group[(i+1)%3][term] 
                            and tf_group[i][term] > tf_group[(i+2)%3][term]} for i in range(3)]
    terms_group_more = [sorted(cnt.items(), key=lambda x: x[1], reverse=True) for cnt in terms_group_more]

    forbidden = ['phone', 'device','also','go','could','use','make','would','remov','review','english','feel','like','howev','small']  # Lista de palabras prohibidas
    num_words_per_cluster = 5  # Número de palabras por clúster

    rating_words = [{} for _ in range(3)]

    for i in range(3):
        subset_cluster = subset[subset["cluster"] == i].copy()  # Crear una copia para evitar advertencias

        rating_words[i]['total'] = round(subset_cluster["Rating"].mean(), 2)

        # Filtrar palabras prohibidas
        cluster_words = [word for word in terms_group_more[i] if word[0] not in forbidden][0:num_words_per_cluster]

        # Asegúrate de que "preprocessed" esté presente en tu DataFrame
        if "preprocessed" in subset_cluster.columns:
            for word in cluster_words:
                reviews = subset_cluster[subset_cluster["preprocessed"].apply(lambda x: any(word[0] in s for s in x))]
                rating_words[i][word[0]] = round(reviews["Rating"].mean(), 2)

    subset["labels"] = [str(rating_words[c]).replace(',', '<br>') for c in clusters]
