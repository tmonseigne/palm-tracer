Tableaux et Indices
=========================

.. role:: python(code)
   :language: python

.. role:: console(code)
   :language: console

Les tableaux sont des structures fondamentales en algorithmie et en programmation scientifique.
En Python, ils sont principalement manipulés avec :console:`numpy`, qui offre une gestion optimisée des tableaux multidimensionnels (ou **tenseurs**).

Cette section explique comment interpréter les indices dans des tableaux 1D, 2D et 3D et leurs conventions d'affichage avec des exemples mathématiques et Python ainsi que quelques subtilités à prendre en compte.

Tableaux 1D : Vecteurs et Espaces
---------------------------------

Un tableau à une seule dimension est appelé **vecteur**. Il peut être représenté sous forme **horizontale** ou **verticale**. Chaque élément est indexé par un indice :math:`(i)` correspondant à sa position :

Mathématiquement, un vecteur ligne (:math:`V \in \mathbb{R}^{1 \times n}`\) s’écrit :

.. math::

	V = \begin{bmatrix} v_0 & v_1 & v_2 & \dots & v_{n-1} \end{bmatrix}

Un vecteur colonne (:math:`V \in \mathbb{R}^{n \times 1}`) s’écrit :

.. math::

	V = \begin{bmatrix} v_0 \\ v_1 \\ v_2 \\ \vdots \\ v_{n-1} \end{bmatrix}

En Python avec `numpy` :

.. code-block:: python

	import numpy as np

	vecteur = np.array([1, 2, 3, 4])
	print(vecteur.shape)  # (4,)
	print(vecteur)        # Affichage Ligne

	vecteur_colonne = vecteur[:, np.newaxis]  # Transformation en colonne
	print(vecteur_colonne.shape)              # (4, 1)
	print(vecteur_colonne)                    # Affichage Ligne

.. important::

	**Subtilité**

	En :console:`numpy`, un tableau de forme :math:`(n,)` est un vecteur sans deuxième dimension. Contrairement à un vecteur explicite de forme :math:`(1, n)` ou :math:`(n, 1)`, il ne se comporte pas toujours comme une matrice.


Tableaux 2D : Matrices
-----------------------

Un tableau 2D est une **matrice** (:math:`M \in \mathbb{R}^{m \times n}`), où chaque élément est référencé par un couple d'indices :math:`(i, j)`, représentant respectivement **la ligne** et **la colonne**.:

Mathématiquement, une matrice :math:`M` de taille :math:`m \times n` s’écrit :

.. math::

	M = \begin{bmatrix}
		 m_{0,0} & m_{0,1} & \dots & m_{0,n-1} \\
		 m_{1,0} & m_{1,1} & \dots & m_{1,n-1} \\
		 \vdots & \vdots & \ddots & \vdots \\
		 m_{m-1,0} & m_{m-1,1} & \dots & m_{m-1,n-1}
	\end{bmatrix}


En Python avec `numpy` :

.. code-block:: python

	import numpy as np

	matrice = np.array([[1, 2, 3], [4, 5, 6]])
	print(matrice)        # Affichage de la matrice
	print(matrice.shape)  # (2, 3) -> 2 lignes, 3 colonnes

.. important::

	**Attention : Coordonnées (x, y) vs Indices (i, j)**

	En informatique :

	- L’indice **i** représente la ligne (axe **Y**).
	- L’indice **j** représente la colonne (axe **X**).
	- Si on parle de **coordonnées cartésiennes** :math:`(x, y)`, l'ordre est inversé : :math:`x` correspond aux colonnes, :math:`y` aux lignes.
	- Donc, un point :math:`(x, y)` se trouve à l’indice :math:`(y, x)` dans un tableau.

	Exemple :

	.. code-block:: python

		import numpy as np

		matrice = np.array([[1, 2, 3], [4, 5, 6]])
		x, y = 1, 2             # Coordonnées classiques
		valeur = matrice[y, x]  # Correspondance (y, x) en indices numpy
		print(valeur)           # matrice[2,1]


Ordre des dimensions en mémoire (C vs Fortran)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La manière dont un tableau est stocké en mémoire peut affecter les performances :

- **Ordre C (row-major)** : Les éléments d'une ligne sont contigus en mémoire (par défaut en :console:`numpy`).
- **Ordre Fortran (column-major)** : Les éléments d'une colonne sont contigus en mémoire (par défaut dans des languages scientifiques tel que :console:`Matlab`, :console:`R`, :console:`Julia`).

Vérification :

.. code-block:: python

	import numpy as np

	A = np.array([[1, 2], [3, 4]], order='C')  # Row-major (C-contiguous)
	B = np.array([[1, 2], [3, 4]], order='F')  # Column-major (F-contiguous)

	print(f"A (Row-major) :\n{A}")
	print(f"Stockage mémoire : {A.ravel(order="K")}", )  # Affiche l'ordre réel en mémoire
	print(f"C-contiguous : {A.flags['C_CONTIGUOUS']}, F-contiguous : {A.flags['F_CONTIGUOUS']}")

	print(f"B (Column-major):\n{B}")
	print(f"Stockage mémoire : {B.ravel(order="K")}", )  # Affiche l'ordre réel en mémoire
	print(f"C-contiguous : {B.flags['C_CONTIGUOUS']}, F-contiguous : {B.flags['F_CONTIGUOUS']}")


Tableaux 3D : Tenseurs et Interprétation
----------------------------------------

Un tableau 3D, qui ajoute une profondeur (axe supplémentaire), représente un **tenseur**  (:math:`T \in \mathbb{R}^{m \times n \times l}`), où chaque élément est référencé par un triplet d'indices :math:`(i,j,k)`.
Il peut être vu comme une pile de matrices :

.. math::

	T =
	\begin{bmatrix}
		M_0 \\ M_1 \\ \vdots \\ M_{p-1}
	\end{bmatrix}

ou de façon explicite :

.. math::

	T[i, j, k] \quad \text{où } i, j, k \text{ sont respectivement les indices de profondeur, ligne et colonne}

En Python :

.. code-block:: python

	import numpy as np

	tenseur = np.zeros((3, 4, 5))  # 3 plans, 4 lignes, 5 colonnes
	print(tenseur.shape)  # (3, 4, 5)


Cas des images et conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Images RGB (Profondeur = 3)**
	- Une image RGB est souvent stockée sous la forme :math:`(hauteur, largeur, 3)`, où la dernière dimension représente les canaux **Rouge, Vert, Bleu**.

	.. code-block:: python

		import numpy as np

		image_rgb = np.random.randint(0, 256, (100, 200, 3), dtype=np.uint8)
		print(image_rgb.shape)  # (100, 200, 3)

2. **Images multi-canaux (TIFF, hyperspectral)**
	- Certaines images (TIFF) suivent une convention :math:`(plan, Y, X)` où :
		- **Plan** = différentes tranches de l'image (e.g., différentes tranches d’une image volumique)
		- **Y** = hauteur (lignes)
		- **X** = largeur (colonnes)

	.. code-block:: python

		import tifffile

		img_tiff = tifffile.imread("image.tiff")
		print(img_tiff.shape)  # (Nombre de plans, Hauteur, Largeur)

Visualisation d’un tenseur en perspective
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour mieux comprendre un tableau 3D , on peut écrire une notation matricielle en **perspective**, simulant une profondeur :

.. math::

	T =
	\begin{bmatrix}
	\begin{bmatrix}
		t_{0,0,0} & t_{0,0,1} & \dots & t_{0,0,n-1} \\
		t_{0,1,0} & t_{0,1,1} & \dots & t_{0,1,n-1} \\
	\end{bmatrix}, \quad
	\begin{bmatrix}
		t_{1,0,0} & t_{1,0,1} & \dots & t_{1,0,n-1} \\
		t_{1,1,0} & t_{1,1,1} & \dots & t_{1,1,n-1} \\
	\end{bmatrix}, \dots
	\end{bmatrix}

Cela permet d'afficher mentalement chaque **plan matriciel** séparément.


Conclusion
----------

Les tableaux sont des structures puissantes, mais il est essentiel de bien comprendre l’ordre des indices selon le contexte (mathématique, NumPy, images, etc.).
