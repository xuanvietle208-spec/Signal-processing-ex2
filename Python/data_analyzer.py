import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('loadcell_data.csv')

t = df['timestamp_ms'].values
adc = df['raw_adc'].values

# Trừ điểm 0 (lấy trung bình 20 mẫu đầu lúc chưa đặt vật)
offset = np.mean(adc[:20])
x = adc - offset

# Đổi dấu để khi đặt tải thì tín hiệu đi lên (dương)
if np.mean(x[40:100]) < 0:
    x = -x

# Chuẩn hóa tín hiệu về đoạn từ 0 đến 1 cho dễ lượng tử hóa
x_min = np.min(x)
x_max = np.max(x)
x_norm = (x - x_min) / (x_max - x_min)

# Tính chu kỳ trích mẫu Ts và tần số lấy mẫu fs thực tế
dt = t[1:] - t[:-1]
Ts = np.mean(dt) / 1000.0
fs = 1.0 / Ts
print(f"Tan so lay mau thuc te fs = {fs:.2f} Hz")

# Lượng tử hóa và tính SQNR theo số bits
bits = []
sqnr_thuc_te = []
sqnr_ly_thuyet = []

# Khảo sát từ 4 bit đến 16 bit
for b in range(4, 17):
    # Số mức lượng tử
    L = 2**b
    delta = 1.0 / (L - 1)  # Bước lượng tử
    
    # Lượng tử hóa bằng cách làm tròn
    xq = np.round(x_norm / delta) * delta
    
    # Lỗi lượng tử e[n]
    e = x_norm - xq
    
    # Tính công suất tín hiệu và công suất nhiễu
    p_signal = np.mean(x_norm**2)
    p_noise = np.mean(e**2)
    
    # Tính SQNR thực tế (dB)
    sqnr = 10 * np.log10(p_signal / p_noise)
    
    # SQNR lý thuyết: 6.02*b + 1.76
    sqnr_theory = 6.02 * b + 1.76
    
    bits.append(b)
    sqnr_thuc_te.append(sqnr)
    sqnr_ly_thuyet.append(sqnr_theory)
    
    print(f"Bit: {b:2d} | SQNR thuc te: {sqnr:6.2f} dB | SQNR ly thuyet: {sqnr_theory:6.2f} dB")

# Vẽ đồ thị
thoi_gian = (t - t[0]) / 1000.0

plt.figure(figsize=(10, 10))

# So sánh tín hiệu gốc và khi bị giảm xuống 4 bit
plt.subplot(3, 1, 1)
delta_4 = 1.0 / (2**4 - 1)
xq_4 = np.round(x_norm / delta_4) * delta_4
plt.plot(thoi_gian, x_norm, 'b-', label='Tin hieu goc (ADC 24-bit)')
plt.step(thoi_gian, xq_4, 'r--', label='Sau luong tu 4-bit (16 muc)', where='mid')
plt.title('Hinh 1: Meo dang bac thang khi giam so bit xuong 4-bit')
plt.xlabel('Thoi gian (s)')
plt.ylabel('Bien do')
plt.legend()
plt.grid(True)

# Đồ thị SQNR thực tế vs lý thuyết
plt.subplot(3, 1, 2)
plt.plot(bits, sqnr_thuc_te, 'bo-', label='SQNR Thuc te')
plt.plot(bits, sqnr_ly_thuyet, 'r--', label='SQNR Ly thuyet (6.02b + 1.76)')
plt.title('Hinh 2: Do thi SQNR tang theo so bit')
plt.xlabel('So bit (b)')
plt.ylabel('SQNR (dB)')
plt.legend()
plt.grid(True)

# Thay đổi tần số lấy mẫu
plt.subplot(3, 1, 3)
idx_zoom = np.where((thoi_gian >= 2.0) & (thoi_gian <= 6.0))[0]

plt.plot(thoi_gian[idx_zoom], x_norm[idx_zoom], 'k-o', label=f'Goc fs ~ {fs:.1f} Hz')
plt.plot(thoi_gian[idx_zoom[::2]], x_norm[idx_zoom[::2]], 'b.--', label=f'Giam 2 lan fs ~ {fs/2:.1f} Hz')
plt.plot(thoi_gian[idx_zoom[::4]], x_norm[idx_zoom[::4]], 'rs--', label=f'Giam 4 lan fs ~ {fs/4:.1f} Hz')
plt.title('Hinh 3: Thay doi tan so lay mau (Zoom doan dat tai)')
plt.xlabel('Thoi gian (s)')
plt.ylabel('Bien do')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()