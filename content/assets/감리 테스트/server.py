import os
import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

def get_category(filename):
    if '건설기술' in filename: return '건설기술 진흥법'
    if '건설산업' in filename: return '건설산업기본법'
    if '산업안전' in filename: return '산업안전보건법'
    return '기타'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files: return "파일이 없습니다.", 400
    file = request.files['file']
    if file.filename == '': return "파일명이 없습니다.", 400

    category = get_category(file.filename)
    os.makedirs(category, exist_ok=True)
    
    filepath = os.path.join(category, file.filename)
    file.save(filepath)
    return jsonify({"message": "성공", "category": category})

@app.route('/files', methods=['GET'])
def get_files():
    files_data = []
    categories = ['건설기술 진흥법', '건설산업기본법', '산업안전보건법', '기타']
    
    for cat in categories:
        if os.path.exists(cat):
            for f in os.listdir(cat):
                if f.endswith('.pdf'):
                    filepath = os.path.join(cat, f)
                    stat = os.stat(filepath)
                    files_data.append({
                        "id": f, "name": f, "category": cat,
                        "size": stat.st_size,
                        "date": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
                        "url": f"/{cat}/{f}"
                    })
    return jsonify(files_data)

# 💡 [신규] 파일 삭제 기능 API
@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.json
    category = data.get('category')
    filename = data.get('filename')
    
    filepath = os.path.join(category, filename)
    if os.path.exists(filepath):
        os.remove(filepath) # 실제 윈도우 폴더에서 파일 삭제
        return jsonify({"message": "삭제 완료"})
    return jsonify({"message": "파일을 찾을 수 없습니다."}), 404

@app.route('/<category>/<filename>')
def serve_pdf(category, filename):
    return send_from_directory(category, filename)

if __name__ == '__main__':
    print("🚀 감리 법령 문서 서버가 시작되었습니다! (포트: 8000)")
    app.run(host='0.0.0.0', port=8000, debug=True)