# LẤY DỮ LIỆU PHIM TỪ NETFLIX

Đây là một đoạn code viết bằng Python để thu thập thông tin về các bộ phim trên Netflix và lưu trữ vào cơ sở dữ liệu MongoDB. Dưới đây là mô tả chi tiết về các thành phần chính và cách sử dụng code này.

## Cài đặt

1. Cài đặt Python (phiên bản 3.6 trở lên) trên máy tính của bạn.

2. Cài đặt các gói thư viện cần thiết bằng cách chạy lệnh sau trong command line:

   ```
   pip install requests beautifulsoup4 pymongo selenium pytube
   ```

3. Tải và cài đặt trình duyệt web Chrome từ trang chủ của Chrome (https://www.google.com/chrome).

4. Tải trình điều khiển ChromeDriver phù hợp với phiên bản Chrome đã cài đặt từ trang chủ của ChromeDriver (https://sites.google.com/a/chromium.org/chromedriver/downloads). Đảm bảo trình điều khiển ChromeDriver đã được thêm vào đường dẫn hệ thống.

5. Đảm bảo bạn đã có một cơ sở dữ liệu MongoDB và đã cung cấp URL kết nối của nó.

## Cấu hình

1. Đặt các giá trị cho biến môi trường sau trong file .env hoặc thiết lập trực tiếp trong mã nguồn:

   - `MONGODB_URL`: URL kết nối đến cơ sở dữ liệu MongoDB.

2. Cấu hình thông tin xác thực B2 Cloud Storage (tùy chọn):

   - `APPLICATION_KEY_ID`: ID của khóa ứng dụng B2 Cloud Storage.
   - `APPLICATION_KEY`: Khóa ứng dụng B2 Cloud Storage.
   - `BUCKET_NAME`: Tên của bucket B2 Cloud Storage.

## Sử dụng

1. Chạy script bằng cách chạy lệnh sau trong command line:

   ```
   python get.py
   ```

2. Script sẽ thu thập thông tin về các bộ phim trên Netflix và lưu trữ chúng vào cơ sở dữ liệu MongoDB đã cấu hình.

3. Kết quả sau khi chạy script sẽ được hiển thị trên màn hình.

## Môi trường

- Python 3.6 trở lên
- Trình duyệt web Chrome
- Trình điều khiển ChromeDriver
- Cơ sở dữ liệu MongoDB

## Thông tin bổ sung

- `requests` để gửi yêu cầu HTTP và nhận phản hồi từ trang web Netflix.
- `beautifulsoup4` để phân tích cú pháp HTML và trích xuất thông tin từ trang web Netflix.
- `pymongo` để kết nối và t

ương tác với cơ sở dữ liệu MongoDB.
- `selenium` để tìm kiếm trên trang web YouTube và lấy URL của trailer.
- `pytube` để tải xuống video từ YouTube (chưa được sử dụng trong phiên bản hiện tại).
- Đoạn code có chứa các chức năng phụ trợ để thêm `_id` cho các object con và định dạng dữ liệu thành các document MongoDB.
- Đoạn code cũng có chức năng kiểm tra xem một bộ phim đã tồn tại trong cơ sở dữ liệu chưa trước khi thêm mới.

**Lưu ý**: Đảm bảo rằng bạn đã thay đổi các thông số cấu hình phù hợp trước khi chạy get.py.