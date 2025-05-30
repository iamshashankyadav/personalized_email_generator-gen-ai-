import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Portfolio:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def load_portfolio(self):
        pass  # No vector DB to load

    def query_links(self, skills):
        if isinstance(skills, list):
            query = " ".join(skills)
        else:
            query = skills

        techstacks = self.data["Techstack"].fillna("").tolist()
        links = self.data["Links"].fillna("").tolist()

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(techstacks + [query])
        sim_scores = cosine_similarity(vectors[-1:], vectors[:-1])[0]

        top_indices = sim_scores.argsort()[-2:][::-1]  # top 2 results
        return [{"links": links[i]} for i in top_indices]
