# clip-zero-shot-classifier-api

Dự án xây dựng hệ thống **phân loại ảnh zero-shot** sử dụng mô hình [CLIP](https://huggingface.co/openai/clip-vit-large-patch14) của OpenAI, được đóng gói thành REST API bằng **FastAPI**.

## Tính năng

- Phân loại ảnh theo nhãn tùy chỉnh mà **không cần training lại** (zero-shot)
- Hỗ trợ nhận ảnh qua URL
- Trả về top-k nhãn kèm độ tin cậy
- API async, không block event loop khi tải ảnh

---

## Chạy trên Google Colab

### Bước 1 — Clone repo về máy

Mở terminal trên máy tính và chạy:

```bash
git clone https://github.com/<your-username>/clip-zero-shot-classifier-api.git
```

---

### Bước 2 — Cấu hình GPU T4

> ⚠️ Làm bước này **trước khi chạy bất kỳ cell nào**.

1. Truy cập [https://colab.research.google.com](https://colab.research.google.com)
2. Chọn **Runtime → Change runtime type**
3. Mục **Hardware accelerator** chọn **GPU**
4. Mục **GPU type** chọn **T4**
5. Nhấn **Save**

---

### Bước 3 — Mở notebook

1. Trong Colab, chọn **File → Open notebook → Upload**
2. Upload file `Zero_shot_CLIP.ipynb` từ thư mục vừa clone về máy

---

### Bước 4 — Chạy notebook

Chạy tuần tự từng cell từ trên xuống bằng **Shift + Enter**.

Cell đầu tiên sẽ tự động cài toàn bộ thư viện cần thiết:

```python
!pip install fastapi nest-asyncio uvicorn transformers torch Pillow requests omegaconf
```

> 💡 Nếu Colab yêu cầu **Restart runtime** sau khi cài xong, nhấn **OK** rồi chạy lại từ cell đầu tiên.

---

## Cấu trúc project

```
clip-zero-shot-classifier-api/
├── config.yaml              # Cấu hình đường dẫn model
├── Zero_shot_CLIP.ipynb     # Notebook chính
├── requirements.txt         # Danh sách thư viện
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
