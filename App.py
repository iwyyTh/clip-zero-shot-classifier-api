"""
app.py - Giao diện demo local cho Zero-shot CLIP
==================================================
Chạy file này trên máy LOCAL (không cần GPU).
API sẽ gọi đến Colab qua Pinggy URL.

Cài thư viện: pip install requests pillow
Chạy: python app.py
"""

import tkinter as tk
from tkinter import messagebox
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO

# ============================================================
#  ⚙️  CẤU HÌNH: Thay URL Pinggy từ Colab vào đây
# ============================================================
DEFAULT_API_URL = "https://your-pinggy-url.pinggy.io"  # ← thay URL Colab ở đây
# ============================================================


class CLIPDemoApp:

    # Nhãn cứng — khớp với ZeroShotClassifier trong notebook
    LABELS = [
        "a photo of cat",
        "a photo of dog",
        "a photo of chicken",
    ]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Zero-shot CLIP Classifier")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1e2e")

        self.api_url = tk.StringVar(value=DEFAULT_API_URL)
        self.image_url = tk.StringVar(
            value="https://pethouse.com.vn/wp-content/uploads/2022/08/anh-cho-poodle-36.jpg")
        self.k_value = tk.IntVar(value=len(self.LABELS))
        self.status_text = tk.StringVar(value="Nhập URL ảnh và nhấn Phân loại")

        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#313244", pady=10)
        header.pack(fill="x")
        tk.Label(header, text="🔍 Zero-shot CLIP Classifier",
                 font=("Segoe UI", 18, "bold"), bg="#313244", fg="#cdd6f4").pack()
        tk.Label(header, text="Phân loại ảnh không cần training • Powered by OpenAI CLIP",
                 font=("Segoe UI", 9), bg="#313244", fg="#a6adc8").pack()

        main = tk.Frame(self.root, bg="#1e1e2e", padx=20, pady=10)
        main.pack(fill="both", expand=True)

        # API URL
        self._section(main, "🌐 Colab API URL")
        api_frame = tk.Frame(main, bg="#1e1e2e")
        api_frame.pack(fill="x", pady=(0, 8))
        tk.Entry(api_frame, textvariable=self.api_url,
                 font=("Consolas", 10), bg="#313244", fg="#cdd6f4",
                 insertbackground="white", relief="flat", bd=5).pack(side="left", fill="x", expand=True)
        tk.Button(api_frame, text="Test", command=self._test_connection,
                  bg="#89b4fa", fg="#1e1e2e", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=8).pack(side="left", padx=(5, 0))

        # Image URL
        self._section(main, "URL Ảnh")
        img_frame = tk.Frame(main, bg="#1e1e2e")
        img_frame.pack(fill="x", pady=(0, 8))
        tk.Entry(img_frame, textvariable=self.image_url,
                 font=("Consolas", 10), bg="#313244", fg="#cdd6f4",
                 insertbackground="white", relief="flat", bd=5).pack(side="left", fill="x", expand=True)
        tk.Button(img_frame, text="Preview", command=self._preview_image,
                  bg="#a6e3a1", fg="#1e1e2e", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=8).pack(side="left", padx=(5, 0))

        # Labels (read-only badges) + K
        row = tk.Frame(main, bg="#1e1e2e")
        row.pack(fill="x", pady=(0, 8))

        left = tk.Frame(row, bg="#1e1e2e")
        left.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._section(left, "🏷️ Nhãn phân loại")
        badge_frame = tk.Frame(left, bg="#313244", padx=8, pady=6)
        badge_frame.pack(fill="x")
        badge_colors = ["#f9e2af", "#cba6f7", "#89b4fa"]
        for i, label in enumerate(self.LABELS):
            tk.Label(badge_frame, text=f"  {label}  ",
                     bg=badge_colors[i % len(badge_colors)], fg="#1e1e2e",
                     font=("Segoe UI", 9, "bold"), padx=4, pady=2).pack(side="left", padx=(0, 6))

        right = tk.Frame(row, bg="#1e1e2e", width=100)
        right.pack(side="right")
        right.pack_propagate(False)
        self._section(right, "Top-K")
        tk.Spinbox(right, from_=1, to=len(self.LABELS), textvariable=self.k_value,
                   font=("Segoe UI", 12, "bold"), width=5,
                   bg="#313244", fg="#cdd6f4", buttonbackground="#45475a",
                   relief="flat").pack()

        # Image preview
        self.preview_label = tk.Label(main, bg="#313244", relief="flat",
                                      text="[ Xem trước ảnh ở đây ]",
                                      fg="#6c7086", font=("Segoe UI", 10))
        self.preview_label.pack(fill="x", ipady=60, pady=(0, 8))

        # Predict button
        tk.Button(main, text="Phân loại ngay", command=self._run_predict,
                  bg="#cba6f7", fg="#1e1e2e", font=("Segoe UI", 13, "bold"),
                  relief="flat", pady=8, cursor="hand2").pack(fill="x", pady=(0, 10))

        # Results
        self._section(main, "Kết quả")
        self.result_frame = tk.Frame(main, bg="#1e1e2e")
        self.result_frame.pack(fill="x")

        # Status bar
        status_bar = tk.Frame(self.root, bg="#313244", pady=4)
        status_bar.pack(fill="x", side="bottom")
        self.status_label = tk.Label(status_bar, textvariable=self.status_text,
                                     bg="#313244", fg="#a6adc8", font=("Segoe UI", 9))
        self.status_label.pack(side="left", padx=10)

    def _section(self, parent, text):
        tk.Label(parent, text=text, bg="#1e1e2e", fg="#89dceb",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(4, 2))

    def _set_status(self, msg, color="#a6adc8"):
        self.status_text.set(msg)
        self.status_label.config(fg=color)

    def _test_connection(self):
        # 1. Lấy chuỗi URL người dùng nhập
        raw_url = self.api_url.get().strip()

        # 2. Xử lý URL thông minh:
        # Cắt chuỗi tại "/predict" (nếu có), lấy phần đầu tiên (base url) và xóa dấu "/" thừa ở cuối.
        base_url = raw_url.split("/predict")[0].rstrip("/")

        # 3. Gắn đuôi /health để test
        health_url = base_url + "/health"

        self._set_status("Đang kiểm tra kết nối...")

        def _check():
            try:
                # Gọi request tới health_url thay vì url cũ
                resp = requests.get(health_url, timeout=10)
                if resp.status_code == 200:
                    self.root.after(0, lambda: self._set_status(
                        "Kết nối thành công!", "#a6e3a1"))
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Kết nối OK", f"API hoạt động tốt!\nĐã gọi tới: {health_url}"))
                else:
                    self.root.after(0, lambda: self._set_status(
                        f"HTTP {resp.status_code}", "#fab387"))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(
                    "Không kết nối được", "#f38ba8"))
                self.root.after(0, lambda: messagebox.showerror(
                    "Lỗi kết nối", f"Đang cố gọi: {health_url}\nLỗi chi tiết: {str(e)}"))

        threading.Thread(target=_check, daemon=True).start()

    def _preview_image(self):
        url = self.image_url.get().strip()
        if not url:
            messagebox.showwarning("Thiếu URL", "Vui lòng nhập URL ảnh!")
            return
        self._set_status("Đang tải ảnh xem trước...")

        def _load():
            try:
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content)).convert("RGB")
                img.thumbnail((500, 200))
                photo = ImageTk.PhotoImage(img)
                self.root.after(0, lambda: self._update_preview(photo))
                self.root.after(0, lambda: self._set_status("Ảnh tải xong"))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(
                    "Lỗi tải ảnh", "#f38ba8"))
                self.root.after(
                    0, lambda: messagebox.showerror("Lỗi ảnh", str(e)))
        threading.Thread(target=_load, daemon=True).start()

    def _update_preview(self, photo):
        self.preview_label.config(image=photo, text="")
        self.preview_label.image = photo

    def _run_predict(self):
        api_base = self.api_url.get().strip().rstrip("/").removesuffix("/predict")
        img_url = self.image_url.get().strip()
        k = self.k_value.get()

        if not api_base or "your-pinggy" in api_base:
            messagebox.showwarning(
                "Chưa cấu hình", "Vui lòng nhập Colab Pinggy URL vào ô đầu tiên!")
            return
        if not img_url:
            messagebox.showwarning("Thiếu URL", "Vui lòng nhập URL ảnh!")
            return

        self._set_status("Đang phân loại... (có thể mất vài giây)")
        self._clear_results()

        def _call():
            try:
                params = {"image_url": img_url, "k": k}
                resp = requests.get(f"{api_base}/predict",
                                    params=params, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                results = data if isinstance(
                    data, list) else data.get("results", [])
                self.root.after(0, lambda: self._show_results(results))
                self.root.after(0, lambda: self._set_status(
                    "Phân loại thành công!", "#a6e3a1"))
            except requests.exceptions.Timeout:
                self.root.after(0, lambda: self._set_status(
                    "Timeout", "#f38ba8"))
                self.root.after(0, lambda: messagebox.showerror(
                    "Timeout", "API không phản hồi trong 120 giây."))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(
                    f"Lỗi: {e}", "#f38ba8"))
                self.root.after(0, lambda: messagebox.showerror("Lỗi", str(e)))

        threading.Thread(target=_call, daemon=True).start()

    def _clear_results(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

    def _show_results(self, results):
        self._clear_results()
        if not results:
            tk.Label(self.result_frame, text="Không có kết quả.",
                     bg="#1e1e2e", fg="#f38ba8", font=("Segoe UI", 10)).pack()
            return

        max_conf = results[0]["confidence"] if results else 100
        badge_colors = ["#f9e2af", "#cba6f7", "#89b4fa"]

        for i, item in enumerate(results):
            label = item["label"]
            conf = item["confidence"]
            bar_width = int((conf / max(max_conf, 1)) * 400)

            row = tk.Frame(self.result_frame, bg="#1e1e2e", pady=4)
            row.pack(fill="x")

            tk.Label(row, text=f"#{i+1}",
                     bg=badge_colors[i] if i < 3 else "#6c7086", fg="#1e1e2e",
                     font=("Segoe UI", 9, "bold"), width=3).pack(side="left", padx=(0, 6))

            tk.Label(row, text=label, bg="#1e1e2e", fg="#cdd6f4",
                     font=("Segoe UI", 10), width=30, anchor="w").pack(side="left")

            canvas = tk.Canvas(row, height=20, width=400, bg="#313244",
                               bd=0, highlightthickness=0)
            canvas.pack(side="left", padx=(6, 6))
            canvas.create_rectangle(0, 0, bar_width, 20,
                                    fill="#a6e3a1" if i == 0 else "#89b4fa", outline="")

            tk.Label(row, text=f"{conf:.1f}%", bg="#1e1e2e", fg="#cdd6f4",
                     font=("Consolas", 10, "bold"), width=7).pack(side="left")


if __name__ == "__main__":
    root = tk.Tk()
    app = CLIPDemoApp(root)
    root.mainloop()
