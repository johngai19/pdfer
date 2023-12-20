
import os,sys,json
from pypdf import PdfReader, PdfWriter
from collections import Counter

class PDFWatermarkRemover:
    @staticmethod
    def find_repeated_xobjects(pdf_reader):
        """
        在所有页面中查找重复出现的 XObjects。
        """
        xobject_names = []

        for page in pdf_reader.pages:
            if '/XObject' in page['/Resources']:
                xobjects = page['/Resources']['/XObject'].get_object()
                xobject_names.extend(xobjects.keys())

        # 计数并返回出现在每一页上的 XObjects
        count = Counter(xobject_names)
        repeated_xobjects = [name for name, freq in count.items() if freq == len(pdf_reader.pages)]
        return repeated_xobjects

    @staticmethod
    def remove_watermark(input_pdf, output_pdf):
        try:
            pdf_reader = PdfReader(input_pdf)
            pdf_writer = PdfWriter()

            # 查找重复的 XObjects
            repeated_xobjects = PDFWatermarkRemover.find_repeated_xobjects(pdf_reader)

            for page in pdf_reader.pages:
                if '/XObject' in page['/Resources']:
                    xobjects = page['/Resources']['/XObject'].get_object()

                    # 移除重复的 XObjects（可能的水印）
                    for obj_name in repeated_xobjects:
                        if obj_name in xobjects:
                            del xobjects[obj_name]
                # 检查并移除页面中的水印
                if '/Annots' in page:
                    annotations = page['/Annots']
                    for annot in annotations:
                        if annot.Subtype == '/Watermark':
                            annotations.remove(annot)
                pdf_writer.add_page(page)

            with open(output_pdf, 'wb') as out:
                pdf_writer.write(out)

            return "Success"
        except Exception as e:
            return f"Failed - {e}"
    
    
    @staticmethod
    def rename_file(input_pdf):
        # 分离文件的目录、基本名称和扩展名
        directory, base_name = os.path.split(input_pdf)
        name, ext = os.path.splitext(base_name)

        # 添加“（去水印）”到文件名
        new_name = f"{name}(no watermark){ext}"
        new_path = os.path.join(directory, new_name)

        return new_path
        
    @staticmethod
    def save_last_path(path):
        # print(f"Saving last path: {path}")  # 调试信息
        config = {'last_path': path}
        with open('config.json', 'w') as f:
            json.dump(config, f)

    @staticmethod
    def load_last_path():
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                last_path = config.get('last_path', '')
                # print(f"Loaded last path: {last_path}")  # 调试信息
                return last_path
        return ''

# 使用示例
# PDFWatermarkRemover.remove_watermark('input.pdf', 'output.pdf')

