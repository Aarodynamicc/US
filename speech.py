import os
import threading
import time
from gtts import gTTS

def _play_audio(text):
    # Overwriting the same file prevents your storage from filling up
    filename = "speech_output.mp3"
    linux_path = f"/mnt/c/html/sign_language_project/inference/{filename}"
    win_path = f"C:\\html\\sign_language_project\\inference\\{filename}"
    
    try:
        # 1. Save the file (overwrites previous)
        tts = gTTS(text=text, lang='en')
        tts.save(linux_path)
        
        # 2. Wait a tiny bit for the drive to sync
        time.sleep(0.2)

        # 3. FIXED: Using \$m to ensure PowerShell sees the variable
        ps_cmd = (
            f'powershell.exe -WindowStyle Hidden -Command "'
            f'Add-Type -AssemblyName PresentationCore; '
            f'\$m = New-Object System.Windows.Media.MediaPlayer; '
            f'\$m.Open(\'{win_path}\'); '
            f'\$m.Play(); '
            f'Start-Sleep -s 2"'
        )
        os.system(ps_cmd)
        
    except Exception as e:
        print(f"Audio Error: {e}")

def speak(text):
    if text:
        # Threading keeps the camera window smooth
        threading.Thread(target=_play_audio, args=(text,), daemon=True).start()
