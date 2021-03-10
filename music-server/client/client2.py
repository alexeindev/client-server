import zmq
import queue
import threading
import logging
import os
from os import path, listdir
from pygame import mixer, time

mixer.init()


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

context = zmq.Context()
#  Socket to talk to server
print("Connecting to the server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


playlist = []


def printMenu():
    print('----------------------- MUSIC SERVICE -----------------------')
    print('Press a number to choose an option: \n')
    print('[1] List available songs')
    print('[2] Play all the playlist')
    print('[3] Add to playlist')
    print('[4] Play a single song')
    print('[5] Exit the music service')
    print('----- Media controls -----')
    print('[6] Resume')
    print('[7] Pause')
    print('[8] Skip \n')


def listSongs():
    socket.send_multipart([b'l'])
    listOfSongs = socket.recv()
    listOfSongs.decode("utf-8")
    listOfSongs = eval(listOfSongs)

    print('- - - - - Song list - - - - -')
    for song in listOfSongs:
        print("- " + song)


def isSongDownloaded(filename):
    listOfFile = os.listdir(path='.')
    downloaded = False
    for file in listOfFile:
        if file == filename:
            downloaded = True
    return downloaded


def queueSong(filename):

    if isSongDownloaded(filename) == False:
        socket.send_multipart([b'd',
                               str(filename).encode('utf-8')])

        m = socket.recv_multipart()
        # Creates the file on the client folder and
        if m[0] == b'File exist':
            with open(filename, 'wb') as file:
                file.write(m[1])
                print('%s has been successfully downloaded ' % filename)
        else:
            print('The file %s does not exist on the server, try again' % filename)
            return

    if not playlist:
        playlist.append(filename)


def unqueueSong():
    if not playlist:
        song = playlist.pop(0)
        logging.debug('Getting ' + str(song) + ' items in queue')
        playSong(song)


def playSong(song):
    mixer.music.load(song)

    # Setting the volume
    mixer.music.set_volume(0.7)

    # Start playing the song
    mixer.music.play()

    time.wait(mixer.get_length())


class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        while True:
            # Print the menu and select and option
            printMenu()
            action = input(
                "Type your choice [#] -> ")

            if action == '1':
                listSongs()
            elif action == '2':
                c = ConsumerThread(name='consumer')
                c.start()
            elif action == '3':
                filename = input("Name of the song -> ")
                queueSong(filename)
            elif action == '4':
                filename = input("Name of the song -> ")
                playSong(filename)
            elif action == '5':
                mixer.music.stop()
                break
            elif action == '6':
                # Resuming the music
                mixer.music.unpause()
            elif action == '7':
                # Pausing the music
                mixer.music.pause()
            elif action == '8':
                unqueueSong()
            else:
                print('invalid action, Try again')
        return


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        logging.debug('RUNNING')
        while True:
            if playlist:
                song = playlist.pop(0)
                logging.debug('Getting ' + str(song) + ' items in queue')
                playSong(song)

        return


if __name__ == '__main__':
    p = ProducerThread(name='producer')
    p.start()
