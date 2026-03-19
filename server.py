import os
import uuid
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Import existing logic
from preprocessing.preprocess import preprocess_image
from ocr.ocr_engine import run_ocr
from line_items.table_extraction import group_text_by_rows, parse_row_by_columns
from validation.validate import is_valid_line_item
from utils.cleaners import clean_description

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique ID for this processing task
        task_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}.{ext}")
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_processed.{ext}")
        
        file.save(input_path)
        
        try:
            # Step 1: Preprocessing
            preprocess_image(input_path, processed_path)
            
            # Step 2: OCR
            blocks = run_ocr(processed_path)
            
            # Step 3: Table Extraction
            rows = group_text_by_rows(blocks)
            
            final_items = []
            for row in rows:
                item = parse_row_by_columns(row["items"])
                if is_valid_line_item(item):
                    item["description"] = clean_description(item["description"])
                    final_items.append(item)
            
            # Return results
            return jsonify({
                "task_id": task_id,
                "invoice_number": "AUTO_DETECTED", # Placeholder or extracted
                "line_items": final_items,
                "processed_image_url": f"/uploads/{task_id}_processed.{ext}"
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
