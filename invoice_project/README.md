# Efficient Invoice Data Extraction 📄🚀

An automated pipeline designed to extract structured data (line items) from invoice images using advanced OCR and NLP techniques. This project streamlines the process of converting unstructured invoice images into machine-readable JSON format.

---

## 🏗️ Project Architecture

The project is organized into modular components, each handling a specific stage of the extraction pipeline:

- **`preprocessing/`**: Enhances raw images for optimal OCR performance.
- **`ocr/`**: Handles text detection and recognition using PaddleOCR.
- **`line_items/`**: Groups text into rows and extracts columnar data (Qty, Description, Price, Total).
- **`nlp/`**: Provides regex-based alternatives for field extraction and number normalization.
- **`validation/`**: Ensures data integrity by filtering out invalid or incomplete line items.
- **`utils/`**: Contains helper functions for text cleaning and regex-based normalization.

---

## 🛠️ Key Features

- **Advanced Preprocessing**: Uses OpenCV for grayscale conversion, Gaussian blurring, and adaptive thresholding to improve text clarity.
- **Robust OCR**: Leverages **PaddleOCR** for high-accuracy text extraction with offline support.
- **Spatial Extraction**: Intelligently groups text into rows based on vertical coordinates and maps them to columns using horizontal offsets.
- **Data Validation**: Built-in checks to ensure extracted items contain essential data (Description, Quantity, and Price/Total).
- **Clean Output**: Automatically removes noise (e.g., random numbers, percentages) from descriptions and outputs a structured `final_invoice.json`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenCV
- PaddlePaddle & PaddleOCR

### Installation

1. Install the required dependencies:
   ```bash
   pip install opencv-python paddlepaddle paddleocr
   ```

2. (Optional) Set environment variables for offline OCR execution:
   ```powershell
   $env:DISABLE_MODEL_SOURCE_CHECK="True"
   ```

---

## 📖 Usage

Place your invoice image (e.g., `invoice.jpg`) in the `input/` directory and run the main entry point:

```bash
python app.py
```

### Workflow Summary:
1. **Preprocessing**: Image is cleaned and saved as `input/preprocessed.jpg`.
2. **OCR**: PaddleOCR extracts text blocks with confidence scores and bounding boxes.
3. **Row Grouping**: Blocks are grouped into logical rows.
4. **Column Parsing**: Data is mapped to `qty`, `description`, `unit_price`, and `total`.
5. **Validation/Cleaning**: Items are validated and descriptions are sanitized.
6. **Output**: Results are saved to `final_invoice.json`.

---

## 📂 Directory Structure

```text
invoice_project/
├── app.py                  # Main execution script
├── preprocessing/          # Image cleaning logic (OpenCV)
├── ocr/                    # OCR engine wrapper (PaddleOCR)
├── line_items/             # Table extraction & parsing
├── nlp/                    # Field extraction & normalization
├── validation/             # Data integrity checks
├── utils/                  # Text cleaners & utilities
├── input/                  # Input images (invoice.jpg)
└── output/                 # Processed results
```

---

## ⚖️ License
Internal Use / Project Portfolio.
