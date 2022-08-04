import threading
import time
import queue
import itertools
import PySimpleGUI as sg


def worker_thread(thread_name, run_freq, gui_queue):
    print("starting thread 1 - {} that runs every {} ms".format(thread_name, run_freq))
    for i in itertools.count():
        time.sleep(run_freq / 1000)
        gui_queue.put('{} - {}'.format(thread_name, i))
        
def the_main_gui(gui_queue):
    layout = [
              [sg.Text('This is multithread window')],
              [sg.Text('', size = (15, 1), key = 'OUTTEXT')],
              [sg.Output(size = (40, 6))],
              [sg.Button('Exit')]
                                ]
    window = sg.Window("Multithreaded window", layout)

    while True:
        event, values = window.read(timeout = 100)
        if event in (None, 'Exit'):
            break
        while True:
            try:
                # get_nowait() -> 실시간으로 데이터를 꺼내는 함수
                message = gui_queue.get_nowait()
            except queue.Empty:
                break
            if message:
                window['OUTTEXT'].update(message)
                #window.refresh()
                print(message)
    window.close()

def main():
    # Queue 생성
    gui_queue = queue.Queue()
    gui_queue.put(1)
    threading.Thread(target=worker_thread, args=('Thread 1', 500, gui_queue), daemon=True).start()
    the_main_gui(gui_queue)

if __name__ == "__main__":
    main()
