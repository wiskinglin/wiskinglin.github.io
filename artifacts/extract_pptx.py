import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def extract_pptx_text(pptx_path, output_txt_path):
    if not os.path.exists(pptx_path):
        print(f"File not found: {pptx_path}")
        return
        
    lines = []
    lines.append(f"=== Extracting {os.path.basename(pptx_path)} ===")
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            # Find all slides
            slide_files = sorted([f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')],
                                 key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
            
            for slide_file in slide_files:
                slide_num = slide_file.replace('ppt/slides/slide', '').replace('.xml', '')
                lines.append(f"\n--- Slide {slide_num} ---")
                
                xml_content = z.read(slide_file)
                root = ET.fromstring(xml_content)
                
                # Find all paragraph elements
                for paragraph in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}p'):
                    para_text = ""
                    for text_node in paragraph.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
                        if text_node.text:
                            para_text += text_node.text
                    if para_text.strip():
                        lines.append(para_text.strip())
                        
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"Successfully wrote extraction to {output_txt_path}")
                        
    except Exception as e:
        print(f"Error reading zip: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_pptx.py <path_to_pptx> <output_txt_path>")
    else:
        extract_pptx_text(sys.argv[1], sys.argv[2])
