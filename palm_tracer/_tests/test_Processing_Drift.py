"""Fichier des tests pour la création de galeries."""
import pytest

from palm_tracer.Processing.Drift import *


##################################################
def test_extract_bead_bad_input():
	"""Test de la génération de l'extraction des billes."""
	with pytest.raises(ValueError) as exception_info: extract_beads(pd.DataFrame(), max_distance=-1)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "max_distance must be strictly positive."

	df = pd.DataFrame([[1, 2], [3, 4]])
	with pytest.raises(ValueError) as exception_info: extract_beads(df)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "Missing columns in data: ['Plane', 'X', 'Y', 'Z']"

	df = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]], columns=['Plane', 'X', 'Y', 'Z'])
	with pytest.raises(ValueError) as exception_info: extract_beads(df, is_3d=False)
	assert exception_info.type == ValueError
	assert str(exception_info.value) == "The planes are not consecutive from 1 to N: [1 5]"

	df = pd.DataFrame([[1, 2, 3, 4], [1, 6, 7, 8]], columns=['Plane', 'X', 'Y', 'Z'])
	res = extract_beads(df)
	assert res.empty

	res = extract_beads(pd.DataFrame())
	assert res.empty


##################################################
def test_extract_beads():
	"""Test de la génération de l'extraction des billes."""
	df = pd.DataFrame([[1, 0, 0, 0], [1, 10, 10, 10], [1, 20, 20, 20], [1, 30, 30, 30], [1, 1, 1, 0],  # P1
					   [2, 1, 1, 0], [2, 11, 10, 10], [2, 20, 21, 20], [2, 31, 30, 30], [2, 1, 1, 0],  # P4
					   [3, 1, 1, 0], [3, 12, 10, 10], [3, 20, 22, 20], [3, 31, 31, 30], [3, 1, 1, 0],  # P3
					   [4, 1, 1, 0], [4, 13, 10, 10], [4, 20, 23, 20], [4, 30, 31, 00], [4, 1, 1, 0],  # P4
					   ], columns=['Plane', 'X', 'Y', 'Z'], dtype=int)

	# Cas 2D 3 trajectoires sur les 4 possibles sont restantes (premiere et dernière colonne de points confondue).
	res = extract_beads(df, max_distance=2, is_3d=False)
	ref = pd.DataFrame([[1, 1, 1, 1, 0], [1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # Bead 1
						[2, 1, 10, 10, 10], [2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # Bead 2
						[3, 1, 20, 20, 20], [3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20],  # Bead 3
						[4, 1, 30, 30, 30], [4, 2, 31, 30, 30], [4, 3, 31, 31, 30], [4, 4, 30, 31, 00]  # Bead 4
						], columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype=int)
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# Cas 3D 2 trajectoires sur les 4 possibles sont restantes (Bille 4 éliminée à cause du Z)
	res = extract_beads(df, max_distance=2, is_3d=True)
	ref = pd.DataFrame([[1, 1, 1, 1, 0], [1, 2, 1, 1, 0], [1, 3, 1, 1, 0], [1, 4, 1, 1, 0],  # Bead 1
						[2, 1, 10, 10, 10], [2, 2, 11, 10, 10], [2, 3, 12, 10, 10], [2, 4, 13, 10, 10],  # Bead 2
						[3, 1, 20, 20, 20], [3, 2, 20, 21, 20], [3, 3, 20, 22, 20], [3, 4, 20, 23, 20]  # Bead 3
						], columns=['Bead', 'Plane', 'X', 'Y', 'Z'], dtype=int)
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"

	# Cas où la distance maximum n'est pas respectée (donc if not np.any(valid): return pd.DataFrame())
	res = extract_beads(df, max_distance=1, is_3d=False)
	print(res)
	ref = pd.DataFrame()
	assert res.equals(ref), f"Résultat incorrect.\tAttendu : {ref}\tObtenu : {res}"
