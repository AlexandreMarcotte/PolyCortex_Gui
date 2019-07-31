from PyQt5.QtWidgets import QFileDialog


def select_file():
    """Set open to False if you want to get the file for saving"""
    # From: https://pythonspot.com/pyqt5-file-dialog/
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    f_name, _ = QFileDialog.getOpenFileName(options=options)
            # caption='QFileDialog.getOpenFileName()', directory='',
            # filter=f'All Files (*);;Python Files (*{f_extension})', options=options)
            # caption='QFileDialog.getOpenFileName()', directory='',
            # filter=f'All Files (*);;Python Files (*{f_extension})', options=options)
        # f_name, _ = QFileDialog.getOpenFileName(
        #     main_window, 'QFileDialog.getOpenFileName()', '',
        #     f'All Files (*);;Python Files (*{f_extension})', options=options)
    # else:
    #     f_name, _ = QFileDialog.getSaveFileName(
    #         main_window, 'QFileDialog.getSaveFileName()', '',
    #         f'All Files (*);;Text Files (*{f_extension})', options=options)
    return f_name

