# BÁO CÁO BÀI TẬP: TÍNH TOÁN VÀ PHÂN CỤM ĐIỂM SỐ SINH VIÊN BẰNG K-MEANS

**Sinh viên thực hiện:** Lương Hoàng Việt  
**Mã sinh viên:** K225480106073  
**Lớp:** 58KTP
**Trường:** Đại học Kỹ thuật Công nghiệp - Đại học Thái Nguyên (TNUT)  

---

## 1. Mục tiêu bài toán
Mục tiêu của bài tập là xây dựng một chương trình tự động đọc dữ liệu điểm thi của sinh viên từ file Excel/CSV (`BangDiem58KTP.csv`), tiến hành làm sạch dữ liệu, tính toán điểm trung bình tích lũy (GPA) dựa trên số tín chỉ của từng môn học. Sau đó, ứng dụng thuật toán học máy không giám sát **K-Means Clustering** để tự động phân nhóm học lực của sinh viên thành 3 cụm khác nhau và trực quan hóa kết quả để phục vụ công tác thống kê, đánh giá học lực một cách trực quan, chính xác.

## 2. Công cụ và Thư viện sử dụng
Chương trình được phát triển bằng ngôn ngữ **Python**, sử dụng các thư viện phân tích và khoa học dữ liệu chuyên dụng:
* **Pandas & NumPy:** Đọc, làm sạch, trích xuất ma trận điểm và xử lý tính toán cấu trúc dữ liệu.
* **Scikit-Learn (sklearn):** Triển khai mô hình học máy K-Means phân cụm dữ liệu.
* **Matplotlib & Seaborn:** Trực quan hóa dữ liệu bằng các biểu đồ thống kê chuyên nghiệp cho báo cáo.

## 3. Quy trình thực hiện

### Bước 1: Tiền xử lý dữ liệu (Data Preprocessing)
* Đọc dữ liệu đầu vào từ file `BangDiem58KTP.csv`.
* Trích xuất các dải thông tin cần thiết từ file: Mã số sinh viên (MSSV), Họ và tên, Số tín chỉ tương ứng với từng môn học và Ma trận điểm thi.
* Làm sạch dữ liệu điểm: Xử lý định dạng dấu phẩy `,` thành dấu chấm `.` để tương thích với kiểu số thực (`float`) trong Python và loại bỏ các giá trị trống, lỗi (`NaN`).

### Bước 2: Tính toán GPA
Chương trình duyệt qua danh sách điểm của từng sinh viên, tiến hành đối chiếu với mảng tín chỉ tương ứng. Căn cứ vào các môn học có điểm số và tín chỉ hợp lệ, GPA được tính theo công thức trung bình cộng có trọng số:

$$\text{GPA} = \frac{\sum (\text{Điểm môn học} \times \text{Số tín chỉ})}{\sum \text{Số tín chỉ}}$$

Kết quả GPA của từng sinh viên được làm tròn đến 2 chữ số thập phân và lưu trữ vào một DataFrame mới, loại bỏ các dòng bị thiếu dữ liệu.

### Bước 3: Áp dụng thuật toán K-Means Clustering
* Sử dụng mô hình `KMeans` với tham số `n_clusters=3` để chia sinh viên thành 3 nhóm học lực. Tham số `random_state=42` và `n_init=10` được cấu hình để đảm bảo kết quả phân cụm đồng nhất và tối ưu qua các lần chạy.
* Do thuật toán K-Means đánh nhãn ngẫu nhiên (0, 1, 2), chương trình đã xử lý sắp xếp và gán lại tên nhóm dựa trên tọa độ tâm cụm (`cluster_centers_`) theo thứ tự tăng dần của điểm GPA. Các nhóm được ánh xạ một cách logic:
    * **Nhóm 1:** Phân khúc sinh viên có GPA thấp nhất.
    * **Nhóm 2:** Phân khúc sinh viên có GPA trung bình.
    * **Nhóm 3:** Phân khúc sinh viên có GPA cao nhất.

### Bước 4: Kết xuất kết quả và Thống kê chi tiết
Danh sách sinh viên sau khi phân cụm được sắp xếp theo thứ tự điểm GPA giảm dần và xuất ra file `KetQua_PhanCum_KMeans.csv` phục vụ việc lưu trữ. Đồng thời, chương trình sử dụng phương thức `groupby` của Pandas để kết xuất bảng thống kê chi tiết của từng cụm lên terminal bao gồm: Số lượng thành viên, GPA nhỏ nhất, GPA lớn nhất và GPA trung bình.

| Nhóm Phân Cụm | Số Lượng Sinh Viên | Điểm GPA Thấp Nhất (Min) | Điểm GPA Cao Nhất (Max) | Điểm GPA Trung Bình (Mean) |
| :--- | :---: | :---: | :---: | :---: |
| **Nhóm 1** | 19 | 1.88 | 2.50 | 2.32 |
| **Nhóm 2** | 20 | 2.53 | 2.87 | 2.69 |
| **Nhóm 3** | 21 | 2.98 | 3.65 | 3.21 |

*(Bảng số liệu trên được kết xuất trực tiếp từ kết quả phân cụm bằng thuật toán K-Means qua file KetQua_PhanCum_KMeans.csv).*

## 4. Trực quan hóa dữ liệu (Visualization)
Để phục vụ công tác báo cáo và xây dựng slide thuyết trình một cách trực quan hơn, chương trình kết xuất đồ họa gồm 2 biểu đồ đặt cạnh nhau trên cùng một khung hình và tối ưu hóa hiển thị:

1. **Biểu đồ cột số lượng (Count Plot):** Thể hiện số lượng sinh viên tuyệt đối phân bố trong 3 nhóm (Nhóm 1, Nhóm 2, Nhóm 3). Trục tung được sử dụng cấu hình `ticker.MaxNLocator(integer=True)` để ép chỉ hiển thị số nguyên rời rạc (tránh việc chia nhỏ trục thành số thập phân như 1.5, 2.5 người), trên đỉnh mỗi cột có đính kèm nhãn số liệu cụ thể.
2. **Biểu đồ phân phối tần suất xếp chồng (Stacked Histogram & KDE):** Trực quan hóa toàn bộ phổ điểm GPA của cả khóa học. Sử dụng tùy chọn `multiple='stack'` kết hợp đường cong phân bố mật độ (`kde=True`) và trục tung số nguyên để người xem thấy rõ xu hướng tập trung điểm số và ranh giới phân tách dứt khoát giữa 3 nhóm do thuật toán K-Means thiết lập.

## 5. Kết luận
Chương trình đã vận hành ổn định và chính xác từ khâu tiền xử lý dữ liệu thô, thực hiện tính toán trọng số, triển khai mô hình học máy không giám sát, cho đến việc kết xuất báo cáo thống kê và trực quan hóa đồ họa. Giải pháp phân cụm K-Means đã chứng minh được tính hiệu quả cao trong việc tự động phân loại học lực dựa trên biến liên tục (GPA) mà không cần can thiệp quy tắc chấm điểm tĩnh bằng tay, giúp tiết kiệm thời gian và đảm bảo tính khách quan khoa học.
