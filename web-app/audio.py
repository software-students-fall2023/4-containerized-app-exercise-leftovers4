import wave
import pyaudio

def record_audio(filename, duration=5, rate=44100, chunk=1024, channels=1):
    """Records audio from microphone

    Args:
        filename (string): File Name
        duration (int): Duration. Defaults to 5.
        rate (int): Bitrate. Defaults to 44100.
        chunk (int): Chunk size. Defaults to 1024.
        channels (int): Number of channels. Defaults to 1.
    """
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
