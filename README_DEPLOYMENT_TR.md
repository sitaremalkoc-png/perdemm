# Perde AI Studio — Yayına alma notları

## Şu anki çalışma şekli
- Ön yüz: mobil/tablet/bilgisayar uyumlu PWA.
- Sunucu: Node.js; tek şifreli giriş.
- Görsel motoru: Hugging Face ZeroGPU üzerindeki `Qwen/Qwen-Image-Edit-2509`.
- Oda ve kumaş fotoğrafı birlikte modele gönderilir.
- Hugging Face tokenı yalnızca sunucu ortam değişkeninde tutulur. Bu ücretsiz yol için OpenAI API anahtarı gerekmez.
- OpenAI API anahtarı bu ücretsiz kota yolunda gerekli değildir.

## Yayın için kullanıcı hesabında yapılacaklar
1. ZIP içeriğini özel bir GitHub deposuna yükle.
2. Render'da **New → Blueprint** ile bu depoyu bağla.
3. Render Environment bölümüne `APP_PASSWORD` ve `HF_TOKEN` ekle.
4. Render deploy tamamlandıktan sonra `/healthz` adresinin 200 döndürdüğünü kontrol et.
5. Uygulamaya telefon ve bilgisayardan giriş yap; tarayıcı menüsünden uygulamayı yükle.

## Hugging Face tokenı
`https://huggingface.co/settings/tokens` sayfasından Read yetkili bir token oluştur. Tokenı sohbete yazma. Yalnızca Render'ın gizli Environment alanına ekle.

## Gizlilik
Mevcut ücretsiz yol, Hugging Face'in resmi herkese açık Qwen Space'ini kullanır. Ücretsiz hesapta ZeroGPU kotası 24 saatlik döngü başına 5 dakikadır; sayaç ilk GPU kullanımından sonra 24 saatte yenilenir. PWA giriş ekranı özel olsa da oda/kumaş fotoğrafları model işleme için bu harici Space'e gönderilir. Kendi hesabındaki özel ZeroGPU Space'i ücretsiz barındırmak için Hugging Face'in güncel şartlarına göre doğrulanmış ve 30 günden eski hesap gerekir. Uygunluk oluşunca `hf-space/` klasörü ile özel model Space'i kurulabilir.
