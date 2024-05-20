from flask import Flask, request, jsonify
from pycorrector import MacBertCorrector
# from pycorrector import ErnieCscCorrector
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 加载预训练模型
m = MacBertCorrector('shibing624/macbert4csc-base-chinese')
# m = ErnieCscCorrector()


@app.route('/correct', methods=['POST'])
def correct_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    corrected_result = m.correct_batch([text])
    response = json.dumps({
        'corrected_result': corrected_result
    }, ensure_ascii=False)
    return app.response_class(response, content_type='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# from flask import Flask, request, jsonify
# from paddlenlp import Taskflow  # 引入 Taskflow
# import json

# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

# # 加载预训练模型，使用 text_correction
# corrector = Taskflow("text_correction")

# @app.route('/correct', methods=['POST'])
# def correct_text():
#     data = request.get_json()
#     if not data or 'text' not in data:
#         return jsonify({'error': 'No text provided'}), 400

#     text = data['text']
#     # 使用 Taskflow 进行纠错
#     corrected_result = corrector(text)
#     response = json.dumps({
#         'corrected_result': corrected_result
#     }, ensure_ascii=False)
#     return app.response_class(response, content_type='application/json')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)
