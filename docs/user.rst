Guide de l'utilisateur de PALM Tracer
=====================================

.. role:: python(code)
   :language: python

.. role:: console(code)
   :language: console

Installation
------------

Ce guide vous aidera à installer le projet étape par étape.


Étape 1 : Téléchargement depuis GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Rendez-vous sur `la page GitHub du projet <https://github.com/tmonseigne/palm-tracer>`_.
2. Cliquez sur **Code** (le bouton vert).
3. Choisissez **Download ZIP** pour télécharger les fichiers du projet sur votre ordinateur.
4. Extrayez les fichiers dans un dossier accessible (par exemple, :console:`C:\\palm-tracer`).


Étape 2 : Installation de Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Téléchargez Python depuis le `site officiel <https://www.python.org/downloads/>`_.
2. Pendant l'installation, assurez-vous de cocher l'option **Add Python to PATH**.
3. Une fois installé, vérifiez que Python fonctionne :

   - Ouvrez un terminal ou une invite de commande (:console:`PowerShell` sur Windows).
   - Tapez la commande suivante :console:`python --version` et appuyez sur **Entrée**

.. note::
   Vous devriez voir une version de Python (par exemple, :console:`Python 3.x.x`).


Étape 3 : Création d'un environnement virtuel (optionnel)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Un environnement virtuel permet de gérer les dépendances du projet de manière isolée.

1. Ouvrez un terminal ou une invite de commande (:console:`PowerShell` sur Windows) dans le dossier où vous avez extrait les fichiers du projet.
   Exemple pour :console:`C:\\palm-tracer`. Ouvrez le terminal et tapez la commande suivante  :console:`cd C:\\palm_tracer` et appuyez sur **Entrée**
2. Créez un environnement virtuel avec la commande suivante :console:`python -m venv venv`
3. Activez l'environnement virtuel :

   - Sous Windows : :console:`.\\venv\\Scripts\\activate`
   - Sous macOS/Linux : :console:`source venv/bin/activate`

4. Vous verrez maintenant :console:`(venv)` au début de votre invite de commande, indiquant que l'environnement virtuel est actif.


Étape 4 : Installation du plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Ouvrez un terminal ou une invite de commande (:console:`PowerShell` sur Windows) dans le dossier où vous avez extrait les fichiers du projet.
   Exemple pour :console:`C:\\palm-tracer`. Ouvrez le terminal et tapez la commande suivante  :console:`cd C:\\palm_tracer` et appuyez sur **Entrée**
2. Assurez-vous que l'environnement virtuel est activé si vous le souhaitez (voir Étape 3).
3. Installez les dépendances nécessaires avec la commande : :console:`python -m pip install .[testing,documentation]`

.. note::
   Les éléments supplémentaires tels que testing installent :console:`Napari` entre autres éléments si vous ne l'aviez pas déjà.

Étape 5 : Lancement du plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Ouvrez un terminal ou une invite de commande (:console:`PowerShell` sur Windows) dans le dossier où vous avez extrait les fichiers du projet.
   Exemple pour :console:`C:\\palm-tracer`. Ouvrez le terminal et tapez la commande suivante  :console:`cd C:\\palm_tracer` et appuyez sur **Entrée**
2. Assurez-vous que l'environnement virtuel est activé si vous le souhaitez (voir Étape 3).
3. Lancez :console:`Napari` avec la commande : :console:`napari`

.. note::
   Si vous n'avez pas créé d'environnement virtuel, :console:`Napari` peut être lancé depuis n'importe où.

4. Activez le plugin dans :console:`Napari` : :menuselection:`Plugins --> PALM Tracer`

Étape 6 : Supprimer la mise à l'échelle de Napari
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Napari utilise QT et celui-ci est paramétré sur la mise à l'échelle automatique de Windows
qui permet, notamment, d'agrandir l'interface sur les petits écrans ayant une résolution élevée.
Cela peut devenir parfois gênant, il est possible de modifier ce comportement.

1. Ouvrez un terminal ou une invite de commande (:console:`PowerShell` sur Windows).
2. Lancez la commande :console:`$env:QT_AUTO_SCREEN_SCALE_FACTOR="0"` dans :console:`PowerShell` sous Windows
   ou :console:`export QT_AUTO_SCREEN_SCALE_FACTOR=0` sous Linux et macOS.
3. Pour réactiver la mise à l'échelle, lancez la commande : :console:`Remove-Item Env:\\QT_AUTO_SCREEN_SCALE_FACTOR` dans :console:`PowerShell` sous Windows
   ou :console:`unset QT_AUTO_SCREEN_SCALE_FACTOR` sous Linux et macOS.

C'est terminé ! 🎉 Vous avez installé et configuré le plugin avec succès.

Utilisation
-----------


FAQ
---

**1. Pourquoi utiliser un environnement virtuel ?**
Pour éviter les conflits entre les dépendances de différents projets. Ou nécessaire lorsque vous n'avez pas les droits administrateur sur votre système.

**2. Et si je n'ai pas `pip install` ?**
Cela signifie que Python n'est pas bien installé. Reprenez l'Étape 2 et assurez-vous d'avoir ajouté Python au `PATH`.

**3. Pourquoi, certaines commandes me mettent une erreur pour me dire que je n'ai pas les autorisations nécessaires ?**
Certaines commandes nécessitent des droits administrateur. Il faut lancer le terminal en mode administrateur sous Windows.

**4. Où puis-je trouver plus d'aide ?**
Consultez la documentation officielle de Python ou contactez le support du projet.
