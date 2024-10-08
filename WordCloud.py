from flask import Flask, request, render_template, send_file
import jieba
from wordcloud import WordCloud
import os
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import stopwordsiso as stopwords

app = Flask(__name__)

# 加载自定义词典
jieba.load_userdict("dict_THUOCL.txt")

# 加载停用词
stop_words = set(stopwords.stopwords("zh"))


def process_text(text):
    # 使用Jieba进行分词
    words = jieba.cut(text)
    # 过滤掉停用词和长度小于1的词
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    word_freq = Counter(filtered_words)
    return word_freq


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    text = request.form.get('text')
    file = request.files.get('file')
    background = request.files.get('background')

    if file:
        text = file.read().decode('utf-8')

    if text:
        word_freq = process_text(text)

        # 设置词云的背景图片
        if background:
            background_img = plt.imread(background)
            wc = WordCloud(font_path="simhei.ttf", mask=background_img, background_color="white")
        else:
            wc = WordCloud(font_path="simhei.ttf", background_color="white")

        wc.generate_from_frequencies(word_freq)

        # 保存词云图片到内存
        img_io = BytesIO()
        plt.figure(figsize=(10, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(img_io, format='PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    else:
        return "请输入文本或上传文件！", 400


if __name__ == '__main__':
    app.run(debug=True)
