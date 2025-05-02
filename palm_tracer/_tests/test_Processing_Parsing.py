""" Fichier des tests pour l'utilisation des DLL. """

import pytest

from palm_tracer.Processing.Parsing import *


##################################################
def test_rearrange_dataframe_columns():
	""" test de la fonction rearrange_dataframe_columns."""
	df = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Z": [7, 8, 9]})
	res = rearrange_dataframe_columns(df, ["Y"], True)
	assert res.columns.tolist() == ["Y", "X", "Z"], "Erreur dans la fonction rearrange_dataframe_columns."
	res = rearrange_dataframe_columns(df, ["Y"], False)
	assert res.columns.tolist() == ["Y"], "Erreur dans la fonction rearrange_dataframe_columns."
	assert pytest.raises(ValueError, rearrange_dataframe_columns, df, ["Alpha"], True)
