import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from pypdf import PdfWriter  # ไลบรารีสำหรับรวม PDF

# ตั้งค่าเริ่มต้น
ctk.set_appearance_mode("dark")

class ModernImageMerger(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Language Dictionary ---
        self.languages = {
            "EN": {
                "title": "Document & Image Studio",
                "sub": "Merge your Images or PDF files easily",
                "mode_lbl": "Select Mode:",
                "mode_img": "Image Merger",
                "mode_pdf": "PDF Merger",
                "btn_add": "+ Add Files",
                "no_files": "No files selected",
                "selected": "Selected: {} files",
                "step2": "Step 2: Settings",
                "vertical": "Vertical (Stack)",
                "horizontal": "Horizontal (Side-by-side)",
                "pdf_info": "PDFs will be merged in selection order",
                "btn_start": "Merge & Save As...",
                "footer": "Designed for Efficiency",
                "warn_select": "Please select files first!",
                "success": "Successfully saved to:\n{}",
                "error": "An error occurred: {}"
            },
            "TH": {
                "title": "สตูดิโอรวมไฟล์และรูปภาพ",
                "sub": "รวมรูปภาพหรือไฟล์ PDF ของคุณได้ในที่เดียว",
                "mode_lbl": "เลือกโหมดการใช้งาน:",
                "mode_img": "รวมรูปภาพ",
                "mode_pdf": "รวม PDF",
                "btn_add": "+ เพิ่มไฟล์",
                "no_files": "ยังไม่ได้เลือกไฟล์",
                "selected": "เลือกแล้ว: {} ไฟล์",
                "step2": "ขั้นตอนที่ 2: ตั้งค่า",
                "vertical": "แนวตั้ง (ต่อลงล่าง)",
                "horizontal": "แนวนอน (ต่อข้าง)",
                "pdf_info": "ไฟล์ PDF จะถูกรวมตามลำดับที่เลือก",
                "btn_start": "เริ่มรวมไฟล์และบันทึก...",
                "footer": "ออกแบบเพื่อการใช้งานที่รวดเร็ว",
                "warn_select": "กรุณาเลือกไฟล์ก่อนครับ!",
                "success": "บันทึกไฟล์เรียบร้อยแล้วที่:\n{}",
                "error": "เกิดข้อผิดพลาด: {}"
            }
        }
        
        self.current_lang = "TH"
        self.selected_files = []

        # --- Window Setup ---
        self.title("Smart Merger v4.0")
        self.geometry("600x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#1a1c1e")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # --- Header & Lang ---
        self.lang_switch = ctk.CTkSegmentedButton(self.main_frame, values=["TH", "EN"], command=self.change_language, selected_color="#00ced1")
        self.lang_switch.set(self.current_lang)
        self.lang_switch.pack(anchor="e", padx=20, pady=10)

        self.header_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#00ced1")
        self.header_label.pack(pady=(10, 5))
        
        self.sub_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=13), text_color="gray")
        self.sub_label.pack(pady=(0, 15))

        # --- Mode Selector (New!) ---
        self.mode_tab = ctk.CTkSegmentedButton(self.main_frame, values=["Image", "PDF"], command=self.switch_mode, 
                                               selected_color="#008b8b", height=40)
        self.mode_tab.set("Image")
        self.mode_tab.pack(fill="x", padx=40, pady=10)

        # --- Selection Area ---
        self.selection_frame = ctk.CTkFrame(self.main_frame, fg_color="#25282b", corner_radius=15)
        self.selection_frame.pack(fill="x", padx=40, pady=10)

        self.btn_select = ctk.CTkButton(self.selection_frame, text="", command=self.select_files, corner_radius=10, fg_color="#008b8b")
        self.btn_select.pack(pady=20)

        self.lbl_status = ctk.CTkLabel(self.selection_frame, text="", text_color="#7f8c8d")
        self.lbl_status.pack(pady=(0, 15))

        # --- Settings Area ---
        self.mode_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.mode_frame.pack(fill="x", padx=40, pady=10)

        self.mode_label = ctk.CTkLabel(self.mode_frame, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.mode_label.pack(anchor="w", padx=10, pady=(0, 5))

        # Radio for Images
        self.direction_var = ctk.StringVar(value="vertical")
        self.radio_frame = ctk.CTkFrame(self.mode_frame, fg_color="#25282b", corner_radius=15)
        self.radio_frame.pack(fill="x")

        self.radio_v = ctk.CTkRadioButton(self.radio_frame, text="", variable=self.direction_var, value="vertical", border_color="#00ced1")
        self.radio_v.pack(side="left", padx=30, pady=20)
        
        self.radio_h = ctk.CTkRadioButton(self.radio_frame, text="", variable=self.direction_var, value="horizontal", border_color="#00ced1")
        self.radio_h.pack(side="left", padx=10, pady=20)

        # Info Label for PDF (Hidden by default)
        self.pdf_info_label = ctk.CTkLabel(self.radio_frame, text="", text_color="#00ced1")

        # --- Action Button ---
        self.btn_merge = ctk.CTkButton(self.main_frame, text="", command=self.process_files, height=55, corner_radius=27, 
                                       fg_color="#00ced1", text_color="#1a1c1e", font=ctk.CTkFont(size=16, weight="bold"))
        self.btn_merge.pack(pady=(30, 10), padx=80, fill="x")

        self.footer_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=10), text_color="#454a4f")
        self.footer_label.pack(side="bottom", pady=10)

        self.update_ui_text()

    def switch_mode(self, mode):
        self.selected_files = [] # Clear selection when switching
        if mode == "PDF":
            self.radio_v.pack_forget()
            self.radio_h.pack_forget()
            self.pdf_info_label.pack(pady=20)
        else:
            self.pdf_info_label.pack_forget()
            self.radio_v.pack(side="left", padx=30, pady=20)
            self.radio_h.pack(side="left", padx=10, pady=20)
        self.update_ui_text()

    def change_language(self, new_lang):
        self.current_lang = new_lang
        self.update_ui_text()

    def update_ui_text(self):
        lang = self.languages[self.current_lang]
        self.header_label.configure(text=lang["title"])
        self.sub_label.configure(text=lang["sub"])
        self.btn_select.configure(text=lang["btn_add"])
        self.mode_label.configure(text=lang["step2"])
        self.radio_v.configure(text=lang["vertical"])
        self.radio_h.configure(text=lang["horizontal"])
        self.pdf_info_label.configure(text=lang["pdf_info"])
        self.btn_merge.configure(text=lang["btn_start"])
        self.footer_label.configure(text=lang["footer"])
        
        if not self.selected_files:
            self.lbl_status.configure(text=lang["no_files"], text_color="#7f8c8d")
        else:
            self.lbl_status.configure(text=lang["selected"].format(len(self.selected_files)), text_color="#00ced1")

    def select_files(self):
        mode = self.mode_tab.get()
        file_types = [("Image files", "*.jpg *.jpeg *.png")] if mode == "Image" else [("PDF files", "*.pdf")]
        
        files = filedialog.askopenfilenames(title=f"Select {mode}s", filetypes=file_types)
        if files:
            self.selected_files = list(files)
            self.update_ui_text()

    def process_files(self):
        mode = self.mode_tab.get()
        if mode == "Image":
            self.merge_images()
        else:
            self.merge_pdfs()

    def merge_images(self):
        lang = self.languages[self.current_lang]
        if not self.selected_files:
            messagebox.showwarning("Warning", lang["warn_select"])
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Image", "*.jpg")], title="Export Image")
        if not save_path: return

        try:
            images = [Image.open(x).convert('RGB') for x in self.selected_files]
            widths, heights = zip(*(i.size for i in images))

            if self.direction_var.get() == "vertical":
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

            new_img.save(save_path, quality=95)
            messagebox.showinfo("Success", lang["success"].format(os.path.basename(save_path)))
        except Exception as e:
            messagebox.showerror("Error", lang["error"].format(str(e)))

    def merge_pdfs(self):
        lang = self.languages[self.current_lang]
        if not self.selected_files:
            messagebox.showwarning("Warning", lang["warn_select"])
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Documents", "*.pdf")], title="Export PDF")
        if not save_path: return

        try:
            merger = PdfWriter()
            for pdf in self.selected_files:
                merger.append(pdf)
            
            with open(save_path, "wb") as f:
                merger.write(f)
            merger.close()
            
            messagebox.showinfo("Success", lang["success"].format(os.path.basename(save_path)))
        except Exception as e:
            messagebox.showerror("Error", lang["error"].format(str(e)))

if __name__ == "__main__":
    app = ModernImageMerger()
    app.mainloop()