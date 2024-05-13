# Plagarism Detector
The Plagiarism Detector project provides a comprehensive solution for detecting plagiarism and finding similarities between text documents. Leveraging the power of natural language processing (NLP), web scraping techniques, and data visualization tools, the project offers users a user-friendly interface to input text or upload files for analysis. The system employs algorithms such as tokenization, cosine similarity calculation, and web scraping to extract relevant information and compare text content. Through an intuitive web application built using Streamlit, users can easily identify potential instances of plagiarism or similarities between documents. The project also includes interactive visualizations, powered by Plotly and Plotly Express, to present the results in a clear and informative manner. Overall, the Plagiarism Detector project serves as a valuable tool for educators, researchers, and content creators to ensure the integrity and originality of written work.

## Features

- Light/dark mode toggle
- Fullscreen mode
- Flexible Input Options 
- Comprehensive Analysis
- Web Scraping Capabilities
- Advanced Similarity Measurement
- Interactive Visualizations
- User-Friendly Interface

## Tech Stack

**Client:** Streamlit, HTML/CSS.

**Server:** Python

**Libraries & Algorithms:** 

*Libraries:*
- Pandas
- NLTK (Natural Language Toolkit)
- Beautiful Soup
- CountVectorizer and cosine_similarity from scikit-learn
- docx2txt
- PyPDF2
- plotly.express (px)
  
*Algorithms:*
- Tokenization
- Cosine Similarity
- Web Scraping
- Document Retrieval
- Data Visualization


## Usage/Examples

```python
def get_similarity(text1, text2):
    text_list = [text1, text2]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    similarity = cosine_similarity(count_matrix)[0][1]
    return similarity

def get_similarity_list(texts, filenames=None):
    similarity_list = []
    if filenames is None:
        filenames = [f"File {i+1}" for i in range(len(texts))]
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            similarity = get_similarity(texts[i], texts[j])
            similarity_list.append((filenames[i], filenames[j], similarity))
    return similarity_list
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/Karthik-02/plagiarism-detection.git
```

Go to the project directory

```bash
  cd plagiarism-detection
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run app.py
```
## Screenshots
![image](https://github.com/Karthik-02/plagiarism-detection/assets/81423983/68ab81eb-da46-4180-b25e-5cd88a609da9)

![image](https://github.com/Karthik-02/plagiarism-detection/assets/81423983/e0c97e0b-1122-4d28-ba46-95b16017d901)

![image](https://github.com/Karthik-02/plagiarism-detection/assets/81423983/09ebf7bc-1736-4927-a2e1-c27616831f35)

![image](https://github.com/Karthik-02/plagiarism-detection/assets/81423983/6b02553c-4c4c-4359-a551-b0f30067a0ba)

![image](https://github.com/Karthik-02/plagiarism-detection/assets/81423983/77223ada-a79b-419b-b1af-08aa58e0fc84)

![image](https://github.com/Karthik-02/plagiarism-detection/assets/81423983/0744bc50-6840-4893-a7c3-99e7834ab747)

## Authors
- [@KarthikS](https://www.github.com/Karthik-02)
  























## Badges
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
