# Proyek Analisis Data: E-Commerce Public Dataset

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis dataset publik e-commerce dengan menggunakan teknik analisis data, visualisasi, dan clustering. Melalui analisis ini, kita akan mencari pola atau tren dalam data transaksi serta mengidentifikasi area untuk meningkatkan pengalaman pelanggan.

## Struktur Proyek
- **data/**: Folder yang berisi dataset yang digunakan dalam analisis.
  - `day.csv`: Dataset harian.
  - `hour.csv`: Dataset per jam.
- **notebooks/**: Folder yang berisi Jupyter Notebook untuk analisis.
- **dashboard.py**: Skrip untuk menjalankan dashboard visualisasi.
- **requirements.txt**: Daftar paket yang diperlukan untuk menjalankan proyek.
- **README.md**: Dokumen ini.

## Pertanyaan Bisnis
1. Apa pola atau tren dalam data transaksi yang menunjukkan area-area untuk peningkatan pengalaman pelanggan?
2. Berdasarkan segmentasi pelanggan yang didapat dari clustering, bagaimana kita bisa menawarkan produk dan layanan yang lebih tepat sasaran untuk setiap segmen pelanggan?

## Instalasi
Untuk menjalankan proyek ini, Anda perlu menginstal paket yang tercantum di `requirements.txt`. Anda dapat menggunakan pip untuk menginstalnya:

```bash
pip install -r requirements.txt

### Daftar Paket
- Paket / Library yang digunakan dalam proyek.

### Daftar Paket
- `pandas==1.5.3`
- `numpy==1.23.5`
- `matplotlib==3.7.0`
- `seaborn==0.12.2`
- `scikit-learn==1.2.2`
- `plotly==5.11.0`
- `streamlit==1.16.0`
- `altair==4.1.0`


## Analisis Data
Analisis dilakukan melalui beberapa tahap, sebagai berikut:

1. **Import Library**: Memuat semua paket yang diperlukan.
2. **Data Wrangling**: Mengumpulkan dan membersihkan data dari dataset yang tersedia.
3. **Exploratory Data Analysis (EDA)**: Melakukan analisis eksploratif untuk memahami data.
4. **Clustering**: Menggunakan teknik clustering untuk mengelompokkan pelanggan berdasarkan perilaku mereka.
5. **Visualisasi**: Membuat visualisasi untuk menampilkan hasil analisis dan memberikan wawasan lebih lanjut.


## Visualisasi
Visualisasi dilakukan dengan menggunakan `matplotlib` dan `seaborn` untuk menggambarkan hubungan antara variabel, seperti suhu dan jumlah penyewaan.

## Menjalankan Dashboard
Untuk menjalankan dashboard visualisasi, gunakan perintah berikut:

```bash
cd dashboard
streamlit run dashboard.py

## Penutup
Proyek ini memberikan wawasan yang berharga mengenai perilaku pelanggan dan dapat digunakan untuk meningkatkan pengalaman pelanggan dalam e-commerce. Analisis dan visualisasi yang dilakukan diharapkan dapat membantu dalam pengambilan keputusan bisnis yang lebih baik.
