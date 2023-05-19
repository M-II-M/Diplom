# from flask import Flask
import whisper


# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     model = whisper.load_model("large")
#     result = model.transcribe("test.ogg", language="ru")
#     print(result["text"])
#     return 'Diplom'
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


model = whisper.load_model("large")
result = model.transcribe("test.ogg", language="ru")
print(result["text"])
