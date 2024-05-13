import streamlit as st
import pandas as pd
import nltk
nltk.download('punkt')
from nltk import tokenize
from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
import docx2txt
from PyPDF2 import PdfReader
import plotly.express as px

def get_sentences(text):
    sentences = tokenize.sent_tokenize(text)
    return sentences

def get_url(sentence):
    base_url = 'https://www.google.com/search?q='
    query = sentence
    query = query.replace(' ', '+')
    url = base_url + query
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    divs = soup.find_all('div', class_='yuRUbf')
    urls = []
    for div in divs:
        a = div.find('a')
        urls.append(a['href'])
    if len(urls) == 0:
        return None
    elif "youtube" in urls[0]:
        return None
    else:
        return urls[0]

def read_text_file(file):
    content = ""
    with io.open(file.name, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def read_docx_file(file):
    text = docx2txt.process(file)
    return text

def read_pdf_file(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_from_file(uploaded_file):
    content = ""
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            content = read_text_file(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            content = read_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = read_docx_file(uploaded_file)
    return content

def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

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
def get_similarity_list2(text, url_list):
    similarity_list = []
    for url in url_list:
        text2 = get_text(url)
        similarity = get_similarity(text, text2)
        similarity_list.append(similarity)
    return similarity_list

def plot_scatter(df):
    fig = px.scatter(df, x='File 1', y='File 2', color='Similarity', title='Similarity Scatter Plot')
    st.plotly_chart(fig, use_container_width=True)

def plot_line(df):
    fig = px.line(df, x='File 1', y='File 2', color='Similarity', title='Similarity Line Chart')
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(df):
    fig = px.bar(df, x='File 1', y='Similarity', color='File 2', title='Similarity Bar Chart')
    st.plotly_chart(fig, use_container_width=True)

def plot_pie(df):
    fig = px.pie(df, values='Similarity', names='File 1', title='Similarity Pie Chart')
    st.plotly_chart(fig, use_container_width=True)

def plot_box(df):
    fig = px.box(df, x='File 1', y='Similarity', title='Similarity Box Plot')
    st.plotly_chart(fig, use_container_width=True)

def plot_histogram(df):
    fig = px.histogram(df, x='Similarity', title='Similarity Histogram')
    st.plotly_chart(fig, use_container_width=True)

def plot_3d_scatter(df):
    fig = px.scatter_3d(df, x='File 1', y='File 2', z='Similarity', color='Similarity',
                        title='Similarity 3D Scatter Plot')
    st.plotly_chart(fig, use_container_width=True)

def plot_violin(df):
    fig = px.violin(df, y='Similarity', x='File 1', title='Similarity Violin Plot')
    st.plotly_chart(fig, use_container_width=True)



st.set_page_config(page_title='Plagiarism Detection')
st.title('Plagiarism Detector')

st.write("""
### Enter the text or upload a file to check for plagiarism or find similarities between files
""")
option = st.radio(
    "Select input option:",
    ('Enter text', 'Upload file', 'Find similarities between files')
)

if option == 'Enter text':
    text = st.text_area("Enter text here", height=200)
    uploaded_files = []
elif option == 'Upload file':
    uploaded_file = st.file_uploader("Upload file (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"])
    if uploaded_file is not None:
        text = get_text_from_file(uploaded_file)
        uploaded_files = [uploaded_file]
    else:
        text = ""
        uploaded_files = []
else:
    uploaded_files = st.file_uploader("Upload multiple files (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"], accept_multiple_files=True)
    texts = []
    filenames = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            text = get_text_from_file(uploaded_file)
            texts.append(text)
            filenames.append(uploaded_file.name)
    text = " ".join(texts)

if st.button('Check for plagiarism or find similarities'):
    st.write("""
    ### Checking for plagiarism or finding similarities...
    """)
    if not text:
        st.write("""
        ### No text found for plagiarism check or finding similarities.
        """)
        st.stop()
    
    if option == 'Find similarities between files':
        similarities = get_similarity_list(texts, filenames)
        df = pd.DataFrame(similarities, columns=['File 1', 'File 2', 'Similarity'])
        df = df.sort_values(by=['Similarity'], ascending=False)
        # Plotting interactive graphs
        plot_scatter(df)
        plot_line(df)
        plot_bar(df)
        plot_pie(df)
        plot_box(df)
        plot_histogram(df)
        plot_3d_scatter(df)
        plot_violin(df)
    else:
        sentences = get_sentences(text)
        url = []
        for sentence in sentences:
            url.append(get_url(sentence))

        if None in url:
            st.write("""
            ### No plagiarism detected!
            """)
            st.stop()

        similarity_list = get_similarity_list2(text, url)
        df = pd.DataFrame({'Sentence': sentences, 'URL': url, 'Similarity': similarity_list})
        df = df.sort_values(by=['Similarity'], ascending=True)
    
    df = df.reset_index(drop=True)
    
    # Make URLs clickable in the DataFrame
    if 'URL' in df.columns:
        df['URL'] = df['URL'].apply(lambda x: '<a href="{}">{}</a>'.format(x, x) if x else '')
    
    # Center align URL column header
    df_html = df.to_html(escape=False)
    if 'URL' in df.columns:
        df_html = df_html.replace('<th>URL</th>', '<th style="text-align: center;">URL</th>')
    st.write(df_html, unsafe_allow_html=True)
    
   