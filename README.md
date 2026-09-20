# BÀI TẬP 2: PHÂN TÍCH TÍN HIỆU CẢM BIẾN LOAD CELL & HX711

## 1. Phần cứng sử dụng

* **Cảm biến lực:** Load Cell thanh 5kg (cầu điện trở Wheatstone toàn phần).
* **Mạch chuyển đổi ADC:** Module ADC 24-bit HX711 tích hợp bộ khuếch đại vi sai $\text{PGA} = 128$.
* **Vi điều khiển:** Arduino Uno R3.
* **Phụ kiện:** Cáp USB kết nối máy tính, dây cắm breadboard, ốc vít gá dầm công-xôn.

## 2. Sơ đồ đấu nối dây

Chi tiết sơ đồ nối dây xem trong file **`Arduino/Wiring_diagram.jpg`**.

### Bảng đối chiếu chân nối:

| Từ thiết bị | Chân / Màu dây | Nối sang thiết bị | Chân nhận | Chức năng |
| :--- | :---: | :--- | :---: | :--- |
| **Load Cell 5kg** | Dây Đỏ | **HX711** | `E+` | Cấp nguồn kích thích dương ($+5\text{V}$) |
| | Dây Đen | | `E-` | Nối mass kích thích ($\text{GND}$) |
| | Dây Trắng | | `A-` | Tín hiệu vi sai âm ($V_{in-}$) |
| | Dây Xanh lá | | `A+` | Tín hiệu vi sai dương ($V_{in+}$) |
| **Module HX711** | `VCC` | **Arduino Uno R3** | `5V` | Nguồn nuôi module |
| | `GND` | | `GND` | Nối đất chung |
| | `DT` | | `D3` | Tín hiệu dữ liệu nối tiếp (Data Out) |
| | `SCK` | | `D2` | Xung nhịp chốt mẫu (Clock) |

> **Lưu ý:** Nếu khi đè tải lên thanh cân mà giá trị số nguyên ADC bị tụt âm sâu hơn, chỉ cần đổi chéo 2 dây **Trắng** và **Xanh lá** ở chân `A-` và `A+` của module HX711.

---

## 3. Cấu trúc tệp tin trong dự án

```
├── Arduino/
│   ├── Wiring_diagram.jpg          # Sơ đồ minh họa đấu nối phần cứng
│   └── loadcell_adc_sketch.ino     # Chương trình Arduino đọc ADC 24-bit từ HX711
├── Python/
│   ├── loadcell_data.csv           # Dữ liệu thực nghiệm thu thập từ cổng Serial
│   └── data_analyzer.py            # Script phân tích SQNR và hạ tần số lấy mẫu
└── README.md                       # Hướng dẫn chi tiết dự án
```

---

## 4. Hướng dẫn thực hiện từng bước

### Bước 1: Đấu nối phần cứng
* Thực hiện đấu dây theo sơ đồ trong file `Arduino/Wiring_diagram.jpg`.
* Bắt chặt 2 ốc cố định một đầu thanh Load Cell xuống bàn/tấm đế, để đầu còn lại treo lơ lửng chịu tải.

### Bước 2: Nạp code vi điều khiển
1. Mở file `Arduino/loadcell_adc_sketch.ino` bằng **Arduino IDE**.
2. Cài đặt thư viện **HX711** (tác giả *Bogdan Necula*) từ `Library Manager`.
3. Chọn đúng bo mạch `Arduino Uno` và cổng COM tương ứng rồi nhấn **Upload**.
4. Mở **Serial Monitor** (Baudrate `9600`) để kiểm tra luồng dữ liệu xuất dạng `timestamp_ms,raw_adc`.

### Bước 3: Thu thập dữ liệu thực tế
* Lưu dữ liệu đọc từ cổng Serial vào file `Python/loadcell_data.csv`.
* Kịch bản đo thực hiện trong khoảng 16 giây:
  * **0 – 3s:** Giữ yên cân (thu mức nền Zero-offset không tải).
  * **3 – 4s:** Đặt nhanh hoặc thả nhẹ vật nặng lên cân (pha quá độ).
  * **4 – 13s:** Giữ nguyên vật trên cân (pha tĩnh có tải).
  * **13 – 16s:** Nhấc vật ra khỏi đĩa cân (pha dỡ tải).

### Bước 4: Xử lý và phân tích số liệu
Di chuyển vào thư mục `Python` và cài đặt các thư viện cần thiết:
```bash
cd Python
pip install numpy pandas matplotlib
```

Chạy script phân tích:
```bash
python data_analyzer.py
```

Chương trình sẽ tự động:
* Khử Zero-offset và chuẩn hóa tín hiệu về thang đo $[0, 1]$.
* Lượng tử hóa đều từ $4\text{ bits}$ đến $16\text{ bits}$, tính toán bảng $\text{SQNR}$ thực nghiệm so sánh với lý thuyết ($6.02b + 1.76\text{ dB}$).
* Mô phỏng hạ tần số lấy mẫu (Decimation) và vẽ 3 đồ thị báo cáo dạng sóng, lỗi lượng tử và mất mát thông tin xung va đập.