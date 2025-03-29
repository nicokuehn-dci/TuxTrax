import subprocess

MIN_JACK_VERSION = (1, 9, 21)

try:
    output = subprocess.check_output(['jackd', '-v'], stderr=subprocess.STDOUT)
    print("JACK2 Version Output:", output.decode())
    version_str = output.decode().split()[1]  # Adjust based on actual output format
    print("Extracted Version String:", version_str)
    version = tuple(map(int, version_str.split('.')))
    print("Parsed Version:", version)
    print("Version Check Passed:", version >= MIN_JACK_VERSION)
except Exception as e:
    print("Error:", e)
