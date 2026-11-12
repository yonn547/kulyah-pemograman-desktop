import tkinter as tk
from tkinter import messagebox
import datetime
import logging

# --- SETUP LOGGING (Global, di luar kelas) ---
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO, # Bisa diganti logging.DEBUG untuk detail lebih banyak
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8' # Penting agar log tidak error saat ada karakter khusus
)

class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)
        self.minsize(600, 700)

        # Color Scheme
        self.BG_MAIN = "#e8f4f8"
        self.BG_FRAME = "#ffffff"
        self.BG_INPUT = "#f9f9f9"
        self.FG_TEXT = "#2c3e50"
        self.FG_LABEL = "#34495e"
        self.ACCENT = "#3498db"
        self.BORDER = "#bdc3c7"
        self.configure(bg=self.BG_MAIN)

        self.users_db = {"admin": "123", "user1": "password1", "mahasiswa": "123456"}
        self.current_user = None
        self.frame_aktif = None

        self._buat_tampilan_login()
        self._buat_tampilan_biodata()
        self._pindah_ke(self.frame_login)
        
        logging.info("Aplikasi dimulai") # Log startup

    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()
        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, bg=self.BG_MAIN)
        tk.Label(self.frame_login, text="HALAMAN LOGIN", font=("Arial", 18, "bold"), bg=self.BG_MAIN, fg=self.FG_TEXT).pack(pady=20)

        frame_form = tk.Frame(self.frame_login, bg=self.BG_FRAME, padx=30, pady=30, relief=tk.GROOVE, borderwidth=2)
        frame_form.pack(fill=tk.X)

        tk.Label(frame_form, text="Username:", font=("Arial", 12), bg=self.BG_FRAME, fg=self.FG_LABEL).pack(anchor="w", pady=(0, 5))
        self.entry_username = tk.Entry(frame_form, font=("Arial", 12), bg=self.BG_INPUT, relief=tk.SOLID, borderwidth=1)
        self.entry_username.pack(fill=tk.X, pady=(0, 15))

        # Frame untuk Password + Tombol Show/Hide
        frame_pwd = tk.Frame(frame_form, bg=self.BG_FRAME)
        frame_pwd.pack(fill=tk.X)
        
        tk.Label(frame_form, text="Password:", font=("Arial", 12), bg=self.BG_FRAME, fg=self.FG_LABEL).pack(anchor="w", pady=(0, 5))
        self.entry_password = tk.Entry(frame_pwd, font=("Arial", 12), show="*", bg=self.BG_INPUT, relief=tk.SOLID, borderwidth=1)
        self.entry_password.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(0, 20))
        
        self.btn_show_pwd = tk.Button(frame_pwd, text="👁️", width=3, font=("Arial", 10), bg=self.BG_INPUT, relief=tk.FLAT, command=self._toggle_password)
        self.btn_show_pwd.pack(side=tk.RIGHT, padx=(5, 0))

        self.btn_login = tk.Button(frame_form, text="Login", font=("Arial", 12, "bold"), bg=self.ACCENT, fg="white", relief=tk.FLAT, cursor="hand2", command=self._coba_login)
        self.btn_login.pack(fill=tk.X)

        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())
        tk.Label(self.frame_login, text="Info: admin/123 | user1/password1", font=("Arial", 9), fg="gray", bg=self.BG_MAIN).pack(pady=10)

    def _buat_tampilan_biodata(self):
        self.frame_biodata = tk.Frame(master=self, bg=self.BG_MAIN)
        self.frame_biodata.columnconfigure(1, weight=1)

        self.label_judul = tk.Label(self.frame_biodata, text="FORM BIODATA MAHASISWA", font=("Arial", 18, "bold"), bg=self.BG_MAIN, fg=self.FG_TEXT)
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=10)

        self.frame_input = tk.LabelFrame(self.frame_biodata, text="Data Mahasiswa", font=("Arial", 12, "bold"), bg=self.BG_FRAME, fg=self.FG_LABEL, relief=tk.GROOVE, borderwidth=2, padx=20, pady=20)
        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW", pady=10)
        self.frame_input.columnconfigure(1, weight=1)

        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        def buat_label(parent, text, row, col):
            tk.Label(parent, text=text, font=("Arial", 11), bg=self.BG_FRAME, fg=self.FG_LABEL).grid(row=row, column=col, sticky="W", pady=6)
        def buat_entry(parent, row, col, textvar):
            ent = tk.Entry(parent, width=32, font=("Arial", 11), bg=self.BG_INPUT, fg=self.FG_TEXT, relief=tk.SOLID, borderwidth=1, textvariable=textvar)
            ent.grid(row=row, column=1, pady=6, sticky="EW", padx=(10, 0))
            return ent

        buat_label(self.frame_input, "Nama Lengkap:", 0, 0); self.entry_nama = buat_entry(self.frame_input, 0, 1, self.var_nama)
        buat_label(self.frame_input, "NIM:", 1, 0); self.entry_nim = buat_entry(self.frame_input, 1, 1, self.var_nim)
        buat_label(self.frame_input, "Jurusan:", 2, 0); self.entry_jurusan = buat_entry(self.frame_input, 2, 1, self.var_jurusan)

        buat_label(self.frame_input, "Alamat:", 3, 0)
        self.frame_alamat = tk.Frame(self.frame_input, bg=self.BG_INPUT, relief=tk.SOLID, borderwidth=1)
        self.frame_alamat.grid(row=3, column=1, pady=6, sticky="EW", padx=(10, 0))
        self.scrollbar_alamat = tk.Scrollbar(self.frame_alamat); self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_alamat = tk.Text(self.frame_alamat, height=5, width=30, font=("Arial", 11), bg=self.BG_INPUT, fg=self.FG_TEXT, relief=tk.FLAT, borderwidth=0)
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_alamat.config(command=self.text_alamat.yview); self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

        buat_label(self.frame_input, "Jenis Kelamin:", 4, 0)
        self.frame_jk = tk.Frame(self.frame_input, bg=self.BG_FRAME); self.frame_jk.grid(row=4, column=1, sticky="W", pady=6, padx=(10, 0))
        tk.Radiobutton(self.frame_jk, text="Pria", variable=self.var_jk, value="Pria", bg=self.BG_FRAME, fg=self.FG_TEXT, selectcolor=self.BG_INPUT).pack(side=tk.LEFT, padx=8)
        tk.Radiobutton(self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita", bg=self.BG_FRAME, fg=self.FG_TEXT, selectcolor=self.BG_INPUT).pack(side=tk.LEFT, padx=8)

        self.check_setuju = tk.Checkbutton(self.frame_input, text="Saya menyetujui pengumpulan data ini.", variable=self.var_setuju, font=("Arial", 10), bg=self.BG_FRAME, fg=self.FG_LABEL, selectcolor=self.BG_INPUT, command=self.validate_form)
        self.check_setuju.grid(row=5, column=0, columnspan=2, pady=12, sticky="W")

        self.btn_submit = tk.Button(self.frame_biodata, text="Submit Biodata", font=("Arial", 12, "bold"), bg=self.BORDER, fg="gray", relief=tk.FLAT, cursor="hand2", command=self.submit_data, state=tk.DISABLED, padx=20, pady=12)
        self.btn_submit.grid(row=2, column=0, columnspan=2, pady=10, sticky="EW")

        self.label_hasil = tk.Label(self.frame_biodata, text="", font=("Arial", 11, "italic"), bg=self.BG_MAIN, fg=self.FG_LABEL, justify=tk.LEFT)
        self.label_hasil.grid(row=3, column=0, columnspan=2, sticky="W", padx=10)

        self.btn_submit.bind("<Enter>", lambda e: self.btn_submit.config(bg="#2980b9") if self.btn_submit['state'] == tk.NORMAL else None)
        self.btn_submit.bind("<Leave>", lambda e: self.btn_submit.config(bg=self.ACCENT) if self.btn_submit['state'] == tk.NORMAL else None)
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)

        # Tombol Aksi Bawah
        frame_aksi = tk.Frame(self.frame_biodata, bg=self.BG_MAIN)
        frame_aksi.grid(row=4, column=0, columnspan=2, pady=10, sticky="EW")
        frame_aksi.columnconfigure(0, weight=1); frame_aksi.columnconfigure(1, weight=1)
        
        self.btn_reset = tk.Button(frame_aksi, text="Reset Form", font=("Arial", 10), bg="#f39c12", fg="white", relief=tk.FLAT, cursor="hand2", command=self._reset_form_biodata)
        self.btn_reset.grid(row=0, column=0, padx=5, sticky="EW")
        
        self.btn_logout = tk.Button(frame_aksi, text="Logout", font=("Arial", 10), bg="#e74c3c", fg="white", relief=tk.FLAT, cursor="hand2", command=self._logout)
        self.btn_logout.grid(row=0, column=1, padx=5, sticky="EW")

        self._buat_menu()

    def _buat_menu(self):
        self.menu_bar = tk.Menu(master=self)
        self.config(menu=self.menu_bar)
        file_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self): self.config(menu="")
    def _tampilkan_menu(self): self.config(menu=self.menu_bar)

    def _toggle_password(self):
        """Fitur Tambahan: Show/Hide Password"""
        if self.entry_password.cget('show') == '*':
            self.entry_password.config(show='')
            self.btn_show_pwd.config(text="🙈")
        else:
            self.entry_password.config(show='*')
            self.btn_show_pwd.config(text="👁️")

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        logging.info(f"Login attempt for username: {username}")

        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set(); return
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set(); return

        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._tampilkan_menu()
            self._pindah_ke(self.frame_biodata)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _logout(self):
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            self.current_user = None
            self._hapus_menu()
            self._update_title_with_user()
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)

    def _reset_form_biodata(self):
        self.var_nama.set(""); self.var_nim.set(""); self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END); self.var_jk.set("Pria"); self.var_setuju.set(0)
        self.label_hasil.config(text="")
        self.btn_submit.config(state=tk.DISABLED, bg=self.BORDER, fg="gray")

    def _update_title_with_user(self):
        self.title(f"Aplikasi Biodata - User: {self.current_user}" if self.current_user else "Aplikasi Biodata Mahasiswa")

    def validate_form(self, *args):
        if self.var_nama.get().strip() and self.var_nim.get().strip() and self.var_jurusan.get().strip() and self.var_setuju.get() == 1:
            self.btn_submit.config(state=tk.NORMAL, bg=self.ACCENT, fg="white")
        else:
            self.btn_submit.config(state=tk.DISABLED, bg=self.BORDER, fg="gray")

    def submit_data(self):
        try:
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!"); return

            nama = self.entry_nama.get().strip(); nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip(); alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            if not nama or not nim or not jurusan:
                messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!"); return
            if not nim.isdigit() or len(nim) < 3:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 3 digit!"); self.entry_nim.focus_set(); return
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!"); self.entry_nama.focus_set(); return

            hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
            messagebox.showinfo("Data Tersimpan", hasil)
            self.label_hasil.config(text=f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}", fg=self.ACCENT)
            
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}") # Log sukses

        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}") # Log error
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL: self.submit_data()

    def simpan_hasil(self):
        try:
            hasil_tersimpan = self.label_hasil.cget("text")
            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu."); return

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\nWaktu: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "-"*50 + "\n" + hasil_tersimpan)
            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")
            logging.info(f"File saved: {filename} by {self.current_user}")
        except Exception as e:
            logging.error(f"Error saving file by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()