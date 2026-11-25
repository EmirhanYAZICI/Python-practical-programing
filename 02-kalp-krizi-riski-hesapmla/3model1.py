import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense  # type: ignore
from tensorflow.keras.optimizers import Adam  # type: ignore

df = pd.read_csv('heart.csv')

# Kategorik verileri sayısal değerlere dönüştürelim
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
label_encoder_sex = LabelEncoder()
label_encoder_cp = LabelEncoder()
df['Sex'] = label_encoder_sex.fit_transform(df['Sex'])
df['ChestPainType'] = label_encoder_cp.fit_transform(df['ChestPainType'])
df['RestingECG'] = label_encoder.fit_transform(df['RestingECG'])
df['ExerciseAngina'] = label_encoder.fit_transform(df['ExerciseAngina'])
df['ST_Slope'] = label_encoder.fit_transform(df['ST_Slope'])


#python 3model1.py terminalden çalıştırma
#Girdi ve Çıktıyı belirle

X = df.drop('HeartDisease' , axis=1)
y = df['HeartDisease']

#veriyi eğitim ve test olarak ayıralım
X_train, X_test , y_train, y_test = train_test_split(X,y, test_size=0.3 , random_state=42)
#veri dengesizliğini düzelt

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
#veriyi ölçeklendir
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_smote)
X_test_scaled = scaler.transform(X_test)

#1.Yapay sinir ağları
print('Model 1: Yapay Sinir Ağları')
model = Sequential()
model.add(Dense(16, input_dim=X_train_scaled.shape[1] ,activation = 'relu'))
model.add(Dense(1, activation='sigmoid'))
#modeli derleyelim
optimizer = Adam(learning_rate=0.001)
model.compile(loss='binary_crossentropy' , optimizer = optimizer , metrics=['accuracy'])
#modeli eğitielim
model.fit(X_train_scaled, y_train_smote, epochs=100 , verbose=1 , validation_data=(X_test_scaled, y_test) )
loss, accuracy = model.evaluate(X_test_scaled, y_test) #loss bize kayıpları accuracy ise dogrulu verecektir ikisinide alabiliriz

#2. Model Random Forest
print("Model 2: Random Forest")
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_smote,y_train_smote)
y_pred_rf= rf_model.predict(X_test_scaled)
rf_accuracy= accuracy_score(y_test,y_pred_rf)

#3. Model Karar Ağaçları Modelleri
print("Model 3: Karar Ağaçları")
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train_smote,y_train_smote)
y_pred_dt= dt_model.predict(X_test_scaled)
dt_accuracy = accuracy_score(y_test,y_pred_dt)

#4. Model Lojistik regresyon 
print("Model 4: Lojistik Regresyon")
lr_model= LogisticRegression(random_state=42)
lr_model.fit(X_train_smote,y_train_smote)
y_pred_lr= lr_model.predict(X_test_scaled) # olceklenmis x verisine gore tahminlemeyi yap demek.
lr_accuracy = accuracy_score(y_test,y_pred_lr)


#  HANGİ MODELİN DOĞRULUK ORANI YÜKSEK ÖĞRENİCEZ
print(f"Yapay Sinir Ağı Doğruluk Oranı:{accuracy * 100:.2f}%")
print(f"Random Forest Doğruluk Oranı:{rf_accuracy * 100:.2f}%")
print(f"Karar Ağaçları Doğruluk Oranı:{dt_accuracy * 100:.2f}%")
print(f"Lojistik Regresyon Doğruluk Oranı:{lr_accuracy * 100:.2f}%")

# KULLANICIDAN VERİ ALMA VE MODELİ EĞİTME

while True:
    user_input_1= float(input("Yaşınızı Giriniz:"))
    user_input_2= input("Cinsiyetinizi Giriniz:")
    
    print("\nGöğüs Ağrısı Tipleri:")
    print("  TA  : Tipik Kalp Ağrısı (Eforla artan klasik ağrı)")
    print("  ATA : Atipik Ağrı (Klasik olmayan göğüs ağrısı)")
    print("  NAP : Kalp Dışı Ağrı (Kas/mide kaynaklı ağrı)")
    print("  ASY : Ağrı Yok (Asemptomatik)")
    user_input_3 = input("Göğüs Ağrısı Tipinizi Giriniz (TA, ATA, NAP, ASY): ").strip().upper()
    
    user_input_4= input("Dinlenme Kan Basıncını Giriniz:")
    user_input_5= input("Kolestrol Değerinizi Giriniz:")
    
    try:
        #kullanıcı verilerini sayısal hale getirme
        user_data = pd.DataFrame({
           "Age":[user_input_1],
           "Sex":[label_encoder_sex.transform([user_input_2])[0]] ,
           "ChestPainType":[label_encoder_cp.transform([user_input_3])[0]],
           "RestingBP":[user_input_4],
           "Cholesterol":[user_input_5],# biz burdaki 5 tane degerle calısıcaz asagıdaki degerler oylesine girdik bir atkisi yok cunku
           "FastingBS":[0],
           "RestingECG":[0],
           "MaxHR":[150],
           "ExerciseAngina":[0], # sabit bir değer
           "Oldpeak":[0.0],
           "ST_Slope":[1]
        })
        
        # Veriyi ölçeklendirelim
        user_data_scaled= scaler.transform(user_data)
        
        #tahmin yapma
        prediction= model.predict(user_data_scaled)
        print(f"Tahmin Sonucunuz: Kalp Hastalığı Riski Oranınız:{prediction[0][0]:.4f}")
        
    except ValueError as e:
        print(f"Bir hata oluştu:{e} Lütfen Bilgileri Kontol Ediniz.")
        
    # yeni tahmin icin kullancıaya sorma
    devam= input("Başka Tahmin Yapmak İstermisiniz? (E/H)")    
    if devam.lower() != "e":
        break