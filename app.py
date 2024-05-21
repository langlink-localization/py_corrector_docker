import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from pycorrector import MacBertCorrector
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 加载预训练模型
m = MacBertCorrector('shibing624/macbert4csc-base-chinese')

# 配置日志
if not app.debug:
    # 在生产环境下配置日志
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask startup')

@app.route('/correct', methods=['POST'])
def correct_text():
    data = request.get_json()
    if not data or 'text' not in data:
        app.logger.error('No text provided')
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    corrected_result = m.correct_batch([text])
    response = json.dumps({
        'corrected_result': corrected_result
    }, ensure_ascii=False)
    app.logger.info(f'Corrected text: {corrected_result}')
    return app.response_class(response, content_type='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
