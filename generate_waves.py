import numpy as np
from scipy.io import wavfile


def generate_wave_file(frequency: int, time: float, sample_rate: int):
    """
    It takes a frequency, time, and sample rate, and creates a .wav file with the given parameters

    :param frequency: The frequency of the wave in Hz
    :type frequency: int
    :param time: The length of the audio file in seconds
    :type time: float
    :param sample_rate: The number of samples per second
    :type sample_rate: int
    """

    samples = np.arange(time * sample_rate) / sample_rate

    signal = np.sin(2 * np.pi * frequency * samples)
    signal *= 32767
    signal = np.int16(signal)

    wavfile.write(str(input("Name your audio: ")), sample_rate, signal)


def run():
    """
    It takes a frequency, a time, and a sample rate, and generates a wave file with a sine wave of the
    given frequency for the given time at the given sample rate
    """

    sample_rate = 44100
    frequency = int(input("Enter fundamental frequency: "))
    time = float(input("Enter duration of signal (in seconds): "))

    generate_wave_file(frequency, time, sample_rate)


if __name__ == 'main':
    run()
