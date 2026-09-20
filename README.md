# BÀI TẬP 2: PHÂN TÍCH TÍN HIỆU CẢM BIẾN LOAD CELL & HX711

## 1. Phần cứng sử dụng

* **Cảm biến lực:** Load Cell thanh 5kg (cầu điện trở Wheatstone toàn phần).

* **Mạch chuyển đổi ADC:** Module ADC 24-bit HX711 tích hợp bộ khuếch đại vi sai $\text{PGA} = 128$.

* **Vi điều khiển:** Arduino Uno R3.

* **Phụ kiện:** Dây cáp USB nạp chương trình, dây cắm test board, ốc vít M4/M5 và vòng đệm gá dầm công-xôn.

## 2. Sơ đồ đấu nối dây

Chi tiết sơ đồ mắc dây được minh họa trong file **`Wiring_diagram.jpg`**.

### Bảng đối chiếu chân nối nhanh:

| Từ thiết bị | Chân / Màu dây | Nối sang thiết bị | Chân nhận | Chức năng | 
 | ----- | ----- | ----- | ----- | ----- | 
| **Load Cell 5kg** | Dây Đỏ | **HX711** | `E+` | Cấp nguồn kích thích dương ($+5\text{V}$) | 
|  | Dây Đen |  | `E-` | Nối mass kích thích ($\text{GND}$) | 
|  | Dây Trắng |  | `A-` | Tín hiệu vi sai âm ($V_{in-}$) | 
|  | Dây Xanh lá |  | `A+` | Tín hiệu vi sai dương ($V_{in+}$) | 
| **Module HX711** | `VCC` | **Arduino Uno R3** | `5V` | Nguồn nuôi module | 
|  | `GND` |  | `GND` | Nối đất chung | 
|  | `DT` |  | `D3` | Dữ liệu nối tiếp (Data Out) | 
|  | `SCK` |  | `D2` | Xung nhịp chốt mẫu (Clock) | 

> **Lưu ý:** Nếu khi đè tải lên thanh cân mà giá trị đọc được tụt âm sâu hơn, bạn chỉ cần đổi chéo 2 dây **Trắng** và **Xanh lá** ở chân `A-` và `A+`.

## 3. Cấu trúc tệp tin trong dự án

```
├── Wiring_diagram.jpg          # Sơ đồ minh họa đấu nối phần cứng
├── loadcell_adc_sketch.ino     # Code Arduino đọc ADC 24-bit từ HX711
├── loadcell_data.csv           # File lưu trữ chuỗi dữ liệu thực nghiệm
├── data_analyzer.py            # Script Python phân tích SQNR và hạ tần số lấy mẫu
└── README.md                   # Hướng dẫn chi tiết dự án

```

## 4. Hướng dẫn thực hiện từng bước

### Bước 1: Đấu nối phần cứng

* Thực hiện đấu dây theo bảng hướng dẫn trên hoặc file `Wiring_diagram.jpg`.

* Cố định một đầu thanh Load Cell xuống mặt phẳng đế, để đầu còn lại lơ lửng làm đĩa đặt tải.

### Bước 2: Nạp code vi điều khiển

1. Mở file `loadcell_adc_sketch.ino` bằng phần mềm **Arduino IDE**.

2. Cài đặt thư viện **HX711** (tác giả *Bogdan Necula*) thông qua mục `Library Manager`.

3. Chọn đúng cổng COM và nạp chương trình vào bo mạch Arduino Uno R3.

4. Mở **Serial Monitor** với tốc độ Baudrate `9600` để kiểm tra luồng dữ liệu trích xuất dạng `timestamp_ms,raw_adc`.

### Bước 3: Thu thập dữ liệu thực tế

* Thu nhận các giá trị đo từ cổng Serial và lưu thành file `loadcell_data.csv` cùng thư mục dự án.

* Đảm bảo kịch bản đo trải qua đủ 4 pha:

  * **0 – 3s:** Để yên cân (đo nhiễu nền tĩnh không tải).

  * **3 – 4s:** Đặt nhanh hoặc thả nhẹ vật nặng lên đĩa cân (pha quá độ).

  * **4 – 13s:** Giữ yên vật trên cân (pha tĩnh có tải).

  * **13 – 16s:** Nhấc vật ra khỏi đĩa cân (pha dỡ tải).

### Bước 4: Xử lý và phân tích số liệu

Cài đặt các thư viện Python cần thiết:

```
pip install numpy pandas matplotlib

```

Chạy script phân tích:

```
python data_analyzer.py

```

Chương trình sẽ tự động:

* Khử Zero-offset và chuẩn hóa tín hiệu về đoạn $[0, 1]$.

* Lượng tử hóa tín hiệu từ $4\text{ bits}$ đến $16\text{ bits}$ và tính bảng $\text{SQNR}$ thực nghiệm so với công thức lý thuyết $6.02b + 1.76\text{ dB}$.

* Mô phỏng hạ tần số lấy mẫu (Decimation) và vẽ 3 đồ thị trực quan phục vụ báo cáo.