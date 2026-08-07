# Thiết lập môi trường

## Sử dụng Anaconda

1. Mở Anaconda
2. Tạo Environment mới (chỉ cần tạo một lần)
3. Cài các thư viện: `streamlit`, `joblib`, `scikit-learn`, `pandas`, `numpy`
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

## Sử dụng pip

1. Mở thư mục chứa dự án và chạy lệnh:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
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

Khi cần ngắt kết nối, nhấn `Ctrl + C` trong terminal đã dùng để chạy `main.py`

Khi muốn thay đổi nội dung, **GIỮ NGUYÊN** các `key` (phần nằm trước dấu `:`), chỉ sửa đổi phần `value` (sau dấu `:`) nếu chưa hiểu rõ code.

Phần nội dung cần được viết liên tục, không xuống dòng bằng Enter.

Khi cần xuống dòng trong content thì dùng `\n` ngay sau vị trí muốn xuống dòng ("vi du`\n`abc").

Khi cần thụt dòng trong content thì dùng `\t` ngay sau vị trí muốn thụt dòng ("vi du`\t`abc").

`key` (trước dấu `:`) cần được đặt trong dấu `''` hoặc `""`.

`value` (sau dấu `:`) cần được đặt trong dấu `''` hoặc `""` nếu là chuỗi ký tự, không cần nếu là số.

Nếu nội dung trong `value` chứa dấu trùng với dấu bao `value` thì dùng dấu `\` ngay trước dấu trùng đó (ví dụ: "vi du `\"`abc`\"`" hoặc 'vi du `\'`abc`\'`').

Nếu nội dung trong `value` không chứa dấu trùng thì không cần dùng dấu `\` (ví dụ: xyz: "vi du `'`abc`'`" hoặc xyz: 'vi du `"`abc`"`').
