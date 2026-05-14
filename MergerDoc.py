import streamlit as st
from PIL import Image
from pypdf import PdfWriter
import fitz
import io

st.set_page_config(page_title="Smart Doc Studio", layout="centered")

st.title("🚀 Smart Doc Studio")
st.subheader("รวมรูปภาพ และจัดการ PDF ออนไลน์")

mode = st.sidebar.selectbox("เลือกโหมดการใช้งาน", ["รวมรูปภาพ (Image Merger)", "รวม PDF (PDF Merger)", "แก้ไข PDF (PDF Edit)"])

if mode == "รวมรูปภาพ (Image Merger)":
    st.header("🖼 รวมรูปภาพ")
    uploaded_images = st.file_uploader("เลือกรูปภาพ...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    direction = st.radio("ทิศทางการรวม", ["แนวตั้ง (Vertical)", "แนวนอน (Horizontal)"])
    
    if st.button("เริ่มรวมรูปภาพ") and uploaded_images:
        images = [Image.open(img).convert('RGB') for img in uploaded_images]
        widths, heights = zip(*(i.size for i in images))
        
        if direction == "แนวตั้ง (Vertical)":
            new_img = Image.new('RGB', (max(widths), sum(heights)), (255, 255, 255))
            y = 0
            for im in images:
                new_img.paste(im, (0, y))
                y += im.size[1]
        else:
            new_img = Image.new('RGB', (sum(widths), max(heights)), (255, 255, 255))
            x = 0
            for im in images:
                new_img.paste(im, (x, 0))
                x += im.size[0]
        
        # ส่งไฟล์ให้ดาวน์โหลด
        buf = io.BytesIO()
        new_img.save(buf, format="JPEG")
        st.image(new_img, caption="Preview", use_container_width=True)
        st.download_button("ดาวน์โหลดผลลัพธ์", buf.getvalue(), "merged_image.jpg", "image/jpeg")

elif mode == "รวม PDF (PDF Merger)":
    st.header("📑 รวมไฟล์ PDF")
    uploaded_pdfs = st.file_uploader("เลือกไฟล์ PDF...", type=["pdf"], accept_multiple_files=True)
    
    if st.button("เริ่มรวม PDF") and uploaded_pdfs:
        merger = PdfWriter()
        for pdf in uploaded_pdfs:
            merger.append(pdf)
        
        buf = io.BytesIO()
        merger.write(buf)
        st.success("รวมไฟล์สำเร็จ!")
        st.download_button("ดาวน์โหลด PDF", buf.getvalue(), "merged_document.pdf", "application/pdf")

elif mode == "แก้ไข PDF (PDF Edit)":
    st.header("✏️ แก้ไขข้อความใน PDF")
    uploaded_pdf = st.file_uploader("เลือกไฟล์ PDF (1 ไฟล์)", type=["pdf"])
    find_text = st.text_input("คำที่ต้องการหา")
    replace_text = st.text_input("เปลี่ยนเป็นคำว่า")
    
    if st.button("ดำเนินการ") and uploaded_pdf and find_text:
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        for page in doc:
            for inst in page.search_for(find_text):
                page.add_redact_annotation(inst, fill=(1,1,1))
                page.apply_redactions()
                page.insert_text(inst.tl, replace_text, fontsize=11, color=(0,0,0))
        
        buf = doc.tobytes()
        st.success("แก้ไขเรียบร้อย!")
        st.download_button("ดาวน์โหลดไฟล์แก้ไข", buf, "edited_document.pdf", "application/pdf")
