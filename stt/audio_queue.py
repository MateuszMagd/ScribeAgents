import queue

audio_queue = queue.Queue(maxsize=50)

def audio_generator():
    while True:
        frame = audio_queue.get()
        if frame is None:
            break
        yield frame
