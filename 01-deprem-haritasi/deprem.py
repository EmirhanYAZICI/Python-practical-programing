import pandas as pd


df=pd.read_excel("deprem.xlsx")
# print(df.head()) # baslıkları alıyor.

# #veri seti hakında genel bir bilgi almak istiyorum
# print("\n Veri Seti Bilgisi")
# print(df.info()) # genel bilgi veriyor


#temel istatistiksel Özet
# print("\nTemel istatiksel Özet")
# print(df.describe())#standart sapma ve dilimlerin ozelliklerini veriyor, genel istatistiği veriyor

# # eksik veriler varmı
# print("\nEKSİK VERİ VARMI")
# print(df.isnull().sum())


# tarih ve saat sutununu birleştirme
df["TarihSaat"] = pd.to_datetime(df["Tarih"].astype(str)+ " " + df["Saat"], format='%Y.%m.%d %H:%M:%S') # birleştirme işlemi yapıcam

df.drop(["Tarih","Saat"], axis=1, inplace=True)
#birleştirme Kontrol et
#print("\nGüncellenmiş Veri Tipleri:")
#print(df["TarihSaat"]) # types ne işe yarar:


#ML ile analiz etme
#düzenleme yapma
df["ML"]= pd.to_numeric(df["ML"],errors="coerce")
# print("\nML sutnundaki eksik değerler")
#print(df["ML"].isnull().sum()) # ML nin icinde bos karakter varmı diye kontrol ediyoz
df_clean = df.dropna(subset=["ML"])# verini icinde boslu vs bosveri varsa temizliyor, cok işimize yarıyor bosluk silmek icin
# print("Temizlenmiş veri seti boyutu:",df_clean.shape) # shape bicimsel olrak bana goster demek .

import matplotlib.pyplot as plt 
import seaborn as sns

#Tarihe Göre Deprem Sayısı, sns tamamen istatiksel işlemleri yapıyor viridis ise grafiğin renk paletni belirliyor.

# plt.figure(figsize=(12,6))
# sns.countplot(data= df_clean, x= df_clean["TarihSaat"].dt.date, palette="viridis")#sayı alıcagımız icin countplot yazdık
# plt.xticks(rotation=45)
# plt.title("Günlere Göre Deprem Sayısı")
# plt.xlabel("Tarih")
# plt.ylabel("Deprem Sayısı")
# plt.tight_layout()
# plt.show()



#Depremin Buyukluk Dagılımı

# plt.figure(figsize=(8,6))
# sns.histplot(df_clean["ML"], bins=20, kde=True, color="skyBlue") #kde cizgi olmasını saglıyo grafikde
# plt.title("Depremin Büyklük Dağılımı")
# plt.xlabel("Büyüklük (ML)")
# plt.ylabel("Frekans"),
# plt.show()


#Depremin Derinlik Dağılımı

# plt.figure(figsize=(8,6))
# sns.scatterplot(data=df_clean, x="Derinlik(km)",y="ML",hue="Yer",palette="deep")
# plt.title("Derinliğine göre Deprem Büyüklükleri")
# plt.xlabel("Derinlik(km)")
# plt.ylabel("Büyüklük(ML)")
# plt.legend(bbox_to_anchor=(0.75,1), loc="upper left") # Göstergeyi (legend) grafiğin sağ dışına alır
# plt.tight_layout() # Grafik, yazılar ve göstergenin üst üste binmesini/kesilmesini önler, acıklama deme kuutdaki duzenini acıklıyoreuz ve saglıyoruz yani
# plt.show()



# Folium, Python ile etkileşimli (interaktif) haritalar oluşturmaya yarayan bir kütüphanedir. Arka planda JavaScript'in popüler harita kütüphanesi Leaflet.js'i kullanır; yani Python'da yazdığın kodla yakınlaştırıp uzaklaştırılabilen, üzerine tıklanabilen web haritaları (.html olarak) üretirsin.

# Özellikle enlem (latitude) ve boylam (longitude) verilerin varsa (örneğin deprem merkez üsleri gibi) harita üzerinde görselleştirmek için birebirdir.

# Başlıca kullanım alanları:

# Nokta / İşaretçi (Marker) ekleme: Belirli koordinatlara pin koyup tıklandığında bilgi penceresi (popup) açtırmak.

# Isı Haritası (HeatMap): Verilerin hangi bölgelerde yoğunlaştığını renklerle göstermek.

# Bölge Boyama (Choropleth): Ülke, şehir veya ilçe sınırlarını veri yoğunluğuna göre renklendirmek.


import folium as flc # harita islemleri yapmak 

#harita merkezini belirle
map_center= [38.0,35.0]
m = flc.Map(location= map_center, zoom_start=5) # acılıs konumunu belirliyoruz
#herbir depremi haritaya ekliyoruz, butun satırları gezmem gerekicek , cunku enlem ve boylam satırlarda
for idx, row in df_clean.iterrows():  #iterrows mesela satırı okudunya bir sonraki satıra geç demek.
    flc.CircleMarker( # depremi buyuklugune gore bir yarı cap yapıyoruz ve buyukluge gore yarıcap buyuyor.
        location=[row["Enlem(N)"], row["Boylam(E)"]],
        radius=row["ML"]*2, # veriyi cekerken daire buyutmemizi sağlıyor.
        popup=f"Yer: {row['Yer']}<br>Büyüklük: {row['ML']}<br>Derinlik : {row['Derinlik(km)']} km", # br altsatıra in demek 
        color = "crimson",
        fill=True, # dairenin icini doldurmamızı sağlıyor
        fill_color = "crimson"
    
    ).add_to(m)    
m.save("Deprem_haritasi.html")
print("Harita Kayıt Edildi.")
