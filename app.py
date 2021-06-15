from flask import Flask, render_template, request
from PIL import Image

from src.cnn_recognizer import CNNRecognizer
from src.fuzzy_recognizer import black_orientation, recognize_letter

app = Flask(__name__)
cnn = CNNRecognizer()


@app.route('/', methods=["get"])
def main():
    return render_template("main.html")


@app.route('/process', methods=["post"])
def process():
    if request.method == "POST":
        try:
            file = request.files["img_file"]
            image = Image.open(file)

            cnn_letter, probas = cnn.predict(image)

            fuzzy_data = black_orientation(image)
            fuzzy_letter = recognize_letter(fuzzy_data)
            return render_template("process.html",
                                   error=False,
                                   cnn_letter=cnn_letter,
                                   proba=max(probas),
                                   probas=[str(p) for p in probas],
                                   fuzzy_letter=fuzzy_letter)
        except Exception as e:
            print(e)
            return render_template("process.html", error=True)


if __name__ == '__main__':
    app.run(debug=True)
