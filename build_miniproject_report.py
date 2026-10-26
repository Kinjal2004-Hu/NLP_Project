from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    return h

def add_para(doc, text, size=12, bold=False, align=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.font.name = 'Times New Roman'
    return p

def add_code_block(doc, code):
    for line in code.split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(line if line.strip() else ' ')
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

def add_output_block(doc, out):
    for line in out.split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(line if line.strip() else ' ')
        r.font.name = 'Consolas'
        r.font.size = Pt(9)

def add_image(doc, path, width=5.5):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)

# ---- TITLE PAGE ----
for _ in range(3):
    doc.add_paragraph('')
add_para(doc, 'NLP Mini Project Report', size=22, bold=True, align='center')
doc.add_paragraph('')
add_para(doc, 'NLP-Based Job Description Keyword Extractor', size=16, bold=True, align='center')
doc.add_paragraph('')
add_para(doc, 'Submitted in fulfilment of the requirements of the', size=12, align='center')
add_para(doc, 'NLP Mini Project Semester VII in degree of', size=12, align='center')
add_para(doc, 'Bachelor of Computer Engineering', size=12, align='center')
doc.add_paragraph('')
add_para(doc, 'BY', size=13, bold=True, align='center')
doc.add_paragraph('')
add_para(doc, 'Mr. Kinjal Shivprasad Ojha (Roll No. 21)', size=12, align='center')
add_para(doc, 'Mr. Ashish Sharma (Roll No. 54)', size=12, align='center')
doc.add_paragraph('')
add_para(doc, 'Under the Guidance of', size=11, align='center')
add_para(doc, 'Ms. Rujuta Vartak', size=12, bold=True, align='center')
doc.add_paragraph('')
doc.add_paragraph('')
add_para(doc, 'Department of Computer Engineering', size=11, align='center')
add_para(doc, 'Shree L. R. Tiwari College of Engineering', size=11, align='center')
add_para(doc, 'Kanakia Park, Mira Road (E), Thane - 401 107, Maharashtra.', size=11, align='center')
add_para(doc, '2026-27', size=11, align='center')
doc.add_page_break()

# ---- APPROVAL ----
add_para(doc, 'NLP Mini Project Report Approval', size=14, bold=True, align='center')
doc.add_paragraph('')
add_para(doc, 'This project report entitled "NLP-Based Job Description Keyword Extractor" by Mr. Kinjal Shivprasad Ojha (Roll No. 21) and Mr. Ashish Sharma (Roll No. 54) is approved for the Mini Project Semester VII project work of B.E CMPN at Shree L.R.Tiwari College of Engineering, in the academic year 2026-2027.', size=12)
doc.add_paragraph('')
doc.add_paragraph('')
add_para(doc, 'Internal Examiner', size=12, bold=True)
doc.add_page_break()

# ---- DECLARATION ----
add_para(doc, 'Declaration', size=14, bold=True, align='center')
doc.add_paragraph('')
add_para(doc, 'I declare that this written submission represents my ideas in my own words and where others\' ideas or words have been included, I have adequately cited and referenced the original sources. I also declare that I have adhered to all principles of academic honesty and integrity and have not misrepresented or fabricated or falsified any idea/data/fact/source in my submission. I understand that any violation of the above will be cause for disciplinary action by the Institute and can also evoke penal action from the sources which have thus not been properly cited or from whom proper permission has not been taken when needed.', size=12)
doc.add_paragraph('')
doc.add_paragraph('')
add_para(doc, '--------------------------------------', size=12)
add_para(doc, 'Signature', size=12)
add_para(doc, 'Mr. Kinjal Shivprasad Ojha (Roll No. 21)', size=12)
doc.add_paragraph('')
add_para(doc, '--------------------------------------', size=12)
add_para(doc, 'Signature', size=12)
add_para(doc, 'Mr. Ashish Sharma (Roll No. 54)', size=12)
doc.add_paragraph('')
add_para(doc, 'Date:', size=12)
add_para(doc, 'Place:', size=12)
doc.add_page_break()

# ---- TABLE OF CONTENTS ----
add_para(doc, 'Table of Contents', size=14, bold=True, align='center')
doc.add_paragraph('')
toc_items = [
    '1. Introduction',
    '2. System Architecture',
    '3. Implementation',
    '4. Technologies Used',
    '5. Results',
    '6. Conclusion',
    '7. References'
]
for item in toc_items:
    add_para(doc, item, size=12)
doc.add_page_break()

# ---- 1. INTRODUCTION ----
add_para(doc, '1. Introduction', size=14, bold=True)
doc.add_paragraph('')
intro = """In today's competitive job market, job descriptions contain critical information about the skills, qualifications, and technologies that employers expect from candidates. Manually analyzing multiple job descriptions to identify key requirements is time-consuming and inefficient. Natural Language Processing (NLP) provides automated techniques to process and extract meaningful information from unstructured text data.

This project, titled "NLP-Based Job Description Keyword Extractor", aims to develop an NLP-based system that processes job descriptions and extracts important technical skills, qualifications, and keywords using tokenization, stop-word removal, and keyword extraction techniques.

The system helps students understand employer requirements and identify the skills needed for a particular job role. By analyzing multiple job descriptions, the system highlights the most frequently occurring and most important terms (such as programming languages, frameworks, tools, and soft skills), enabling students to plan their careers, identify skill gaps, and prepare more effectively for job opportunities.

The main objectives of this project are:
1. To preprocess job description text by converting to lowercase, removing punctuation, and eliminating stop words.
2. To tokenize the text into individual words for analysis.
3. To extract keywords using TF-IDF (Term Frequency-Inverse Document Frequency) scoring.
4. To visualize the extracted keywords using bar charts for easy interpretation.
5. To present the top keywords for each job description as well as across all job descriptions."""
add_para(doc, intro, size=12)
doc.add_page_break()

# ---- 2. SYSTEM ARCHITECTURE ----
add_para(doc, '2. System Architecture', size=14, bold=True)
doc.add_paragraph('')
arch = """The system follows a sequential NLP pipeline architecture consisting of the following stages:

1. Input Stage: The system accepts one or more job description texts as input. Each job description is a free-form text containing information about the job role, required skills, qualifications, and responsibilities.

2. Preprocessing Stage: The raw text is preprocessed by converting all characters to lowercase and removing punctuation and special characters using regular expressions. This ensures uniformity in the text data.

3. Tokenization Stage: The preprocessed text is split into individual tokens (words) based on whitespace. This breaks down the text into meaningful units for further analysis.

4. Stop-Word Removal Stage: Common English stop words (such as 'a', 'the', 'is', 'are', 'with', 'and', etc.) and domain-specific filler words (such as 'candidate', 'experience', 'skills', etc.) are removed from the token list. This filters out words that do not contribute meaningful information about the job requirements.

5. Keyword Extraction Stage: TF-IDF (Term Frequency-Inverse Document Frequency) is applied to compute the importance of each term across the job descriptions. TF-IDF gives higher scores to terms that appear frequently in a specific document but rarely across all documents, identifying the most distinctive keywords.

6. Visualization Stage: The extracted keywords and their scores are visualized using horizontal bar charts. Word frequency across all documents and per-document TF-IDF scores are displayed graphically.

7. Output Stage: The system outputs the top 15 keywords by frequency, the top 5 TF-IDF keywords for each job description, and the top 10 keywords by mean TF-IDF score, along with the generated graphs.

The architecture can be summarized as:
Input Text -> Lowercase Conversion -> Punctuation Removal -> Tokenization -> Stop-Word Removal -> TF-IDF Computation -> Keyword Ranking -> Visualization -> Output"""
add_para(doc, arch, size=12)
doc.add_page_break()

# ---- 3. IMPLEMENTATION ----
add_para(doc, '3. Implementation', size=14, bold=True)
doc.add_paragraph('')
add_para(doc, 'The project is implemented in Python using scikit-learn for TF-IDF vectorization, matplotlib for visualization, and standard libraries for text preprocessing. The complete source code is given below:', size=12)
doc.add_paragraph('')
with open('MiniProject_KeywordExtractor.py', 'r') as f:
    code = f.read()
add_code_block(doc, code)
doc.add_page_break()

# ---- 4. TECHNOLOGIES USED ----
add_para(doc, '4. Technologies Used', size=14, bold=True)
doc.add_paragraph('')
techs = [
    ('Python 3.14', 'Primary programming language used for implementing the NLP pipeline.'),
    ('scikit-learn', 'Used for TF-IDF vectorization (TfidfVectorizer) to compute term importance scores.'),
    ('Matplotlib', 'Used for generating bar chart visualizations of keyword frequencies and TF-IDF scores.'),
    ('Pandas', 'Used for data manipulation and handling of text data.'),
    ('NumPy', 'Used for numerical operations on TF-IDF score arrays.'),
    ('Regular Expressions (re)', 'Used for removing punctuation and special characters during preprocessing.'),
    ('Collections (Counter)', 'Used for counting word frequencies across the job descriptions.')
]
for name, desc in techs:
    p = doc.add_paragraph()
    r1 = p.add_run(f'{name}: ')
    r1.bold = True
    r1.font.size = Pt(12)
    r2 = p.add_run(desc)
    r2.font.size = Pt(12)
doc.add_page_break()

# ---- 5. RESULTS ----
add_para(doc, '5. Results', size=14, bold=True)
doc.add_paragraph('')
add_para(doc, 'The system was tested on three sample job descriptions: Data Scientist, Software Developer, and Web Developer. The following results were obtained:', size=12)
doc.add_paragraph('')
add_para(doc, '5.1 Top 15 Keywords by Frequency', size=12, bold=True)
out1 = """Top 15 Keywords Across All Job Descriptions:
  data: 2
  learning: 2
  sql: 2
  cloud: 2
  development: 2
  git: 2
  react: 2
  scientist: 1
  python: 1
  machine: 1
  deep: 1
  tensorflow: 1
  pandas: 1
  numpy: 1
  visualization: 1"""
add_output_block(doc, out1)
doc.add_paragraph('')
add_image(doc, 'proj_word_freq.png', 5.5)
doc.add_paragraph('')
add_para(doc, '5.2 TF-IDF Top Keywords per Job Description', size=12, bold=True)
out2 = """TF-IDF Top Keywords per Job Description:

JD 1 (Data Scientist):
  learning: 0.6276
  data: 0.6276
  aws: 0.3138
  cloud: 0.2386
  sql: 0.2386

JD 2 (Software Developer):
  development: 0.6767
  angular: 0.3383
  api: 0.3383
  boot: 0.3383
  git: 0.2573

JD 3 (Web Developer):
  js: 0.6767
  control: 0.3383
  css: 0.3383
  communication: 0.3383
  cloud: 0.2573"""
add_output_block(doc, out2)
doc.add_paragraph('')
add_image(doc, 'proj_tfidf_jd.png', 6.0)
doc.add_paragraph('')
add_para(doc, '5.3 Top 10 Keywords by Mean TF-IDF', size=12, bold=True)
add_image(doc, 'proj_mean_tfidf.png', 5.5)
doc.add_page_break()

# ---- 6. CONCLUSION ----
add_para(doc, '6. Conclusion', size=14, bold=True)
doc.add_paragraph('')
conclusion = """Thus, we studied the applications of Natural Language Processing and selected Job Description Keyword Extraction as our mini-project. The system uses tokenization to split text into smaller units, stop-word removal to eliminate common words, and keyword extraction to identify important skills and qualifications from job descriptions. This application can help students plan their careers, identify skill gaps, and prepare more effectively for job opportunities.

The TF-IDF based keyword extraction successfully identified the most relevant technical terms for each job role. For the Data Scientist role, terms like 'learning', 'data', 'aws', and 'cloud' were highlighted. For the Software Developer role, 'development', 'angular', 'api', and 'boot' emerged as key terms. For the Web Developer role, 'js', 'css', 'control', and 'communication' were identified as important. The word frequency analysis revealed that terms like 'data', 'learning', 'sql', 'cloud', 'development', 'git', and 'react' appear across multiple job descriptions, indicating commonly demanded skills in the industry.

The system demonstrates the effectiveness of basic NLP techniques (tokenization, stop-word removal, and TF-IDF) in extracting meaningful keywords from unstructured job description text. Future enhancements could include the use of more advanced techniques such as named entity recognition (NER), RAKE (Rapid Automatic Keyword Extraction), and integration of a comprehensive skills database to improve extraction accuracy and coverage."""
add_para(doc, conclusion, size=12)
doc.add_page_break()

# ---- 7. REFERENCES ----
add_para(doc, '7. References', size=14, bold=True)
doc.add_paragraph('')
refs = [
    '1. Bird, S., Klein, E., and Loper, E. "Natural Language Processing with Python." O\'Reilly Media, 2009.',
    '2. Manning, C. D., Raghavan, P., and Schutze, H. "Introduction to Information Retrieval." Cambridge University Press, 2008.',
    '3. scikit-learn Documentation: TF-IDF Vectorizer - https://scikit-learn.org/stable/modules/feature_extraction.html',
    '4. Jurafsky, D. and Martin, J. H. "Speech and Language Processing." 3rd Edition, 2023.',
    '5. Ratnasekar, D. and Vasanth, S. "Keyword Extraction from Job Descriptions using NLP." International Journal of Advanced Research in Computer Science, 2020.',
    '6. Matplotlib Documentation: https://matplotlib.org/stable/contents.html'
]
for ref in refs:
    add_para(doc, ref, size=12)

doc.save('NLP_MiniProject_Report_Kinjal_Ashish.docx')
print('saved NLP_MiniProject_Report_Kinjal_Ashish.docx')
