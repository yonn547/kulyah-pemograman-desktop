import tkinter as tk
from tkinter import messagebox

# --- Color Scheme ---
BG_MAIN = "#e8f4f8"      # Biru muda untuk background utama
BG_FRAME = "#ffffff"     # Putih untuk frame
BG_INPUT = "#f9f9f9"     # Abu-abu sangat muda untuk input
FG_TEXT = "#2c3e50"      # Biru tua untuk teks
FG_LABEL = "#34495e"     # Abu-abu gelap untuk label
ACCENT = "#3498db"       # Biru untuk aksen
BORDER = "#bdc3c7"       # Abu-abu untuk border

# --- Event Handlers ---
def submit_data():
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
        return

    nama = var_nama.get().strip()
    nim = var_nim.get().strip()
    jurusan = var_jurusan.get().strip()
    alamat = text_alamat.get("1.0", tk.END).strip()
    jenis_kelamin = var_jk.get()

    if not nama or not nim or not jurusan or not alamat:
        messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
        return

    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
    label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}", fg=ACCENT)
    messagebox.showinfo("Data Tersimpan", hasil)

def validate_form(*args):
    nama_valid = var_nama.get().strip() != ""
    nim_valid = var_nim.get().strip() != ""
    jurusan_valid = var_jurusan.get().strip() != ""
    setuju_valid = var_setuju.get() == 1

    if nama_valid and nim_valid and jurusan_valid and setuju_valid:
        btn_submit.config(state=tk.NORMAL, bg=ACCENT, fg="white")
    else:
        btn_submit.config(state=tk.DISABLED, bg=BORDER, fg="gray")

def on_enter(event):
    if btn_submit['state'] == tk.NORMAL:
        btn_submit.config(bg="#2980b9")  # Biru lebih gelap saat hover

def on_leave(event):
    if btn_submit['state'] == tk.NORMAL:
        btn_submit.config(bg=ACCENT)

def submit_shortcut(event=None):
    if btn_submit['state'] == tk.NORMAL:
        submit_data()

def simpan_hasil():
    hasil_tersimpan = label_hasil.cget("text")
    if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
        messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
        return

    with open("biodata_tersimpan.txt", "w") as file:
        file.write(hasil_tersimpan)
    messagebox.showinfo("Info", "Data berhasil disimpan ke file 'biodata_tersimpan.txt'.")

def keluar_aplikasi():
    if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
        window.destroy()

# --- Root Window ---
window = tk.Tk()
window.title("Form Biodata Mahasiswa - Yonn")
window.geometry("580x680")
window.resizable(True, True)
window.minsize(580, 680)
window.configure(bg=BG_MAIN)

# --- Frame Utama ---
main_frame = tk.Frame(master=window, bg=BG_MAIN, padx=25, pady=25)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(1, weight=1)

# --- Variabel Kontrol ---
var_jk = tk.StringVar(value="Pria")
var_setuju = tk.IntVar()
var_nama = tk.StringVar()
var_nim = tk.StringVar()
var_jurusan = tk.StringVar()

# --- Trace untuk validasi real-time ---
var_nama.trace_add("write", validate_form)
var_nim.trace_add("write", validate_form)
var_jurusan.trace_add("write", validate_form)

# --- Judul ---
label_judul = tk.Label(
    master=main_frame, 
    text="FORM BIODATA MAHASISWA",
    font=("Arial", 18, "bold"),
    bg=BG_MAIN,
    fg=FG_TEXT
)
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

# --- Frame Input dengan Border ---
frame_input = tk.LabelFrame(
    master=main_frame,
    text="Data Mahasiswa",
    font=("Arial", 12, "bold"),
    bg=BG_FRAME,
    fg=FG_LABEL,
    relief=tk.GROOVE,
    borderwidth=2,
    padx=20,
    pady=20
)
frame_input.grid(row=1, column=0, columnspan=2, sticky="EW", pady=10)
frame_input.columnconfigure(1, weight=1)

# Fungsi helper untuk membuat label
def create_label(parent, text, row, col, sticky="W"):
    return tk.Label(
        master=parent,
        text=text,
        font=("Arial", 11),
        bg=BG_FRAME,
        fg=FG_LABEL
    ).grid(row=row, column=col, sticky=sticky, pady=6)

# Fungsi helper untuk membuat entry
def create_entry(parent, row, col, textvariable):
    entry = tk.Entry(
        master=parent,
        width=32,
        font=("Arial", 11),
        bg=BG_INPUT,
        fg=FG_TEXT,
        relief=tk.SOLID,
        borderwidth=1,
        textvariable=textvariable
    )
    entry.grid(row=row, column=col, pady=6, sticky="EW", padx=(10, 0))
    return entry

# Input Nama
create_label(frame_input, "Nama Lengkap:", 0, 0)
entry_nama = create_entry(frame_input, 0, 1, var_nama)

# Input NIM
create_label(frame_input, "NIM:", 1, 0)
entry_nim = create_entry(frame_input, 1, 1, var_nim)

# Input Jurusan
create_label(frame_input, "Jurusan:", 2, 0)
entry_jurusan = create_entry(frame_input, 2, 1, var_jurusan)

# Input Alamat
tk.Label(
    master=frame_input,
    text="Alamat:",
    font=("Arial", 11),
    bg=BG_FRAME,
    fg=FG_LABEL
).grid(row=3, column=0, sticky="NW", pady=6)

frame_alamat = tk.Frame(
    master=frame_input,
    bg=BG_INPUT,
    relief=tk.SOLID,
    borderwidth=1
)
frame_alamat.grid(row=3, column=1, pady=6, sticky="EW", padx=(10, 0))

scrollbar_alamat = tk.Scrollbar(master=frame_alamat)
scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

text_alamat = tk.Text(
    master=frame_alamat,
    height=5,
    width=30,
    font=("Arial", 11),
    bg=BG_INPUT,
    fg=FG_TEXT,
    relief=tk.FLAT,
    borderwidth=0
)
text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_alamat.config(command=text_alamat.yview)
text_alamat.config(yscrollcommand=scrollbar_alamat.set)

# Jenis Kelamin
tk.Label(
    master=frame_input,
    text="Jenis Kelamin:",
    font=("Arial", 11),
    bg=BG_FRAME,
    fg=FG_LABEL
).grid(row=4, column=0, sticky="W", pady=6)

frame_jk = tk.Frame(master=frame_input, bg=BG_FRAME)
frame_jk.grid(row=4, column=1, sticky="W", pady=6, padx=(10, 0))

tk.Radiobutton(
    master=frame_jk,
    text="Pria",
    variable=var_jk,
    value="Pria",
    font=("Arial", 11),
    bg=BG_FRAME,
    fg=FG_TEXT,
    activebackground=BG_FRAME,
    selectcolor=BG_INPUT
).pack(side=tk.LEFT, padx=8)

tk.Radiobutton(
    master=frame_jk,
    text="Wanita",
    variable=var_jk,
    value="Wanita",
    font=("Arial", 11),
    bg=BG_FRAME,
    fg=FG_TEXT,
    activebackground=BG_FRAME,
    selectcolor=BG_INPUT
).pack(side=tk.LEFT, padx=8)

# Checkbox
check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10),
    bg=BG_FRAME,
    fg=FG_LABEL,
    activebackground=BG_FRAME,
    selectcolor=BG_INPUT,
    command=validate_form
)
check_setuju.grid(row=5, column=0, columnspan=2, pady=12, sticky="W")

# --- Button Submit ---
btn_submit = tk.Button(
    master=main_frame,
    text="Submit Biodata",
    font=("Arial", 12, "bold"),
    bg=BORDER,
    fg="gray",
    activebackground="#2980b9",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2",
    command=submit_data,
    state=tk.DISABLED,
    padx=20,
    pady=12
)
btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")

# --- Label Hasil ---
label_hasil = tk.Label(
    master=main_frame,
    text="",
    font=("Arial", 11, "italic"),
    bg=BG_MAIN,
    fg=FG_LABEL,
    justify=tk.LEFT
)
label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10, pady=10)

# --- Event Binding ---
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

entry_nama.bind("<Return>", submit_shortcut)
entry_nim.bind("<Return>", submit_shortcut)
entry_jurusan.bind("<Return>", submit_shortcut)

# --- Menu Bar ---
menu_bar = tk.Menu(master=window)
window.config(menu=menu_bar)

file_menu = tk.Menu(master=menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Simpan Hasil", command=simpan_hasil)
file_menu.add_separator()
file_menu.add_command(label="Keluar", command=keluar_aplikasi)

window.mainloop()