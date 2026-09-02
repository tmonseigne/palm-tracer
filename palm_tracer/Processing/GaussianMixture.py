"""Ajuste et évalue des mélanges gaussiens unidimensionnels."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


##################################################
@dataclass(frozen=True)
class GaussianMixture:
	"""
	Représente un mélange gaussien unidimensionnel ajusté par l'algorithme Expectation-Maximization (EM).

	La densité du modèle est définie par :

	.. math::

		p(x \\mid \\Theta) = \\sum_{k=1}^{K} \\pi_k
		\\frac{1}{\\sigma_k\\sqrt{2\\pi}}
		\\exp\\!\\left[-\\frac{1}{2}\\left(\\frac{x-\\mu_k}{\\sigma_k}\\right)^2\\right],

	avec :math:`\\pi_k \\geq 0`, :math:`\\sigma_k > 0` et :math:`\\sum_k \\pi_k = 1`.
	La log-vraisemblance mémorisée correspond à la somme des logarithmes des densités attribuées aux :math:`n` observations :

	.. math::

		\\mathcal{L}(\\Theta) = \\sum_{i=1}^{n}\\log p(x_i \\mid \\Theta).

	Les composantes sont systématiquement triées par moyenne croissante.
	Cet ordre stable évite que deux ajustements équivalents permutent arbitrairement leurs indices dans les résultats et les représentations.
	``frozen=True`` interdit la réaffectation des attributs de l'instance, mais les tableaux NumPy qu'ils contiennent restent modifiables.

	:param weights: Proportions :math:`\\pi_k` des composantes, sous forme d'un tableau de taille :math:`K` dont la somme vaut un.
	:param means: Moyennes :math:`\\mu_k` des composantes, triées par ordre croissant dans un tableau de taille :math:`K`.
	:param sigmas: Écarts-types :math:`\\sigma_k` strictement positifs des composantes, dans un tableau de taille :math:`K`.
	:param log_likelihood: Log-vraisemblance finale :math:`\\mathcal{L}(\\Theta)` du modèle retenu.
	:param converged: Indique si le critère de convergence a été atteint avant le nombre maximal d'itérations.
	:param n_iter: Nombre d'itérations exécutées par l'initialisation retenue.
	"""

	weights: np.ndarray
	means: np.ndarray
	sigmas: np.ndarray
	log_likelihood: float
	converged: bool
	n_iter: int

	##################################################
	@classmethod
	def fit(cls, data: np.ndarray, n_component: int = 2, max_iter: int = 200, tolerance: float = 1e-5, n_init: int = 3) -> GaussianMixture:
		"""
		Ajuste un mélange de ``n_component`` gaussiennes sur les données brutes.

		Les données sont converties en nombres flottants 64 bits, aplaties, puis débarrassées de leurs valeurs non finies.
		L'ajustement est ensuite effectué indépendamment depuis plusieurs points de départ afin de réduire le risque qu'EM converge
		vers un maximum local défavorable :

		#. :meth:`_initialize_centers` choisit les centres initiaux par quantiles pour le premier essai, puis par k-means++ pour les suivants.
		#. :meth:`_parameters_from_centers` exécute un k-means classique et en déduit les proportions, moyennes et écarts-types initiaux.
		#. :meth:`_expectation_maximization` affine ces paramètres par Expectation-Maximization (EM).
		#. Le résultat ayant la log-vraisemblance finale la plus élevée est conservé et ses composantes sont triées par moyenne croissante.

		Pour une initialisation donnée, l'ajustement est déclaré convergé lorsque deux log-vraisemblances successives vérifient :

		.. math::

			\\left|\\mathcal{L}^{(t)}-\\mathcal{L}^{(t-1)}\\right|
			\\leq \\varepsilon\\max\\!\\left(1,\\left|\\mathcal{L}^{(t-1)}\\right|\\right),

		où :math:`\\varepsilon` correspond à ``tolerance``.
		Un écart-type minimal égal au maximum entre :math:`10^{-6}` fois l'écart-type global
		et la précision machine empêche une composante de devenir exactement singulière.

		La complexité temporelle est approximativement :math:`O(RINK)` et la mémoire temporaire :math:`O(NK)`, avec :math:`R` initialisations,
		:math:`I` itérations Expectation-Maximization (EM), :math:`N` observations et :math:`K` composantes.

		:param data: Observations à ajuster. Le tableau est aplati et les valeurs non finies sont ignorées.
		:param n_component: Nombre :math:`K` de composantes gaussiennes.
			Il doit être strictement positif et ne pas dépasser le nombre d'observations ni le nombre de valeurs distinctes.
		:param max_iter: Nombre maximal d'itérations Expectation-Maximization (EM) exécutées pour chacune des initialisations.
		:param tolerance: Tolérance relative :math:`\\varepsilon` utilisée pour détecter la stabilisation de la log-vraisemblance.
		:param n_init: Nombre d'ajustements Expectation-Maximization (EM) exécutés avec des paramètres initiaux différents.
			Le résultat ayant la meilleure log-vraisemblance est conservé.
		:return: Nouvelle instance contenant les paramètres du meilleur ajustement.
		:raises ValueError: Si un paramètre est invalide, si les données sont insuffisantes ou si leur variance est nulle.
		"""
		values = np.asarray(data, dtype=np.float64).ravel()
		values = values[np.isfinite(values)]
		if n_component < 1:
			raise ValueError("Le nombre de composantes doit être strictement positif.")
		if max_iter < 1:
			raise ValueError("Le nombre maximal d'itérations doit être strictement positif.")
		if tolerance <= 0:
			raise ValueError("La tolérance doit être strictement positive.")
		if n_init < 1:
			raise ValueError("Le nombre d'initialisations doit être strictement positif.")
		if values.size < n_component:
			raise ValueError("Le nombre d'observations est inférieur au nombre de composantes.")
		if np.unique(values).size < n_component:
			raise ValueError("Le nombre de valeurs distinctes est inférieur au nombre de composantes.")

		global_sigma = float(np.std(values))
		if global_sigma <= 0:
			raise ValueError("Les données doivent présenter une variance strictement positive.")
		sigma_min = max(global_sigma * 1e-6, float(np.finfo(np.float64).eps))
		rng = np.random.default_rng(0)
		best_result: tuple[np.ndarray, np.ndarray, np.ndarray, float, bool, int] | None = None

		for init_id in range(n_init):
			centers = cls._initialize_centers(values, n_component, init_id, rng)
			weights, means, sigmas = cls._parameters_from_centers(values, centers, global_sigma, sigma_min)
			result = cls._expectation_maximization(values, weights, means, sigmas, sigma_min, max_iter, tolerance)
			if best_result is None or result[3] > best_result[3]: best_result = result

		if best_result is None:  # pragma: no cover - Garde impossible après la validation de n_init.
			raise RuntimeError("Aucune initialisation du mélange gaussien n'a été évaluée.")
		weights, means, sigmas, log_likelihood, converged, n_iter = best_result
		order = np.argsort(means)
		return cls(weights[order], means[order], sigmas[order], log_likelihood, converged, n_iter)

	##################################################
	def probability_density(self, x: np.ndarray) -> np.ndarray:
		"""
		Évalue la densité de probabilité totale du mélange.

		Chaque abscisse est d'abord standardisée séparément pour chacune des :math:`K` composantes :

		.. math::

			z_k(x) = \\frac{x-\\mu_k}{\\sigma_k}.

		La méthode évalue ensuite les densités normales et calcule leur somme pondérée :

		.. math::

			p(x) = \\sum_{k=1}^{K}\\pi_k
			\\frac{\\exp\\!\\left[-z_k(x)^2/2\\right]}{\\sigma_k\\sqrt{2\\pi}}.

		Les opérations utilisent la diffusion NumPy : un axe final de taille :math:`K` est temporairement ajouté à ``x`` pour évaluer
		toutes les composantes sans boucle Python. La somme sur cet axe restitue ensuite exactement la forme initiale de ``x``.
		Lorsque les poids sont normalisés, l'intégrale de la densité sur l'ensemble de la droite vaut un.

		:param x: Abscisse scalaire ou tableau d'abscisses auxquelles évaluer le mélange.
		:return: Densité totale évaluée en chaque abscisse, avec la même forme que ``x``.
		"""
		values = np.asarray(x, dtype=np.float64)
		standardized = (values[..., np.newaxis] - self.means) / self.sigmas
		components = np.exp(-0.5 * standardized ** 2) / (self.sigmas * np.sqrt(2.0 * np.pi))
		return np.sum(self.weights * components, axis=-1)

	##################################################
	def make_curve(self, limits: tuple[float, float] | list[float], n_point: int = 128) -> tuple[np.ndarray, np.ndarray]:
		"""
		Construit une courbe régulière représentant la densité du mélange.

		Pour des bornes :math:`x_{min}` et :math:`x_{max}`, les ``n_point`` abscisses sont uniformément réparties selon :

		.. math::

			x_j = x_{min} + j\\frac{x_{max}-x_{min}}{M-1},
			\\qquad j \\in \\{0,\\ldots,M-1\\},

		où :math:`M` correspond à ``n_point``. Les ordonnées sont obtenues en appliquant :meth:`probability_density` à cette grille.
		La méthode retourne la densité théorique brute ; la conversion éventuelle en effectifs ou en courbe cumulée reste de la responsabilité du grapher.

		:param limits: Couple contenant les bornes finies :math:`(x_{min},x_{max})`, avec :math:`x_{min}<x_{max}`.
		:param n_point: Nombre :math:`M` de points de la grille régulière, supérieur ou égal à deux.
		:return: Couple ``(x_grid, density)`` contenant deux tableaux unidimensionnels de taille ``n_point``.
		:raises ValueError: Si les bornes ne sont pas finies et strictement croissantes, ou si moins de deux points sont demandés.
		"""
		if n_point < 2:
			raise ValueError("La courbe doit contenir au moins deux points.")
		if len(limits) != 2 or not np.all(np.isfinite(limits)) or limits[0] >= limits[1]:
			raise ValueError("Les limites de la courbe doivent être finies et strictement croissantes.")
		x_grid = np.linspace(limits[0], limits[1], n_point, dtype=np.float64)
		return x_grid, self.probability_density(x_grid)

	##################################################
	@staticmethod
	def _initialize_centers(data: np.ndarray, n_component: int, init_id: int, rng: np.random.Generator) -> np.ndarray:
		"""
		Choisit les centres servant de point de départ au k-means.

		La première initialisation est déterministe.
		Elle place les centres sur les quantiles situés au milieu de ``n_component`` intervalles de même probabilité.
		Le centre d'indice :math:`k` utilise ainsi le quantile :math:`(k + 0.5) / K`.
		Pour deux composantes, les centres correspondent donc aux quantiles 25 % et 75 %.

		Les initialisations suivantes emploient la stratégie k-means++ :

		#. Le premier centre est une observation choisie uniformément dans les données.
		#. Chaque centre suivant est une observation tirée avec une probabilité proportionnelle au carré de sa distance au centre déjà sélectionné le
		   plus proche. Les zones encore éloignées des centres sont ainsi privilégiées.

		Le générateur ``rng`` est créé avec une graine fixe par :meth:`fit`, ce qui rend ces tirages reproductibles.
		Cette méthode choisit uniquement les centres initiaux ; :meth:`_parameters_from_centers` exécute ensuite le k-means classique avant l'ajustement EM.

		:param data: Observations unidimensionnelles finies utilisées comme centres candidats.
		:param n_component: Nombre de centres à choisir.
		:param init_id: Indice de l'initialisation. La valeur zéro sélectionne les quantiles ; les valeurs suivantes sélectionnent k-means++.
		:param rng: Générateur pseudo-aléatoire utilisé par k-means++.
		:return: Centres initiaux, sous forme d'un tableau de taille ``n_component``.
		"""
		if init_id == 0:
			quantiles = (np.arange(n_component, dtype=np.float64) + 0.5) / n_component
			return np.asarray(np.quantile(data, quantiles), dtype=np.float64)

		centers = np.empty(n_component, dtype=np.float64)
		centers[0] = data[rng.integers(data.size)]
		minimum_distances = (data - centers[0]) ** 2
		for component_id in range(1, n_component):
			distance_sum = float(np.sum(minimum_distances))
			if distance_sum <= 0:
				centers[component_id:] = np.quantile(data, (np.arange(component_id, n_component) + 0.5) / n_component)
				break
			centers[component_id] = data[rng.choice(data.size, p=minimum_distances / distance_sum)]
			minimum_distances = np.minimum(minimum_distances, (data - centers[component_id]) ** 2)
		return centers

	##################################################
	@staticmethod
	def _parameters_from_centers(data: np.ndarray, centers: np.ndarray, global_sigma: float, sigma_min: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
		"""
		Affine les centres par k-means, puis construit les paramètres initiaux d'EM.

		Le k-means applique au maximum 50 fois les deux étapes de Lloyd suivantes :

		#. Chaque observation est affectée au centre le plus proche :

		   .. math::

			  c_i = \\underset{k}{\\operatorname{argmin}}\\,|x_i-m_k|.

		#. Chaque centre possédant au moins une observation devient la moyenne de son groupe :

		   .. math::

			  m_k = \\frac{1}{n_k}\\sum_{i:c_i=k}x_i.

		L'affinement s'arrête lorsque tous les déplacements de centres sont inférieurs à ``sigma_min``.
		Les affectations finales servent ensuite à initialiser les paramètres du mélange :

		.. math::

			\\pi_k = \\frac{n_k}{N}, \\qquad
			\\mu_k = m_k, \\qquad
			\\sigma_k = \\sqrt{\\frac{1}{n_k}\\sum_{i:c_i=k}(x_i-\\mu_k)^2}.

		Une composante contenant moins de deux observations reçoit provisoirement ``global_sigma``.
		Chaque poids est minoré par la précision machine puis renormalisé, et chaque écart-type calculé est minoré par ``sigma_min``.
		Ces protections fournissent à Expectation-Maximization (EM) des paramètres finis et non singuliers.

		:param data: Observations unidimensionnelles finies à regrouper.
		:param centers: Centres choisis par :meth:`_initialize_centers`, sous forme d'un tableau de taille :math:`K`.
		:param global_sigma: Écart-type de l'ensemble des observations, utilisé lorsqu'un groupe contient moins de deux valeurs.
		:param sigma_min: Écart-type minimal autorisé et tolérance absolue d'arrêt du k-means.
		:return: Triplet ``(weights, means, sigmas)`` contenant les paramètres initiaux d'EM, chacun sous forme d'un tableau de taille :math:`K`.
		"""
		for _ in range(50):
			labels = np.argmin(np.abs(data[:, np.newaxis] - centers), axis=1)
			updated_centers = centers.copy()
			for component_id in range(centers.size):
				component = data[labels == component_id]
				if component.size > 0: updated_centers[component_id] = np.mean(component)
			if np.allclose(updated_centers, centers, rtol=0.0, atol=sigma_min): break
			centers = updated_centers

		labels = np.argmin(np.abs(data[:, np.newaxis] - centers), axis=1)
		counts = np.bincount(labels, minlength=centers.size).astype(np.float64)
		weights = np.maximum(counts / data.size, np.finfo(np.float64).eps)
		weights /= np.sum(weights)
		means = centers.copy()
		sigmas = np.full(centers.size, global_sigma, dtype=np.float64)
		for component_id in range(centers.size):
			component = data[labels == component_id]
			if component.size > 1: sigmas[component_id] = max(float(np.std(component)), sigma_min)
		return weights, means, sigmas

	##################################################
	@staticmethod
	def _expectation_maximization(data: np.ndarray, weights: np.ndarray, means: np.ndarray, sigmas: np.ndarray, sigma_min: float, max_iter: int,
								  tolerance: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, bool, int]:
		"""
		Exécute les étapes d'espérance et de maximisation jusqu'à convergence.

		À l'étape d'espérance, la responsabilité :math:`r_{ik}` représente la probabilité conditionnelle que
		l'observation :math:`x_i` appartienne à la composante :math:`k` compte tenu des paramètres courants :

		.. math::

			r_{ik} =
			\\frac{\\pi_k\\mathcal{N}(x_i\\mid\\mu_k,\\sigma_k)}
			{\\sum_{j=1}^{K}\\pi_j\\mathcal{N}(x_i\\mid\\mu_j,\\sigma_j)}.

		Les probabilités sont calculées dans le domaine logarithmique. La soustraction du plus grand logarithme de chaque ligne applique l'identité
		log-sum-exp et évite que les exponentielles de densités très faibles deviennent numériquement nulles.

		À l'étape de maximisation, les responsabilités remplacent les appartenances binaires du k-means.
		Pour l'effectif pondéré :math:`N_k=\\sum_i r_{ik}`, les paramètres sont mis à jour par :

		.. math::

			\\pi_k = \\frac{N_k}{N}, \\qquad
			\\mu_k = \\frac{1}{N_k}\\sum_{i=1}^{N}r_{ik}x_i,

		.. math::

			\\sigma_k = \\sqrt{
			\\frac{1}{N_k}\\sum_{i=1}^{N}r_{ik}(x_i-\\mu_k)^2}.

		Chaque écart-type est minoré par ``sigma_min`` afin d'empêcher une composante de s'effondrer sur une observation.
		Les étapes Expectation et Maximization (EM) alternent jusqu'à ce que la variation relative de log-vraisemblance
		soit inférieure à ``tolerance`` ou que ``max_iter`` soit atteint.
		Une convergence non atteinte ne provoque pas d'exception : les derniers paramètres finis sont retournés avec ``converged=False``.

		:param data: Observations unidimensionnelles finies, sous forme d'un tableau de taille :math:`N`.
		:param weights: Proportions initiales :math:`\\pi_k`, normalisées dans un tableau de taille :math:`K`.
		:param means: Moyennes initiales :math:`\\mu_k`, dans un tableau de taille :math:`K`.
		:param sigmas: Écarts-types initiaux :math:`\\sigma_k` strictement positifs, dans un tableau de taille :math:`K`.
		:param sigma_min: Écart-type minimal autorisé pendant les mises à jour.
		:param max_iter: Nombre maximal de couples d'étapes Expectation-Maximization (EM) exécutés.
		:param tolerance: Tolérance relative appliquée à la variation de log-vraisemblance.
		:return: Tuple ``(weights, means, sigmas, log_likelihood, converged, n_iter)`` contenant les paramètres finaux, la log-vraisemblance,
			l'état de convergence et le nombre d'itérations exécutées.
		"""
		previous_log_likelihood = -np.inf
		converged = False
		log_likelihood = -np.inf
		n_iter = 0
		for n_iter in range(1, max_iter + 1):
			standardized = (data[:, np.newaxis] - means) / sigmas
			log_probabilities = (np.log(weights) - np.log(sigmas) - 0.5 * np.log(2.0 * np.pi) - 0.5 * standardized ** 2)
			maximum_logs = np.max(log_probabilities, axis=1, keepdims=True)
			exponentials = np.exp(log_probabilities - maximum_logs)
			normalizers = np.sum(exponentials, axis=1, keepdims=True)
			responsibilities = exponentials / normalizers
			log_likelihood = float(np.sum(maximum_logs[:, 0] + np.log(normalizers[:, 0])))

			if np.isfinite(previous_log_likelihood):
				scale = max(1.0, abs(previous_log_likelihood))
				if abs(log_likelihood - previous_log_likelihood) <= tolerance * scale:
					converged = True
					break
			previous_log_likelihood = log_likelihood

			effective_counts = np.sum(responsibilities, axis=0)
			weights = effective_counts / data.size
			means = np.sum(responsibilities * data[:, np.newaxis], axis=0) / effective_counts
			variances = np.sum(responsibilities * (data[:, np.newaxis] - means) ** 2, axis=0) / effective_counts
			sigmas = np.sqrt(np.maximum(variances, sigma_min ** 2))

		return weights, means, sigmas, log_likelihood, converged, n_iter
