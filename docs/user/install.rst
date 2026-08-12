Installation
=====================================

.. _install_page:

.. role:: python(code)
   :language: python

.. role:: console(code)
   :language: console

.. |powershell| image:: /_static/img/Powershell.svg
   :height: 1.2em
   :alt: PowerShell

.. |terminal| image:: /_static/img/Terminal.svg
   :height: 1.2em
   :alt: Terminal

Ce guide vous aidera à installer le projet étape par étape.

.. important::
   | Toutes les lignes de commandes décrites sont effectuées à partir de |powershell| :console:`PowerShell` sous **Windows**.
   | De préférence, le terminal doit être lancé en mode **administrateur** pour éviter des problèmes de droits, dans le cas contraire, il est possible que des blocages apparaissent.
   | Si vous êtes sur le terminal |terminal| :console:`cmd` ou un autre système d'exploitation, des différences peuvent apparaitre. (Ex : `$env:...` devient `export ...`)


Étape 1 : Téléchargement de PalmTracer
----------------------------------------

Deux méthodes sont possibles pour récupérer le projet **PalmTracer**.
Si vous utilisez déjà **Git**, la première méthode est recommandée, car elle facilite le suivi des mises à jour.
Une `(très) courte introduction à Git <https://tmonseigne.github.io/Intro_Git/>`_ est disponible si vous souhaitez débuter avec Git.
Sinon, vous pouvez télécharger une archive ZIP.

Méthode 1 (recommandée) : via Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si Git (ou toute interface graphique utilisant git) est installé sur votre machine, clonez simplement le dépôt :

.. code-block:: powershell

   cd C:\ # Pour installer le dépôt à la racine, mais vous pouvez le mettre où vous voulez
   git clone https://github.com/tmonseigne/palm-tracer.git

Le dossier :file:`palm-tracer` sera alors créé dans le répertoire courant.

Méthode 2 : téléchargement manuel (ZIP)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `Téléchargez directement l'archive ZIP de PalmTracer <https://github.com/tmonseigne/palm-tracer/archive/refs/heads/master.zip>`_.
2. Extrayez l'archive dans un dossier accessible (par exemple, :file:`C:\\palm-tracer`). Vous devez avoir ensuite plusieurs dossiers et fichiers :file:`palm_tracer, docs, README.md...`.
   Ils ont peut-être été mis dans un sous-dossier :file:`palm-tracer-master` et doivent être remonté d'un cran.


Étape 2 : Installation de Python et des éléments additionnels
------------------------------------------------------------------------

1. Téléchargez la dernière version de Python 64-bit compatible depuis le `site officiel <https://www.python.org/downloads/>`_ (`Python 3.14 <https://www.python.org/downloads/latest/python3.14/>`_).
2. Pendant l'installation, assurez-vous de cocher l'option **Add Python to PATH**.
   Installer pour tout les utilisateurs est recommandé, mais pas obligatoire. L'installation peut prendre quelques minutes.
3. Une fois installé, vérifiez que Python fonctionne :

   - Ouvrez un terminal ou une invite de commande (|powershell| :console:`PowerShell` sur Windows).
   - Tapez la commande suivante :console:`python --version` et appuyez sur **Entrée**

.. note::
   Vous devriez voir une version de Python (par exemple, :console:`Python 3.x.x`).

   **Attention** : Si Python a changé de version récemment, certaines bibliothèques peuvent ne plus être compatibles.
   Ex : Il a fallu attendre 8 mois après la sortie de python 3.14 pour que Napari soit compatible.

4. Les différentes bibliothèques nécessitent parfois des éléments additionnels pour fonctionner :

   - `Build Tools for Visual Studio <https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/>`_. Pendant l'installation, assurez-vous de cocher **C++ build tools**
   - vcredist : celui-ci sera installé avec **Build Tools for Visual Studio**.


Étape 3 (Optionnelle) : Création d'un environnement virtuel
------------------------------------------------------------------------

Un environnement virtuel permet de gérer les dépendances du projet de manière isolée.

1. Ouvrez un terminal ou une invite de commande (:console:`PowerShell` sur Windows) dans le dossier où vous avez extrait les fichiers du projet.
   Exemple pour :file:`C:\\palm-tracer`. Ouvrez le terminal et tapez la commande suivante  :console:`cd C:\\palm_tracer` et appuyez sur **Entrée**
2. Créez un environnement virtuel avec la commande suivante :console:`python -m venv venv`
3. Activez l'environnement virtuel :

   - Sous Windows : :console:`.\\venv\\Scripts\\activate`
   - Sous macOS/Linux : :console:`source venv/bin/activate`

4. Vous verrez maintenant :console:`(venv)` au début de votre invite de commande, indiquant que l'environnement virtuel est actif.


Étape 4 : Installation du plugin
------------------------------------------------------------------------

1. Ouvrez un terminal ou une invite de commande (|powershell| :console:`PowerShell` sur Windows) dans le dossier où vous avez extrait les fichiers du projet.
   Exemple pour :file:`C:\\palm-tracer`. Ouvrez le terminal et tapez la commande suivante  :console:`cd C:\\palm_tracer` et appuyez sur **Entrée**
2. Assurez-vous que l'environnement virtuel est activé si vous le souhaitez (voir Étape 3).
3. Installez les dépendances nécessaires avec la commande :

.. code-block:: powershell

   $env:SETUPTOOLS_SCM_PRETEND_VERSION_FOR_PALM_TRACER = "1.4.0" # Parfois, il est nécessaire de forcer la version de setuptools_scm pour éviter des erreurs d'installation.
   python -m pip install -e .[testing,documentation]


Étape 5 : Vérification de l'installation en lançant le plugin
------------------------------------------------------------------------

1. Si vous avez créé un environnement virtuel, assurez-vous qu'il est activé (voir Étape 3).
2. Lancez Napari avec la commande : :console:`napari`
3. Activez le plugin dans Napari : :menuselection:`Plugins --> PALM Tracer --> PALM Tracer`
4. Vous pouvez également lancer Napari avec le plugin directement activé via la commande : :console:`napari -w palm-tracer`

Étape 6 (Optionnelle) : Supprimer la mise à l'échelle Windows
------------------------------------------------------------------------
Napari utilise QT et celui-ci est paramétré sur la mise à l'échelle automatique de Windows qui permet, notamment, d'agrandir l'interface sur les petits écrans ayant une résolution élevée.
Cela peut devenir parfois gênant avec une interface démesurée, il est possible de modifier ce comportement.

1. Ouvrez un terminal ou une invite de commande (|powershell| :console:`PowerShell` sur Windows).
2. Lancez la commande :console:`$env:QT_AUTO_SCREEN_SCALE_FACTOR="0"` dans |powershell| :console:`PowerShell` sous Windows
   ou :console:`export QT_AUTO_SCREEN_SCALE_FACTOR=0` sous Linux et macOS.
3. Pour réactiver la mise à l'échelle, lancez la commande : :console:`Remove-Item Env:\\QT_AUTO_SCREEN_SCALE_FACTOR` dans |powershell| :console:`PowerShell` sous Windows
   ou :console:`unset QT_AUTO_SCREEN_SCALE_FACTOR` sous Linux et macOS.

C'est terminé ! 🎉 Vous avez installé et configuré le plugin avec succès.

FAQ
---

1. Pourquoi utiliser un environnement virtuel ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Pour éviter les conflits entre les dépendances de différents projets. Ou nécessaire lorsque vous n'avez pas les droits administrateur sur votre système.

2. Et si je n'ai pas :console:`pip install` ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Cela signifie que Python n'est pas bien installé. Reprenez l'Étape 1 et assurez-vous d'avoir ajouté Python au :console:`PATH`.

3. La commande :console:`napari` provoque une erreur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
La commande :console:`napari` peut provoquer une erreur malgré une installation réussie, il faut l'ajouter au :console:`PATH` (les variables d'environnement) de votre système.
Le chemin à ajouter est :file:`<Path_to_python>\\Scripts\napari.exe`.
Si vous n'avez pas les droits ou ne savez pas comment faire pour ajouter une variable d'environnement, vous pouvez tout de même lancer Napari avec la commande :console:`python -m napari` depuis le terminal ou l'invite de commande.

4. Pourquoi, certaines commandes me mettent une erreur pour me dire que je n'ai pas les autorisations nécessaires ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Certaines commandes nécessitent des droits administrateur. Il faut lancer le terminal en mode administrateur sous Windows.

5. Je dois tout recommencer à chaque mise à jour ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Si vous avez utilisé la commande :console:`python -m pip install -e .[testing,documentation]` remplacer les fichiers devrait mettre automatiquement à jour votre Napari.
Mais il est possible d'observer des blocages, dans ce cas, il est nécessaire de réinstaller le plugin avec la commande précédente.

6. Où puis-je trouver plus d'aide ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Consultez la documentation officielle de Python, Napari ou contactez le support du projet.
