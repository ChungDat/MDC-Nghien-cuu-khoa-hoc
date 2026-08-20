# TODO
* Sửa lỗi bong bóng chat

# Thiết lập môi trường

## Sử dụng Anaconda

1. Mở Anaconda
2. Tạo Environment mới (chỉ cần tạo một lần)
3. Cài các thư viện: `joblib`, `mord`, `pandas`, `scikit-learn`, `numpy`, `streamlit`, `supabase`
4. Mở thư mục chứa dự án và chạy lệnh:

```bash
conda activate [tên môi trường]
python main.py
```

## Sử dụng uv

1. Mở thư mục chứa dự án và chạy lệnh:

```bash
uv sync
uv run main.py
```

# Cấu hình

`config.json` chứa đường đẫn đến các file sử dụng trong chương trình, bao gồm:

- Các file kịch bản
- Câu hỏi
- Ý nghĩa PAIS
- Ý nghĩa điểm likert
- Thời gian delay của các bong bóng chat
- Đường dẫn đến file mô hình dự đoán

# Lưu ý

Giao diện web sẽ tự động mở khi chạy `main.py`.

Nếu web không tự động mở, mở trình duyệt và truy cập `http://localhost:8501`

# Các file cấu hình
* `.streamlit/secrets.toml`: Chứa các thông tin nhạy cảm, bao gồm mật khẩu quản trị và thông tin kết nối Supabase, KHÔNG UPLOAD file này, dán nội dung vào phần secret của streamlit cloud.
* `.streamlit/config.toml`: Chứa các thiết lập cho giao diện Streamlit (Để ẩn sidebar mặc định).
* `config.json`: Chứa các đường dẫn đến các file sử dụng trong chương trình.

# Các thư mục/file quan trọng
```
./
|   .streamlit/
|   |   secrets.toml (BẢO MẬT, KHÔNG UP TRỰC TIẾP LÊN GIT)
|   |   config.toml
|   data/
|   |   form/
|   |   |   questions.json
|   |   |   answers.json
|   |   |   likert.json
|   |   script/
|   |   |   scene_1.json
|   |   |   scene_2.json
|   |   |   scene_3.json
|   db
|   |   queries.py
|   models
|   |   v1_rf.joblib
|   |   v1_lr.joblib
|   |   v1_olr.joblib
|   pages/
|   |   scene_1.py
|   |   scene_2.py
|   |   scene_3.py
|   |   dashboard.py
|   supabase/
|   |   migrations/
|   app.py
|   config.json
|   main.py
|   pyproject.toml
|   README.md
|   ui.py
|   utils.py
```