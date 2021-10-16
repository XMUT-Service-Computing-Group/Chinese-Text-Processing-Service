from flask import Flask, redirect

import NLPfunctions

app = Flask(__name__)
# 处理中文编码
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["GET"])
def readme():
    return redirect("https://github.com/XMUT-Service-Computing-Group/Chinese-Text-Processing-Service#readme", code=301)


@app.route("/key_words", methods=["GET"])
def key_words():
    return NLPfunctions.key_words()


@app.route("/sentiment_scores", methods=["GET"])
def sentiment_scores():
    return NLPfunctions.sentiment_scores()


@app.route("/sentiment_train", methods=["GET"])
def sentiment_train():
    return NLPfunctions.sentiment_train()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
