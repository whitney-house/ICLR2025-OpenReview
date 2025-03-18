"""
load csv file and check top-k institutions and authors
"""
import csv
from collections import Counter
from constants import ACCEPT_KEYWORDS


class Analyser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.accepted_papers = self._load_papers()

    def _load_papers(self):
        """load all submissions, choose the accepted ones"""
        accepted_papers = []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Decision") in ACCEPT_KEYWORDS:
                    accepted_papers.append(row)
        return accepted_papers

    def top_calculations(self, category, k=5):
        """calculate ranking of institutions"""
        category_count = Counter()
        for paper in self.accepted_papers:
            categories = paper.get(category, "").split(",")
            for c in categories:
                c = c.strip()
                if c:
                    category_count[c] += 1
        return category_count.most_common(k)


if __name__ == "__main__":
    filepath = "test.csv"
    analyser = Analyser(filepath)

    top_inst = analyser.top_calculations('Affiliations', k=10)
    print(top_inst)
