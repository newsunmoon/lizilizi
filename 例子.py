import jieba
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from collections import Counter
import re
import string
from bs4 import BeautifulSoup


# 定义数据清洗函数
def clean_text(text):
    text = text.replace('\n', '')
    text = text.replace(' ', '')
    text = text.strip()
    return text


# 定义分词函数
def segment(text):
    stopwords = ['的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '这', '那', '之', '与', '和', '或', '虽然',
                 '但是', '然而', '因此']
    # 移除标点符号和换行符
    punctuation = "、，。！？；：“”‘’~@#￥%……&*（）【】｛｝+-*/=《》<>「」『』【】〔〕｟｠«»“”‘’'':;,/\\|[]{}()$^"
    text = text.translate(str.maketrans('', '', punctuation)).replace('\n', '')
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords]
    return words


# Removing punctuation, numbers
def remove_punctuation(text):
    text = re.sub(r'\d+', '', text)  # Using raw string to avoid warning
    return re.sub(f'[{re.escape(string.punctuation)}]', '', text)


def extract_body_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('body').get_text()
    return text


def run():
    st.set_page_config(
        page_title="Text Analysis",
        page_icon="📚",
    )

    st.write("# Welcome to the Text Analysis App! 📚")

    url = st.text_input('Enter URL to analyze:')

    if url:
        try:
            r = requests.get(url)
            r.encoding = 'utf-8'
            text = r.text
            text = extract_body_text(text)
            text = remove_punctuation(text)
            text = clean_text(text)
            words = segment(text)
            word_counts = Counter(words)

            top_words = word_counts.most_common(20)

            wordcloud_options = {
                "tooltip": {
                    "trigger": 'item',
                    "formatter": '{b} : {c}'
                },
                "xAxis": [{
                    "type": "category",
                    "data": [word for word, count in top_words],
                    "axisLabel": {
                        "interval": 0,
                        "rotate": 30
                    }
                }],
                "yAxis": [{"type": "value"}],
                "series": [{
                    "type": "bar",
                    "data": [count for word, count in top_words]
                }]
            }

            st_echarts(wordcloud_options, height='500px')
        except Exception as e:
            st.write(f"An error occurred: {e}")


if __name__ == "__main__":
    run()
