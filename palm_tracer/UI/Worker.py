from typing import Callable, Optional

from qtpy.QtCore import QObject, Signal, Slot


##################################################
class Worker(QObject):
	"""
    Worker générique pour exécuter une fonction dans un thread séparé avec gestion des signaux.

    Cette classe permet de déporter une opération bloquante ou longue (ex. traitement d’image)
    dans un thread secondaire, sans bloquer le thread principal (GUI).

    La fonction passée doit être sans argument et peut retourner un résultat (ou None).
    Les signaux permettent de notifier la fin du traitement, de transmettre un résultat ou une erreur.
    """

	finished = Signal()
	"""Signal émis à la fin du traitement (qu’il ait réussi ou échoué)"""
	result = Signal(object)
	"""Signal émis lorsque la fonction renvoie un résultat (peut être None)"""
	error = Signal(str)
	"""Signal émis en cas d’exception pendant l’exécution"""

	##################################################
	def __init__(self, function: Callable[[], object], parent: Optional[QObject] = None):
		"""
		Initialisation de la classe

		:param function: Fonction à exécuter dans le thread secondaire. Ne doit pas interagir avec des objets Qt.
		:param parent: Parent Qt, par défaut None.
		"""
		super().__init__(parent)
		self.function = function

	##################################################
	@Slot()
	def run(self):
		"""
        Point d'entrée du thread secondaire.

        Exécute la fonction `fn`, émet les signaux appropriés en cas de succès ou d'erreur, et signale systématiquement la fin via `finished`.
        """
		try: self.result.emit(self.function())
		except Exception as e: self.error.emit(str(e))
		finally: self.finished.emit()
