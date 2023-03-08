import Levenshtein
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def jaccard_similarity(domain1, domain2):
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    X = vectorizer.fit_transform([domain1, domain2])
    jaccard_sim = cosine_similarity(X)[0][1]
    return jaccard_sim

def similarity_score(domain1, domain2):
    lev_distance = Levenshtein.distance(domain1, domain2)
    lev_similarity = 1 - (lev_distance / max(len(domain1), len(domain2)))
    jaccard_sim = jaccard_similarity(domain1, domain2)
    return (lev_similarity + jaccard_sim) / 2

log_file = "/data/dns/2022-08-13_dns.09:00:00-10:00:00.log"
threshold = 0.8

with open(log_file, "r") as f:
    domains = [line.strip() for line in f]

for i in range(len(domains)):
    for j in range(i+1, len(domains)):
        similarity = similarity_score(domains[i], domains[j])
        if similarity >= threshold:
            print("Similarity score:", similarity)
            print("Domain 1:", domains[i])
            print("Domain 2:", domains[j])
            print()
