Installation
============

.. _install_page:

.. role:: console(code)
   :language: console

.. |windows| image:: /_static/img/Windows.svg
   :height: 1.2em
   :alt: Windows

.. |macos| image:: /_static/img/MacOS.svg
   :height: 1.2em
   :alt: MacOS

.. |linux| image:: /_static/img/Linux.svg
   :height: 1.2em
   :alt: Linux

.. |powershell| image:: /_static/img/Powershell.svg
   :height: 1.2em
   :alt: PowerShell

.. |terminal| image:: /_static/img/Terminal.svg
   :height: 1.2em
   :alt: Terminal

Récupérer PALM Tracer
---------------------

Téléchargez et extrayez l'`archive ZIP du projet <https://github.com/tmonseigne/palm-tracer/archive/refs/heads/master.zip>`_, ou clonez le dépôt avec Git.

.. code-block:: console

   git clone https://github.com/tmonseigne/palm-tracer.git

Le dossier du projet contient notamment :file:`pyproject.toml` et :file:`install.cmd`.

Installation automatique sous Windows
-------------------------------------

Double-cliquez sur :file:`install.cmd` et acceptez la demande de droits administrateur. Le script prépare Python et les outils de compilation Microsoft,
installe PALM Tracer directement dans l'interpréteur sélectionné, crée son raccourci sur le bureau et lance l'application.

.. note::
   L'installation des outils de compilation peut prendre plusieurs minutes et occuper plusieurs gigaoctets.
   En cas d'échec, consultez le journal :file:`palm-tracer-install.log` dans le dossier temporaire de Windows.

Installation manuelle
---------------------

Installez `Python <https://www.python.org/downloads/>`_ en version 64 bits, à partir de Python 3.12.
Sous |windows| Windows, cochez **Add Python to PATH** lors de l'installation. Si une dépendance doit être compilée,
installez les `Build Tools for Visual Studio <https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/>`_ avec la charge de travail C++.

Ouvrez un terminal (|powershell| :console:`PowerShell` sous Windows). Utilisez :console:`cd` pour vous placer dans le dossier du projet.
Par exemple, sous Windows, si vous avez extrait le projet dans :file:`C:\\Mon dossier\\palm-tracer`, tapez la commande suivante et appuyez sur **Entrée**.

.. code-block:: powershell

   cd "C:\Mon dossier\palm-tracer"

Remplacez le chemin de l'exemple par celui de votre dossier. Gardez les guillemets si le chemin contient des espaces.
Sous |macos| macOS ou |linux| Linux, utilisez la même commande avec votre chemin, par exemple :console:`cd "/chemin/vers/palm-tracer"`.
Vérifiez avec :console:`dir` sous Windows ou :console:`ls` sous macOS et Linux que :file:`pyproject.toml` apparaît dans la liste.
Après extraction du ZIP, ce fichier peut se trouver dans un sous-dossier :file:`palm-tracer-master`.

Vérifiez ensuite la version de Python.

.. code-block:: console

   python --version

Vous devriez voir une ligne de ce type.

.. code-block:: text

   Python 3.14.10

Le numéro affiché peut varier. Il faut Python 3.12 ou une version ultérieure. Sous macOS ou Linux, si :console:`python` est introuvable,
essayez :console:`python3 --version` et utilisez :console:`python3` dans les commandes Python du guide.

Environnement virtuel (facultatif)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Depuis le dossier du projet, créez un environnement avec :console:`python -m venv venv`, puis activez-le.

- Sous |windows| Windows dans |powershell| :console:`PowerShell`, exécutez :console:`.\venv\Scripts\Activate.ps1`.
- Sous |macos| macOS et |linux| Linux, exécutez :console:`source venv/bin/activate`.

L'invite du terminal affiche généralement :console:`(venv)`. Gardez ce terminal pour la suite. Si vous en ouvrez un autre, activez de nouveau l'environnement.

Installer le plugin
^^^^^^^^^^^^^^^^^^^

Depuis le dossier du projet, installez PALM Tracer pour l'interpréteur actif.

.. code-block:: console

   python -m pip install -e ".[testing,documentation]"

Une fois l’installation terminée, la commande :console:`python -m pip show palm-tracer` doit afficher les informations du paquet, dont son nom et sa version.

.. _launch_palmtracer:

Lancer PALM Tracer
------------------

Lancez Napari avec le plugin depuis l'environnement Python où vous l'avez installé.

.. code-block:: console

   napari -w palm-tracer

Si Napari est déjà ouvert, sélectionnez :menuselection:`Plugins --> PALM Tracer --> PALM Tracer`.

Raccourci sur le bureau (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dans |powershell| :console:`PowerShell`, exécutez cette commande depuis le dossier du projet.

.. code-block:: powershell

   powershell -NoProfile -ExecutionPolicy Bypass -File .\make_shortcut.ps1

Le raccourci ouvre PALM Tracer dans Napari et affiche les journaux dans une console.

FAQ
---

Pourquoi utiliser un environnement virtuel ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Il isole les dépendances de PALM Tracer de celles des autres projets. Il permet aussi d'installer les paquets Python dans un dossier où vous avez les droits d'écriture.

Que faire si Python ou pip est introuvable ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si :console:`python` est introuvable sous Windows, vérifiez que l'option **Add Python to PATH** a été cochée, puis ouvrez un nouveau |terminal| terminal.
Si Python fonctionne, vérifiez pip avec :console:`python -m pip --version`. Si Python signale que le module pip manque, essayez :console:`python -m ensurepip --upgrade`.
Sous Linux, vérifiez les paquets Python et pip de votre distribution si :console:`ensurepip` est indisponible.

Que faire si Napari ne démarre pas ou si le plugin n'apparaît pas ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si la commande :console:`napari` est introuvable, lancez :console:`python -m napari -w palm-tracer` depuis l'environnement où vous avez installé le plugin.
Si le plugin manque dans le menu, vérifiez son installation avec :console:`python -m pip show palm-tracer` dans ce même environnement.
Si Napari demande le nom du widget, utilisez :console:`napari -w palm-tracer "PALM Tracer"`.

Que faire si Windows refuse l'accès pendant l'installation ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

L'installation automatique et celle des outils de compilation Microsoft peuvent demander les droits administrateur.
Pour une installation manuelle avec un Python déjà disponible, placez le projet dans un dossier accessible en écriture et utilisez un environnement virtuel.

Dois-je réinstaller PALM Tracer après chaque mise à jour ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Avec l'installation en mode éditable (:console:`-e`), Napari charge le code depuis le dossier du projet. Après avoir mis à jour ce dossier, relancez Napari.
Si les dépendances ont changé, exécutez de nouveau la commande d'installation du plugin.

Que faire si l'interface est trop grande ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vérifiez d'abord la mise à l'échelle dans les paramètres d'affichage de votre système.
Sous Windows, pour essayer temporairement de désactiver la mise à l'échelle Qt, fermez Napari et lancez ces commandes dans |powershell| :console:`PowerShell`.

.. code-block:: powershell

   $env:QT_ENABLE_HIGHDPI_SCALING = "0"
   napari -w palm-tracer

Pour rétablir le réglage par défaut, fermez ce terminal ou exécutez ``Remove-Item Env:\QT_ENABLE_HIGHDPI_SCALING`` avant de relancer Napari.
`Mise à l'échelle dans Qt 6 <https://doc.qt.io/qt-6/highdpi.html#environment-variable-reference>`_

Où trouver de l'aide ?
^^^^^^^^^^^^^^^^^^^^^^

Consultez la `documentation de démarrage de Napari <https://napari.org/stable/getting_started/launch_napari.html>`_.
Si le problème concerne PALM Tracer, relevez le message d'erreur avant de contacter le support du projet.
