import threading
class ThreadManager:
    def __init__(self):
        self.threads = []

    def start_thread(self, target, args=()):
        thread = threading.Thread(target=target, args=args)
        thread.start()
        self.threads.append(thread)

    def stop_all_threads(self):
        for thread in self.threads:
            thread.join()