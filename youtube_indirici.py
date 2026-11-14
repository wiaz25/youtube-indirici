import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

import yt_dlp


def masaustu_yolu() -> Path:
    home = Path.home()
    adaylar = [
        home / "Desktop",
        home / "OneDrive" / "Desktop",
        home / "OneDrive" / "Masaüstü",
        home / "Masaüstü",
    ]
    for yol in adaylar:
        if yol.exists():
            return yol
    return home


class Uygulama:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("YouTube Video İndirici")
        root.geometry("560x300")
        root.resizable(False, False)

        self.url_var = tk.StringVar()
        self.cozunurluk_var = tk.StringVar()
        self.durum_var = tk.StringVar(value="Video bağlantısını yapıştırın.")
        self.baslik_var = tk.StringVar(value="")

        frm = ttk.Frame(root, padding=15)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Video bağlantısı:").pack(anchor="w")
        satir = ttk.Frame(frm)
        satir.pack(fill="x", pady=(2, 10))
        self.url_entry = ttk.Entry(satir, textvariable=self.url_var)
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.getir_btn = ttk.Button(satir, text="Çözünürlükleri Getir", command=self.cozunurluk_getir)
        self.getir_btn.pack(side="left", padx=(8, 0))

        ttk.Label(frm, textvariable=self.baslik_var, wraplength=520, foreground="#555").pack(anchor="w")

        ttk.Label(frm, text="Çözünürlük:").pack(anchor="w", pady=(10, 0))
        self.combo = ttk.Combobox(frm, textvariable=self.cozunurluk_var, state="readonly", width=30)
        self.combo.pack(anchor="w", pady=(2, 10))

        self.indir_btn = ttk.Button(frm, text="Masaüstüne İndir", command=self.indir, state="disabled")
        self.indir_btn.pack(anchor="w")

        self.bar = ttk.Progressbar(frm, maximum=100)
        self.bar.pack(fill="x", pady=(15, 4))
        ttk.Label(frm, textvariable=self.durum_var).pack(anchor="w")

        self.yukseklikler = []

    # ---------- yardımcılar ----------
    def ui(self, fonksiyon, *args):
        self.root.after(0, lambda: fonksiyon(*args))

    def durum(self, metin):
        self.ui(self.durum_var.set, metin)

    # ---------- çözünürlükleri getir ----------
    def cozunurluk_getir(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Uyarı", "Önce bir video bağlantısı yapıştırın.")
            return
        self.getir_btn.config(state="disabled")
        self.indir_btn.config(state="disabled")
        self.durum_var.set("Video bilgileri alınıyor...")
        threading.Thread(target=self._getir_is, args=(url,), daemon=True).start()

    def _getir_is(self, url):
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "noplaylist": True}) as ydl:
                bilgi = ydl.extract_info(url, download=False)
            yukseklikler = sorted(
                {f["height"] for f in bilgi.get("formats", [])
                 if f.get("height") and f.get("vcodec") not in (None, "none")},
                reverse=True,
            )
            if not yukseklikler:
                raise RuntimeError("Video formatı bulunamadı.")
            self.ui(self._getir_bitti, bilgi.get("title", ""), yukseklikler)
        except Exception as e:
            self.ui(self._hata, str(e))

    def _getir_bitti(self, baslik, yukseklikler):
        self.yukseklikler = yukseklikler
        self.baslik_var.set(baslik)
        degerler = [f"{h}p" for h in yukseklikler]
        self.combo["values"] = degerler
        self.combo.current(0)
        self.getir_btn.config(state="normal")
        self.indir_btn.config(state="normal")
        self.durum_var.set("Çözünürlük seçin ve indirin.")

    # ---------- indir ----------
    def indir(self):
        url = self.url_var.get().strip()
        secim = self.cozunurluk_var.get()
        if not url or not secim:
            return
        yukseklik = int(secim.replace("p", ""))
        self.getir_btn.config(state="disabled")
        self.indir_btn.config(state="disabled")
        self.bar["value"] = 0
        threading.Thread(target=self._indir_is, args=(url, yukseklik), daemon=True).start()

    def _ilerleme(self, d):
        if d["status"] == "downloading":
            toplam = d.get("total_bytes") or d.get("total_bytes_estimate")
            if toplam:
                yuzde = d["downloaded_bytes"] / toplam * 100
                self.ui(self.bar.config, {"value": yuzde})
            hiz = d.get("_speed_str", "").strip()
            self.durum(f"İndiriliyor... %{self.bar['value']:.0f}  {hiz}")
        elif d["status"] == "finished":
            self.durum("Video ve ses birleştiriliyor...")

    def _indir_is(self, url, h):
        hedef = masaustu_yolu()
        secenekler = {
            "format": (
                f"bv*[height<={h}][ext=mp4]+ba[ext=m4a]/"
                f"bv*[height<={h}]+ba/"
                f"b[height<={h}]"
            ),
            "merge_output_format": "mp4",
            "outtmpl": str(hedef / "%(title)s [%(height)sp].%(ext)s"),
            "noplaylist": True,
            "progress_hooks": [self._ilerleme],
            "quiet": True,
        }
        try:
            with yt_dlp.YoutubeDL(secenekler) as ydl:
                ydl.download([url])
            self.ui(self._bitti, str(hedef))
        except Exception as e:
            self.ui(self._hata, str(e))

    def _bitti(self, klasor):
        self.bar["value"] = 100
        self.durum_var.set("İndirme tamamlandı!")
        self.getir_btn.config(state="normal")
        self.indir_btn.config(state="normal")
        messagebox.showinfo("Bitti", f"Video şuraya indirildi:\n{klasor}")

    def _hata(self, mesaj):
        self.durum_var.set("Hata oluştu.")
        self.getir_btn.config(state="normal")
        if self.yukseklikler:
            self.indir_btn.config(state="normal")
        messagebox.showerror("Hata", mesaj)


if __name__ == "__main__":
    root = tk.Tk()
    Uygulama(root)
    root.mainloop()
