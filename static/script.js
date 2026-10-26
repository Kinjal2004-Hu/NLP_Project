const jdContainer = document.getElementById('jd-container');
const addBtn = document.getElementById('add-jd');
const extractBtn = document.getElementById('extract-btn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');

let jdCount = 1;

const SAMPLE_DATA = [
    "We are looking for a Data Scientist with experience in Python, Machine Learning, Deep Learning, and SQL. The candidate should have knowledge of TensorFlow, Pandas, NumPy, and data visualization tools like Matplotlib. Strong analytical and problem-solving skills are required. Experience with cloud platforms such as AWS or Azure is preferred.",
    "Job Description: Software Developer required. Must have strong skills in Java, Spring Boot, Microservices, REST API development, and SQL databases. Knowledge of Git, Docker, Kubernetes, and Agile methodology is essential. Candidate should have 2+ years of experience in full-stack development with React or Angular frontend.",
    "We need a Web Developer proficient in HTML, CSS, JavaScript, React, Node.js, and MongoDB. The candidate should understand responsive design, version control using Git, and basic SEO principles. Experience with Express.js and deployment on cloud services is a plus. Good communication and teamwork skills are expected."
];

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.jd-textarea').value = SAMPLE_DATA[0];
    if (location.search.includes('auto=1')) {
        extractBtn.click();
    }
});

addBtn.addEventListener('click', () => {
    jdCount++;
    const entry = document.createElement('div');
    entry.className = 'jd-entry';
    entry.innerHTML = `
        <label>Job Description ${jdCount}:</label>
        <textarea class="jd-textarea" rows="4" placeholder="Paste job description text here..."></textarea>
        <button class="btn-remove" onclick="removeEntry(this)">Remove</button>
    `;
    jdContainer.appendChild(entry);
    if (jdCount <= SAMPLE_DATA.length) {
        entry.querySelector('.jd-textarea').value = SAMPLE_DATA[jdCount - 1];
    }
});

function removeEntry(btn) {
    btn.parentElement.remove();
    jdCount--;
    renumberEntries();
}

function renumberEntries() {
    document.querySelectorAll('.jd-entry').forEach((entry, idx) => {
        entry.querySelector('label').textContent = `Job Description ${idx + 1}:`;
    });
    jdCount = document.querySelectorAll('.jd-entry').length;
}

extractBtn.addEventListener('click', async () => {
    const textareas = document.querySelectorAll('.jd-textarea');
    const jobDescriptions = Array.from(textareas).map(t => t.value.trim()).filter(v => v);

    if (jobDescriptions.length === 0) {
        alert('Please enter at least one job description.');
        return;
    }

    loading.classList.remove('hidden');
    results.classList.add('hidden');
    extractBtn.disabled = true;

    try {
        const response = await fetch('/api/extract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_descriptions: jobDescriptions })
        });

        if (!response.ok) {
            throw new Error('Extraction failed');
        }

        const data = await response.json();
        renderResults(data);
        results.classList.remove('hidden');
        results.scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        alert('Error: ' + err.message);
    } finally {
        loading.classList.add('hidden');
        extractBtn.disabled = false;
    }
});

function renderResults(data) {
    document.getElementById('num-jds').textContent = data.num_jds;
    document.getElementById('total-words').textContent = data.total_words;
    document.getElementById('unique-keywords').textContent = data.results.word_frequency.length;

    document.getElementById('freq-chart').src = 'data:image/png;base64,' + data.charts.frequency;
    document.getElementById('tfidf-chart').src = 'data:image/png;base64,' + data.charts.tfidf;
    document.getElementById('mean-chart').src = 'data:image/png;base64,' + data.charts.mean;

    const freqTbody = document.querySelector('#freq-table tbody');
    freqTbody.innerHTML = '';
    data.results.word_frequency.forEach((item, idx) => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${idx + 1}</td><td>${item.word}</td><td>${item.count}</td>`;
        freqTbody.appendChild(row);
    });

    const meanTbody = document.querySelector('#mean-table tbody');
    meanTbody.innerHTML = '';
    data.results.mean_tfidf.forEach((item, idx) => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${idx + 1}</td><td>${item.term}</td><td>${item.score}</td>`;
        meanTbody.appendChild(row);
    });

    const jdDiv = document.getElementById('jd-keywords');
    jdDiv.innerHTML = '';
    data.results.jd_keywords.forEach((kws, idx) => {
        const card = document.createElement('div');
        card.className = 'jd-keyword-card';
        let kwHtml = kws.map(k => `<span class="kw">${k.term}<span class="score">${k.score}</span></span>`).join('');
        card.innerHTML = `<h4>JD ${idx + 1} — Top 5 Keywords</h4>${kwHtml}`;
        jdDiv.appendChild(card);
    });
}
