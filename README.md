# Automatic Verification of Climate Claims with Real-Time Data Using Large Language Models

## Giới thiệu

Đây là framework kiểm tra tính xác thực các phát ngôn liên quan đến khí hậu, sử dụng GPT-4 và mô hình tranh luận đa tác nhân, tích hợp dữ liệu thời gian thực từ các nguồn uy tín (NASA, NCEI) nhằm phát hiện thông tin sai lệch và hỗ trợ truyền thông khí hậu chính xác.

## Tính năng chính

- Kiểm tra phát ngôn về khí hậu dựa trên dữ liệu thực tế từ NASA và NCEI.
- Sử dụng multi-agent debate: các "Claimant" (ủng hộ, phản đối, GPT-4) tranh luận và một "Verifier" tổng hợp kết quả.
- Phân tích cảm xúc và ý định của phát ngôn để đánh giá nguy cơ lan truyền thông tin sai lệch.
- Đánh giá mức độ tin cậy, giải thích chi tiết, và đề xuất câu hỏi bổ sung nếu cần.

## Cấu trúc thư mục

```
README.md
requirement.txt
TruthSeeker-HNHV-2025-final.docx
TruthSeeker.ipynb
archive/
  chroma_store_nasa/
    chroma.sqlite3
    <id>/
      data_level0.bin
      header.bin
      length.bin
      link_lists.bin
  chroma_store_ncei/
    chroma.sqlite3
    <id>/
      data_level0.bin
      header.bin
      length.bin
      link_lists.bin
```

- `TruthSeeker.ipynb`: Notebook chính chứa toàn bộ logic kiểm tra phát ngôn.
- `archive/chroma_store_nasa`, `archive/chroma_store_ncei`: Lưu trữ vectorstore dữ liệu NASA và NCEI.
- `requirement.txt`: Danh sách thư viện cần thiết.

## Cài đặt

1. Tạo môi trường Python 3.12 (khuyến nghị).
2. Cài đặt các thư viện:
   ```sh
   pip install -r requirement.txt
   ```

## Sử dụng

1. Mở `TruthSeeker.ipynb` bằng Jupyter hoặc VS Code.
2. Thiết lập API key cho OpenAI và NewsAPI (thay thế biến `your_openai` và `NEWSAPI_KEY` trong notebook).
3. Chạy các cell để khởi tạo vectorstore, phân tích phát ngôn, và nhận kết quả kiểm tra.

Ví dụ kiểm tra phát ngôn:

```python
statement = "Of course the climate is changing. It always has. It always will"
result = truthseekers(statement)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## Quy trình kiểm tra

- **Claimant Assess**: Mỗi agent (Support, Denier, GPT-4) đánh giá phát ngôn dựa trên dữ liệu và kiến thức chuyên môn.
- **Verifier**: Tổng hợp các đánh giá, xác định mức độ tin cậy, rủi ro, và đề xuất câu hỏi bổ sung nếu cần.
- **Neutral Verifier**: Đánh giá cuối cùng, đảm bảo tính khách quan và tổng hợp các ý kiến.

## Yêu cầu hệ thống

- Python >= 3.12
- Kết nối Internet để truy cập API và tải mô hình.

## Tài liệu tham khảo

- [LangChain](https://python.langchain.com/)
- [OpenAI API](https://platform.openai.com/)
- [Transformers](https://huggingface.co/docs/transformers/index)
- [ChromaDB](https://docs.trychroma.com/)

## Đóng góp & Liên hệ

Vui lòng liên hệ tác giả hoặc tạo issue trên repository để báo lỗi hoặc đề xuất cải tiến.

---

