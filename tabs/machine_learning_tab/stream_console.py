from PyQt5 import QtCore


class Stream_console(QtCore.QObject):
    """https://unix.stackexchange.com/questions/182537/
    write-python-stdout-to-file-immediately/182610"""

    message = QtCore.pyqtSignal(str)
    def __init__(self, text_edit, machine_learning_tab):
        super().__init__()
        self.text_edit = text_edit
        self.machine_learning_tab = machine_learning_tab

        self.x = None

    def write(self, message):
        # Faire un thread pour pouvoir faire cette function en meme temps de
        # plotter les informations quelle remet à chacune de ces boucles
        # self.x = message
        # if 'loss' in message:
        #     self.text_edit.insertPlainText(message)
        if 'val_loss' in message:
            message = message + '\n'
        #     self.text_edit.insertPlainText(message)
        self.machine_learning_tab.write_consol_message_in_txt_edit(message)

        # self.message.emit(str(message))

    def flush(self):
        # TODO: ALEXM
        # When you pull the sys.stdout so that it write into a file or here a
        # QTextEdit it will have a different buffer (4k) that will no flush
        # until full - find a way to programmatically change this buffer so that
        # it flush at every line it receive
        pass
        # sys.stdout.buffer.flush(
