# Báo cáo bài tập cuối kỳ Nhập môn An toàn thông tin

## Bài 1

### Xây dụng hệ mật trên đường cong Elliptic cho mục đích mã hóa và chữ ký số

Em sử dụng 3 phương pháp tạo đường cong Elliptic là Barreto-Naehrig (BN), Cocks-Pinch (CP) và Dupont-Enge-Morain (DEM) được mô tả ở [\[BN05\]](https://github.com/scipr-lab/ecfactory/blob/master/references/Barreto%20Naehrig%202005%20---%20Pairing-Friendly%20Elliptic%20Curves%20of%20Prime%20Order.pdf) và [\[FST10\]](https://github.com/scipr-lab/ecfactory/blob/master/references/Freeman%20Scott%20Teske%202010%20---%20A%20Taxonomy%20of%20Pairing-Friendly%20Elliptic%20Curves.pdf). Để sinh đường cong, em sử dụng thư viện [ecfactory](https://github.com/scipr-lab/ecfactory/).

Các đường cong $E$ được em xây dựng có số điểm là số nguyên tố có độ dài _480 bit_. Ba đường cong em xây dựng được lưu ở 3 file [bn_elliptic_curve](/part1/inputs/bn_elliptic_curve.txt), [cp_elliptic_curve](/part1/inputs/cp_elliptic_curve.txt) và [dem_elliptic_curve](/part1/inputs/dem_elliptic_curve.txt). Cấu trúc các file này là như sau:

- Dòng đầu tiên chứa $p$ là số nguyên tố định nghĩa lên trường $Z_p$, trên đó đường cong elliptic $E$ được định nghĩa,
- Dòng thứ 2 chứa $a$ và $b$ là hệ số của đường cong $E$. Tức là $E$ có phương trình $y^2 = x^3 + ax + b$,
- Dòng cuối cùng chứa số điểm $n$ trên đường cong.

### Xây dụng hệ mật RSA có độ dài khóa 3072 bit cho mục đích mã hóa và chữ ký số

### Xâu dựng hệ mật El Gamal có độ dài khóa 1023 bit cho mục đích mã hóa và chũ ký số
