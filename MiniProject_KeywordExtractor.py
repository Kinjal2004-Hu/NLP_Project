from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import re

job_descriptions = [
    """We are looking for a Data Scientist with experience in Python, Machine Learning, Deep Learning, and SQL. The candidate should have knowledge of TensorFlow, Pandas, NumPy, and data visualization tools like Matplotlib. Strong analytical and problem-solving skills are required. Experience with cloud platforms such as AWS or Azure is preferred.""",
    """Job Description: Software Developer required. Must have strong skills in Java, Spring Boot, Microservices, REST API development, and SQL databases. Knowledge of Git, Docker, Kubernetes, and Agile methodology is essential. Candidate should have 2+ years of experience in full-stack development with React or Angular frontend.""",
    """We need a Web Developer proficient in HTML, CSS, JavaScript, React, Node.js, and MongoDB. The candidate should understand responsive design, version control using Git, and basic SEO principles. Experience with Express.js and deployment on cloud services is a plus. Good communication and teamwork skills are expected."""
]

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    return words

all_words = []
for jd in job_descriptions:
    all_words.extend(preprocess(jd))

stop_words = {'a', 'an', 'the', 'and', 'or', 'with', 'in', 'on', 'to', 'of', 'for', 'is', 'are', 'have', 'has', 'should', 'must', 'we', 'our', 'the', 'such', 'as', 'by', 'not', 'be', 'this', 'that', 'it', 'its', 'who', 'whom', 'whose', 'which', 'what', 'where', 'when', 'how', 'why', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'than', 'too', 'very', 'can', 'will', 'just', 'do', 'does', 'did', 'done', 'but', 'if', 'then', 'else', 'while', 'at', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'once', 'here', 'there', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'need', 'looking', 'required', 'preferred', 'essential', 'expected', 'strong', 'good', 'basic', 'plus', 'candidate', 'job', 'description', 'developer', 'knowledge', 'experience', 'skills', 'role', 'using'}

filtered = [w for w in all_words if w not in stop_words and len(w) > 2]
freq = Counter(filtered)
top_words = freq.most_common(15)
print("Top 15 Keywords Across All Job Descriptions:")
for word, count in top_words:
    print(f"  {word}: {count}")

vectorizer = TfidfVectorizer(stop_words=list(stop_words), max_features=15)
tfidf_matrix = vectorizer.fit_transform(job_descriptions)
feature_names = vectorizer.get_feature_names_out()

print("\nTF-IDF Top Keywords per Job Description:")
for i, jd in enumerate(job_descriptions):
    scores = tfidf_matrix[i].toarray().flatten()
    top_idx = scores.argsort()[::-1][:5]
    top_terms = [(feature_names[j], round(scores[j], 4)) for j in top_idx if scores[j] > 0]
    print(f"\nJD {i+1}:")
    for term, score in top_terms:
        print(f"  {term}: {score}")

words_list, counts_list = zip(*top_words)
plt.figure(figsize=(10, 5))
plt.barh(words_list[::-1], counts_list[::-1], color='teal')
plt.xlabel('Frequency')
plt.title('Top 15 Keywords Across Job Descriptions')
plt.tight_layout()
plt.savefig('proj_word_freq.png', dpi=150)
print("\nSaved: proj_word_freq.png")

plt.figure(figsize=(10, 5))
for i in range(len(job_descriptions)):
    scores = tfidf_matrix[i].toarray().flatten()
    top_idx = scores.argsort()[::-1][:5]
    top_terms = [feature_names[j] for j in top_idx if scores[j] > 0]
    top_scores = [scores[j] for j in top_idx if scores[j] > 0]
    plt.subplot(1, 3, i+1)
    plt.barh(top_terms[::-1], top_scores[::-1], color=['coral', 'steelblue', 'seagreen'][i])
    plt.title(f'JD {i+1} Top TF-IDF')
    plt.xlabel('TF-IDF Score')
plt.tight_layout()
plt.savefig('proj_tfidf_jd.png', dpi=150)
print("Saved: proj_tfidf_jd.png")

plt.figure(figsize=(8, 5))
all_tfidf_scores = tfidf_matrix.toarray().mean(axis=0)
sorted_idx = all_tfidf_scores.argsort()[::-1][:10]
plt.barh([feature_names[j] for j in sorted_idx][::-1], all_tfidf_scores[sorted_idx][::-1], color='mediumpurple')
plt.xlabel('Mean TF-IDF Score')
plt.title('Top 10 Keywords by Mean TF-IDF')
plt.tight_layout()
plt.savefig('proj_mean_tfidf.png', dpi=150)
print("Saved: proj_mean_tfidf.png")
