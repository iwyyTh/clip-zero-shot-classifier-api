# Zero-shot CLIP Classifier

Phân loại ảnh không cần training, sử dụng mô hình **OpenAI CLIP** chạy trên Google Colab và giao diện desktop local (`App.py`).

---

## Cấu trúc dự án

```
CLIP-ZERO-SHOT-CLASSIFIER-API/
├── venv/
├── App.py                  # Giao diện desktop (chạy local)
├── README.md
├── requirements.txt
└── Zero_shot_CLIP.ipynb    # Mô hình + API (chạy trên Colab)
```

---

## Hướng dẫn sử dụng

### Bước 1 — Chạy notebook trên Google Colab

1. Mở file `Zero_shot_CLIP.ipynb` trên [Google Colab](https://colab.research.google.com)
2. Chọn Runtime **GPU (T4)**: `Runtime > Change runtime type > T4 GPU`
3. Chạy lần lượt các cell từ đầu đến cell **"Get Pinggy URL"**:

   | Cell               | Mô tả                                  |
   | ------------------ | -------------------------------------- |
   | Install Libraries  | Cài các thư viện cần thiết             |
   | Create Config File | Tạo file cấu hình model                |
   | Build Model        | Định nghĩa class `ZeroShotClassifier`  |
   | Initialize Model   | Load mô hình CLIP                      |
   | Initialize API     | Khởi động FastAPI server tại cổng 8000 |
   | **Get Pinggy URL** | Tạo public URL để truy cập từ ngoài    |

4. Sau khi chạy cell **Get Pinggy URL**, console sẽ in ra một URL dạng:
   ```
   https://xxxx-xxxx.pinggy.link/predict
   ```
   > 💡 Có thể chạy tiếp các cell **Call Local API** và **Call Public API** để kiểm tra API hoạt động đúng trên Colab.

---

### Bước 2 — Cài đặt và chạy App.py (local)

```bash
pip install -r requirements.txt
python App.py
```

---

### Bước 3 — Sử dụng giao diện

#### Nhập Pinggy URL và kiểm tra kết nối

- Dán URL Pinggy (bao gồm `/predict`) vào ô **Colab API URL**
- Nhấn **Test** → thông báo ✅ nghĩa là kết nối thành công

#### Xem trước ảnh

- Dán URL ảnh vào ô **URL Ảnh**
- Nhấn **Preview** để xem trước ảnh trong giao diện

#### Phân loại

- Chọn số lượng nhãn **Top-K** muốn hiển thị
- Nhấn **Phân loại ngay** để gửi ảnh đến API và nhận kết quả

Kết quả trả về gồm nhãn và độ chính xác (%), hiển thị dưới dạng thanh bar trực quan.

---

## 🏷️ Nhãn phân loại

Mô hình hiện hỗ trợ 3 nhãn:

- `a photo of cat`
- `a photo of dog`
- `a photo of chicken`

---

## ⚠️ Lưu ý

- Colab session sẽ **timeout sau ~12 giờ** không hoạt động — cần chạy lại notebook và lấy URL mới.
- Pinggy URL **thay đổi mỗi lần** khởi động lại tunnel.
- `tkinter` là thư viện built-in của Python, **không cần cài thêm**.

## Video Demo

https://github.com/user-attachments/assets/0dbd2602-c0bf-4f68-9d80-37a3d0bbbcdd


