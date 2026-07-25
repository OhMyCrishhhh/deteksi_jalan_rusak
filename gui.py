import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
import time

from detector import RoadDamageDetector

class RoadDamageGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==========================
        # Konfigurasi Window
        # ==========================
        self.title("Deteksi Jalan Rusak")
        self.geometry("1200x700")
        self.minsize(1000, 650)
        self.detector = RoadDamageDetector()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.current_image = None
        self.image_path = None
        self.result_image = None


        self.create_widgets()

    def create_widgets(self):

        # ==========================
        # Judul
        # ==========================
        title = ctk.CTkLabel(
            self,
            text="DETEKSI JALAN RUSAK",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=20)

        # ==========================
        # Frame Utama
        # ==========================
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ==========================
        # Frame Kiri
        # ==========================
        self.left_frame = ctk.CTkFrame(main_frame, width=600)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        preview_title = ctk.CTkLabel(
            self.left_frame,
            text="Preview Gambar",
            font=("Segoe UI", 18, "bold")
        )
        preview_title.pack(pady=10)

        self.image_label = ctk.CTkLabel(
            self.left_frame,
            text="Belum ada gambar",
            width=550,
            height=450
        )
        self.image_label.pack(pady=10)

        # ==========================
        # Frame Kanan
        # ==========================
        right_frame = ctk.CTkFrame(main_frame, width=350)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        info = ctk.CTkLabel(
            right_frame,
            text="HASIL DETEKSI",
            font=("Segoe UI", 20, "bold")
        )
        info.pack(pady=15)

        self.lbl_jumlah = ctk.CTkLabel(right_frame, text="Jumlah Kerusakan : -")
        self.lbl_jumlah.pack(anchor="w", padx=20, pady=5)

        self.lbl_luas = ctk.CTkLabel(right_frame, text="Luas Kerusakan : -")
        self.lbl_luas.pack(anchor="w", padx=20, pady=5)

        self.lbl_persen = ctk.CTkLabel(right_frame, text="Persentase : -")
        self.lbl_persen.pack(anchor="w", padx=20, pady=5)

        self.lbl_resolusi = ctk.CTkLabel(right_frame, text="Resolusi : -")
        self.lbl_resolusi.pack(anchor="w", padx=20, pady=5)

        self.lbl_waktu = ctk.CTkLabel(right_frame, text="Waktu : -")
        self.lbl_waktu.pack(anchor="w", padx=20, pady=5)

        self.lbl_status = ctk.CTkLabel(
            right_frame,
            text="Status : Menunggu",
            font=("Segoe UI", 16, "bold"),
            text_color="blue"
        )
        self.lbl_status.pack(pady=20)

        # ==========================
        # Progress Bar
        # ==========================
        self.progress = ctk.CTkProgressBar(right_frame, width=250)
        self.progress.pack(pady=15)
        self.progress.set(0)

        # ==========================
        # Tombol
        # ==========================
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", pady=15)

        pilih_btn = ctk.CTkButton(
            button_frame,
            text="Pilih Foto",
            command=self.load_image,
            width=180,
            height=40
        )
        pilih_btn.pack(side="left", padx=20)

        self.deteksi_btn = ctk.CTkButton(
            button_frame,
            text="Deteksi",
            command=self.detect_damage,
            width=180,
            height=40,
        state="disabled"
)
        self.deteksi_btn.pack(side="left", padx=20)

        self.simpan_btn = ctk.CTkButton(
            button_frame,
            text="Simpan",
            command=self.save_result,
            width=180,
            height=40,
            state="disabled"
)
        self.simpan_btn.pack(side="left", padx=20)

        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self.reset,
            width=180,
            height=40
        )
        reset_btn.pack(side="left", padx=20)

    # ======================================

    def load_image(self):

        file = filedialog.askopenfilename(
            filetypes=[
                ("Image", "*.jpg *.jpeg *.png")
            ]
        )

        if not file:
            return
        
        print("File dipilih:", file)
        print("Load image dipanggil")
        self.image_path = file

        image = Image.open(file).copy()

        image.thumbnail((550, 450))

        self.current_image = ctk.CTkImage(
            light_image=image.copy(),
            dark_image=image.copy(),
            size=image.size
)

        self.image_label.configure(
            image=self.current_image,
            text=""
)
        print("Preview berhasil diperbarui")
        
    # Simpan referensi agar gambar tidak hilang

        self.deteksi_btn.configure(state="normal")
        self.progress.set(0)

        self.lbl_status.configure(
            text="Status : Gambar berhasil dipilih",
            text_color="green"
        )

    # Memastikan CTkLabel menggunakan gambar terbaru
        self.update_idletasks()

        

    # ======================================

    def reset(self):

        self.current_image = None

    # Hapus path gambar
        self.image_path = None

    # Hapus hasil deteksi
        self.result_image = None

    # Hapus preview
        self.image_label.destroy()

        self.image_label = ctk.CTkLabel(
        self.left_frame,
            text="Belum ada gambar",
            width=550,
            height=450
)

        self.image_label.pack(pady=10)
    
    # Reset progress
        self.progress.set(0)

    # Disable tombol
        self.deteksi_btn.configure(state="disabled")
        self.simpan_btn.configure(state="disabled")

    # Reset label
        self.lbl_jumlah.configure(text="Jumlah Kerusakan : -")
        self.lbl_luas.configure(text="Luas Kerusakan : -")
        self.lbl_persen.configure(text="Persentase : -")
        self.lbl_resolusi.configure(text="Resolusi : -")
        self.lbl_waktu.configure(text="Waktu : -")

        self.lbl_status.configure(
        text="Status : Menunggu",
        text_color="blue"
    )
    # ============================
    # detect_damage()
    # ============================

    def detect_damage(self):
        print("Tombol Deteksi Ditekan")

        if self.image_path is None:
            return

        self.progress.set(0.2)

        data = self.detector.process(self.image_path)

        self.progress.set(1)

        self.show_result(data["result"])

        h, w = data["original"].shape[:2]

        self.lbl_jumlah.configure(
        text=f"Jumlah Kerusakan : {data['count']}"
    )

        self.lbl_luas.configure(
        text=f"Luas Kerusakan : {int(data['area'])} pixel"
    )

        self.lbl_persen.configure(
        text=f"Persentase : {data['percentage']:.2f}%"
    )

        self.lbl_resolusi.configure(
        text=f"Resolusi : {w} x {h}"
    )

        self.lbl_waktu.configure(
        text=f"Waktu : {data['time']:.3f} detik"
    )

        self.lbl_status.configure(
        text=f"Status : {data['status']}",
        text_color="green"
    )

        self.result_image = data["result"]

        self.simpan_btn.configure(state="normal")

    # ============================
    # show_result()
    # ============================

    def show_result(self, image):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(image)

        image.thumbnail((550, 450))

        self.current_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
)

        self.image_label.configure(
            image=self.current_image,
            text=""
)
        print("Preview berhasil diperbarui")


    # ============================
    # save_result()
    # ============================

    def save_result(self):


        if self.result_image is None:
            messagebox.showwarning(
            "Peringatan",
            "Belum ada hasil deteksi yang dapat disimpan."
        )
            return

        file = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ]
    )
        



        if not file:
            return

        success = cv2.imwrite(file, self.result_image)
    


    
        if  success:
            messagebox.showinfo(
            "Berhasil",
            "Hasil deteksi berhasil disimpan."
        )
        else:
            messagebox.showerror(
            "Gagal",
            "Gagal menyimpan hasil deteksi."
        )