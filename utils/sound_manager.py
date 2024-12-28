from pydub import AudioSegment
from pydub.playback import play
import threading  # Asenkron müzik çalma için threading modülünü ekliyoruz

class SoundManager:
    def __init__(self):
        # Ses dosyalarının yollarını tutan bir sözlük
        self.sounds = {
            "background": "sounds/background_music.ogg",
            "explosion": "sounds/explosion.ogg",
            "wow": "sounds/wow.ogg",
        }

    def play_sound(self, sound_name):
        """Ses dosyasını çalacak fonksiyon"""
        if sound_name in self.sounds:
            sound = AudioSegment.from_file(self.sounds[sound_name])
            self._play_async(sound)  # Ses çalmayı asenkron hale getiriyoruz

    def _play_async(self, sound):
        """Asenkron müzik çalma fonksiyonu"""
        # Müzik çalma işlemini ayrı bir iş parçacığı (thread) üzerinde çalıştırıyoruz
        threading.Thread(target=self._play, args=(sound,)).start()

    def _play(self, sound):
        """Sesi çalma fonksiyonu"""
        play(sound)

# Kullanım örneği
if __name__ == "__main__":
    sound_manager = SoundManager()
    sound_manager.play_sound("background_music")  # Arka plan müziğini çalmaya başla
