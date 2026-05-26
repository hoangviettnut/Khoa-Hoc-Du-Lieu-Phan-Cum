import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# 1. Đọc dữ liệu từ file đã làm sạch
file_path = 'BangDiem58KTP.csv'
df = pd.read_csv(file_path, header=None)

# Trích xuất thông tin sinh viên (Từ dòng 1, 2 và từ cột 4 trở đi)
mssv_list = df.iloc[1, 4:].values
ten_sv_list = df.iloc[2, 4:].values

# Trích xuất số tín chỉ (Cột 3, từ dòng 4 trở đi)
# Chuyển đổi sang định dạng số
tin_chi = pd.to_numeric(df.iloc[4:, 3], errors='coerce').values

# Trích xuất ma trận điểm (Từ dòng 4, cột 4 trở đi)
diem_matrix = df.iloc[4:, 4:]

# 2. Tính toán GPA cho từng sinh viên
danh_sach_gpa = []

for i in range(diem_matrix.shape[1]):
    mssv = mssv_list[i]
    ten = ten_sv_list[i]
    
    # Xử lý chuỗi điểm của sinh viên (đổi dấu ',' thành '.' và ép kiểu sang float)
    diem_sv = diem_matrix.iloc[:, i].astype(str).str.replace(',', '.')
    diem_sv = pd.to_numeric(diem_sv, errors='coerce').values
    
    # Lọc các môn có cả điểm hợp lệ và có số tín chỉ
    hop_le = ~np.isnan(diem_sv) & ~np.isnan(tin_chi)
    
    if np.sum(hop_le) > 0:
        tong_tc = np.sum(tin_chi[hop_le])
        if tong_tc > 0:
            tong_diem = np.sum(diem_sv[hop_le] * tin_chi[hop_le])
            gpa = tong_diem / tong_tc
            
            danh_sach_gpa.append({
                'MSSV': mssv,
                'Họ và tên': ten,
                'GPA': round(gpa, 2)
            })

# Chuyển đổi danh sách thành DataFrame
df_gpa = pd.DataFrame(danh_sach_gpa)
df_gpa = df_gpa.dropna()

# 3. Phân cụm điểm số với K-Means
print("Đang tiến hành phân cụm K-Means thành 3 nhóm...")
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_gpa['Cluster_Raw'] = kmeans.fit_predict(df_gpa[['GPA']])

# Thuật toán K-Means đánh số nhóm ngẫu nhiên (0, 1, 2). 
# Đoạn code dưới đây để sắp xếp lại tên nhóm theo thứ tự: 
# Nhóm 1 (GPA thấp nhất) -> Nhóm 2 (GPA trung bình) -> Nhóm 3 (GPA cao nhất)
tam_cum = kmeans.cluster_centers_.flatten()
chi_so_sap_xep = np.argsort(tam_cum)
anh_xa_nhom = {chi_so_sap_xep[i]: f"Nhóm {i+1}" for i in range(3)}

df_gpa['Nhóm Phân Cụm'] = df_gpa['Cluster_Raw'].map(anh_xa_nhom)
df_gpa = df_gpa.drop(columns=['Cluster_Raw']) # Xóa cột tạm

# Sắp xếp danh sách theo điểm GPA giảm dần cho đẹp
df_gpa = df_gpa.sort_values(by='GPA', ascending=False)

# In kết quả thống kê chi tiết (CẬP NHẬT TẠI ĐÂY)
print("\n=== THỐNG KÊ CHI TIẾT TỪNG NHÓM ===")
thong_ke = df_gpa.groupby('Nhóm Phân Cụm')['GPA'].agg(
    Số_lượng='count',
    GPA_Min='min',
    GPA_Max='max',
    GPA_Trung_bình='mean'
).round(2) # Làm tròn 2 chữ số thập phân
print(thong_ke.to_string())
print("===================================\n")

# 4. Lưu ra file CSV kết quả
output_file = 'KetQua_PhanCum_KMeans.csv'
df_gpa.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"Đã lưu danh sách phân cụm vào file: {output_file}")

# ---------------------------------------------------------
# 5. TRỰC QUAN HÓA DỮ LIỆU (VISUALIZATION) DÀNH CHO BÁO CÁO
# ---------------------------------------------------------
print("\nĐang tạo biểu đồ trực quan hóa...")

# Đặt style cho biểu đồ
sns.set_theme(style="whitegrid")

# Tạo 1 khung hình (figure) chứa 2 biểu đồ cạnh nhau (1 hàng, 2 cột)
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# --- Biểu đồ 1: Số lượng sinh viên mỗi nhóm ---
sns.countplot(data=df_gpa, x='Nhóm Phân Cụm', hue='Nhóm Phân Cụm', order=['Nhóm 1', 'Nhóm 2', 'Nhóm 3'], palette='viridis', legend=False, ax=axes[0])
axes[0].set_title('Số lượng sinh viên theo từng nhóm', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Nhóm (GPA từ thấp đến cao)', fontsize=12)
axes[0].set_ylabel('Số lượng sinh viên', fontsize=12)

# Ép trục Y (số lượng) chỉ hiển thị số nguyên (1, 2, 3...)
axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# Thêm số liệu cụ thể lên trên từng cột
for p in axes[0].patches:
    axes[0].annotate(f'{int(p.get_height())}', 
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')

# --- Biểu đồ 2: Phân bố điểm GPA (Histogram) ---
# Dùng Histogram (biểu đồ tần suất) có chia màu theo nhóm, kèm đường cong phân bố (kde)
sns.histplot(data=df_gpa, x='GPA', hue='Nhóm Phân Cụm', hue_order=['Nhóm 1', 'Nhóm 2', 'Nhóm 3'], 
             palette='viridis', multiple='stack', kde=True, ax=axes[1], bins=15)

axes[1].set_title('Phân bố điểm GPA của các nhóm', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Điểm GPA', fontsize=12)
axes[1].set_ylabel('Số lượng sinh viên', fontsize=12)

# Tương tự, ép trục Y của biểu đồ phân bố chỉ hiển thị số nguyên
axes[1].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# Căn chỉnh lại khoảng cách giữa các biểu đồ và hiển thị
plt.tight_layout()

plt.savefig('BieuDo_PhanCum_GPA.png', dpi=300)

plt.show()