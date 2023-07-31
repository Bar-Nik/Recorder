import wave
import os
import time
import threading
import tkinter
import pyaudio
from playsound import playsound


class VoiceRecorder():

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('MyRecorder')
        self.root.geometry('470x270+300+200')
        self.root.resizable(False, False)

        self.button = tkinter.Button(
            text='Записать',
            font=('Arial', 12, 'bold'),
            command=self.click_handler,
            width=15,
            height=1,
            bg='#ee675c',
        )
        self.button.grid(row=0, column=0, padx=5, pady=5)

        self.button1 = tkinter.Button(
            text='Слушать',
            font=('Arial', 12, 'bold'),
            command=self.click_listen,
            width=15,
            height=1,
        )
        self.button1.grid(row=0, column=1, padx=5, pady=5)

        self.label = tkinter.Label(text='00:00:00',
                                   width=15,
                                   height=1,
                                   )
        self.label.grid(row=0, column=2)


        self.my_list = tkinter.Listbox(bg='#d1e6d9')
        self.my_list.grid(row=1, column=0, columnspan=3, stick='wesn', padx=5)
        self.viewing_records()

        scrollbar = tkinter.Scrollbar(orient="vertical", command=self.my_list.yview)
        scrollbar.grid(row=1, column=0, stick='sne', columnspan=3, padx=5, pady=1)

        self.my_list["yscrollcommand"] = scrollbar.set

        self.button2 = tkinter.Button(
            text='Обновить',
            font=('Arial', 12,),
            command=self.viewing_records,
            width=15,
            height=1,
            bg='white',
        )
        self.button2.grid(row=2, column=0, stick='wens', padx=5, pady=5)

        self.button3 = tkinter.Button(
            text='Удалить',
            font=('Arial', 12,),
            command=self.delete,
            width=15,
            height=1,
            bg='white',
        )
        self.button3.grid(row=2, column=1, stick='wens', padx=5, pady=5)


        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
            #input_device_index=9,
        )

        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f'{int(hours):02d}:{int(mins):02d}:{int(secs):02d}')

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1

        while exists:
            if os.path.exists(f'recording{i}.wav'):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f'recording{i}.wav', 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

    def click_listen(self):
        selection = self.my_list.curselection()
        selection_get = self.my_list.get(selection[0])
        playsound(selection_get.split()[0])

        # exists = True
        # i = 1
        #
        # while exists:
        #     if os.path.exists(f'recording{i}.wav'):
        #         i += 1
        #     else:
        #         playsound(f'recording{i - 1}.wav')
        #         exists = False

    def viewing_records(self):
        self.my_list.delete(0, tkinter.END)
        sp = [filename for root, dirs, files in os.walk('.') for filename in files if '.wav' in filename]
        records_list = sorted(sp, key=lambda x: int(x.rstrip('.wav').lstrip('recording')), reverse=True)
        for i in records_list:
            self.my_list.insert(0, ' ' + i)

    def delete(self):
        selection = self.my_list.curselection()
        selection_get = self.my_list.get(selection[0])
        self.my_list.delete(selection[0])
        if os.path.isfile(selection_get.split()[0]):
            os.remove(selection_get.split()[0])
        else:
            print('Path is not a file')


VoiceRecorder()
