"""
Fichier contenant la classe :class:`SignalWrapper`.

Cette classe fournit une abstraction légère pour gérer des signaux dans une application basée sur Qt.
Elle encapsule un objet `Signal` de PyQt/PySide et facilite la gestion des connexions et des émissions de signaux.
"""

from qtpy.QtCore import QObject, Signal


##################################################
class SignalWrapper(QObject):
	"""
	Classe d'encapsulation pour les signaux Qt.

	Cette classe simplifie la gestion des signaux en fournissant une interface minimale pour connecter des fonctions et émettre des signaux.

	Attributs :
			- **_signal (QtCore.Signal)** : Signal Qt encapsulé dans cette classe.
	"""

	_signal = Signal(object)  # Signal encapsulé, prêt à être utilisé dans l'application.

	##################################################
	def __init__(self):
		"""Initialise l'objet SignalWrapper."""
		super().__init__()  # Appelle le constructeur de la classe parent QObject.

	##################################################
	def connect(self, f):
		"""
		Connecte une fonction ou un slot au signal encapsulé.

		:param f: Fonction ou slot à connecter.
		"""
		self._signal.connect(f)  # Connexion de la fonction fournie au signal.

	##################################################
	def emit(self, value):
		"""
		Émet le signal encapsulé.

		Utilisé pour notifier les parties de l'application abonnées au signal.
		"""
		self._signal.emit(value)  # Émission du signal.
