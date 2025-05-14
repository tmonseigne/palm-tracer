""" Fichier des tests pour l'utilisation des DLL. """

from pathlib import Path

import pytest

from palm_tracer._tests.Utils import *
from palm_tracer.Processing import Tracking
from palm_tracer.Tools import print_warning

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
@pytest.mark.skipif(is_not_dll_friendly(), reason="DLL uniquement sur Windows")
def test_tracking():
	"""Test basique sur le tracking."""
	tracking = Tracking()
	file = "stack"
	for watershed in [True, False]:
		for gaussian in range(5):
			suffix = get_loc_suffix(gaussian, watershed)
			suffix_trc = suffix + "-" + get_trc_suffix()

			path = Path(f"{INPUT_DIR}/ref/{file}-localizations-{suffix}.csv")
			if path.exists() and path.is_file():
				localizations = pd.read_csv(path)
				tracks = tracking.run(localizations, max_distance, min_life, decrease, cost_birth)
				if save_output: tracks.to_csv(f"{OUTPUT_DIR}/{file}-tracking-{suffix_trc}.csv", index=False)

				assert len(tracks) > 0, "Aucun Tracking trouvé"

				path = Path(f"{INPUT_DIR}/ref/{file}-tracking-{suffix_trc}.csv")
				if path.exists() and path.is_file():
					print(f"Comparaison avec : '{path}'")
					ref = pd.read_csv(path)
					assert compare_points(tracks, ref, group_cols=["Track"]), f"Test invalide pour les paramètres {suffix_trc}"
			else:
				print_warning(f"Fichier de localisations '{path}' indisponible.")
	assert True
