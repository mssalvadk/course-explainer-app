import os
import datetime
import winsound

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hook.log')


def log(message):
    with open(log_path, 'a') as f:
        f.write(f"{datetime.datetime.now().isoformat()} {message}\n")


log("hook fired")

# winsound plays reliably from hidden hook processes, but only supports WAV.
# Drop a notification.wav into sounds/ to use a custom sound; otherwise
# fall back to the built-in Windows exclamation sound.
wav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds', 'notification.wav')

try:
    if os.path.exists(wav_path):
        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        log(f"played {wav_path}")
    else:
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
        log("played SystemExclamation")
except Exception as e:
    # Don't break the hook, but record what went wrong
    log(f"error: {e!r}")
