from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'with', 'in', 'on', 'to', 'of', 'for', 'is', 'are',
    'have', 'has', 'should', 'must', 'we', 'our', 'such', 'as', 'by', 'not', 'be',
    'this', 'that', 'it', 'its', 'who', 'whom', 'whose', 'which', 'what', 'where',
    'when', 'how', 'why', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'than', 'too', 'very', 'can', 'will', 'just', 'do', 'does', 'did', 'done',
    'but', 'if', 'then', 'else', 'while', 'at', 'from', 'up', 'down', 'out', 'off',
    'over', 'under', 'again', 'further', 'once', 'here', 'there', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'need', 'looking', 'required', 'preferred', 'essential', 'expected', 'strong',
    'good', 'basic', 'plus', 'candidate', 'job', 'description', 'developer',
    'knowledge', 'experience', 'skills', 'role', 'using'
}


def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.split()


def extract_keywords(job_descriptions):
    all_words = []
    for jd in job_descriptions:
        all_words.extend(preprocess(jd))

    filtered = [w for w in all_words if w not in STOP_WORDS and len(w) > 2]
    freq = Counter(filtered)
    top_words = freq.most_common(15)

    vectorizer = TfidfVectorizer(stop_words=list(STOP_WORDS), max_features=15)
    tfidf_matrix = vectorizer.fit_transform(job_descriptions)
    feature_names = vectorizer.get_feature_names_out()

    jd_keywords = []
    for i in range(len(job_descriptions)):
        scores = tfidf_matrix[i].toarray().flatten()
        top_idx = scores.argsort()[::-1][:5]
        keywords = []
        for j in top_idx:
            if scores[j] > 0:
                keywords.append({
                    'term': feature_names[j],
                    'score': round(float(scores[j]), 4)
                })
        jd_keywords.append(keywords)

    mean_scores = tfidf_matrix.toarray().mean(axis=0)
    sorted_idx = mean_scores.argsort()[::-1][:10]
    mean_keywords = [
        {'term': feature_names[j], 'score': round(float(mean_scores[j]), 4)}
        for j in sorted_idx
    ]

    return {
        'word_frequency': [{'word': w, 'count': c} for w, c in top_words],
        'jd_keywords': jd_keywords,
        'mean_tfidf': mean_keywords
    }


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return data


def generate_frequency_chart(word_frequency):
    words = [w['word'] for w in word_frequency][::-1]
    counts = [w['count'] for w in word_frequency][::-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(words, counts, color='teal')
    ax.set_xlabel('Frequency')
    ax.set_title('Top Keywords by Frequency')
    return fig_to_base64(fig)


def generate_tfidf_chart(jd_keywords):
    fig, axes = plt.subplots(1, len(jd_keywords), figsize=(5 * len(jd_keywords), 5))
    if len(jd_keywords) == 1:
        axes = [axes]
    colors = ['coral', 'steelblue', 'seagreen', 'mediumpurple', 'gold']
    for i, kws in enumerate(jd_keywords):
        terms = [k['term'] for k in kws][::-1]
        scores = [k['score'] for k in kws][::-1]
        axes[i].barh(terms, scores, color=colors[i % len(colors)])
        axes[i].set_title(f'JD {i+1} Top TF-IDF')
        axes[i].set_xlabel('TF-IDF Score')
    plt.tight_layout()
    return fig_to_base64(fig)


def generate_mean_chart(mean_keywords):
    terms = [k['term'] for k in mean_keywords][::-1]
    scores = [k['score'] for k in mean_keywords][::-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(terms, scores, color='mediumpurple')
    ax.set_xlabel('Mean TF-IDF Score')
    ax.set_title('Top Keywords by Mean TF-IDF')
    return fig_to_base64(fig)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/extract', methods=['POST'])
def api_extract():
    data = request.get_json()
    job_descriptions = data.get('job_descriptions', [])

    job_descriptions = [jd.strip() for jd in job_descriptions if jd.strip()]
    if not job_descriptions:
        return jsonify({'error': 'No job descriptions provided'}), 400

    results = extract_keywords(job_descriptions)

    freq_chart = generate_frequency_chart(results['word_frequency'])
    tfidf_chart = generate_tfidf_chart(results['jd_keywords'])
    mean_chart = generate_mean_chart(results['mean_tfidf'])

    return jsonify({
        'results': results,
        'charts': {
            'frequency': freq_chart,
            'tfidf': tfidf_chart,
            'mean': mean_chart
        },
        'num_jds': len(job_descriptions),
        'total_words': sum(len(preprocess(jd)) for jd in job_descriptions)
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
