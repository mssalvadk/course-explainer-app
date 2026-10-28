import os
import winsound

# winsound plays reliably from hidden hook processes, but only supports WAV.
# Drop a notification.wav into sounds/ to use a custom sound; otherwise
# fall back to the built-in Windows exclamation sound.
wav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds', 'notification.wav')

try:
    if os.path.exists(wav_path):
        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
    else:
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
except Exception:
    # Silently fail so a sound problem never breaks the hook
    pass
