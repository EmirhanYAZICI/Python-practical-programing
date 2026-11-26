#ekrandaki goruntuleri kareler haline alıcaz ve herbir gorunutuyu siyah beyaza ceviricez 
#Klavye kontrolü: Metin yazdırabilir (write), tek tek tuşlara basabilir, hotkey= kısayol tuslarını basci birsekilde girebilmemizi saglıyor pyautogui uzerinden
# (press) veya Ctrl + C gibi kısayolları (hotkey) kullanabilir.pyautogui yani kullanabilmemizi sağlıyor kodla
import cv2
import time
import pyautogui#ne işe yarıyor 
import webbrowser # wp acıcak
import os # pek gerekli degil ama

def send_whatsapp_message():
    phone_number = "+905527162054"
    # guncel tarihi ve saati çekiyoruz
    timestamp= time.strftime("%d %H:%M")
    #GONDERİLECEK MESAJ
    message = f"Hareket Tespit Edildi. Tarih/Saat:{timestamp}"
    #whatsapp web api urlsini oluştur
    web_url= f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    
    try:
        #işlem başlatıldı
        print(f"[İNFO] Whatsapp üzerinden mesaj gönderiliyor:{message}")
        webbrowser.Opera(web_url)
        #Whatsapp web yuklemesi icin bekliyoruz.
        time.sleep(20)
        #enter tusuna basarak mesajını gönder
        pyautogui.press("enter")
        #mesajın iletilmesi icin 5 saniye bekle
        time.sleep(5)
        #tarayıcı sekmesini kapat
        pyautogui.hotkey("ctrl","w")
        # başarılı gonderim logu
        print("[İNFO] Whatsapp mesajı  gonderildi.")
        return True
    except Exception as e:
        #hata durumunu yakalamak
        print("[ERROR] Whatsapp gönderiminde hata oluştu.")
        return False # hata vermesi durumunda başa donmemizi saglıyor.
    
def main():
    pyautogui.PAUSE= 1.5
    #kamerayı olaya dahil etme
    cap= cv2.VideoCapture(0) # 0 her zaman dahili kamerayı temsil eder.
    if not cap.isOpened():
        print("Kamera Açılmadı!")
        return
    
    #hareket algılama iöin önceki kare
    #MOG2 algoritması ile hareket algılama
    backsub = cv2.createBackgroundSubtractorMOG2(
        history=500, # 500 kareyi alıyoz.
        varThreshold=25, #25 kafi frame başı ne kadar hassasiyet olucağını gösteriyor.
        detectShadows=True # golgeleride dahil et demek.

    )    
    last_motion_time = 0
    cooldown = 10
    while True:
        ret, frame = cap.read() # ben frame aldıgım calısıyosa frame ret in iöine at ture false gorevi goruyor.
        if not ret:
            print("[ERROR] Kamera görüntüsü alınamadı!")
            break                                                                                                         # 127: Sınır değer (127'den büyük olanlar 255/beyaz, küçük olanlar 0/siyah olur)                       
        # hareketi algılama algoritması                                                                                   #Amacı: Gri görüntüyü temizleyip tam siyah (0) ve tam beyaz (255) yapar (gölgeleri yok eder, hareketi netleştirir).
        fgMask= backsub.apply(frame) # goruntuyu analiz edicek arka planda farklı olan pikselleri bulucak                 # _ (Alttan tire): Fonksiyondan dönen ilk değeri (eşik sayısını) kullanmayacağımız için çöpe atar; asıl işlenmiş görüntü thresh değişkenine alınır. 
        _ ,thresh = cv2.threshold(fgMask, 250, 255, cv2.THRESH_BINARY)    
        thresh= cv2.erode(thresh, None, iterations=2)   # iteration titreme icin ,  gurultu temizleme 
        thresh= cv2.dilate(thresh, None, iterations=2)   # gurultuleri analiz ediyor dilate   siyah-beyaz görüntüdeki beyaz alanların kenarlarını dışa doğru genişletip kalınlaştırır.
        
        #hareket eden bolgelerin veya nesnelerin sınırlarını oğrenme
        contours, _= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected= False # asagıdaki for dongusu surekli kontrol edecek
        for contour in contours:
            if cv2.contourArea(contour) < 1500: # alanı boyle yapıyoz kucuk sekilde yapıyoz
                continue
            motion_detected=True 
            break
        # suanki zamanı al , cooldown= soguma demek
        current_time = time.time()
        
        # hareket varsa cooldown suresini kontrol et ,bekleme suresi demek cooldown
        if motion_detected and (current_time - last_motion_time > cooldown):
            print("[İNFO] Hareket Algılandı.")
            #whatsapp mesajını gnder
            if send_whatsapp_message():
                last_motion_time = current_time # son hareket zamanını yolla karşı tarafa
                cv2.putText(frame,"Hareket Algilandi!", (10,30), cv2.FONT_HERSHEY_SIMPLEX,1 , (0,0,255), 2) # sol ust koseye yazı koymamızı saglıyor
            else:    
                print("[WARNİNG] Whatsapp mesaji gönderilemedi!")
                time.sleep(5)
        else:
            cv2.putText(frame,"Hareket Algılanamadı!",(10,30) ,cv2.FONT_HERSHEY_SIMPLEX ,1 , (0, 255, 0), 2)
                    
        #canlı goruntu ve hareket maskesini goster    
        
        cv2.imshow("Kamera",frame)
        cv2.imshow("Hareket Maskesi", thresh)
        
        #Çıkış için q tuşuna bas
        if cv2.waitKey(1) & 0XFF == ord("q"):  #  1ms bekle, 'q' tuşuna basıldıysa kontrol et
            break                              # Döngüden çık (kamerayı kapat) ord ascı kodunu verir.
           
    #program sonlandıogında kaynaları temizleme ve kamerayı serbest bırakma işlemden
    cap.release() # Kamerayı serbest bırakır (bağlantıyı keser)
    cv2.destroyAllWindows() #OpenCV'nin açtığı tüm pencereleri kapatır
         
if __name__== "__main__":     # Bu dosya doğrudan çalıştırıldıysa (başka yerden import edilmediyse)
    main()                      # Ana fonksiyonu (main) başlat
         
                                                
        