# PDF Watermark Remover Tool

## Introduction
The PDF Watermark Remover Tool is a PyQt5-based application for removing watermarks from PDF documents.

## Algorithm Explanation
This tool utilizes the PyPDF library in Python to process PDF files. It identifies watermark elements (typically images or text layers) in the PDF and attempts to remove them. Note that this tool might not recognize all types of watermarks and may not completely remove them in some cases.

## Usage
1. Open a PDF file.
2. Choose whether to overwrite the original file or save as a new file.
3. Click the "Start Removing Watermark" button.

## Risk Disclaimer
- This program may remove all images in the PDF, including non-watermark images. Use it with caution.
- Removing watermarks may risk infringing on others' legal rights. Please ensure you have the rights to the file.
- Back up your PDF files before operation.

## Installation and Running
1. Clone the repository to your local machine:
2. Navigate to the project directory:
3. Install dependencies:
4. Run the application:
For a detailed list of dependencies, see [requirements.txt](./requirements.txt).

## Open Source License
This project is under the [GPL v3 license](LICENSE).

## 中文版
查看 [中文版 README](README_CN.md)。

---

Author: weizy0219
Company Website: [www.wesinx.com](http://www.wesinx.com)