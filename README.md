# clip-zero-shot-classifier-api

Dự án xây dựng hệ thống **phân loại ảnh zero-shot** sử dụng mô hình [CLIP](https://huggingface.co/openai/clip-vit-large-patch14) của OpenAI, được đóng gói thành REST API bằng **FastAPI**.

## Tính năng

- Phân loại ảnh theo nhãn tùy chỉnh mà **không cần training lại** (zero-shot)
- Hỗ trợ nhận ảnh qua URL
- Trả về top-k nhãn kèm độ tin cậy
- API async, không block event loop khi tải ảnh

---

## Chạy trên Google Colab (khuyến nghị)

### Bước 1 — Mở Google Colab

Truy cập [https://colab.research.google.com](https://colab.research.google.com) và tạo notebook mới.

---

### Bước 2 — Cấu hình GPU T4

> Làm bước này **trước tiên**, trước khi chạy bất kỳ cell nào.

1. Trên thanh menu, chọn **Runtime** (hoặc **Môi trường chạy**)
2. Chọn **Change runtime type** (Thay đổi loại môi trường chạy)
3. Ở mục **Hardware accelerator**, chọn **GPU**
4. Ở mục **GPU type**, chọn **T4**
5. Nhấn **Save**

Kiểm tra GPU đã được kích hoạt chưa bằng cách chạy cell sau:

```python
!nvidia-smi
```

Kết quả hiển thị `Tesla T4` là thành công.

---

### Bước 3 — Clone repo về Colab

```python
!git clone https://github.com/iwyyTh/clip-zero-shot-classifier-api.git
%cd clip-zero-shot-classifier-api
```

---

### Bước 4 — Cài đặt thư viện từ `requirements.txt`

```python
!pip install -r requirements.txt
```

Chờ cài xong (khoảng 2–3 phút).

> Nếu Colab hiện thông báo **"Restart runtime"** sau khi cài xong, nhấn **OK** rồi chạy lại từ **Bước 3**.

---

### Bước 5 — Tạo file cấu hình

```python
yaml_config = """
model_path: "openai/clip-vit-large-patch14"
"""
with open("config.yaml", "w", encoding="utf-8") as f:
    f.write(yaml_config)
```

---

### Bước 6 — Chạy notebook

Mở file `notebook.ipynb` trong Colab và chạy tuần tự từng cell từ trên xuống bằng cách nhấn **Shift + Enter** hoặc nút ▶ ở đầu mỗi cell.

---

## Cấu trúc project

```
clip-zero-shot-classifier-api/
├── config.yaml          # Cấu hình đường dẫn model
├── notebook.ipynb       # Notebook chính
├── requirements.txt     # Danh sách thư viện
└── README.md
```

---

## Thư viện sử dụng

| Thư viện       | Mục đích                           |
| -------------- | ---------------------------------- |
| `transformers` | Load mô hình CLIP                  |
| `fastapi`      | REST API framework                 |
| `uvicorn`      | ASGI server                        |
| `nest-asyncio` | Cho phép chạy async trong notebook |
| `Pillow`       | Xử lý ảnh                          |
| `requests`     | Tải ảnh từ URL                     |
| `omegaconf`    | Đọc file cấu hình YAML             |
| `torch`        | Backend deep learning              |

---

## Nhãn mặc định

```python
labels = [
    "a photo of cat",
    "a photo of dog",
    "a photo of chicken",
]
```

Có thể tuỳ chỉnh danh sách nhãn trong class `ZeroShotClassifier`.

---

## Tham khảo

- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [HuggingFace CLIP](https://huggingface.co/openai/clip-vit-large-patch14)
- [FastAPI Docs](https://fastapi.tiangolo.com)
