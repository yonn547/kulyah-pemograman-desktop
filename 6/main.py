import tkinter as tk
from tkinter import ttk, messagebox
import threading, time
from styles import apply_theme, THEMES
from task_manager import TaskManager


class TaskFlowApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TaskFlow — Desktop Task Manager")
        self.root.geometry("900x650")
        self.root.minsize(500, 450)          # Responsive (materi 2.2)

        self.tm = TaskManager()
        self.style = ttk.Style()
        self.current_theme = tk.StringVar(value="Dark")
        self.current_layout = "desktop"
        self.anim_running = False

        apply_theme(self.root, self.style, self.current_theme.get())
        self.root.configure(bg=self.root.theme_colors["bg"])

        self._build_ui()
        self._bind_resize()

    # ================= UI =================
    def _build_ui(self):
        c = self.root.theme_colors

        # ---- HEADER ----
        self.header = tk.Frame(self.root, bg=c["bg"])
        self.header.pack(fill="x", padx=20, pady=(15, 5))

        self.title_lbl = tk.Label(self.header, text="🗂️  TaskFlow",
                                  bg=c["bg"], fg=c["accent"],
                                  font=("Segoe UI", 20, "bold"))
        self.title_lbl.pack(side="left")

        # Theme switcher (materi 1.2)
        ttk.Label(self.header, text="Tema:", style="App.TLabel").pack(side="right", padx=(0, 5))
        self.theme_combo = ttk.Combobox(self.header, textvariable=self.current_theme,
                                        values=list(THEMES.keys()), state="readonly", width=10)
        self.theme_combo.pack(side="right")
        self.theme_combo.bind("<<ComboboxSelected>>", self._on_theme_change)

        # ---- NOTEBOOK (TAB) ----
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_tasks = ttk.Frame(self.notebook, style="App.TFrame")
        self.tab_dash = ttk.Frame(self.notebook, style="App.TFrame")
        self.notebook.add(self.tab_tasks, text="📋 Tugas")
        self.notebook.add(self.tab_dash, text="📊 Dashboard")

        self._build_tasks_tab()
        self._build_dashboard_tab()

        # ---- STATUS BAR ----
        self.status_lbl = ttk.Label(self.root, text="Siap.", style="App.TLabel")
        self.status_lbl.pack(fill="x", padx=20, pady=(0, 8))

    # ---------- TAB TUGAS ----------
    def _build_tasks_tab(self):
        c = self.root.theme_colors

        # Form input
        form = ttk.Frame(self.tab_tasks, style="Card.TFrame", padding=15)
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Tambah Tugas", style="CardTitle.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        ttk.Label(form, text="Judul:", style="CardTitle.TLabel").grid(row=1, column=0, sticky="w")
        self.entry_title = ttk.Entry(form, style="App.TEntry", width=40)
        self.entry_title.grid(row=1, column=1, padx=8, sticky="ew")

        ttk.Label(form, text="Prioritas:", style="CardTitle.TLabel").grid(row=1, column=2, sticky="w", padx=(10, 0))
        self.priority_var = tk.StringVar(value="Normal")
        self.priority_combo = ttk.Combobox(form, textvariable=self.priority_var,
                                           values=["Low", "Normal", "High"],
                                           state="readonly", width=10)
        self.priority_combo.grid(row=1, column=3, padx=8)

        ttk.Button(form, text="➕ Tambah", style="Accent.TButton",
                   command=self._add_task).grid(row=1, column=4, padx=(10, 0))

        form.columnconfigure(1, weight=1)

        # Daftar tugas
        list_frame = ttk.Frame(self.tab_tasks, style="Card.TFrame", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.task_listbox = tk.Listbox(
            list_frame, bg=c["card"], fg=c["text"], selectbackground=c["accent"],
            font=("Consolas", 11), borderwidth=0, highlightthickness=0, activestyle="none")
        self.task_listbox.pack(side="left", fill="both", expand=True)
        self.task_listbox.bind("<Double-Button-1>", lambda e: self._toggle_task())

        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        sb.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=sb.set)

        # Tombol aksi
        actions = ttk.Frame(self.tab_tasks, style="App.TFrame")
        actions.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(actions, text="✔ Tandai Selesai", style="Accent.TButton",
                   command=self._toggle_task).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="🗑 Hapus", style="Danger.TButton",
                   command=self._delete_task).pack(side="left")

        self._refresh_list()

    # ---------- TAB DASHBOARD ----------
    def _build_dashboard_tab(self):
        c = self.root.theme_colors

        # Kartu metrik (materi 3.2)
        metrics = ttk.Frame(self.tab_dash, style="App.TFrame")
        metrics.pack(fill="x", padx=10, pady=10)

        self.card_total = self._make_metric_card(metrics, "Total Tugas", "0")
        self.card_done = self._make_metric_card(metrics, "Selesai", "0")
        self.card_pending = self._make_metric_card(metrics, "Pending", "0")

        # Progress bar animasi (materi 3.1)
        prog_frame = ttk.Frame(self.tab_dash, style="Card.TFrame", padding=15)
        prog_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(prog_frame, text="Progress Penyelesaian", style="CardTitle.TLabel").pack(anchor="w")
        self.progress = ttk.Progressbar(prog_frame, style="Accent.Horizontal.TProgressbar",
                                        mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(10, 5))
        self.progress_lbl = ttk.Label(prog_frame, text="0%", style="Muted.TLabel")
        self.progress_lbl.pack(anchor="e")

        # Log real-time (materi 3.2)
        log_frame = ttk.LabelFrame(self.tab_dash, text="Log Aktivitas", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(log_frame, height=10, bg=c["bg"], fg=c["success"],
                                font=("Consolas", 9), state="disabled", borderwidth=0)
        self.log_text.pack(fill="both", expand=True)

        # Tombol refresh animasi
        ctrl = ttk.Frame(self.tab_dash, style="App.TFrame")
        ctrl.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(ctrl, text="🔄 Refresh Statistik", style="Accent.TButton",
                   command=self._refresh_dashboard).pack(side="left", padx=(0, 8))
        ttk.Button(ctrl, text="🧹 Bersihkan Log", style="Danger.TButton",
                   command=self._clear_log).pack(side="left")

        self._refresh_dashboard()

    def _make_metric_card(self, parent, title, value):
        card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        card.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        val_lbl = ttk.Label(card, text=value, style="Metric.TLabel")
        val_lbl.pack(anchor="w", pady=(5, 0))
        return val_lbl

    # ================= LOGIC =================
    def _add_task(self):
        title = self.entry_title.get().strip()
        if not title:
            self._log("⚠ Judul tugas kosong.")
            messagebox.showwarning("Peringatan", "Judul tugas tidak boleh kosong!")
            return
        self.tm.add(title, self.priority_var.get())
        self.entry_title.delete(0, "end")
        self._refresh_list()
        self._refresh_dashboard()
        self._log(f"✔ Ditambahkan: '{title}' ({self.priority_var.get()})")

    def _toggle_task(self):
        sel = self.task_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.tm.toggle(idx)
        self._refresh_list()
        self._refresh_dashboard()
        status = "selesai" if self.tm.tasks[idx]["done"] else "dibuka"
        self._log(f"↻ Tugas '{self.tm.tasks[idx]['title']}' ditandai {status}.")

    def _delete_task(self):
        sel = self.task_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        title = self.tm.tasks[idx]["title"]
        if messagebox.askyesno("Hapus", f"Hapus tugas '{title}'?"):
            self.tm.delete(idx)
            self._refresh_list()
            self._refresh_dashboard()
            self._log(f"🗑 Dihapus: '{title}'")

    def _refresh_list(self):
        self.task_listbox.delete(0, "end")
        for t in self.tm.tasks:
            mark = "✔" if t["done"] else "○"
            line = f" {mark}  [{t['priority']:<6}] {t['title']}"
            self.task_listbox.insert("end", line)
            if t["done"]:
                self.task_listbox.itemconfig("end", fg=self.root.theme_colors["muted"])

    def _refresh_dashboard(self):
        total, done, pending, progress = self.tm.stats()
        self.card_total.config(text=str(total))
        self.card_done.config(text=str(done))
        self.card_pending.config(text=str(pending))

        # Animasi progress smooth (materi 3.1)
        self._animate_progress(progress)

    def _animate_progress(self, target):
        def run():
            current = float(self.progress["value"])
            steps = 20
            for i in range(steps + 1):
                val = current + (target - current) * (i / steps)
                self.progress["value"] = val
                self.progress_lbl.config(text=f"{val:.0f}%")
                time.sleep(0.02)
        if not self.anim_running:
            self.anim_running = True
            threading.Thread(target=run, daemon=True).start()
            self.root.after(600, lambda: setattr(self, "anim_running", False))

    # ================= THEME =================
    def _on_theme_change(self, event=None):
        name = self.current_theme.get()
        apply_theme(self.root, self.style, name)
        c = self.root.theme_colors

        # Update widget tk biasa (tidak otomatis ikut ttk style)
        self.root.configure(bg=c["bg"])
        self.header.configure(bg=c["bg"])
        self.title_lbl.configure(bg=c["bg"], fg=c["accent"])
        self.task_listbox.configure(bg=c["card"], fg=c["text"],
                                    selectbackground=c["accent"])
        self.log_text.configure(bg=c["bg"], fg=c["success"])
        self._refresh_list()
        self._log(f"🎨 Tema diubah ke '{name}'.")

    # ================= RESPONSIVE (materi 2.2) =================
    def _bind_resize(self):
        self.root.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        if event.widget != self.root:
            return
        w = self.root.winfo_width()
        if w < 550:
            layout = "mobile"
        elif w < 780:
            layout = "tablet"
        else:
            layout = "desktop"

        if layout != self.current_layout:
            self.current_layout = layout
            # Sesuaikan ukuran font header sebagai respon
            size = {"mobile": 14, "tablet": 17, "desktop": 20}[layout]
            self.title_lbl.config(font=("Segoe UI", size, "bold"))

    # ================= UTIL =================
    def _log(self, msg):
        from datetime import datetime
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"[{stamp}] {msg}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.status_lbl.config(text=msg)

    def _clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TaskFlowApp()
    app.run()