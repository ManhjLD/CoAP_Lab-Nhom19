# Bài thực hành CoAP với Python
# Thông tin sinh viên

- Họ tên: Lưu Đức Mạnh
- Mã sinh viên: B23DCCN531
- Nhóm: 19
# Môi trường

- Python 3.9 trở lên (đã kiểm tra cú pháp với Python 3.11).
- Thư viện `aiocoap`.
- CoAP dùng UDP, cổng mặc định `5683`.

Cài đặt trong thư mục `CoAP_Lab`:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Mỗi bài dùng cùng cổng mặc định. Chỉ chạy một server tại một thời điểm, mở
các terminal riêng và khởi động server trước client. Server mặc định lắng
nghe trên `127.0.0.1` để chạy cùng máy với client. Khi chạy trên nhiều máy,
lấy địa chỉ IPv4 LAN của máy server (ví dụ bằng `ipconfig` trên Windows), rồi
truyền địa chỉ đó cho cả server và client. Ví dụ nếu IP server là
`192.168.1.10`:

```bash
python bai1/coap_server_bai1.py --host 192.168.1.10
python bai1/coap_client_bai1.py --server 192.168.1.10
```

Thay đường dẫn chương trình tương ứng khi chạy Bài 2 hoặc Bài 3. Cho phép UDP
cổng 5683 qua firewall khi chạy trên mạng LAN. Không dùng `0.0.0.0` làm địa
chỉ bind: transport `aiocoap` trên môi trường này không hỗ trợ bind wildcard.

## Bài 1 — Gửi và nhận thông điệp

URI: `coap://localhost:5683/iot/lab/message`

Terminal 1:

```bash
python bai1/coap_server_bai1.py
```

Terminal 2 (thay thông tin sinh viên):

```bash
python bai1/coap_client_bai1.py --student-name "Nguyen Van A" --student-id "B23DCCN001"
```

Server trả lời GET với `2.05 Content`, nhận POST và trả lời `2.04 Changed`.
Ví dụ chạy client trên máy khác:

```bash
python bai1/coap_client_bai1.py --server 192.168.1.10 --student-name "Nguyen Van A" --student-id "B23DCCN001"
```

## Bài 2 — Giám sát cảm biến

URI: `coap://localhost:5683/iot/lab/sensor01/data`

Terminal 1:

```bash
python bai2/sensor_server_bai2.py
```

Terminal 2:

```bash
python bai2/monitor_client_bai2.py
```

Server cập nhật nhiệt độ và độ ẩm mỗi 3 giây; GET trả về JSON với
`device_id`, `temperature` và `humidity` cùng Content-Format JSON. Client
truy vấn định kỳ 3 giây, hiển thị thời điểm nhận và cảnh báo khi nhiệt độ
vượt 35 °C hoặc độ ẩm thấp hơn 40%. Có thể đổi chu kỳ hoặc địa chỉ server:

```bash
python bai2/monitor_client_bai2.py --server 192.168.1.10 --interval 3
```

## Bài 3 — Điều khiển đèn và CoAP Observe

URI: `coap://localhost:5683/iot/lab/light01/status`

Mở ba terminal:

```bash
python bai3/light_server_bai3.py
```

```bash
python bai3/light_controller_bai3.py
```

```bash
python bai3/light_monitor_bai3.py
```

Nhập `ON`, `OFF` hoặc `STATUS` tại controller; `EXIT` kết thúc controller.
Monitoring client dùng CoAP Observe (`observe=0`) để nhận thông báo khi trạng
thái thực sự thay đổi, không polling GET. PUT chấp nhận JSON gồm `device_id`
và `command`; lệnh sai hoặc thiết bị không hợp lệ nhận phản hồi CoAP lỗi.

## Kết quả và minh chứng

Bài 1:

GET request received: /iot/lab/message

POST request received:
Payload: Xin chao tu CoAP Client - B23DCCN531 - Luu Duc Manh
Time: 17:12:35

Bài 2:

Terminal 1():
Sensor CoAP Server started on 192.168.1.10:5683
Resource: /iot/lab/sensor01/data
Sensor updated: 36.2 C, 36.4 %
Sensor updated: 35.2 C, 41.5 %
Sensor updated: 35.8 C, 32.5 %
Sensor updated: 27.5 C, 74.4 %
Sensor updated: 26.3 C, 76.4 %

Terminal 2():
Device: sensor01
Temperature: 26.3 C
Humidity: 76.4 %

Trang thai: Binh thuong

------------------------------

[17:23:51] Received sensor data

Device: sensor01
Temperature: 32.2 C
Humidity: 48.5 %

Trang thai: Binh thuong

------------------------------

[17:23:54] Received sensor data

Device: sensor01
Temperature: 31.5 C
Humidity: 37.0 %

CANH BAO: Do am thap

------------------------------

[17:23:57] Received sensor data

Device: sensor01
Temperature: 21.0 C
Humidity: 36.9 %

CANH BAO: Do am thap

------------------------------

[17:24:00] Received sensor data

Device: sensor01
Temperature: 29.5 C
Humidity: 32.5 %

CANH BAO: Do am thap

------------------------------

[17:24:03] Received sensor data

Device: sensor01
Temperature: 21.9 C
Humidity: 33.3 %

CANH BAO: Do am thap

------------------------------

Bài 3:

Terminal 1:
Resource: /iot/lab/light01/status

New Observe registration received

PUT request received:
Device: light01
Command: ON
Light state changed: OFF -> ON
Notify observers: ON

PUT request received:
Device: light01
Command: OFF
Light state changed: ON -> OFF
Notify observers: OFF

Terminal 2:

Nhap lenh (ON/OFF/STATUS/EXIT): ON

Sending PUT request...
Response Code: 2.04 Changed
Response: {"device_id": "light01", "status": "ON"}
Nhap lenh (ON/OFF/STATUS/EXIT): OFF

Sending PUT request...
Response Code: 2.04 Changed
Response: {"device_id": "light01", "status": "OFF"}
Nhap lenh (ON/OFF/STATUS/EXIT): STATUS

Sending GET request...
Response Code: 2.05 Content
Response: {"device_id": "light01", "status": "OFF"}
Nhap lenh (ON/OFF/STATUS/EXIT): EXIT 

Terminal 3:

[17:29:03] Initial State
Device: light01
Status: OFF

Observe registration successful. Waiting for changes...

[17:29:11] State Updated
Device: light01
Status: ON

[17:29:25] State Updated
Device: light01
Status: OFF