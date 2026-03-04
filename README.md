# TruthSeeker - Xác Thực Tự Động Các Phát Ngôn Về Khí Hậu Bằng Dữ Liệu Thực Tế và Mô Hình Ngôn Ngữ Lớn

**TruthSeeker** là một hệ thống kiểm tra tính xác thực các phát ngôn liên quan đến khí hậu sử dụng GPT-4, tranh luận đa tác nhân (Multi-Agent Debate), và dữ liệu thời gian thực từ các nguồn uy tín (NASA, NCEI). Hệ thống này giúp phát hiện thông tin sai lệch, đánh giá độ đáng tin cậy của phát ngôn, và hỗ trợ truyền thông khí hậu chính xác.

## Mục lục

- [Tính năng](#tính-năng)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Sử dụng](#sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Quy trình xác thực](#quy-trình-xác-thực)
- [API và Tích hợp](#api-và-tích-hợp)
- [Ví dụ](#ví-dụ)
- [Triển khai với Docker](#triển-khai-với-docker)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)
- [Đóng góp](#đóng-góp)
- [Liên hệ](#liên-hệ)

## Tính năng

- **Kiểm tra dữ liệu khí hậu**: Xác thực phát ngôn dựa trên dữ liệu thực tế từ NASA, NCEI và các nguồn tin uy tín
- **Multi-Agent Debate**: Các agent (ủng hộ, phản đối, trung lập) tranh luận để đạt được kết luận khách quan
- **Phân tích tâm lý**: Đánh giá cảm xúc, ý định và rủi ro lan truyền thông tin sai lệch
- **Đánh giá toàn diện**: Cung cấp mức độ tin cậy, giải thích chi tiết, các bằng chứng hỗ trợ và câu hỏi bổ sung
- **Vectorstore**: Tích hợp ChromaDB để lưu trữ và tìm kiếm dữ liệu khí hậu hiệu quả
- **API OpenAI**: Sử dụng GPT-4 để phân tích ngôn ngữ tự nhiên và lập luận

## Kiến trúc hệ thống

### Thành phần chính

```
TruthSeeker
├── Claimant (Người ủng hộ)     - Phán xét ủng hộ phát ngôn
├── Denier (Người phản đối)     - Phán xét phản đối phát ngôn
├── Neutral Agent (Agent trung lập) - Phán xét khách quan
├── Intent Analyzer              - Phân tích ý định và cảm xúc
└── Verifier (Bộ xác thực)      - Tổng hợp kết quả và đưa ra kết luận
```

### Quy trình xác thực

1. **Nhập phát ngôn** → Tiền xử lý và phân tách
2. **Trích xuất dữ liệu** → Tìm kiếm dữ liệu liên quan trong vectorstore
3. **Phân tích ý định** → Đánh giá cảm xúc, ý định lan truyền
4. **Tranh luận đa tác nhân** → Các agent đưa ra ý kiến từ các góc độ khác nhau
5. **Xác thực** → Bộ xác thực tổng hợp ý kiến và đưa ra kết luận cuối cùng
6. **Xuất kết quả** → Báo cáo chi tiết với điểm tin cậy, bằng chứng, kiến nghị

## Yêu cầu hệ thống

- **Python**: 3.12 hoặc cao hơn
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB)
- **Kết nối Internet**: Để truy cập API OpenAI, NASA, NCEI
- **Thẻ API**:
  - OpenAI API key (GPT-4)
  - NewsAPI key (tùy chọn)

### Hệ điều hành được hỗ trợ

- Windows 10/11
- macOS 12+
- Linux (Ubuntu 20.04+)

## Cài đặt

### 1. Clone repository

```bash
git clone <https://github.com/LeNguyenNhatTan Automatic-Verification-of-Climate-Claims-with-Real-Time-Data-Using-Large-Language-Models.git>
cd Automatic-Verification-of-Climate-Claims-with-Real-Time-Data-Using-Large-Language-Models
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt các phụ thuộc

```bash
pip install -r requirements.txt
```

### 4. Cấu hình biến môi trường

Tạo tệp `.env` trong thư mục gốc dự án:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEWSAPI_KEY=your_newsapi_key_here
```

## Cấu hình

### Cấu trúc thư mục

```
app/
├── main.py                 # Điểm khởi đầu ứng dụng
├── schemas.py              # Định nghĩa schema dữ liệu
├── requirements.txt        # Danh sách phụ thuộc
├── agents/
│   ├── claimant.py         # Agent ủng hộ
│   ├── verifier.py         # Bộ xác thực
│   ├── neutral_verifier.py # Bộ xác thực trung lập
│   ├── intent_sentiment.py # Phân tích ý định và cảm xúc
│   ├── truthseeker.py      # Hệ thống chính
│   └── setting.py          # Cấu hình agent
├── core/
│   ├── config.py           # Cấu hình chung
│   └── logging.py          # Logging
├── rag/
│   └── vectorstore.py      # Quản lý vectorstore
└── archive/
    └── chroma_store_*/     # ChromaDB lưu trữ
```


## Sử dụng

### Chạy ứng dụng

#### Tùy chọn 1: Chạy trực tiếp

```bash
python app/main.py
```

#### Tùy chọn 2: Chạy với Docker

```bash
docker-compose -f docker-compose.dev.yml up
```

#### Tùy chọn 3: Sử dụng script bắt đầu

```bash
# Windows
start.bat

# macOS/Linux
bash start.bat  # hoặc chỉnh sửa thành script shell
```

## Cấu trúc dữ liệu kết quả

```json
{
  "statement": "Phát ngôn đầu vào",
  "intent_analysis": {
    "sentiment": "neutral|positive|negative",
    "intent": "inform|influence|mislead",
    "misinformation_risk": "low|medium|high"
  },
  "assessments": {
    "support": {
      "reasoning": "Lập luận ủng hộ",
      "confidence": 0.0-1.0,
      "evidence": ["bằng chứng 1", "bằng chứng 2"]
    },
    "oppose": {
      "reasoning": "Lập luận phản đối",
      "confidence": 0.0-1.0,
      "evidence": ["bằng chứng 1", "bằng chứng 2"]
    },
    "neutral": {
      "reasoning": "Lập luận trung lập",
      "confidence": 0.0-1.0,
      "evidence": ["bằng chứng 1", "bằng chứng 2"]
    }
  },
  "verification": {
    "verdict": "accurate|partially_accurate|inaccurate|unclear",
    "confidence_score": 0.0-1.0,
    "explanation": "Giải thích chi tiết",
    "supporting_evidence": ["bằng chứng"],
    "additional_questions": ["câu hỏi bổ sung"]
  }
}
```

## Quy trình xác thực chi tiết

### Bước 1: Nhập và tiền xử lý
- Nhận phát ngôn từ người dùng
- Làm sạch và chuẩn hóa văn bản
- Phân tách từ khóa chính

### Bước 2: Trích xuất thông tin liên quan
- Tìm kiếm trong ChromaDB
- Lấy dữ liệu từ NASA API
- Lấy dữ liệu từ NCEI API

### Bước 3: Phân tích ý định
- Xác định cảm xúc (sentiment)
- Xác định ý định (intent)
- Đánh giá rủi ro lan truyền thông tin sai lệch

### Bước 4: Tranh luận đa tác nhân
- **Claimant (Ủng hộ)**: Lập luận ủng hộ phát ngôn
- **Verifier (Phản đối)**: Lập luận phản đối phát ngôn
- **Neutral Agent**: Lập luận khách quan

### Bước 5: Xác thực cuối cùng
- Tổng hợp các lập luận
- Tính điểm tin cậy tổng hợp
- Đưa ra kết luận (chính xác, một phần chính xác, sai lệch, không rõ)
- Đề xuất câu hỏi bổ sung

## API và Tích hợp

### OpenAI API

Dùng GPT-4 cho phân tích ngôn ngữ tự nhiên:

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### NASA API

Trích xuất dữ liệu về khí hậu:

```
https://api.nasa.gov/climate/data
```

### NCEI API

Dữ liệu khí tượng học toàn cầu:

```
https://www.ncei.noaa.gov/products/weather-global-temperature-index
```

### ChromaDB

Lưu trữ vector của tài liệu:

```python
from app.rag.vectorstore import VectorStore

vectorstore = VectorStore()
results = vectorstore.search(query, top_k=5)
```

## Liên hệ

- **GitHub Issues**: Báo cáo bugs hoặc đề xuất features
- **Email**: Liên hệ tác giả qua email

---

**Lưu ý**: Dự án này sử dụng OpenAI API, có thể phát sinh chi phí. Vui lòng kiểm tra giá của OpenAI trước khi sử dụng.

