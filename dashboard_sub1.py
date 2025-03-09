import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')
with st.sidebar:
    # Menambahkan logo perusahaan
    st.header('Project sederhana')
    st.write('Nama : Danan Rukmana')
    st.write('Gmail : gmgdanan@gmail.com')
    st.write('project analisis penyewaan sepeda')
url1 = "https://raw.githubusercontent.com/DananRukmana/DananRukmana/refs/heads/main/hour.csv"
url2 = "https://raw.githubusercontent.com/DananRukmana/DananRukmana/refs/heads/main/day.csv"
df1 = pd.read_csv('url1')
df_hour = pd.DataFrame(df1)
df2 = pd.read_csv('url2')
df_day = pd.DataFrame(df2)

jam_sibuk = df_hour.groupby('hr')['cnt'].sum()
cuaca = df_day.groupby('weathersit').cnt.sum()
day_grup = df_day.groupby('workingday')['cnt'].mean()
season_grup = df_day.groupby('season')['cnt'].mean() 
bulan_trend = df_day.groupby('mnth')['cnt'].sum()

avg_recency = df_day['dteday'].nunique()  # Misalnya, jumlah hari unik dalam dataset
avg_frequency = df_day['registered'].mean()  # Rata-rata penyewaan oleh pengguna terdaftar
avg_monetary = df_day['cnt'].mean()

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
max_date = df_day['dteday'].max()
df_rfm = df_day.groupby('dteday').agg({
    'registered': 'sum'  
}).reset_index()

df_rfm['Recency'] = (max_date - df_rfm['dteday']).dt.days
df_rfm['Frequency'] = df_rfm['registered']
df_rfm['Monetary'] = df_rfm['registered']
rfm = df_rfm[['Recency', 'Frequency', 'Monetary']]
rfm.head()


st.header('Analisis Perilaku Customer Dalam Penyewaan Sepeda Pertanggal :sparkles:')
st.subheader('Analisis penyewaan pertanggal')
col1, col2 = st.columns(2)
with col1:
     hari = 17
     st.metric(' Pada Tanggal :', hari)


with col2:
     total = jam_sibuk.values.max()
     st.metric(' Total sepeda yang disewa', total)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    jam_sibuk.index,
    jam_sibuk.values,
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks(range(0,25,1))

st.pyplot(fig)

st.subheader("Analisis Kondisi Saat Customer Melakukan Penyewaan")
col1, col2 = st.columns(2)
with col1:
     fig,ax = plt.subplots(figsize=(6,6))
     ax.pie(cuaca.values, labels=cuaca.index, autopct='%1.1f%%', colors=['green', 'yellow', 'blue'], startangle=140)
     ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
     ax.tick_params(axis='x', labelsize=35)
     ax.tick_params(axis='y', labelsize=30)
     st.pyplot(fig)

with col2:
     fig, ax = plt.subplots(figsize=(6,6))
     ax.bar(['Hari Libur', 'Hari Kerja'], day_grup, color=['green', 'blue'])
     ax.set_xlabel('Jenis Hari')
     ax.set_ylabel('Rata-rata Penyewaan Sepeda', fontsize=17)
     ax.set_title('Perbandingan Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan')
     
     st.pyplot(fig)


fig,ax = plt.subplots(figsize=(6,6))
ax.bar(['1', '2', '3', '4'], season_grup, color=['green', 'skyblue', 'orange', 'blue'])
ax.set_xlabel('Musin')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
ax.set_title('Pola Penyewaan Sepeda per Musim')
st.pyplot(fig)

    
st.subheader("Analisis Kondisi Pola Penyewaan Sepanjang Tahun") 
fig,ax = plt.subplots(figsize=(14,6))
ax.plot(bulan_trend.index, bulan_trend.values, marker='o', linewidth=2, color='b')
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penyewaan Sepeda')
ax.set_title('Tren Penyewaan Sepeda Sepanjang Tahun')
ax.set_xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
st.pyplot(fig)     

st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)

with col1:
     avg_recency = df_day['dteday'].nunique()
     st.metric("Average Recency (days)", value=avg_recency)

with col2:
     avg_frequency = round(df_day['registered'].mean(), 2)
     st.metric("Average Frequency", value=avg_frequency)

with col3:
     avg_frequency = format_currency(df_day['cnt'].mean(), "AUD", locale='es_CO') 
     st.metric("Average Monetary", value=avg_frequency)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(rfm['Recency'], bins=20, kde=True, ax=axes[0], color='blue')
axes[0].set_title('Recency')
axes[0].set_xlabel('Hari Sejak Terakhir Menyewa')
axes[0].set_ylabel('Jumlah Penyewa')
sns.histplot(rfm['Frequency'], bins=20, kde=True, ax=axes[1], color='green')
axes[1].set_title('Frequency')
axes[1].set_xlabel('Jumlah Transaksi')
axes[1].set_ylabel('Jumlah Penyewa')
sns.histplot(rfm['Monetary'], bins=20, kde=True, ax=axes[2], color='red')
axes[2].set_title('Monetary')
axes[2].set_xlabel('Total Sepeda Disewa')
axes[2].set_ylabel('Jumlah Penyewa')
st.pyplot(fig)

st.caption('Danan Rukmana / 08 03 2025')

