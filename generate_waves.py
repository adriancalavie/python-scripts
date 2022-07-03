import numpy as np
from scipy.io import wavfile

generated_files_location = "./generated_files/.wav/"

def generate_wave_file(frequency: int, time: float, sample_rate: int):
    """
    It takes a frequency, time, and sample rate as input, and generates a wave file with the given
    frequency, time, and sample rate.
    
    :param frequency: The frequency of the wave you want to generate
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

    file_name = input("Name your audio: ")
    wavfile.write(generated_files_location + file_name, sample_rate, signal)


def run():
    """
    It takes a frequency, a time, and a sample rate, and generates a wave file with a sine wave of the
    given frequency for the given time at the given sample rate
    """

    sample_rate = 44100
    frequency = int(input("Enter fundamental frequency: "))
    time = float(input("Enter duration of signal (in seconds): "))

    generate_wave_file(frequency, time, sample_rate)


if __name__ == '__main__':
    run()
