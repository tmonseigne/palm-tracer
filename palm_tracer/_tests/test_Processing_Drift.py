"""Teste les fonctions d'extraction des billes et de correction de la dérive."""

import pytest

from palm_tracer.Processing.Drift import *
from palm_tracer.Processing.Drift import _assign_tracks_to_points_greedy  # Certains cas bizarres sont vérifiés directement et non en intégration.


##################################################
def test_extract_bead_bad_input():
	"""Vérifie la génération de l'extraction des billes avec des entrées incorrectes."""
	with pytest.raises(ValueError) as exception_info: extract_beads(pd.DataFrame(), max_distance=-1)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "max_distance must be strictly positive."

	df = pd.DataFrame([[1, 2], [3, 4]])
	with pytest.raises(ValueError) as exception_info: extract_beads(df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "Missing columns in data: ['Plane', 'X', 'Y', 'Z']."

	df = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]], columns=['Plane', 'X', 'Y', 'Z'])
	with pytest.raises(ValueError) as exception_info: extract_beads(df, is_3d=False)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "The planes are not consecutive: [1 5]."

	df = pd.DataFrame([[1, 2, 3, 4], [1, 6, 7, 8]], columns=['Plane', 'X', 'Y', 'Z'])
	with pytest.raises(ValueError) as exception_info: extract_beads(df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "We need at least 2 planes."

	res = extract_beads(pd.DataFrame())
	assert res.empty


##################################################
def test_extract_beads_no_match_returns_empty():
	"""Vérifie qu'aucun match directement."""
	df = pd.DataFrame([[1, 0, 0, 0], [2, 10, 10, 0], ], columns=["Plane", "X", "Y", "Z"], dtype="int32")
	res = extract_beads(df, max_distance=1, is_3d=False, strict=True)
	assert res.empty


##################################################
def test_assign_tracks_no_pairs():
	"""Vérifie le passage dans le cas particulier ou tous les éléments sont trop éloignés."""
	ind = np.array([[5, 5], [5, 5]], dtype=np.int32)  # n_points = 5 => p_j >= 5 => tout invalide
	dist = np.array([[0.1, 0.2], [0.3, 0.4]], dtype=np.float64)
	keep_t, keep_p = _assign_tracks_to_points_greedy(ind, dist, n_points=5)
	assert keep_t.size == 0
	assert keep_p.size == 0


##################################################
def test_assign_tracks_skip_used_track():
	"""Vérifie qu'un suivi avec 2 candidats valides ⇒ après avoir pris le 1er, le 2e déclenche used_tracks."""
	ind = np.array([[0, 1]], dtype=np.int32)  # 1 track, 2 candidats
	dist = np.array([[0.1, 0.2]], dtype=np.float64)
	keep_t, keep_p = _assign_tracks_to_points_greedy(ind, dist, n_points=2)
	assert keep_t.tolist() == [0]
	assert keep_p.tolist() == [0]


##################################################
def test_extract_beads():
	"""Vérifie la génération de l'extraction des billes."""
	df = pd.DataFrame([[1, 0, 0, 0], [1, 10, 10, 10], [1, 20, 20, 20], [1, 30, 30, 30], [1, 1, 1, 0],  # P1
					   [2, 1, 1, 0], [2, 11, 10, 10], [2, 20, 21, 20], [2, 31, 30, 30],  # .			 P2
					   [3, 1, 1, 0], [3, 12, 10, 10], [3, 20, 22, 20], [3, 31, 31, 30],  # .			 P3
					   [4, 1, 1, 0], [4, 13, 10, 10], [4, 20, 23, 20], [4, 30, 30, 00]],  # .			 P4
					  columns=['Plane', 'X', 'Y', 'Z'], dtype="int32")

	# Cas 2D 3 trajectoires sur les 4 possibles sont restantes (premiere et dernière colonne de points confondue).
	res = extract_beads(df, max_distance=2, is_3d=False)
	ref = pd.DataFrame([[1, 1, 1, 1, 0], [1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # .			Bille 1
						[2, 1, 10, 10, 10], [2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # .Bille 2
						[3, 1, 20, 20, 20], [3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20],  # .Bille 3
						[4, 1, 30, 30, 30], [4, 2, 31, 30, 30], [4, 3, 31, 31, 30], [4, 4, 30, 30, 00]],  # Bille 4
					   columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# Cas 3D 2 trajectoires sur les 4 possibles sont restantes (Bille 4 éliminée à cause du Z)
	res = extract_beads(df, max_distance=2, is_3d=True)
	ref = pd.DataFrame([[1, 1, 1, 1, 0], [1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # .			Bille 1
						[2, 1, 10, 10, 10], [2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # .Bille 2
						[3, 1, 20, 20, 20], [3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20]],  # Bille 3
					   columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# Cas où la distance maximum n'est pas respectée (strictement inférieure donc toutes les billes avec un rayon d'au moins 1 sont rejetées)
	res = extract_beads(df, max_distance=1, is_3d=False, strict=True)
	ref = pd.DataFrame([[1, 1, 1, 1, 0], [1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0]], columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# Cas où la distance maximum n'est pas respectée (non strictement inférieure donc toutes les billes avec un rayon de 1 sont conservées)
	res = extract_beads(df, max_distance=1, is_3d=False, strict=False)
	ref = pd.DataFrame([[1, 1, 1, 1, 0], [1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # .			Bille 1
						[2, 1, 10, 10, 10], [2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # .Bille 2
						[3, 1, 20, 20, 20], [3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20]],  # Bille 3
					   columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# Cas où on commence au plan 2
	df = pd.DataFrame([[2, 1, 1, 0], [2, 11, 10, 10], [2, 20, 21, 20], [2, 31, 30, 30],  # .P2
					   [3, 1, 1, 0], [3, 12, 10, 10], [3, 20, 22, 20], [3, 31, 31, 30],  # .P3
					   [4, 1, 1, 0], [4, 13, 10, 10], [4, 20, 23, 20], [4, 30, 30, 00]],  # P4
					  columns=['Plane', 'X', 'Y', 'Z'], dtype="int32")

	res = extract_beads(df, max_distance=2, is_3d=False)
	ref = pd.DataFrame([[1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # .			Bille 1
						[2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # .Bille 2
						[3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20],  # .Bille 3
						[4, 2, 31, 30, 30], [4, 3, 31, 31, 30], [4, 4, 30, 30, 00]],  # Bille 4
					   columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_remove_beads():
	"""Vérifie la suppression des billes."""
	df = pd.DataFrame([[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0],  # P1 : drift 0
					   [2, 0, 1, 0], [2, 1, 0, 0], [2, 1, 1, 0], [2, 1, 0, 0],  # .				P2 : drift [1, 2, 3]]
					   [3, 3, 1, 0], [3, 2, 0, 0], [3, 0, 2, 0], [3, 1, 1, 0],  # .				P3 : drift [2, 1, 0]]
					   [4, 1, 1, 2], [4, 3, 0, 0], [4, 0, 3, 0], [4, 0, 0, 0]],  # .			P4 : drift [-3, -2, -1]]
					  columns=['Plane', 'X', 'Y', 'Z'], dtype="int32")
	bead = pd.DataFrame([[1, 1, 1, 1, 1], [1, 2, 0, 1, 0], [1, 3, 3, 1, 0], [1, 4, 1, 1, 2]], columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")

	res = remove_beads(df, bead)
	ref = pd.DataFrame([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0],  # P1 : drift 0
						[2, 1, 0, 0], [2, 1, 1, 0], [2, 1, 0, 0],  # .				P2 : drift [1, 2, 3]]
						[3, 2, 0, 0], [3, 0, 2, 0], [3, 1, 1, 0],  # .				P3 : drift [2, 1, 0]]
						[4, 3, 0, 0], [4, 0, 3, 0], [4, 0, 0, 0]],  # .				P4 : drift [-3, -2, -1]]
					   columns=['Plane', 'X', 'Y', 'Z'], dtype="int32")
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	res = remove_beads(pd.DataFrame(), pd.DataFrame())
	assert res.empty


##################################################
def test_get_drift_bad_input():
	"""Vérifie la récupération du déplacement avec des entrées incorrectes."""
	res = get_drift(pd.DataFrame())
	assert res.empty

	df = pd.DataFrame([[1, 2], [3, 4]])
	with pytest.raises(ValueError) as exception_info: get_drift(df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "Missing columns in data: ['Bead', 'Plane', 'X', 'Y', 'Z']."

	df = pd.DataFrame([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]], columns=['Bead', 'Plane', 'X', 'Y', 'Z'])
	with pytest.raises(ValueError) as exception_info: get_drift(df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "The planes are not consecutive: [2 7]."

	df = pd.DataFrame([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]], columns=['Bead', 'Plane', 'X', 'Y', 'Z'])
	with pytest.raises(ValueError) as exception_info: get_drift(df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "We need at least 2 planes."


##################################################
def test_get_drift():
	"""Vérifie la récupération du déplacement."""
	df = pd.DataFrame([[1, 1, 1, 1, 0], [1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # .			   Bille 1
					   [2, 1, 10, 10, 10], [2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # .Bille 2
					   [3, 1, 20, 20, 20], [3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20],  # .Bille 3
					   [4, 1, 30, 30, 30], [4, 2, 31, 30, 30], [4, 3, 31, 31, 30], [4, 4, 30, 30, 00]],  # Bille 4
					  columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")

	res = get_drift(df, False)
	ref = pd.DataFrame([[2, 0.50, 0.25, 0], [3, 0.25, 0.50, 0], [4, 0, 0, 0]], columns=['Plane', 'X', 'Y', 'Z'], dtype=np.float64)
	assert res.astype(np.float64).equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	res = get_drift(df, True)
	ref = pd.DataFrame([[2, 0.50, 0.25, 0], [3, 0.25, 0.50, 0], [4, 0, 0, -7.5]], columns=['Plane', 'X', 'Y', 'Z'], dtype=np.float64)
	assert res.astype(np.float64).equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# Cas où on commence au plan 2
	df = pd.DataFrame([[1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # .		   Bille 1
					   [2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # .Bille 2
					   [3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20],  # .Bille 3
					   [4, 2, 31, 30, 30], [4, 3, 31, 31, 30], [4, 4, 30, 30, 00]],  # Bille 4
					  columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")
	res = get_drift(df, False)
	ref = pd.DataFrame([[3, 0.25, 0.50, 0], [4, 0, 0, 0]], columns=['Plane', 'X', 'Y', 'Z'], dtype=np.float64)
	assert res.astype(np.float64).equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_apply_drift_bad_input():
	"""Vérifie la récupération du déplacement avec des entrées incorrectes."""
	res = remove_drift(pd.DataFrame(), pd.DataFrame())
	assert res.empty

	df = pd.DataFrame([[1, 2], [3, 4]])
	with pytest.raises(ValueError) as exception_info: remove_drift(df, df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "Missing columns in data: ['Plane', 'X', 'Y', 'Z']."

	df2 = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]], columns=['Plane', 'X', 'Y', 'Z'])
	with pytest.raises(ValueError) as exception_info: remove_drift(df2, df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "Missing columns in data: ['Plane', 'X', 'Y', 'Z']."


##################################################
def test_remove_drift():
	"""Vérifie la suppression du drift."""
	df = pd.DataFrame([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0],  # P1 : drift 0
					   [2, 1, 1, 0], [2, 1, 0, 0], [2, 0, 1, 0], [2, 1, 0, 0],  # .				P2 : drift [1, 2, 3]]
					   [3, 1, 1, 0], [3, 2, 0, 0], [3, 0, 2, 0], [3, 1, 1, 0],  # .				P3 : drift [2, 1, 0]]
					   [4, 1, 1, 0], [4, 3, 0, 0], [4, 0, 3, 0], [4, 0, 0, 0]],  # .			P4 : drift [-3, -2, -1]]
					  columns=['Plane', 'X', 'Y', 'Z'], dtype="int32")
	drift = pd.DataFrame([[2, 1, 2, 3], [3, 2, 1, 0], [4, -3, -2, -1]], columns=['Plane', 'X', 'Y', 'Z'], dtype="int32")

	res = remove_drift(df, drift, True)
	ref = pd.DataFrame([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0],
						[2, 0, -1, -3], [2, 0, -2, -3], [2, -1, -1, -3], [2, 0, -2, -3],
						[3, -2, -2, -3], [3, -1, -3, -3], [3, -3, -1, -3], [3, -2, -2, -3],
						[4, 1, 0, -2], [4, 3, -1, -2], [4, 0, 2, -2], [4, 0, -1, -2]],
					   columns=['Plane', 'X', 'Y', 'Z'], dtype=np.float64)
	assert res.astype(np.float64).equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	res = remove_drift(df, drift, False)
	ref = pd.DataFrame([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0],
						[2, 0, -1, 0], [2, 0, -2, 0], [2, -1, -1, 0], [2, 0, -2, 0],
						[3, -2, -2, 0], [3, -1, -3, 0], [3, -3, -1, 0], [3, -2, -2, 0],
						[4, 1, 0, 0], [4, 3, -1, 0], [4, 0, 2, 0], [4, 0, -1, 0]],
					   columns=['Plane', 'X', 'Y', 'Z'], dtype=np.float64)
	assert res.astype(np.float64).equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_chain_drift():
	"""Vérifie l'enchaînement de la correction de Drift."""
	bead = pd.DataFrame([[1, 1, 1, 1, 1], [1, 2, 0, 1, 0], [1, 3, 1, 0, 0], [1, 4, 1, 1, 2]], columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype="int32")
	drift = get_drift(bead, True)

	new_bead = remove_drift(bead, drift, True)
	assert np.allclose(new_bead[["X", "Y", "Z"]].to_numpy(), 1)

	new_drift = get_drift(new_bead, True)
	assert np.allclose(new_drift[["X", "Y", "Z"]].to_numpy(), 0)


##################################################
def test_drift_correction():
	"""Vérifie le pipeline de la correction de Drift."""
	df = pd.DataFrame([[1, 0, 0, 0], [1, 10, 10, 10], [1, 20, 20, 20], [1, 30, 30, 30], [1, 1, 1, 0],  # P1
					   [2, 1, 1, 0], [2, 11, 10, 10], [2, 20, 21, 20], [2, 31, 30, 30],  # .			 P2
					   [3, 1, 1, 0], [3, 12, 10, 10], [3, 20, 22, 20], [3, 31, 31, 30],  # .			 P3
					   [4, 1, 1, 0], [4, 13, 10, 10], [4, 20, 23, 20], [4, 30, 30, 30]],  # .			 P4
					  columns=['Plane', 'X', 'Y', 'Z'], dtype="int32")
	_, res = drift_correction(df, max_distance=2)
	ref = pd.DataFrame([[1, 0, 0, 0], [1, 10, 10, 10], [1, 20, 20, 20], [1, 30, 30, 30], [1, 1, 1, 0],  # .			P1
						[2, 0.5, 0.75, 0], [2, 10.5, 9.75, 10], [2, 19.5, 20.75, 20], [2, 30.5, 29.75, 30],  # .	P2
						[3, 0.25, 0.25, 0], [3, 11.25, 9.25, 10], [3, 19.25, 21.25, 20], [3, 30.25, 30.25, 30],  # .P3
						[4, 0.25, 0.25, 0], [4, 12.25, 9.25, 10], [4, 19.25, 22.25, 20], [4, 29.25, 29.25, 30]],  # P4
					   columns=['Plane', 'X', 'Y', 'Z'], dtype=np.float64)
	assert res.astype(np.float64).equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"


##################################################
def test_median_filter_centered():
	"""Vérifie le lissage d'un drift."""
	# 1D
	df = np.array([10.0, 11.0, 50.0, 12.0, 13.0, 14.0])
	res = median_filter_centered(df, size=5)
	ref = np.array([11.0, 11.5, 12.0, 13.0, 13.5, 13.0])
	assert np.allclose(res, ref, atol=0), f"Résultat incorrect.\nAttendu : \n{ref}\nObtenu : \n{res}"

	# 2D
	df = np.array([[10.0, 100.0, 1000.0], [11.0, 101.0, 1001.0], [50.0, 102.0, 2000.0], [12.0, 103.0, 1003.0], [13.0, 104.0, 1004.0]])
	res = median_filter_centered(df, size=5)
	ref = np.array([[11, 101, 1001], [11.5, 101.5, 1002], [12, 102, 1003], [12.5, 102.5, 1003.5], [13, 103, 1004]])
	assert np.allclose(res, ref, atol=0), f"Résultat incorrect.\nAttendu : \n{ref}\nObtenu : \n{res}"

	# Bonnes dimensions, mais aucune ligne
	df = np.ones((0, 2))
	res = median_filter_centered(df)
	assert np.allclose(res, df, atol=0), f"Résultat incorrect.\nAttendu : \n{ref}\nObtenu : \n{res}"

	# Mauvaise taille de médiane
	df = np.ones((2, 2))
	with pytest.raises(ValueError) as exception_info: median_filter_centered(df, 4)

	# Tableau 3D
	df = np.ones((2, 2, 2))
	with pytest.raises(ValueError) as exception_info: median_filter_centered(df)
