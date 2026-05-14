import streamlit as st
from PIL import Image
from pypdf import PdfWriter
import io

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Smart Doc Studio", page_icon="🚀")

st.title("🚀 Smart Doc Studio")
st.markdown("---")

# เมนูเลือกโหมดด้านข้าง
mode = st.sidebar.selectbox(
    "เลือกโหมดการใช้งาน", 
    ["🖼 รวมรูปภาพ (Image Merger)", "📑 รวม PDF (PDF Merger)"]
)

# --- โหมดรวมรูปภาพ ---
if mode == "🖼 รวมรูปภาพ (Image Merger)":
    st.header("รวมรูปภาพ")
    uploaded_images = st.file_uploader(
        "เลือกรูปภาพ (JPG, PNG)", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        direction = st.radio("เลือกทิศทาง", ["แนวตั้ง (Vertical)", "แนวนอน (Horizontal)"])
    
    if st.button("เริ่มรวมรูปภาพ") and uploaded_images:
        try:
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
            
            # จัดการไฟล์เพื่อดาวน์โหลด
            buf = io.BytesIO()
            new_img.save(buf, format="JPEG", quality=95)
            
            st.image(new_img, caption="Preview Result", use_container_width=True)
            st.download_button(
                label="📥 ดาวน์โหลดรูปภาพที่รวมแล้ว",
                data=buf.getvalue(),
                file_name="merged_image.jpg",
                mime="image/jpeg"
            )
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")

# --- โหมดรวม PDF ---
elif mode == "📑 รวม PDF (PDF Merger)":
    st.header("รวมไฟล์ PDF")
    uploaded_pdfs = st.file_uploader(
        "เลือกไฟล์ PDF (เลือกได้หลายไฟล์)", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    if st.button("เริ่มรวม PDF") and uploaded_pdfs:
        try:
            merger = PdfWriter()
            for pdf in uploaded_pdfs:
                merger.append(pdf)
            
            buf = io.BytesIO()
            merger.write(buf)
            
            st.success(f"รวมไฟล์สำเร็จ! ทั้งหมด {len(uploaded_pdfs)} ไฟล์")
            st.download_button(
                label="📥 ดาวน์โหลดไฟล์ PDF ที่รวมแล้ว",
                data=buf.getvalue(),
                file_name="merged_document.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการรวม PDF: {e}")

st.markdown("---")
st.caption("Powered by Streamlit | Designed for Efficiency")
