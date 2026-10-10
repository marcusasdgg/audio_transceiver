import pyaudio

def find_first_dev(p, name):
    dev_count = p.get_device_count()
    for i in range(dev_count):
        dev = p.get_device_info_by_index(i)
        if dev["name"].find(name) != -1:
            return (i,dev)
    return None


if __name__ == "__main__":
    print(find_first_dev(pyaudio.PyAudio(), "TANDBERG"))