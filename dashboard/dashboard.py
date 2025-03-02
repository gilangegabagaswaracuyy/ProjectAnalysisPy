import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
import os

# Judul Dashboard
st.title("Dashboard Analisis Data E-Commerce")

# Memuat dataset dengan caching
@st.cache_resource
def load_data():
    day_file = pd.read_csv("data/day.csv")
    hour_file = pd.read_csv("data/day.csv")
    
    # Cek apakah file ada
    if not os.path.exists(day_file):
        st.error(f"File tidak ditemukan: {day_file}")
        return None, None  # Mengembalikan None jika file tidak ditemukan
    
    if not os.path.exists(hour_file):
        st.error(f"File tidak ditemukan: {hour_file}")
        return None, None  # Mengembalikan None jika file tidak ditemukan
    
    try:
        df_day = pd.read_csv(day_file)
        df_hour = pd.read_csv(hour_file)
    except pd.errors.EmptyDataError:
        st.error("File CSV kosong.")
        return None, None
    except pd.errors.ParserError:
        st.error("Kesalahan saat parsing file CSV.")
        return None, None
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")
        return None, None
    
    return df_day, df_hour

df_day, df_hour = load_data()

# Jika data tidak berhasil dimuat, hentikan eksekusi lebih lanjut
if df_day is None or df_hour is None:
    st.stop()

# Menampilkan data
if st.checkbox("Tampilkan Data Hari"):
    st.subheader("Data Hari")
    st.write(df_day.head())  # Menampilkan 5 baris pertama dari dataset hari

if st.checkbox("Tampilkan Data Jam"):
    st.subheader("Data Jam")
    st.write(df_hour.head())  # Menampilkan 5 baris pertama dari dataset jam

# RFM Analysis
st.subheader("Analisis RFM")

# Menghitung RFM
try:
    df_day['date'] = pd.to_datetime(df_day['dteday'])  # Mengkonversi kolom 'dteday' menjadi format datetime
    rfm = df_day.groupby('instant').agg({
        'date': 'max',
        'cnt': 'sum'
    }).reset_index()  # Menghitung total penyewaan per 'instant'

    # Menghitung Recency
    rfm['Recency'] = (df_day['date'].max() - rfm['date']).dt.days  # Menghitung jumlah hari sejak pembelian terakhir
    rfm.rename(columns={'date': 'LastPurchase', 'cnt': 'Monetary'}, inplace=True)  # Mengganti nama kolom
    rfm['Frequency'] = df_day.groupby('instant')['cnt'].count().values  # Menghitung frekuensi penyewaan
except Exception as e:
    st.error(f"Terjadi kesalahan saat menghitung RFM: {e}")

# KMeans Clustering
try:
    imp = SimpleImputer(strategy='mean')  # Menggunakan imputasi rata-rata untuk menangani nilai yang hilang
    X_imputed = imp.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])  # Mengisi nilai yang hilang
    kmeans = KMeans(n_clusters=4, n_init=10, random_state=0)  # Menginisialisasi KMeans dengan 4 kluster
    clusters = kmeans.fit_predict(X_imputed)  # Menerapkan KMeans pada data
    rfm['Cluster'] = clusters  # Menambahkan hasil kluster ke DataFrame RFM
except Exception as e:
    st.error(f"Terjadi kesalahan saat melakukan clustering: {e}")

# Menampilkan hasil clustering
st.write(rfm.head())  # Menampilkan 5 baris pertama dari DataFrame RFM yang sudah berisi kluster

# Visualisasi Hasil Clustering RFM
st.subheader("Visualisasi Hasil Clustering RFM")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Recency', y='Monetary', hue='Cluster', data=rfm, palette='Set1', ax=ax)
plt.title('Hasil Clustering RFM')  # Judul grafik
plt.xlabel('Recency')  # Label sumbu x
plt.ylabel('Monetary')  # Label sumbu y
plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')  # Menambahkan legenda
st.pyplot(fig)  # Menampilkan grafik

# Analisis Pola Transaksi
st.subheader("Pola atau Tren dalam Data Transaksi")
st.write("""
Dengan menganalisis data penyewaan, kita dapat mengidentifikasi area-area untuk peningkatan pengalaman pelanggan. 
Kami akan memvisualisasikan jumlah penyewaan berdasarkan suhu dan waktu untuk memahami tren ini.
""")

# Visualisasi Suhu dan Penyewaan
st.subheader("Hubungan antara Suhu dan Jumlah Penyewaan")
# Menambahkan slider untuk memilih rentang suhu
temp_range = st.slider("Pilih rentang suhu:", min_value=float(df_hour['temp'].min()), max_value=float(df_hour['temp'].max()), value=(0.00, 1.0),)
# Filter data berdasarkan rentang suhu yang dipilih
filtered_df_hour = df_hour[(df_hour['temp'] >= temp_range[0]) & (df_hour['temp'] <= temp_range[1])]

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', data=filtered_df_hour, ax=ax2)
plt.title('Hubungan antara Suhu dan Jumlah Penyewaan')  # Judul grafik
plt.xlabel('Suhu')  # Label sumbu x
plt.ylabel('Jumlah Penyewaan')  # Label sumbu y
st.pyplot(fig2)  # Menampilkan grafik

# Analisis Lanjutan berdasarkan Kluster
st.subheader("Analisis Produk dan Layanan Berdasarkan Kluster")
for cluster in range(4):
    st.write(f"### Kluster {cluster}")
    cluster_data = rfm[rfm['Cluster'] == cluster]  # Mengambil data untuk kluster tertentu
    
    st.write("Rata-rata Recency, Frequency, dan Monetary untuk Kluster ini:")
    st.write(cluster_data[['Recency', 'Frequency', 'Monetary']].mean())  # Menampilkan rata-rata RFM untuk kluster ini

    st.write("Visualisasi RFM untuk Kluster ini:")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Recency', y='Monetary', data=cluster_data, ax=ax3)
    plt.title(f'RFM Kluster {cluster}')  # Judul grafik
    plt.xlabel('Recency')  # Label sumbu x
    plt.ylabel('Monetary')  # Label sumbu y
    st.pyplot(fig3)  # Menampilkan grafik

# Kesimpulan
st.subheader("Kesimpulan")
st.write("""
- Analisis RFM menunjukkan segmentasi pelanggan berdasarkan perilaku pembelian mereka.
- Pola penyewaan berdasarkan suhu dan waktu dapat memberikan wawasan untuk meningkatkan pengalaman pelanggan.
- Berdasarkan hasil clustering, kita dapat menawarkan produk dan layanan yang lebih sesuai untuk setiap segmen pelanggan.
""")
