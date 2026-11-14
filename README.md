# youtube-indirici
# YouTube İndirici

YouTube video bağlantısını yapıştırıp çözünürlük seçerek videoyu **ses dahil, tek bir MP4 dosyası** olarak masaüstüne indiren basit bir Windows programı.

## Özellikler
- Video bağlantısını yapıştır, mevcut çözünürlükleri listele (360p, 720p, 1080p, 4K vb.)
- Seçtiğin çözünürlükte en yüksek kalitede indir
- Video ve ses otomatik birleştirilir
- Dosya doğrudan masaüstüne kaydedilir
- Kurulum gerektirmez, FFmpeg programın içindedir

## Nasıl kullanılır?
1. [Releases](../../releases) bölümünden en son `YouTube Indirici.exe` dosyasını indir.
2. Çift tıklayarak aç. İlk açılış birkaç saniye sürebilir.
3. Windows "Bilinmeyen uygulama" uyarısı gösterirse **Daha fazla bilgi → Yine de çalıştır** seçeneğini kullan. Program imzalı olmadığı için bu uyarı normaldir, kaynak kodu bu depoda açıktır.
4. Video bağlantısını yapıştır, **Çözünürlükleri Getir** düğmesine bas.
5. Çözünürlüğü seç ve **Masaüstüne İndir** düğmesine bas.

## Sorun giderme
- **İndirme hata veriyor:** YouTube sık değişiklik yapar. Programın yeni sürümünü Releases bölümünden indir.
- **Bazı çözünürlükler listede yok:** Video o çözünürlükte yüklenmemiş olabilir.
- **Yaş sınırlı veya özel videolar** indirilemez.

## Kaynak koddan çalıştırma
```
pip install -U yt-dlp
python youtube_indirici.py
```
Kaynak koddan çalıştırırken `ffmpeg.exe` dosyası script ile aynı klasörde veya sistemde (PATH) bulunmalıdır.

## Exe oluşturma
`ffmpeg.exe` ve `ffprobe.exe` dosyalarını script ile aynı klasöre koyup:
```
python -m pip install -U pyinstaller
python -m PyInstaller --onefile --windowed --name "YouTube Indirici" --collect-all yt_dlp --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." youtube_indirici.py
```
Çıktı `dist` klasöründe oluşur.

## Yasal uyarı
Bu program yalnızca **kendi içeriklerini**, **Creative Commons lisanslı** veya **indirme izni olan** videoları indirmek için tasarlanmıştır. YouTube içeriklerini indirmek YouTube Hizmet Şartları'na aykırı olabilir ve telif hakkı içeren videoların indirilmesinden kullanıcı sorumludur. Geliştirici, programın kötüye kullanımından sorumlu tutulamaz.

## Teşekkür
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Unlicense)
- [FFmpeg](https://ffmpeg.org) (LGPL/GPL, kullanılan derlemenin lisansına bakınız)

## Lisans
MIT
