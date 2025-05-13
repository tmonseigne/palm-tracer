from typing import Callable, Optional

from qtpy.QtCore import QObject, QThread, Signal, Slot

class Worker(QObject):
    finished = Signal()
    result_ready = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, fn: Callable[[], None], parent: Optional[QObject] = None):
        super().__init__(parent)
        self.fn = fn

    @Slot()
    def run(self):
        try:
            result = self.fn()
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()
