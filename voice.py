import subprocess
import os


def convert(voice_filename, converted_filename, sr=16000):
    """
    Function converts ogg to wav.
    :param voice_filename: name for downloaded file from Telegram
    :param converted_filename: new name for converted file
    :param sr: sample rate
    :return: None
    """
    subprocess.call(f'ffmpeg -i {voice_filename}'
                    f' -af aresample=resampler=soxr -ar {sr}'
                    f' {converted_filename}', shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'{voice_filename}')

