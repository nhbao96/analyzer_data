import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from data_processing import process_excel_file

app = Flask(__name__)

# Đặt đường dẫn cố định cho thư mục lưu trữ file
DATA_DIR = os.path.join(os.getcwd(), 'data_dir')
os.makedirs(DATA_DIR, exist_ok=True)

# Route để hiển thị giao diện welcome
@app.route('/')
def index():
    return render_template('index.html')

# Route để xử lý upload file và xử lý dữ liệu
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Không có file nào được chọn"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(DATA_DIR, filename)  # Lưu file vào thư mục data_dir
        file.save(file_path)

        # Xử lý file Excel và lưu kết quả vào data_dir với tên {file_name}_Cleaned.xlsx
        output_file = process_excel_file(file_path, DATA_DIR)
        
        return jsonify({"message": "Xử lý file thành công", "processed_file": output_file})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
