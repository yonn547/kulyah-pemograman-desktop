import tkinter as tk
from tkinter import ttk

# Palet warna untuk 3 tema
THEMES = {
    "Light": {
        "bg": "#f5f6fa", "card": "#ffffff", "text": "#2c3e50",
        "accent": "#3498db", "accent_hover": "#2980b9",
        "success": "#27ae60", "danger": "#e74c3c", "muted": "#7f8c8d"
    },
    "Dark": {
        "bg": "#1e2328", "card": "#252a31", "text": "#ffffff",
        "accent": "#00d4ff", "accent_hover": "#0099cc",
        "success": "#00ff88", "danger": "#ff4444", "muted": "#95a5a6"
    },
    "Ocean": {
        "bg": "#0b3d5c", "card": "#12557d", "text": "#eaf6ff",
        "accent": "#00bcd4", "accent_hover": "#008ba3",
        "success": "#4caf50", "danger": "#ff5252", "muted": "#b0bec5"
    }
}

def apply_theme(root, style, theme_name):
    """Terapkan tema ke seluruh widget ttk & tk."""
    t = THEMES[theme_name]

    # Frame & Label dasar
    style.configure("App.TFrame", background=t["bg"])
    style.configure("Card.TFrame", background=t["card"], relief="flat")
    style.configure("App.TLabel", background=t["bg"], foreground=t["text"],
                    font=("Segoe UI", 10))
    style.configure("Title.TLabel", background=t["bg"], foreground=t["accent"],
                    font=("Segoe UI", 18, "bold"))
    style.configure("CardTitle.TLabel", background=t["card"], foreground=t["text"],
                    font=("Segoe UI", 11, "bold"))
    style.configure("Metric.TLabel", background=t["card"], foreground=t["success"],
                    font=("Segoe UI", 22, "bold"))
    style.configure("Muted.TLabel", background=t["card"], foreground=t["muted"],
                    font=("Segoe UI", 9))

    # Button
    style.configure("Accent.TButton", background=t["accent"], foreground="#ffffff",
                    borderwidth=0, padding=(14, 8), font=("Segoe UI", 10, "bold"))
    style.map("Accent.TButton",
              background=[("active", t["accent_hover"]), ("pressed", t["accent_hover"])])

    style.configure("Danger.TButton", background=t["danger"], foreground="#ffffff",
                    borderwidth=0, padding=(10, 6), font=("Segoe UI", 9, "bold"))
    style.map("Danger.TButton", background=[("active", "#c0392b")])

    # Entry
    style.configure("App.TEntry", fieldbackground=t["card"], foreground=t["text"],
                    padding=(8, 6), borderwidth=1)

    # Progressbar
    style.configure("Accent.Horizontal.TProgressbar",
                    background=t["accent"], troughcolor=t["card"])

    # Notebook (tab)
    style.configure("TNotebook", background=t["bg"], borderwidth=0)
    style.configure("TNotebook.Tab", background=t["card"], foreground=t["text"],
                    padding=(16, 8))
    style.map("TNotebook.Tab",
              background=[("selected", t["accent"])],
              foreground=[("selected", "#ffffff")])

    # Simpan palet ke root agar bisa diakses widget tk biasa
    root.theme_colors = t