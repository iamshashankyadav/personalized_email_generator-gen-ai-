import pandas as pd
import chromadb

import uuid

class Portfolio:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

        # ✅ Validate required columns
        required_columns = {"Techstack", "Links"}
        missing_columns = required_columns - set(self.data.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns in uploaded CSV: {', '.join(missing_columns)}")

        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )


    def query_links(self, skills):
        if isinstance(skills, list):
            query = " ".join(skills)
        else:
            query = skills  # assume it's already a string

        result = self.collection.query(query_texts=[query], n_results=2)
        return result.get('metadatas', [])


# Usage example
if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.load_portfolio()
    print(portfolio.query_links( ['instrumentation analytics and data governance', 'experimentation platforms', 'waterfall and Agile project management methodologies', 'cross-team and cross-organization collaboration', 'facilitation skills', 'verbal and written communication', 'presentation skills']))
