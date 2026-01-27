Test Report Main Computer
=========================

Environnement
-------------

.. list-table::

   * - Python
     - 3.13.9
   * - Platform
     - Windows-11-10.0.26200-SP0
   * - JAVA_HOME
     - C:\Program Files\OpenJDK\jdk-25
   * - System
     - Windows
   * - CPU
     - 13th Gen Intel(R) Core(TM) i9-13950HX (2.20 GHz - 24 Cores (32 Logical))
   * - RAM
     - 63.69 GB
   * - GPU
     - NVIDIA GeForce RTX 4090 Laptop GPU (Memory: 16376 MB)

Summary
-------

194 tests collected, 194 passed ✅, 0 failed ❌, 0 skipped ⏭️ in 0:01:23s on 27/01/2026 at 14:43:01

Monitoring
----------

.. raw:: html

   <div style="position: relative; width: 100%; height: 620px; max-width: 100%; margin: 0 0 1em 0; padding:0;">
     <iframe src="monitoring_main_computer.html"
             style="position: absolute; margin: 0; padding:0; width: 100%; height: 100%; border: none;">
     </iframe>
   </div>

Test Cases
----------

.. raw:: html

   <div class="test-page">

Palmtracer
^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Getter Localization
     - ✅
     - 238ms
   * - Getter Tracks
     - ✅
     - 125ms
   * - Getter Tracks Compute
     - ✅
     - 160ms
   * - Reset Result
     - ✅
     - 146ms
   * - Reset Filtered
     - ✅
     - 181ms
   * - Update Filtered
     - ✅
     - 424ms
   * - Load Bad Dll
     - ✅
     - 150ms
   * - Load Nothing
     - ✅
     - 343ms
   * - Load
     - ✅
     - 224ms
   * - Process No Input
     - ✅
     - 133ms
   * - Process Nothing
     - ✅
     - 204ms
   * - Process Bad Dll
     - ✅
     - 121ms
   * - Process Multiple Stack
     - ✅
     - 160ms
   * - Process Only Localization
     - ✅
     - 219ms
   * - Process Only Localization Spline Bad
     - ✅
     - 167ms
   * - Process Only Localization Spline
     - ✅
     - 211ms
   * - Process Only Tracking
     - ✅
     - 301ms
   * - Process Only Tracking Blinking
     - ✅
     - 349ms
   * - Process Only Tracks Compute
     - ✅
     - 588ms
   * - Process Only Visualization Hr
     - ✅
     - 329ms
   * - Process Only Visualization Graph
     - ✅
     - 735ms
   * - Process Only Gallery
     - ✅
     - 170ms
   * - Process All
     - ✅
     - 4.27s
   * - Process Filter Plan
     - ✅
     - 161ms
   * - Process Filter All Localization
     - ✅
     - 227ms
   * - Process Filter All Tracking
     - ✅
     - 682ms
   * - Process Filter All Tracks Compute
     - ✅
     - 750ms
   * - Process Filter Outside
     - ✅
     - 151ms
   * - Add Color
     - ✅
     - 174ms

.. raw:: html

   <details>
      <summary>Log Test : Update Filtered</summary>
      <pre>[27-01-2026 14:41:42] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144142.log<br>[27-01-2026 14:41:42] Commencer le traitement.<br>[27-01-2026 14:41:42] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:42] Paramètres sauvegardés.<br>[27-01-2026 14:41:42] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:42] Localisation activée.<br>[27-01-2026 14:41:42] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:42] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:42] 	Enregistrement du fichier de localisation filtré<br>[27-01-2026 14:41:42] Tracking activé.<br>[27-01-2026 14:41:42] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:42] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:42] 	Enregistrement du fichier de trajectoires filtré<br>[27-01-2026 14:41:42] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:42] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:42] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:42] 	Enregistrement du fichier de trajectoires filtré<br>[27-01-2026 14:41:42] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:42] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:42] Visualisation graphique désactivée.<br>[27-01-2026 14:41:42] Génération de la galerie désactivée.<br>[27-01-2026 14:41:42] Traitement terminé.<br>[27-01-2026 14:41:42] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144142.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Load Bad Dll</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Process non effectué car DLL manquantes.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Load Nothing</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier de paramètres valide à charger.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Load</summary>
      <pre>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:43] Paramètres sauvegardés.<br>[27-01-2026 14:41:43] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:43] Localisation activée.<br>[27-01-2026 14:41:43] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:43] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:43] Tracking désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:43] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:43] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:43] Visualisation graphique désactivée.<br>[27-01-2026 14:41:43] Génération de la galerie désactivée.<br>[27-01-2026 14:41:43] Traitement terminé.<br>[27-01-2026 14:41:43] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>Chargement du fichier de configuration 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\settings-20260127_144143.json'.<br>	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/localizations-20260127_144143.csv' chargé avec succès.<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/localizations_filtered-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/localizations_filtered-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_filtered-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_filtered-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking-reconnected-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking-reconnected-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_filtered_reconnected-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_filtered_reconnected-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_MSD-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_MSD-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_MSD-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_MSD-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_InstantD-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_InstantD-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_InstantD_filtered-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_InstantD_filtered-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_Fit-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_Fit-20260127_144143.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_Fit_filtered-20260127_144143.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_Fit_filtered-20260127_144143.csv'<br>	Pile chargé avec succès (taille : (10, 128, 256)).</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process No Input</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Nothing</summary>
      <pre>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:43] Paramètres sauvegardés.<br>[27-01-2026 14:41:43] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:43] Localisation désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:43] Tracking désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:43] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:43] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:43] Visualisation graphique désactivée.<br>[27-01-2026 14:41:43] Génération de la galerie désactivée.<br>[27-01-2026 14:41:43] Traitement terminé.<br>[27-01-2026 14:41:43] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:43] Paramètres sauvegardés.<br>[27-01-2026 14:41:43] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:43] Localisation désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:43] Tracking désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:43] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:43] Visualisation haute résolution activée.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pour la visualisation.<br>[27-01-2026 14:41:43] Visualisation graphique activée.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pour la visualisation de graphiques.<br>[27-01-2026 14:41:43] Génération de la galerie activée.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pour la génération d'une galerie.<br>[27-01-2026 14:41:43] Traitement terminé.<br>[27-01-2026 14:41:43] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:43] Paramètres sauvegardés.<br>[27-01-2026 14:41:43] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:43] Localisation désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:43] Tracking désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:43] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:43] Visualisation haute résolution activée.<br>[27-01-2026 14:41:43] 	Aucune donnée de trajectoires pour la visualisation.<br>[27-01-2026 14:41:43] Visualisation graphique activée.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pour la visualisation de graphiques.<br>[27-01-2026 14:41:43] Génération de la galerie activée.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pour la génération d'une galerie.<br>[27-01-2026 14:41:43] Traitement terminé.<br>[27-01-2026 14:41:43] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:43] Paramètres sauvegardés.<br>[27-01-2026 14:41:43] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:43] Localisation désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:43] Tracking désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:43] Calcul sur les trajectoires activé.<br>[27-01-2026 14:41:43] 	Aucune donnée de tracking calculée, aucun calcul supplémentaire ne peut être effectué.<br>[27-01-2026 14:41:43] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:43] Visualisation graphique désactivée.<br>[27-01-2026 14:41:43] Génération de la galerie désactivée.<br>[27-01-2026 14:41:43] Traitement terminé.<br>[27-01-2026 14:41:43] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:43] Paramètres sauvegardés.<br>[27-01-2026 14:41:43] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:43] Localisation désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:43] Tracking activé.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation calculée, aucun calcul supplémentaire ne peut être effectué.<br>[27-01-2026 14:41:43] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:43] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:43] Visualisation graphique désactivée.<br>[27-01-2026 14:41:43] Génération de la galerie désactivée.<br>[27-01-2026 14:41:43] Traitement terminé.<br>[27-01-2026 14:41:43] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Bad Dll</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Process non effectué car DLL manquantes.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Multiple Stack</summary>
      <pre>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:43] Paramètres sauvegardés.<br>[27-01-2026 14:41:43] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:43] Localisation désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:43] Tracking désactivé.<br>[27-01-2026 14:41:43] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:43] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:43] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:43] Visualisation graphique désactivée.<br>[27-01-2026 14:41:43] Génération de la galerie désactivée.<br>[27-01-2026 14:41:43] Traitement terminé.<br>[27-01-2026 14:41:43] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_quadrant_PALM_Tracer/log-20260127_144143.log<br>[27-01-2026 14:41:43] Commencer le traitement.<br>[27-01-2026 14:41:43] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_quadrant_PALM_Tracer<br>[27-01-2026 14:41:44] Paramètres sauvegardés.<br>[27-01-2026 14:41:44] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:44] Localisation désactivé.<br>[27-01-2026 14:41:44] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:44] Tracking désactivé.<br>[27-01-2026 14:41:44] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:44] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:44] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:44] Visualisation graphique désactivée.<br>[27-01-2026 14:41:44] Génération de la galerie désactivée.<br>[27-01-2026 14:41:44] Traitement terminé.<br>[27-01-2026 14:41:44] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_quadrant_PALM_Tracer/log-20260127_144143.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Localization</summary>
      <pre>[27-01-2026 14:41:44] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144144.log<br>[27-01-2026 14:41:44] Commencer le traitement.<br>[27-01-2026 14:41:44] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:44] Paramètres sauvegardés.<br>[27-01-2026 14:41:44] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:44] Localisation activée.<br>[27-01-2026 14:41:44] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:44] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:44] Tracking désactivé.<br>[27-01-2026 14:41:44] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:44] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:44] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:44] Visualisation graphique désactivée.<br>[27-01-2026 14:41:44] Génération de la galerie désactivée.<br>[27-01-2026 14:41:44] Traitement terminé.<br>[27-01-2026 14:41:44] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144144.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Localization Spline Bad</summary>
      <pre>[27-01-2026 14:41:44] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144144.log<br>[27-01-2026 14:41:44] Commencer le traitement.<br>[27-01-2026 14:41:44] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:44] Paramètres sauvegardés.<br>[27-01-2026 14:41:44] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:44] Localisation activée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Localization Spline</summary>
      <pre>[27-01-2026 14:41:44] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144144.log<br>[27-01-2026 14:41:44] Commencer le traitement.<br>[27-01-2026 14:41:44] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:44] Paramètres sauvegardés.<br>[27-01-2026 14:41:44] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:44] Localisation activée.<br>[27-01-2026 14:41:44] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:44] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:44] Tracking désactivé.<br>[27-01-2026 14:41:44] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:44] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:44] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:44] Visualisation graphique désactivée.<br>[27-01-2026 14:41:44] Génération de la galerie désactivée.<br>[27-01-2026 14:41:44] Traitement terminé.<br>[27-01-2026 14:41:44] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144144.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Tracking</summary>
      <pre>[27-01-2026 14:41:44] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144144.log<br>[27-01-2026 14:41:44] Commencer le traitement.<br>[27-01-2026 14:41:44] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:44] Paramètres sauvegardés.<br>[27-01-2026 14:41:44] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:44] Localisation désactivé.<br>[27-01-2026 14:41:44] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:44] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144144.csv' chargé avec succès.<br>[27-01-2026 14:41:44] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:44] Tracking activé.<br>[27-01-2026 14:41:44] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:44] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:44] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:44] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:44] Visualisation graphique désactivée.<br>[27-01-2026 14:41:44] Génération de la galerie désactivée.<br>[27-01-2026 14:41:44] Traitement terminé.<br>[27-01-2026 14:41:44] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144144.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Tracking Blinking</summary>
      <pre>[27-01-2026 14:41:45] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Commencer le traitement.<br>[27-01-2026 14:41:45] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:45] Paramètres sauvegardés.<br>[27-01-2026 14:41:45] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:45] Localisation désactivé.<br>[27-01-2026 14:41:45] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:45] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144144.csv' chargé avec succès.<br>[27-01-2026 14:41:45] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:45] Tracking activé.<br>[27-01-2026 14:41:45] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:45] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:45] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:45] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:45] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:45] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:45] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:45] Visualisation graphique désactivée.<br>[27-01-2026 14:41:45] Génération de la galerie désactivée.<br>[27-01-2026 14:41:45] Traitement terminé.<br>[27-01-2026 14:41:45] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Tracks Compute</summary>
      <pre>[27-01-2026 14:41:45] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Commencer le traitement.<br>[27-01-2026 14:41:45] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:45] Paramètres sauvegardés.<br>[27-01-2026 14:41:45] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:45] Localisation désactivé.<br>[27-01-2026 14:41:45] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:45] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144144.csv' chargé avec succès.<br>[27-01-2026 14:41:45] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:45] Tracking désactivé.<br>[27-01-2026 14:41:45] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:45] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:45] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:45] Calcul sur les trajectoires activé.<br>[27-01-2026 14:41:45] 	Aucune métrique de sélectionnée, aucun calcul supplémentaire ne peut être effectué.<br>[27-01-2026 14:41:45] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:45] Visualisation graphique désactivée.<br>[27-01-2026 14:41:45] Génération de la galerie désactivée.<br>[27-01-2026 14:41:45] Traitement terminé.<br>[27-01-2026 14:41:45] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Commencer le traitement.<br>[27-01-2026 14:41:45] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:45] Paramètres sauvegardés.<br>[27-01-2026 14:41:45] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:45] Localisation désactivé.<br>[27-01-2026 14:41:45] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:45] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144144.csv' chargé avec succès.<br>[27-01-2026 14:41:45] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:45] Tracking désactivé.<br>[27-01-2026 14:41:45] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:45] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:45] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:45] Calcul sur les trajectoires activé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:45] 	Enregistrement du fichier de calcul des MSD.<br>[27-01-2026 14:41:45] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:45] Visualisation graphique désactivée.<br>[27-01-2026 14:41:45] Génération de la galerie désactivée.<br>[27-01-2026 14:41:45] Traitement terminé.<br>[27-01-2026 14:41:45] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Commencer le traitement.<br>[27-01-2026 14:41:45] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:45] Paramètres sauvegardés.<br>[27-01-2026 14:41:45] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:45] Localisation désactivé.<br>[27-01-2026 14:41:45] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:45] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144144.csv' chargé avec succès.<br>[27-01-2026 14:41:45] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:45] Tracking désactivé.<br>[27-01-2026 14:41:45] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:45] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:45] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:45] Calcul sur les trajectoires activé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:45] 	Enregistrement du fichier de calcul des diffusions instantannées.<br>[27-01-2026 14:41:45] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br>[27-01-2026 14:41:45] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:45] Visualisation graphique désactivée.<br>[27-01-2026 14:41:45] Génération de la galerie désactivée.<br>[27-01-2026 14:41:45] Traitement terminé.<br>[27-01-2026 14:41:45] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Commencer le traitement.<br>[27-01-2026 14:41:45] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:45] Paramètres sauvegardés.<br>[27-01-2026 14:41:45] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:45] Localisation désactivé.<br>[27-01-2026 14:41:45] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:41:45] Tracking désactivé.<br>[27-01-2026 14:41:45] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:41:45] Calcul sur les trajectoires activé.<br>[27-01-2026 14:41:45] 	Aucune donnée de tracking calculée, aucun calcul supplémentaire ne peut être effectué.<br>[27-01-2026 14:41:45] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:45] Visualisation graphique désactivée.<br>[27-01-2026 14:41:45] Génération de la galerie désactivée.<br>[27-01-2026 14:41:45] Traitement terminé.<br>[27-01-2026 14:41:45] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Commencer le traitement.<br>[27-01-2026 14:41:45] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:45] Paramètres sauvegardés.<br>[27-01-2026 14:41:45] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:45] Localisation activée.<br>[27-01-2026 14:41:45] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:45] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:45] Tracking activé.<br>[27-01-2026 14:41:45] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:45] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:45] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:45] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:45] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:45] Calcul sur les trajectoires activé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:45] 	Enregistrement du fichier de calcul des diffusions instantannées.<br>[27-01-2026 14:41:45] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br>[27-01-2026 14:41:45] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:45] Visualisation graphique désactivée.<br>[27-01-2026 14:41:45] Génération de la galerie désactivée.<br>[27-01-2026 14:41:45] Traitement terminé.<br>[27-01-2026 14:41:45] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Visualization Hr</summary>
      <pre>[27-01-2026 14:41:45] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:45] Commencer le traitement.<br>[27-01-2026 14:41:45] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:46] Paramètres sauvegardés.<br>[27-01-2026 14:41:46] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:46] Localisation désactivé.<br>[27-01-2026 14:41:46] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:46] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:46] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:46] Tracking désactivé.<br>[27-01-2026 14:41:46] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:46] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:46] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:46] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:46] Visualisation haute résolution activée.<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, Integrated Intensity).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, Sigma X).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, Sigma Y).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, Circularity).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, Theta).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, MSE XY).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, Z).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation haute résolution (x2, MSE Z).<br>[27-01-2026 14:41:46] Visualisation graphique désactivée.<br>[27-01-2026 14:41:46] Génération de la galerie désactivée.<br>[27-01-2026 14:41:46] Traitement terminé.<br>[27-01-2026 14:41:46] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144145.log<br>[27-01-2026 14:41:46] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144146.log<br>[27-01-2026 14:41:46] Commencer le traitement.<br>[27-01-2026 14:41:46] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:46] Paramètres sauvegardés.<br>[27-01-2026 14:41:46] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:46] Localisation désactivé.<br>[27-01-2026 14:41:46] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:46] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:46] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:46] Tracking désactivé.<br>[27-01-2026 14:41:46] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:46] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:46] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:46] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:46] Visualisation haute résolution activée.<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation des trajectoires haute résolution (x2, Track Number).<br>[27-01-2026 14:41:46] 		Calcul sur les trajectoires à effectuer pour définir une couleur lors de la visualisation.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:46] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation des trajectoires haute résolution (x2, Length).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation des trajectoires haute résolution (x2, Instant D).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation des trajectoires haute résolution (x2, MSD).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation des trajectoires haute résolution (x2, Total Intensity).<br>[27-01-2026 14:41:46] Visualisation graphique désactivée.<br>[27-01-2026 14:41:46] Génération de la galerie désactivée.<br>[27-01-2026 14:41:46] Traitement terminé.<br>[27-01-2026 14:41:46] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144146.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Visualization Graph</summary>
      <pre>[27-01-2026 14:41:46] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144146.log<br>[27-01-2026 14:41:46] Commencer le traitement.<br>[27-01-2026 14:41:46] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:46] Paramètres sauvegardés.<br>[27-01-2026 14:41:46] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:46] Localisation désactivé.<br>[27-01-2026 14:41:46] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:46] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:46] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:46] Tracking désactivé.<br>[27-01-2026 14:41:46] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:46] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:46] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:46] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:46] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:46] Visualisation graphique activée.<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation graphique (Histogram, Integrated Intensity).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation graphique (Plane Heat Map, Integrated Intensity).<br>[27-01-2026 14:41:46] 	Enregistrement de la visualisation graphique (Plane Violin, Integrated Intensity).<br>[27-01-2026 14:41:46] 	Annulation de la visualisation graphique : Sigma X uniforme.<br>[27-01-2026 14:41:46] 	Annulation de la visualisation graphique : Sigma Y uniforme.<br>[27-01-2026 14:41:46] 	Annulation de la visualisation graphique : Circularity uniforme.<br>[27-01-2026 14:41:46] 	Annulation de la visualisation graphique : Theta uniforme.<br>[27-01-2026 14:41:46] 	Annulation de la visualisation graphique : MSE XY uniforme.<br>[27-01-2026 14:41:46] 	Annulation de la visualisation graphique : Z uniforme.<br>[27-01-2026 14:41:46] 	Annulation de la visualisation graphique : MSE Z uniforme.<br>[27-01-2026 14:41:46] Génération de la galerie désactivée.<br>[27-01-2026 14:41:46] Traitement terminé.<br>[27-01-2026 14:41:46] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144146.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Gallery</summary>
      <pre>[27-01-2026 14:41:47] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144147.log<br>[27-01-2026 14:41:47] Commencer le traitement.<br>[27-01-2026 14:41:47] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:47] Paramètres sauvegardés.<br>[27-01-2026 14:41:47] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:47] Localisation désactivé.<br>[27-01-2026 14:41:47] 	Chargement d'une localisation pré-calculée.<br>[27-01-2026 14:41:47] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:47] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:47] Tracking désactivé.<br>[27-01-2026 14:41:47] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:47] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144145.csv' chargé avec succès.<br>[27-01-2026 14:41:47] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:47] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:47] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:47] Visualisation graphique désactivée.<br>[27-01-2026 14:41:47] Génération de la galerie activée.<br>[27-01-2026 14:41:47] 	Enregistrement de la galerie ({'ROI Size': 9, 'ROIs Per Line': 30}).<br>[27-01-2026 14:41:47] Traitement terminé.<br>[27-01-2026 14:41:47] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144147.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process All</summary>
      <pre>[27-01-2026 14:41:47] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144147.log<br>[27-01-2026 14:41:47] Commencer le traitement.<br>[27-01-2026 14:41:47] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:47] Paramètres sauvegardés.<br>[27-01-2026 14:41:47] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:47] Localisation activée.<br>[27-01-2026 14:41:47] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:47] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:47] Tracking activé.<br>[27-01-2026 14:41:47] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:47] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:47] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:47] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:47] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:47] Calcul sur les trajectoires activé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:47] 	Enregistrement du fichier de calcul des MSD.<br>[27-01-2026 14:41:47] 	Enregistrement du fichier de calcul des diffusions instantannées.<br>[27-01-2026 14:41:47] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br>[27-01-2026 14:41:47] 		Filtrage du fichier de calcul sur trajectoires 8 trajectoires au lieu de 104 : 96 suppression(s)<br>[27-01-2026 14:41:47] Visualisation haute résolution activée.<br>[27-01-2026 14:41:47] 	Enregistrement de la visualisation haute résolution (x2, Integrated Intensity).<br>[27-01-2026 14:41:47] Visualisation graphique activée.<br>[27-01-2026 14:41:47] 	Enregistrement de la visualisation graphique (Histogram, Integrated Intensity).<br>[27-01-2026 14:41:47] 	Enregistrement de la visualisation graphique (Plane Heat Map, Integrated Intensity).<br>[27-01-2026 14:41:47] 	Enregistrement de la visualisation graphique (Plane Violin, Integrated Intensity).<br>[27-01-2026 14:41:48] 	Enregistrement de la visualisation graphique (Histogram, Sigma X).<br>[27-01-2026 14:41:48] 	Enregistrement de la visualisation graphique (Plane Heat Map, Sigma X).<br>[27-01-2026 14:41:48] 	Enregistrement de la visualisation graphique (Plane Violin, Sigma X).<br>[27-01-2026 14:41:48] 	Enregistrement de la visualisation graphique (Histogram, Sigma Y).<br>[27-01-2026 14:41:48] 	Enregistrement de la visualisation graphique (Plane Heat Map, Sigma Y).<br>[27-01-2026 14:41:49] 	Enregistrement de la visualisation graphique (Plane Violin, Sigma Y).<br>[27-01-2026 14:41:49] 	Enregistrement de la visualisation graphique (Histogram, Circularity).<br>[27-01-2026 14:41:49] 	Enregistrement de la visualisation graphique (Plane Heat Map, Circularity).<br>[27-01-2026 14:41:49] 	Enregistrement de la visualisation graphique (Plane Violin, Circularity).<br>[27-01-2026 14:41:49] 	Enregistrement de la visualisation graphique (Histogram, Theta).<br>[27-01-2026 14:41:49] 	Enregistrement de la visualisation graphique (Plane Heat Map, Theta).<br>[27-01-2026 14:41:50] 	Enregistrement de la visualisation graphique (Plane Violin, Theta).<br>[27-01-2026 14:41:50] 	Enregistrement de la visualisation graphique (Histogram, MSE XY).<br>[27-01-2026 14:41:50] 	Enregistrement de la visualisation graphique (Plane Heat Map, MSE XY).<br>[27-01-2026 14:41:51] 	Enregistrement de la visualisation graphique (Plane Violin, MSE XY).<br>[27-01-2026 14:41:51] 	Annulation de la visualisation graphique : Z uniforme.<br>[27-01-2026 14:41:51] 	Annulation de la visualisation graphique : MSE Z uniforme.<br>[27-01-2026 14:41:51] Génération de la galerie activée.<br>[27-01-2026 14:41:51] 	Enregistrement de la galerie ({'ROI Size': 9, 'ROIs Per Line': 30}).<br>[27-01-2026 14:41:51] Traitement terminé.<br>[27-01-2026 14:41:51] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144147.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Filter Plan</summary>
      <pre>[27-01-2026 14:41:51] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log<br>[27-01-2026 14:41:51] Commencer le traitement.<br>[27-01-2026 14:41:51] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:51] Paramètres sauvegardés.<br>[27-01-2026 14:41:51] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:51] Localisation activée.<br>[27-01-2026 14:41:51] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:51] 		96 localisation(s) trouvée(s).<br>[27-01-2026 14:41:51] Tracking désactivé.<br>[27-01-2026 14:41:51] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:51] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144147.csv' chargé avec succès.<br>[27-01-2026 14:41:51] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:51] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:51] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:51] Visualisation graphique désactivée.<br>[27-01-2026 14:41:51] Génération de la galerie désactivée.<br>[27-01-2026 14:41:51] Traitement terminé.<br>[27-01-2026 14:41:51] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Filter All Localization</summary>
      <pre>[27-01-2026 14:41:51] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log<br>[27-01-2026 14:41:51] Commencer le traitement.<br>[27-01-2026 14:41:51] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:51] Paramètres sauvegardés.<br>[27-01-2026 14:41:51] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:51] Localisation activée.<br>[27-01-2026 14:41:51] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:51] 		414 localisation(s) trouvée(s).<br>[27-01-2026 14:41:51] 		Filtrage du fichier de localisation 0 localisations au lieu de 414 : 414 suppression(s)<br>[27-01-2026 14:41:51] Tracking désactivé.<br>[27-01-2026 14:41:51] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:51] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144147.csv' chargé avec succès.<br>[27-01-2026 14:41:51] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:51] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:51] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:51] Visualisation graphique désactivée.<br>[27-01-2026 14:41:51] Génération de la galerie désactivée.<br>[27-01-2026 14:41:51] Traitement terminé.<br>[27-01-2026 14:41:51] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log<br>[27-01-2026 14:41:51] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log<br>[27-01-2026 14:41:51] Commencer le traitement.<br>[27-01-2026 14:41:51] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:51] Paramètres sauvegardés.<br>[27-01-2026 14:41:51] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:51] Localisation activée.<br>[27-01-2026 14:41:51] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:51] 		414 localisation(s) trouvée(s).<br>[27-01-2026 14:41:51] 		Filtrage du fichier de localisation 0 localisations au lieu de 414 : 414 suppression(s)<br>[27-01-2026 14:41:51] 	Enregistrement du fichier de localisation filtré<br>[27-01-2026 14:41:51] Tracking désactivé.<br>[27-01-2026 14:41:51] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:41:51] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-reconnected-20260127_144147.csv' chargé avec succès.<br>[27-01-2026 14:41:51] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:41:51] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:51] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:51] Visualisation graphique désactivée.<br>[27-01-2026 14:41:51] Génération de la galerie désactivée.<br>[27-01-2026 14:41:51] Traitement terminé.<br>[27-01-2026 14:41:51] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Filter All Tracking</summary>
      <pre>[27-01-2026 14:41:51] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log<br>[27-01-2026 14:41:51] Commencer le traitement.<br>[27-01-2026 14:41:51] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:51] Paramètres sauvegardés.<br>[27-01-2026 14:41:51] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:51] Localisation activée.<br>[27-01-2026 14:41:51] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:51] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:51] Tracking activé.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:52] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:52] Visualisation graphique désactivée.<br>[27-01-2026 14:41:52] Génération de la galerie désactivée.<br>[27-01-2026 14:41:52] Traitement terminé.<br>[27-01-2026 14:41:52] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144151.log<br>[27-01-2026 14:41:52] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144152.log<br>[27-01-2026 14:41:52] Commencer le traitement.<br>[27-01-2026 14:41:52] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:52] Paramètres sauvegardés.<br>[27-01-2026 14:41:52] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:52] Localisation activée.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:52] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:52] Tracking activé.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] 		Filtrage du fichier de trajectoires 0 points au lieu de 455 : 455 suppression(s)<br>[27-01-2026 14:41:52] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] 		Filtrage du fichier de trajectoires 143 points au lieu de 455 : 312 suppression(s)<br>[27-01-2026 14:41:52] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:41:52] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:52] Visualisation graphique désactivée.<br>[27-01-2026 14:41:52] Génération de la galerie désactivée.<br>[27-01-2026 14:41:52] Traitement terminé.<br>[27-01-2026 14:41:52] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144152.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Filter All Tracks Compute</summary>
      <pre>[27-01-2026 14:41:52] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144152.log<br>[27-01-2026 14:41:52] Commencer le traitement.<br>[27-01-2026 14:41:52] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:52] Paramètres sauvegardés.<br>[27-01-2026 14:41:52] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:52] Localisation activée.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:52] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:52] Tracking activé.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] 		Filtrage du fichier de trajectoires 0 points au lieu de 455 : 455 suppression(s)<br>[27-01-2026 14:41:52] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] 		Filtrage du fichier de trajectoires 143 points au lieu de 455 : 312 suppression(s)<br>[27-01-2026 14:41:52] Calcul sur les trajectoires activé.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de calcul des MSD.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de calcul des diffusions instantannées.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br>[27-01-2026 14:41:52] 		Filtrage du fichier de calcul sur trajectoires 14 trajectoires au lieu de 39 : 25 suppression(s)<br>[27-01-2026 14:41:52] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:52] Visualisation graphique désactivée.<br>[27-01-2026 14:41:52] Génération de la galerie désactivée.<br>[27-01-2026 14:41:52] Traitement terminé.<br>[27-01-2026 14:41:52] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144152.log<br>[27-01-2026 14:41:52] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144152.log<br>[27-01-2026 14:41:52] Commencer le traitement.<br>[27-01-2026 14:41:52] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:52] Paramètres sauvegardés.<br>[27-01-2026 14:41:52] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:52] Localisation activée.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:52] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de localisation filtré<br>[27-01-2026 14:41:52] Tracking activé.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] 		Filtrage du fichier de trajectoires 0 points au lieu de 455 : 455 suppression(s)<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires filtré<br>[27-01-2026 14:41:52] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:52] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:52] 		Filtrage du fichier de trajectoires 143 points au lieu de 455 : 312 suppression(s)<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de trajectoires filtré<br>[27-01-2026 14:41:52] Calcul sur les trajectoires activé.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de calcul des MSD.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de calcul des diffusions instantannées.<br>[27-01-2026 14:41:52] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br>[27-01-2026 14:41:53] 		Filtrage du fichier de calcul sur trajectoires 14 trajectoires au lieu de 39 : 25 suppression(s)<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des MSD filtré.<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des diffusions instantannées filtré.<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des métriques de l'ajustement filtré.<br>[27-01-2026 14:41:53] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:53] Visualisation graphique désactivée.<br>[27-01-2026 14:41:53] Génération de la galerie désactivée.<br>[27-01-2026 14:41:53] Traitement terminé.<br>[27-01-2026 14:41:53] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144152.log<br>[27-01-2026 14:41:53] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144153.log<br>[27-01-2026 14:41:53] Commencer le traitement.<br>[27-01-2026 14:41:53] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:41:53] Paramètres sauvegardés.<br>[27-01-2026 14:41:53] Fichier Meta sauvegardé.<br>[27-01-2026 14:41:53] Localisation activée.<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:41:53] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de localisation filtré<br>[27-01-2026 14:41:53] Tracking activé.<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de trajectoires.<br>[27-01-2026 14:41:53] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:53] 		Filtrage du fichier de trajectoires 0 points au lieu de 455 : 455 suppression(s)<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de trajectoires filtré<br>[27-01-2026 14:41:53] 	Reconnexion des trajectoires après scintillement.<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de trajectoires reconnectées.<br>[27-01-2026 14:41:53] 		455 point(s) trouvé(s).<br>[27-01-2026 14:41:53] 		Filtrage du fichier de trajectoires 0 points au lieu de 455 : 455 suppression(s)<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de trajectoires filtré<br>[27-01-2026 14:41:53] Calcul sur les trajectoires activé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des MSD.<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des diffusions instantannées.<br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br>[27-01-2026 14:41:53] 		Filtrage du fichier de calcul sur trajectoires 0 trajectoires au lieu de 104 : 104 suppression(s)<br>[27-01-2026 14:41:53] Visualisation haute résolution désactivée.<br>[27-01-2026 14:41:53] Visualisation graphique désactivée.<br>[27-01-2026 14:41:53] Génération de la galerie désactivée.<br>[27-01-2026 14:41:53] Traitement terminé.<br>[27-01-2026 14:41:53] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144153.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Add Color</summary>
      <pre>[27-01-2026 14:41:53] 		Calcul sur les trajectoires à effectuer pour définir une couleur lors de la visualisation.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:41:53] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:53] 	Aucune donnée de tracking calculée, aucun calcul supplémentaire ne peut être effectué.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:41:53] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:53] 		Calcul sur les trajectoires à effectuer pour définir une couleur lors de la visualisation.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:41:53] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:41:53] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:53] 		Calcul sur les trajectoires à effectuer pour définir une couleur lors de la visualisation.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:41:53] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>[27-01-2026 14:41:53] 	Enregistrement du fichier de calcul des métriques de l'ajustement.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:41:53] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span></pre>
   </details>

Processing Astigmatism3D
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Get Z From Planes
     - ✅
     - 1ms
   * - Get Z From Step
     - ✅
     - 1ms
   * - Sigma Model
     - ✅
     - 1ms
   * - Model Validity
     - ✅
     - 2ms
   * - Model Projection Validity
     - ✅
     - 11ms

Processing Gallery
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Make Gallery
     - ✅
     - 6ms

Processing Grapher
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Get Fig
     - ✅
     - 353ms
   * - Blank
     - ✅
     - 40ms
   * - Histogram
     - ✅
     - 462ms
   * - Scatter
     - ✅
     - 307ms
   * - Astigmatism3D Curve
     - ✅
     - 60ms

Processing Palm
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Palm Dll Valid
     - ✅
     - 1ms
   * - Palm Cpu Image
     - ✅
     - 598ms
   * - Palm Cpu Stack
     - ✅
     - 3.14s
   * - Palm Cpu Stack Plane Selection
     - ✅
     - 188ms
   * - Palm Cpu Stack Dll Check Quadrant
     - ✅
     - 216ms
   * - Cpu Auto Threshold
     - ✅
     - 27ms
   * - Tracking
     - ✅
     - 4.70s
   * - Blinking Reconnection
     - ✅
     - 168ms
   * - Tracks Compute
     - ✅
     - 63ms
   * - Align
     - ✅
     - 528ms
   * - Wavelett
     - ✅
     - 34ms
   * - Astigmatism 3D Calibration
     - ✅
     - 5ms
   * - Astigmatism 3D Estimation
     - ✅
     - 7ms

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack Plane Selection</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-plane_select-103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 227 Points comparés, 227 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack Dll Check Quadrant</summary>
      <pre><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 269 Points comparés, 269 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_0_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 224 Points comparés, 224 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_1_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 223 Points comparés, 223 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_2_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 225 Points comparés, 225 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_3_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 222 Points comparés, 222 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_4_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 222 Points comparés, 222 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_0_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 214 Points comparés, 214 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_1_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 212 Points comparés, 212 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_2_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 217 Points comparés, 217 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_3_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 211 Points comparés, 211 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_4_1.0_0.0_7-5_2_10_0.5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 214 Points comparés, 214 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-0.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-1.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-2.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Compute</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-MSD-True.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-True.csv'<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-MSD-False.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-False.csv'<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-1.csv'<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-2.csv'<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-3.csv'<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Problème avec les identifiants des trajectoires, attention au filtrage</span><span style="font-weight: bold"></span></pre>
   </details>

Processing Parsing
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Get Meta
     - ✅
     - 3ms
   * - Get Max Point
     - ✅
     - 1ms
   * - Rearrange Dataframe Columns
     - ✅
     - 4ms
   * - Log10 Dataframe
     - ✅
     - 4ms
   * - Parse Irregular Array
     - ✅
     - 3ms
   * - Parse Result
     - ✅
     - 14ms
   * - Parse Localization For Tracking
     - ✅
     - 8ms

Processing Visualization
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Normalize Data
     - ✅
     - 1ms
   * - Render Hr Image
     - ✅
     - 22ms
   * - Render Hr Image Bad Input
     - ✅
     - 2ms
   * - Render Tracks Image
     - ✅
     - 15ms
   * - Render Tracks Image Bad Input
     - ✅
     - 3ms
   * - Render Roi
     - ✅
     - 33ms
   * - Render Roi Bad Input
     - ✅
     - 1ms
   * - Plot Histogram
     - ✅
     - 861ms
   * - Plot Histogram Bad Input
     - ✅
     - 121ms
   * - Plot Violin
     - ✅
     - 650ms
   * - Plot Violin Bad Input
     - ✅
     - 58ms
   * - Plot Heatmap
     - ✅
     - 335ms
   * - Plot Heatmap Bad Input
     - ✅
     - 56ms

Settings Groups
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Base Group
     - ✅
     - 120ms
   * - Batch
     - ✅
     - 146ms
   * - Batch Get Path
     - ✅
     - 196ms
   * - Batch Get Stacks
     - ✅
     - 156ms
   * - Calibration
     - ✅
     - 167ms
   * - Localization
     - ✅
     - 209ms
   * - Gaussian Fit
     - ✅
     - 147ms
   * - Spline Fit
     - ✅
     - 115ms
   * - Tracking
     - ✅
     - 127ms
   * - Gallery
     - ✅
     - 108ms
   * - Visualization Hr
     - ✅
     - 120ms
   * - Visualization Graph
     - ✅
     - 107ms
   * - Filtering
     - ✅
     - 130ms
   * - Filtering Gl
     - ✅
     - 115ms
   * - Filtering T
     - ✅
     - 119ms
   * - Tracks Blinking Reconnection
     - ✅
     - 118ms
   * - Tracks Computes
     - ✅
     - 110ms

.. raw:: html

   <details>
      <summary>Log Test : Batch</summary>
      <pre>- Activate : True<br>- Files : -1<br>- Mode : 0<br><br>{'Files': -1, 'Mode': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Batch Get Stacks</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Error lors de la concatenation des piles (elles seront traité indépendamment):<br>ValueError: all the input array dimensions except for the concatenation axis must match exactly, but along dimension 1, the array at index 0 has size 128 and the array at index 1 has size 256</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Calibration</summary>
      <pre>- Activate : True<br>- Pixel Size : 0.32<br>- Exposure : 0.05<br>- Intensity : 0.012<br><br>{'Pixel Size': 0.32, 'Exposure': 0.05, 'Intensity': 0.012}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Localization</summary>
      <pre>- Activate : True<br>- Preview : True<br>- Threshold : 90.0<br>- Auto Threshold : True<br>- ROI Shape : 0<br>- ROI Size : 7<br>- Watershed : True<br>- Fit : 0<br>- Gaussian Fit :<br>  - Activate : True<br>  - Mode : 0<br>  - Sigma : 1.0<br>  - Theta : 0.0<br>- Spline Fit :<br>  - Activate : True<br>  - Sensor : 0<br>  - Variance Map : <br>  - File : <br><br>{'Preview': True, 'Threshold': 90.0, 'Auto Threshold': True, 'ROI Shape': 0, 'ROI Size': 7, 'Watershed': True, 'Fit': 0, 'Gaussian Fit Mode': 0, 'Gaussian Fit Sigma': 1.0, 'Gaussian Fit Theta': 0.0, 'Spline Fit Sensor': 0, 'Spline Fit Variance Map': '', 'Spline Fit File': ''}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gaussian Fit</summary>
      <pre>- Activate : True<br>- Mode : 2<br>- Sigma : 1.0<br>- Theta : 0.0<br><br>{'Mode': 2, 'Sigma': 1.0, 'Theta': 0.0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Spline Fit</summary>
      <pre>- Activate : True<br>- Sensor : 1<br>- Variance Map : <br>- File : <br><br>{'Sensor': 1, 'Variance Map': '', 'File': ''}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking</summary>
      <pre>- Activate : True<br>- Max Distance : 2.0<br>- Blinking Reconnection :<br>  - Activate : False<br>  - Mode : 0<br>  - Max Duration : 1<br>  - Max Speed : 1.0<br><br>{'Max Distance': 2.0, 'Blinking Reconnection Mode': 0, 'Blinking Reconnection Max Duration': 1, 'Blinking Reconnection Max Speed': 1.0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gallery</summary>
      <pre>- Activate : True<br>- ROI Size : 11<br>- ROIs Per Line : 30<br><br>{'ROI Size': 11, 'ROIs Per Line': 30}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Visualization Hr</summary>
      <pre>- Activate : True<br>- Ratio : 1<br>- Type : 0<br>- Source L : 1<br>- Source T : 1<br><br>{'Ratio': 1, 'Type': 0, 'Source L': 1, 'Source T': 1}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Visualization Graph</summary>
      <pre>- Activate : True<br>- Mode : 1<br>- Source : 0<br><br>{'Mode': 1, 'Source': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering</summary>
      <pre>- Activate : True<br>- Save : True<br>- Plane : [1, 100]<br>- Localization :<br>  - Activate : True<br>  - Intensity : [0, 100]<br>  - Sigma X : [0.0, 1.0]<br>  - Sigma Y : [0.0, 1.0]<br>  - Circularity : [0.0, 1.0]<br>  - Theta : [-1.0, 1.0]<br>  - Z : [-1.0, 1.0]<br>  - MSE XY : [0.0, 1.0]<br>  - MSE Z : [0.0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Length : [1, 100]<br>  - Instant D : [-1.0, 1.0]<br>  - D Coeff : [-1.0, 1.0]<br>  - Alpha : [-1.0, 1.0]<br>  - Speed : [0.0, 1.0]<br>  - Confinement : [-1.0, 1.0]<br><br>{'Save': True, 'Plane': [1, 100], 'Localization Intensity': [0, 100], 'Localization Sigma X': [0.0, 1.0], 'Localization Sigma Y': [0.0, 1.0], 'Localization Circularity': [0.0, 1.0], 'Localization Theta': [-1.0, 1.0], 'Localization Z': [-1.0, 1.0], 'Localization MSE XY': [0.0, 1.0], 'Localization MSE Z': [0.0, 1.0], 'Tracks Length': [1, 100], 'Tracks Instant D': [-1.0, 1.0], 'Tracks D Coeff': [-1.0, 1.0], 'Tracks Alpha': [-1.0, 1.0], 'Tracks Speed': [0.0, 1.0], 'Tracks Confinement': [-1.0, 1.0]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering Gl</summary>
      <pre>- Activate : True<br>- Intensity : [2, 9]<br>- Sigma X : [0.0, 1.0]<br>- Sigma Y : [0.0, 1.0]<br>- Circularity : [0.0, 1.0]<br>- Theta : [-1.0, 1.0]<br>- Z : [-1.0, 1.0]<br>- MSE XY : [0.0, 1.0]<br>- MSE Z : [0.0, 1.0]<br><br>{'Intensity': [2, 9], 'Sigma X': [0.0, 1.0], 'Sigma Y': [0.0, 1.0], 'Circularity': [0.0, 1.0], 'Theta': [-1.0, 1.0], 'Z': [-1.0, 1.0], 'MSE XY': [0.0, 1.0], 'MSE Z': [0.0, 1.0]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering T</summary>
      <pre>- Activate : True<br>- Length : [2, 3]<br>- Instant D : [-1.0, 1.0]<br>- D Coeff : [-1.0, 1.0]<br>- Alpha : [-1.0, 1.0]<br>- Speed : [0.0, 1.0]<br>- Confinement : [-1.0, 1.0]<br><br>{'Length': [2, 3], 'Instant D': [-1.0, 1.0], 'D Coeff': [-1.0, 1.0], 'Alpha': [-1.0, 1.0], 'Speed': [0.0, 1.0], 'Confinement': [-1.0, 1.0]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Blinking Reconnection</summary>
      <pre>- Activate : True<br>- Mode : 1<br>- Max Duration : 1<br>- Max Speed : 1.0<br><br>{'Mode': 1, 'Max Duration': 1, 'Max Speed': 1.0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Computes</summary>
      <pre>- Activate : True<br>- MSD : True<br>- Instant Diffusion : False<br>- Fit Length : 4<br>- 3D : False<br>- Log Scale : False<br>- Fit : 0<br><br>{'MSD': True, 'Instant Diffusion': False, 'Fit Length': 4, '3D': False, 'Log Scale': False, 'Fit': 0}</pre>
   </details>

Settings Settings
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Settings
     - ✅
     - 153ms
   * - Settings Group Getter
     - ✅
     - 122ms
   * - Settings Signal
     - ✅
     - 135ms

.. raw:: html

   <details>
      <summary>Log Test : Settings</summary>
      <pre>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : -1<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 0.32<br>    - Exposure : 0.05<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - Auto Threshold : True<br>    - ROI Shape : 0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Fit : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 0<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>    - Spline Fit :<br>      - Activate : True<br>      - Sensor : 0<br>      - Variance Map : <br>      - File : <br>  - Tracking :<br>    - Activate : False<br>    - Max Distance : 1.0<br>    - Blinking Reconnection :<br>      - Activate : False<br>      - Mode : 0<br>      - Max Duration : 1<br>      - Max Speed : 1.0<br>  - TracksCompute :<br>    - Activate : False<br>    - MSD : False<br>    - Instant Diffusion : False<br>    - Fit Length : 4<br>    - 3D : False<br>    - Log Scale : False<br>    - Fit : 0<br>  - Gallery :<br>    - Activate : False<br>    - ROI Size : 9<br>    - ROIs Per Line : 30<br>  - VisualizationHR :<br>    - Activate : False<br>    - Ratio : 2<br>    - Type : 0<br>    - Source L : 1<br>    - Source T : 1<br>  - VisualizationGraph :<br>    - Activate : False<br>    - Mode : 0<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Save : False<br>    - Plane : [1, 100]<br>    - Localization :<br>      - Activate : True<br>      - Intensity : [0, 100]<br>      - Sigma X : [0.0, 1.0]<br>      - Sigma Y : [0.0, 1.0]<br>      - Circularity : [0.0, 1.0]<br>      - Theta : [-1.0, 1.0]<br>      - Z : [-1.0, 1.0]<br>      - MSE XY : [0.0, 1.0]<br>      - MSE Z : [0.0, 1.0]<br>    - Tracks :<br>      - Activate : True<br>      - Length : [1, 100]<br>      - Instant D : [-1.0, 1.0]<br>      - D Coeff : [-1.0, 1.0]<br>      - Alpha : [-1.0, 1.0]<br>      - Speed : [0.0, 1.0]<br>      - Confinement : [-1.0, 1.0]</pre>
   </details>

Settings Signal
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Connect And Emit Direct
     - ✅
     - 1ms
   * - Disconnect
     - ✅
     - 1ms
   * - Block Simple Coalescence Last Value
     - ✅
     - 1ms
   * - Block Without Emits No Output
     - ✅
     - 1ms
   * - Nested Blocks Emit Once At Outer Exit
     - ✅
     - 1ms
   * - Emit Default None Coalesced
     - ✅
     - 1ms
   * - Block Flags Reset After Flush
     - ✅
     - 1ms
   * - Blocked Returns Context Manager Instance
     - ✅
     - 1ms
   * - Internal Block Begin End Paths
     - ✅
     - 1ms
   * - Coalescence Overwrite Multiple Times
     - ✅
     - 1ms
   * - Emit Direct After Previous Block
     - ✅
     - 1ms

Settings Types
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Base Setting
     - ✅
     - 1ms
   * - Create Setting From Dict
     - ✅
     - 473ms
   * - Create Setting From Dict Fail
     - ✅
     - 119ms
   * - Spin Int
     - ✅
     - 105ms
   * - Spin Float
     - ✅
     - 113ms
   * - Check Box
     - ✅
     - 106ms
   * - Combo
     - ✅
     - 115ms
   * - Browse File
     - ✅
     - 103ms
   * - File List
     - ✅
     - 117ms
   * - Check Range Int
     - ✅
     - 103ms
   * - Check Range Float
     - ✅
     - 115ms
   * - Button
     - ✅
     - 103ms

Tools Fileio
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Save Json
     - ✅
     - 1ms
   * - Open Json
     - ✅
     - 1ms
   * - Open Json Bad File
     - ✅
     - 1ms
   * - Save Tif
     - ✅
     - 3ms
   * - Save Tif 2D
     - ✅
     - 2ms
   * - Save Tif Bad Stack
     - ✅
     - 1ms
   * - Open Tif
     - ✅
     - 9ms
   * - Open Tif Bad File
     - ✅
     - 1ms
   * - Save Png
     - ✅
     - 6ms
   * - Save Png Color
     - ✅
     - 9ms
   * - Save Png Bad Sample
     - ✅
     - 1ms
   * - Open Calibration Mat Bad File
     - ✅
     - 1ms
   * - Open Calibration Mat
     - ✅
     - 28ms

.. raw:: html

   <details>
      <summary>Log Test : Open Calibration Mat</summary>
      <pre>{'dz': np.uint8(10), 'coeff': array([[[[ 1.76262995e-03,  6.60182966e-04,  1.75444511e-04, ...,<br>          -7.81234667e-06,  8.00063481e-06, -2.51688152e-06],<br>         [ 1.75704551e-03,  6.45794673e-04,  1.96373905e-04, ...,<br>          -7.81234667e-06,  8.00063572e-06, -2.51688152e-06],<br>         [ 1.74238149e-03,  6.11375668e-04,  2.48690136e-04, ...,<br>          -5.07905042e-07, -5.15571901e-06,  1.83311408e-06],<br>         [ 1.71448046e-03,  6.15136058e-04,  2.82197463e-04, ...,<br>           3.08603285e-06,  3.93476876e-06, -1.32345281e-06],<br>         [ 1.68601575e-03,  6.72109716e-04,  2.53685779e-04, ...,<br>          -1.85213310e-06,  3.18481398e-06, -5.18025331e-07],<br>         [ 1.67045288e-03,  7.41014606e-04,  1.85979850e-04, ...,<br>          -1.85213310e-06,  3.18481398e-06, -5.18025331e-07]],<br><br>        [[ 2.70473980e-03, -9.48156667e-05,  1.01578154e-03, ...,<br>          -7.81234667e-06,  8.00063572e-06, -2.51688152e-06],<br>         [ 2.70959642e-03, -1.02119076e-04,  1.03564339e-03, ...,<br>          -7.81234667e-06,  8.00063572e-06, -2.51688152e-06],<br>         [ 2.71256035e-03, -8.98670405e-05,  1.04932650e-03, ...,<br>          -5.07905042e-07, -5.15571901e-06,  1.83311408e-06],<br>         [ 2.70262384e-03, -1.70290077e-05,  1.01669191e-03, ...,<br>           3.08603285e-06,  3.93476876e-06, -1.32345281e-06],<br>         [ 2.69394857e-03,  1.13344904e-04,  9.06467263e-04, ...,<br>          -1.85213310e-06,  3.18481398e-06, -5.18025331e-07],<br>         [ 2.69722054e-03,  2.37507324e-04,  7.71025720e-04, ...,<br>          -1.85213310e-06,  3.18481398e-06, -5.18025331e-07]],<br><br>        [[ 3.56831495e-03, -4.40529606e-04,  1.41770788e-03, ...,<br>           9.90122135e-06, -7.44254885e-06,  2.23133543e-06],<br>         [ 3.59475426e-03, -4.64643032e-04,  1.46338262e-03, ...,<br>           9.90122135e-06, -7.44254885e-06,  2.23133543e-06],<br>         [ 3.66876321e-03, -4.95911052e-04,  1.53967657e-03, ...,<br>          -3.95631878e-06,  1.27160592e-05, -3.91617095e-06],<br>         [ 3.76045704e-03, -4.57936869e-04,  1.55345595e-03, ...,<br>           8.09040648e-06, -2.39337242e-05,  6.82765040e-06],<br>         [ 3.84947704e-03, -3.24017310e-04,  1.45022175e-03, ...,<br>           4.05997935e-06, -7.87759382e-06,  1.60339005e-06],<br>         [ 3.93907167e-03, -1.99005764e-04,  1.31643086e-03, ...,<br>           4.05997935e-06, -7.87759382e-06,  1.60339005e-06]],<br><br>        ...,<br><br>        [[ 2.42101937e-03,  8.45823204e-04,  2.58160017e-05, ...,<br>          -1.51463273e-05,  1.15915709e-05, -2.29856619e-06],<br>         [ 2.43261014e-03,  8.29919532e-04,  3.14000754e-05, ...,<br>          -1.51463273e-05,  1.15915709e-05, -2.29856619e-06],<br>         [ 2.46658362e-03,  7.86881545e-04,  6.60509904e-05, ...,<br>          -1.63374498e-05,  6.06615640e-06, -8.61550902e-08],<br>         [ 2.49986164e-03,  7.28350074e-04,  1.45897924e-04, ...,<br>           5.97384405e-06, -3.04068908e-06,  6.25882933e-07],<br>         [ 2.52369908e-03,  6.22923486e-04,  2.85503629e-04, ...,<br>           1.95473440e-05, -2.00541726e-05,  4.52503036e-06],<br>         [ 2.53130752e-03,  4.63657198e-04,  4.77367372e-04, ...,<br>           1.95473440e-05, -2.00541726e-05,  4.52503036e-06]],<br><br>        [[ 2.46633077e-03,  9.78531549e-04, -2.31912054e-04, ...,<br>           1.37966417e-05, -9.95016126e-06,  1.74210243e-06],<br>         [ 2.46035471e-03,  9.55297786e-04, -2.44177354e-04, ...,<br>           1.37966417e-05, -9.95016126e-06,  1.74210243e-06],<br>         [ 2.42791767e-03,  9.01909196e-04, -2.63140537e-04, ...,<br>           1.22992269e-05, -7.90170816e-06,  1.20454467e-06],<br>         [ 2.35864520e-03,  8.85267160e-04, -3.00246233e-04, ...,<br>          -1.18684829e-06, -2.77304537e-07,  1.98907600e-07],<br>         [ 2.28697783e-03,  8.83703528e-04, -3.15127894e-04, ...,<br>          -3.88470380e-06,  2.21625555e-06, -2.01877484e-07],<br>         [ 2.24619033e-03,  8.52560741e-04, -2.84196023e-04, ...,<br>          -3.88470380e-06,  2.21625555e-06, -2.01877484e-07]],<br><br>        [[ 2.24976288e-03,  6.56987599e-04, -1.60009586e-04, ...,<br>           1.37966417e-05, -9.95016126e-06,  1.74210243e-06],<br>         [ 2.25791475e-03,  7.09359127e-04, -2.15561231e-04, ...,<br>           1.37966417e-05, -9.95016126e-06,  1.74210243e-06],<br>         [ 2.27287575e-03,  8.60852888e-04, -3.72661190e-04, ...,<br>           1.22992269e-05, -7.90170816e-06,  1.20454467e-06],<br>         [ 2.26707128e-03,  1.06072903e-03, -5.67374227e-04, ...,<br>          -1.18684829e-06, -2.77304537e-07,  1.98907600e-07],<br>         [ 2.26142514e-03,  1.22725707e-03, -7.24507263e-04, ...,<br>          -3.88470380e-06,  2.21625555e-06, -2.01877498e-07],<br>         [ 2.27620034e-03,  1.31491164e-03, -8.16303713e-04, ...,<br>          -3.88470380e-06,  2.21625555e-06, -2.01877484e-07]]],<br><br><br>       [[[ 2.50432733e-03,  7.29281281e-04, -1.06346182e-04, ...,<br>           6.38279914e-07,  4.49990921e-07, -2.51688152e-06],<br>         [ 2.50045164e-03,  7.42255477e-04, -9.99131153e-05, ...,<br>           6.38279914e-07,  4.49990921e-07, -2.51688152e-06],<br>         [ 2.49238522e-03,  7.78569840e-04, -8.14959785e-05, ...,<br>          -5.32000104e-06,  3.43623128e-07,  1.83311408e-06],<br>         [ 2.49468768e-03,  8.28152406e-04, -6.91811219e-05, ...,<br>           6.98521126e-06, -3.55899736e-08, -1.32345281e-06],<br>         [ 2.50335736e-03,  8.54119193e-04, -7.16763170e-05, ...,<br>           2.96341909e-06,  1.63073810e-06, -5.18025331e-07],<br>         [ 2.50790780e-03,  8.44355556e-04, -8.26389223e-05, ...,<br>           2.96341909e-06,  1.63073810e-06, -5.18025331e-07]],<br><br>        [[ 3.34816240e-03,  1.10411760e-03,  1.83151744e-04, ...,<br>           6.38279914e-07,  4.49990893e-07, -2.51688152e-06],<br>         [ 3.35706770e-03,  1.11100858e-03,  1.77484195e-04, ...,<br>           6.38279914e-07,  4.49990893e-07, -2.51688152e-06],<br>         [ 3.37493583e-03,  1.11753412e-03,  1.58074618e-04, ...,<br>          -5.32000104e-06,  3.43623128e-07,  1.83311408e-06],<br>         [ 3.40374932e-03,  1.12074276e-03,  1.21079844e-04, ...,<br>           6.98521126e-06, -3.55899701e-08, -1.32345281e-06],<br>         [ 3.43565480e-03,  1.09196187e-03,  7.21496835e-05, ...,<br>           2.96341909e-06,  1.63073810e-06, -5.18025331e-07],<br>         [ 3.45852808e-03,  1.03788241e-03,  2.93494068e-05, ...,<br>           2.96341909e-06,  1.63073810e-06, -5.18025331e-07]],<br><br>        [[ 4.15255735e-03,  1.21607853e-03,  2.38900349e-04, ...,<br>           1.71013028e-06, -7.48542391e-07,  2.23133543e-06],<br>         [ 4.18164860e-03,  1.22658629e-03,  2.27846642e-04, ...,<br>           1.71013028e-06, -7.48542391e-07,  2.23133543e-06],<br>         [ 4.26620850e-03,  1.24448119e-03,  2.00715600e-04, ...,<br>           9.72728594e-06,  9.67545475e-07, -3.91617095e-06],<br>         [ 4.39114682e-03,  1.25448627e-03,  1.58967116e-04, ...,<br>          -1.92940915e-05, -3.45077410e-06,  6.82765040e-06],<br>         [ 4.52651083e-03,  1.22891343e-03,  1.02709004e-04, ...,<br>          -6.88503769e-06, -3.06742368e-06,  1.60339005e-06],<br>         [ 4.63719154e-03,  1.17594027e-03,  5.85151683e-05, ...,<br>          -6.88503769e-06, -3.06742368e-06,  1.60339005e-06]],<br><br>        ...,<br><br>        [[ 3.23184626e-03,  7.15018017e-04, -1.56621187e-04, ...,<br>           1.14111538e-06,  4.69587212e-06, -2.29856619e-06],<br>         [ 3.23272939e-03,  7.09118845e-04, -1.52200737e-04, ...,<br>           1.14111538e-06,  4.69587212e-06, -2.29856619e-06],<br>         [ 3.25040473e-03,  7.11649715e-04, -1.41282828e-04, ...,<br>          -4.46360264e-06,  5.80769120e-06, -8.61550902e-08],<br>         [ 3.28356633e-03,  7.48515537e-04, -1.25732433e-04, ...,<br>           1.77011441e-06, -1.16304034e-06,  6.25882990e-07],<br>         [ 3.30430828e-03,  8.10477126e-04, -9.79500110e-05, ...,<br>          -6.98590839e-06, -6.47908064e-06,  4.52503036e-06],<br>         [ 3.29495524e-03,  8.86261405e-04, -5.47631862e-05, ...,<br>          -6.98590839e-06, -6.47908064e-06,  4.52503036e-06]],<br><br>        [[ 3.21156066e-03,  5.10538230e-04, -2.36081207e-04, ...,<br>          -8.77373850e-07, -4.72385409e-06,  1.74210243e-06],<br>         [ 3.17653408e-03,  4.82119998e-04, -2.29000419e-04, ...,<br>          -8.77373850e-07, -4.72385409e-06,  1.74210243e-06],<br>         [ 3.08391824e-03,  4.27323772e-04, -2.11444887e-04, ...,<br>           1.09445239e-07, -4.28807380e-06,  1.20454467e-06],<br>         [ 2.97635957e-03,  3.82855389e-04, -2.02165538e-04, ...,<br>          -1.14473448e-06,  3.19418291e-07,  1.98907600e-07],<br>         [ 2.89408537e-03,  3.69043933e-04, -1.99531700e-04, ...,<br>          -5.78252539e-08,  1.61062314e-06, -2.01877498e-07],<br>         [ 2.84472900e-03,  3.74690688e-04, -1.93674074e-04, ...,<br>          -5.78252539e-08,  1.61062314e-06, -2.01877498e-07]],<br><br>        [[ 2.76500615e-03,  3.91764363e-04, -1.05213629e-04, ...,<br>          -8.77373850e-07, -4.72385409e-06,  1.74210243e-06],<br>         [ 2.78157718e-03,  3.67830275e-04, -1.25967650e-04, ...,<br>          -8.77373850e-07, -4.72385409e-06,  1.74210243e-06],<br>         [ 2.82380963e-03,  3.03756970e-04, -1.84434713e-04, ...,<br>           1.09445239e-07, -4.28807380e-06,  1.20454467e-06],<br>         [ 2.86435662e-03,  2.37772285e-04, -2.55582534e-04, ...,<br>          -1.14473448e-06,  3.19418291e-07,  1.98907600e-07],<br>         [ 2.90116272e-03,  1.89206432e-04, -3.13543424e-04, ...,<br>          -5.78252539e-08,  1.61062314e-06, -2.01877484e-07],<br>         [ 2.93078925e-03,  1.50247040e-04, -3.48360889e-04, ...,<br>          -5.78252539e-08,  1.61062314e-06, -2.01877498e-07]]],<br><br><br>       [[[ 3.03333206e-03,  2.34798223e-04, -3.88136890e-04, ...,<br>          -6.01238253e-06, -7.10065342e-06,  5.55543647e-06],<br>         [ 3.04403179e-03,  2.46142241e-04, -3.96200136e-04, ...,<br>          -6.01238253e-06, -7.10065342e-06,  5.55543647e-06],<br>         [ 3.07939714e-03,  2.85391783e-04, -4.11682093e-04, ...,<br>           8.66587527e-07,  5.84296549e-06, -4.00310364e-06],<br>         [ 3.13653285e-03,  3.38411570e-04, -4.20559692e-04, ...,<br>           2.94367305e-06, -4.00594854e-06,  6.12300084e-07],<br>         [ 3.17734620e-03,  3.85404477e-04, -3.97038413e-04, ...,<br>           4.67081918e-06,  7.66619976e-08, -2.50615903e-06],<br>         [ 3.18008475e-03,  4.10458946e-04, -3.51257710e-04, ...,<br>           4.67081918e-06,  7.66619976e-08, -2.50615903e-06]],<br><br>        [[ 4.35788836e-03,  6.37791294e-04, -6.49477995e-04, ...,<br>          -6.01238253e-06, -7.10065342e-06,  5.55543647e-06],<br>         [ 4.35950747e-03,  6.07817667e-04, -6.80675090e-04, ...,<br>          -6.01238253e-06, -7.10065342e-06,  5.55543647e-06],<br>         [ 4.35346039e-03,  5.42431429e-04, -7.33177294e-04, ...,<br>           8.66587527e-07,  5.84296549e-06, -4.00310364e-06],<br>         [ 4.34703473e-03,  4.67290345e-04, -7.74532207e-04, ...,<br>           2.94367305e-06, -4.00594854e-06,  6.12300084e-07],<br>         [ 4.32166038e-03,  4.01943631e-04, -7.62167852e-04, ...,<br>           4.67081918e-06,  7.66620047e-08, -2.50615903e-06],<br>         [ 4.27853456e-03,  3.54904943e-04, -7.12326902e-04, ...,<br>           4.67081918e-06,  7.66619976e-08, -2.50615903e-06]],<br><br>        [[ 5.21460036e-03,  5.15071792e-04, -9.39907099e-04, ...,<br>           6.90705156e-06,  5.94546373e-06, -5.67339202e-06],<br>         [ 5.22423629e-03,  4.46743536e-04, -1.00768940e-03, ...,<br>           6.90705156e-06,  5.94546373e-06, -5.67339202e-06],<br>         [ 5.26508503e-03,  3.06951319e-04, -1.13824545e-03, ...,<br>          -8.61368363e-08, -1.07809683e-05,  6.90578281e-06],<br>         [ 5.33977011e-03,  1.77931564e-04, -1.23552175e-03, ...,<br>          -5.71268993e-06,  1.70321764e-05, -6.54603400e-06],<br>         [ 5.40896226e-03,  8.68186762e-05, -1.24480377e-03, ...,<br>          -8.20971491e-06,  1.74274624e-06,  1.62661252e-06],<br>         [ 5.45234187e-03,  3.50549053e-05, -1.19940052e-03, ...,<br>          -8.20971491e-06,  1.74274624e-06,  1.62661252e-06]],<br><br>        ...,<br><br>        [[ 3.72943073e-03,  2.19338457e-04, -3.39058373e-04, ...,<br>           3.63716049e-06, -2.19982689e-06,  1.00235025e-06],<br>         [ 3.72844725e-03,  2.21116570e-04, -3.35801538e-04, ...,<br>           3.63716049e-06, -2.19982689e-06,  1.00235025e-06],<br>         [ 3.75166046e-03,  2.21750248e-04, -3.48616624e-04, ...,<br>           6.89331455e-06,  5.54922599e-06, -2.09210089e-06],<br>         [ 3.81580601e-03,  2.25420314e-04, -3.97362805e-04, ...,<br>           1.32168270e-06,  7.14608575e-07, -2.68559091e-07],<br>         [ 3.88901751e-03,  2.31123471e-04, -4.81403637e-04, ...,<br>          -6.36897812e-06,  7.09601090e-06, -2.82429255e-06],<br>         [ 3.94907640e-03,  2.44604453e-04, -5.86893759e-04, ...,<br>          -6.36897812e-06,  7.09601090e-06, -2.82429255e-06]],<br><br>        [[ 3.48462793e-03,  3.42066742e-05, -2.40250360e-04, ...,<br>          -5.09877509e-06,  5.02453020e-07,  7.23051414e-07],<br>         [ 3.43471277e-03,  3.92961047e-05, -2.13823485e-04, ...,<br>          -5.09877509e-06,  5.02453020e-07,  7.23051414e-07],<br>         [ 3.31702898e-03,  5.61296220e-05, -1.59749252e-04, ...,<br>          -4.85306828e-06, -6.74439775e-07,  1.32362470e-06],<br>         [ 3.18974303e-03,  7.66050143e-05, -1.04084829e-04, ...,<br>           9.08248623e-08,  9.16141119e-07, -1.40429813e-06],<br>         [ 3.10212979e-03,  8.55766921e-05, -8.39355271e-05, ...,<br>           2.55778855e-06,  1.00499062e-06, -1.21071105e-06],<br>         [ 3.05591966e-03,  7.78644462e-05, -1.03152146e-04, ...,<br>           2.55778855e-06,  1.00499062e-06, -1.21071105e-06]],<br><br>        [[ 3.06982221e-03,  2.36133070e-04, -5.04176714e-05, ...,<br>          -5.09877509e-06,  5.02453020e-07,  7.23051414e-07],<br>         [ 3.05330427e-03,  2.05488541e-04, -3.63740764e-05, ...,<br>          -5.09877509e-06,  5.02453020e-07,  7.23051414e-07],<br>         [ 3.00587411e-03,  1.23114005e-04,  3.79174980e-06, ...,<br>          -4.85306828e-06, -6.74439775e-07,  1.32362470e-06],<br>         [ 2.95047695e-03,  3.83989100e-05,  5.62091518e-05, ...,<br>           9.08248694e-08,  9.16141119e-07, -1.40429813e-06],<br>         [ 2.91381381e-03, -2.69165466e-05,  9.74204377e-05, ...,<br>           2.55778855e-06,  1.00499062e-06, -1.21071105e-06],<br>         [ 2.88865645e-03, -7.85319207e-05,  1.19581942e-04, ...,<br>           2.55778855e-06,  1.00499062e-06, -1.21071105e-06]]],<br><br><br>       ...,<br><br><br>       [[[ 3.16187670e-03, -4.67400969e-04,  4.51783475e-04, ...,<br>          -1.85942824e-07, -2.07119456e-06,  1.30779324e-06],<br>         [ 3.15810647e-03, -5.05033589e-04,  4.86024626e-04, ...,<br>          -1.85942824e-07, -2.07119456e-06,  1.30779324e-06],<br>         [ 3.17789218e-03, -6.13084529e-04,  5.30798221e-04, ...,<br>           5.89917090e-06, -2.05147535e-06, -3.39958888e-07],<br>         [ 3.26516922e-03, -7.59898569e-04,  5.12680970e-04, ...,<br>           1.35139624e-06,  4.97463179e-06, -4.03053446e-06],<br>         [ 3.41615803e-03, -8.79681320e-04,  3.91539448e-04, ...,<br>           3.09551092e-06,  1.79006520e-06, -2.82672363e-06],<br>         [ 3.57381045e-03, -9.56193777e-04,  2.50019773e-04, ...,<br>           3.09551092e-06,  1.79006520e-06, -2.82672363e-06]],<br><br>        [[ 3.84366699e-03, -5.60550718e-04,  5.33733517e-04, ...,<br>          -1.85942824e-07, -2.07119456e-06,  1.30779324e-06],<br>         [ 3.84246977e-03, -5.52165904e-04,  5.15987573e-04, ...,<br>          -1.85942824e-07, -2.07119456e-06,  1.30779324e-06],<br>         [ 3.85740539e-03, -5.34106744e-04,  4.37614304e-04, ...,<br>           5.89917090e-06, -2.05147535e-06, -3.39958888e-07],<br>         [ 3.91057739e-03, -5.24670002e-04,  2.60712375e-04, ...,<br>           1.35139624e-06,  4.97463179e-06, -4.03053446e-06],<br>         [ 4.00642958e-03, -5.11312624e-04, -2.37807490e-06, ...,<br>           3.09551092e-06,  1.79006520e-06, -2.82672363e-06],<br>         [ 4.11505718e-03, -5.03855525e-04, -2.56041007e-04, ...,<br>           3.09551092e-06,  1.79006520e-06, -2.82672363e-06]],<br><br>        [[ 4.34940774e-03, -9.72292735e-04,  4.60055016e-04, ...,<br>          -3.21394100e-06,  1.75557852e-06, -5.26980216e-07],<br>         [ 4.34951158e-03, -9.37857374e-04,  4.17957170e-04, ...,<br>          -3.21394100e-06,  1.75557852e-06, -5.26980273e-07],<br>         [ 4.36356803e-03, -8.23243987e-04,  3.03312059e-04, ...,<br>          -4.42559667e-06,  5.36416383e-06, -1.09266557e-06],<br>         [ 4.40934254e-03, -6.58917939e-04,  1.32212546e-04, ...,<br>          -1.44061653e-06, -2.05772926e-06,  2.91244100e-06],<br>         [ 4.49895021e-03, -4.93778556e-04, -6.10117895e-05, ...,<br>          -7.35568392e-07,  8.22234597e-06, -3.83254292e-06],<br>         [ 4.60180780e-03, -3.68937501e-04, -2.36896711e-04, ...,<br>          -7.35568392e-07,  8.22234597e-06, -3.83254292e-06]],<br><br>        ...,<br><br>        [[ 4.27506119e-03, -4.59451257e-04, -8.01331626e-05, ...,<br>          -7.37063601e-07,  1.39748481e-05, -8.89395415e-06],<br>         [ 4.26127436e-03, -4.37014329e-04, -1.01624682e-04, ...,<br>          -7.37063601e-07,  1.39748481e-05, -8.89395415e-06],<br>         [ 4.22738679e-03, -3.76256095e-04, -1.74932182e-04, ...,<br>           4.53002667e-06,  4.81427696e-06, -4.79287201e-06],<br>         [ 4.17078985e-03, -2.92320765e-04, -2.55729479e-04, ...,<br>           5.28796454e-06,  1.50018525e-06, -3.62431160e-06],<br>         [ 4.10616398e-03, -1.89833256e-04, -2.94572732e-04, ...,<br>          -7.42702332e-06, -8.17192995e-06,  7.37063465e-06],<br>         [ 4.05870844e-03, -1.07748994e-04, -3.10516945e-04, ...,<br>          -7.42702332e-06, -8.17192995e-06,  7.37063465e-06]],<br><br>        [[ 4.10424219e-03, -2.53162638e-04, -3.18291422e-04, ...,<br>           2.17742877e-06, -1.04200362e-05,  5.14725980e-06],<br>         [ 4.11759457e-03, -2.53612350e-04, -2.96993792e-04, ...,<br>           2.17742877e-06, -1.04200362e-05,  5.14725980e-06],<br>         [ 4.15776623e-03, -2.62261310e-04, -2.48313940e-04, ...,<br>           5.78079664e-07, -1.03723069e-05,  5.86634178e-06],<br>         [ 4.20093257e-03, -2.71592144e-04, -2.06340395e-04, ...,<br>          -8.37764128e-06, -3.03575212e-06,  5.81177392e-06],<br>         [ 4.21837717e-03, -2.76147330e-04, -1.58222305e-04, ...,<br>           1.38269536e-06,  5.58029069e-06, -3.44198997e-06],<br>         [ 4.21013450e-03, -2.92802259e-04, -1.24366110e-04, ...,<br>           1.38269536e-06,  5.58029069e-06, -3.44198997e-06]],<br><br>        [[ 3.96745792e-03,  1.29739914e-04, -1.86688310e-04, ...,<br>           2.17742877e-06, -1.04200362e-05,  5.14725980e-06],<br>         [ 4.00416832e-03,  1.26439525e-04, -2.31079553e-04, ...,<br>           2.17742877e-06, -1.04200362e-05,  5.14725980e-06],<br>         [ 4.10044659e-03,  1.05282947e-04, -3.64988635e-04, ...,<br>           5.78079664e-07, -1.03723069e-05,  5.86634178e-06],<br>         [ 4.19675233e-03,  5.37182423e-05, -5.42872585e-04, ...,<br>          -8.37764128e-06, -3.03575212e-06,  5.81177392e-06],<br>         [ 4.19948436e-03, -2.62836966e-05, -6.73761650e-04, ...,<br>           1.38269536e-06,  5.58029069e-06, -3.44198997e-06],<br>         [ 4.14496614e-03, -1.03521095e-04, -7.27128470e-04, ...,<br>           1.38269536e-06,  5.58029069e-06, -3.44198997e-06]]],<br><br><br>       [[[ 2.86900718e-03, -3.95589654e-04, -3.79972160e-04, ...,<br>          -4.04952459e-07,  1.85218505e-06, -9.68076506e-07],<br>         [ 2.85079307e-03, -3.97897646e-04, -3.78888682e-04, ...,<br>          -4.04952459e-07,  1.85218505e-06, -9.68076506e-07],<br>         [ 2.80661695e-03, -4.18455049e-04, -3.36168712e-04, ...,<br>           7.76343825e-07, -3.07135178e-06,  5.38980601e-07],<br>         [ 2.77097686e-03, -4.75460634e-04, -2.28242992e-04, ...,<br>          -7.90943091e-07, -7.11697112e-06,  2.90880917e-06],<br>         [ 2.77116033e-03, -5.67170035e-04, -7.90281847e-05, ...,<br>          -1.80452992e-06, -6.69010615e-06,  3.04349032e-06],<br>         [ 2.80040945e-03, -6.57834811e-04,  4.83392287e-05, ...,<br>          -1.80452992e-06, -6.69010615e-06,  3.04349032e-06]],<br><br>        [[ 3.55796213e-03, -2.69746728e-04, -2.42929571e-04, ...,<br>          -4.04952459e-07,  1.85218505e-06, -9.68076506e-07],<br>         [ 3.55549017e-03, -2.72594363e-04, -2.36416061e-04, ...,<br>          -4.04952459e-07,  1.85218505e-06, -9.68076506e-07],<br>         [ 3.54726566e-03, -2.99820007e-04, -2.03327625e-04, ...,<br>           7.76343825e-07, -3.07135178e-06,  5.38980601e-07],<br>         [ 3.52252694e-03, -3.75524338e-04, -1.11566704e-04, ...,<br>          -7.90943091e-07, -7.11697112e-06,  2.90880917e-06],<br>         [ 3.50533053e-03, -4.78293456e-04,  3.53972428e-05, ...,<br>          -1.80452992e-06, -6.69010615e-06,  3.04349032e-06],<br>         [ 3.50343878e-03, -5.71103476e-04,  1.88793041e-04, ...,<br>          -1.80452992e-06, -6.69010615e-06,  3.04349032e-06]],<br><br>        [[ 3.78752779e-03, -2.01108633e-04,  3.11129086e-04, ...,<br>          -1.28372460e-06,  1.74637833e-07,  5.02916066e-07],<br>         [ 3.79368174e-03, -2.09731908e-04,  3.10168281e-04, ...,<br>          -1.28372460e-06,  1.74637833e-07,  5.02916066e-07],<br>         [ 3.83676076e-03, -2.37245345e-04,  2.82686582e-04, ...,<br>           3.02473381e-06,  2.08616689e-06, -1.59612921e-06],<br>         [ 3.91507335e-03, -2.97183899e-04,  2.29521538e-04, ...,<br>           3.18124808e-06,  6.67959375e-06, -4.19962589e-06],<br>         [ 4.02324041e-03, -3.78559605e-04,  1.76230766e-04, ...,<br>           4.21149434e-06, -3.27528323e-06,  9.25795462e-07],<br>         [ 4.12384560e-03, -4.59114264e-04,  1.46719962e-04, ...,<br>           4.21149434e-06, -3.27528323e-06,  9.25795462e-07]],<br><br>        ...,<br><br>        [[ 3.81478365e-03, -3.81797727e-04,  1.57786693e-04, ...,<br>           5.30771786e-07, -1.27070134e-05,  5.48384423e-06],<br>         [ 3.80831910e-03, -3.83212056e-04,  1.55426969e-04, ...,<br>           5.30771786e-07, -1.27070134e-05,  5.48384423e-06],<br>         [ 3.78261949e-03, -4.06857609e-04,  1.44330683e-04, ...,<br>          -2.20036227e-07, -9.56433996e-06,  4.22947369e-06],<br>         [ 3.73641239e-03, -4.62762022e-04,  8.52882367e-05, ...,<br>          -2.58459977e-06, -9.37274945e-06,  4.12974168e-06],<br>         [ 3.70715163e-03, -5.22796996e-04, -3.83910410e-05, ...,<br>          -1.65898030e-06,  1.39399735e-05, -5.61709203e-06],<br>         [ 3.69341043e-03, -5.69878903e-04, -1.51612971e-04, ...,<br>          -1.65898030e-06,  1.39399735e-05, -5.61709203e-06]],<br><br>        [[ 3.71288438e-03, -3.49456444e-04,  2.21997616e-04, ...,<br>          -3.22086498e-06,  5.02174271e-06, -1.61690014e-06],<br>         [ 3.73208709e-03, -3.52303847e-04,  1.98302267e-04, ...,<br>          -3.22086498e-06,  5.02174271e-06, -1.61690014e-06],<br>         [ 3.77312093e-03, -3.81098333e-04,  1.29476932e-04, ...,<br>          -2.56750809e-06,  7.22671894e-06, -3.34185188e-06],<br>         [ 3.80111602e-03, -4.49924089e-04,  2.80084732e-05, ...,<br>           2.98617624e-06,  1.43995694e-05, -6.14766986e-06],<br>         [ 3.80589417e-03, -5.26931603e-04, -9.25619534e-05, ...,<br>           2.21730670e-06, -4.74567923e-06,  1.95759048e-06],<br>         [ 3.77823203e-03, -5.85736765e-04, -1.68568396e-04, ...,<br>           2.21730670e-06, -4.74567923e-06,  1.95759048e-06]],<br><br>        [[ 3.85054084e-03, -4.23542835e-04, -3.66594439e-04, ...,<br>          -3.22086498e-06,  5.02174271e-06, -1.61690014e-06],<br>         [ 3.86240031e-03, -4.47103987e-04, -3.42463958e-04, ...,<br>          -3.22086498e-06,  5.02174271e-06, -1.61690014e-06],<br>         [ 3.87599948e-03, -5.18918619e-04, -2.59212917e-04, ...,<br>          -2.56750809e-06,  7.22671894e-06, -3.34185188e-06],<br>         [ 3.84611939e-03, -6.16463483e-04, -1.27309118e-04, ...,<br>           2.98617624e-06,  1.43995694e-05, -6.14766986e-06],<br>         [ 3.72716296e-03, -6.90635119e-04,  9.41026337e-06, ...,<br>           2.21730670e-06, -4.74567923e-06,  1.95759048e-06],<br>         [ 3.59099428e-03, -7.27745355e-04,  1.02904203e-04, ...,<br>           2.21730670e-06, -4.74567923e-06,  1.95759048e-06]]],<br><br><br>       [[[ 2.19857320e-03, -8.40150926e-04, -6.45891269e-05, ...,<br>           3.95188181e-07, -1.05204435e-06, -9.68076506e-07],<br>         [ 2.17705872e-03, -8.46519251e-04, -6.97329160e-05, ...,<br>           3.95188181e-07, -1.05204435e-06, -9.68076506e-07],<br>         [ 2.13539624e-03, -8.40582943e-04, -8.59591892e-05, ...,<br>          -3.74941828e-06, -1.45441015e-06,  5.38980601e-07],<br>         [ 2.10870290e-03, -8.07657314e-04, -1.03953680e-04, ...,<br>          -6.29845817e-06,  1.60945615e-06,  2.90880917e-06],<br>         [ 2.11252854e-03, -7.62527226e-04, -1.16328993e-04, ...,<br>          -6.05427067e-06,  2.44036528e-06,  3.04349032e-06],<br>         [ 2.13437737e-03, -7.30766391e-04, -1.21270772e-04, ...,<br>          -6.05427067e-06,  2.44036528e-06,  3.04349032e-06]],<br><br>        [[ 2.98421038e-03, -9.38832294e-04, -4.26155981e-04, ...,<br>           3.95188181e-07, -1.05204435e-06, -9.68076506e-07],<br>         [ 2.98322854e-03, -9.35180287e-04, -4.26169834e-04, ...,<br>           3.95188181e-07, -1.05204435e-06, -9.68076506e-07],<br>         [ 2.97262194e-03, -9.20963241e-04, -4.17815609e-04, ...,<br>          -3.74941828e-06, -1.45441015e-06,  5.38980601e-07],<br>         [ 2.94272811e-03, -8.76781007e-04, -3.89689958e-04, ...,<br>          -6.29845817e-06,  1.60945615e-06,  2.90880917e-06],<br>         [ 2.92972988e-03, -8.05612770e-04, -3.62716557e-04, ...,<br>          -6.05427067e-06,  2.44036528e-06,  3.04349032e-06],<br>         [ 2.94062006e-03, -7.35042500e-04, -3.52732081e-04, ...,<br>          -6.05427067e-06,  2.44036528e-06,  3.04349032e-06]],<br><br>        [[ 3.61404009e-03, -4.29375184e-04, -5.39395667e-04, ...,<br>           5.74299349e-07,  1.68338602e-06,  5.02916066e-07],<br>         [ 3.60807101e-03, -4.47536819e-04, -5.47973148e-04, ...,<br>           5.74299349e-07,  1.68338602e-06,  5.02916066e-07],<br>         [ 3.60088539e-03, -5.15822612e-04, -5.61263820e-04, ...,<br>           2.40868007e-06, -2.70222063e-06, -1.59612910e-06],<br>         [ 3.58509971e-03, -6.25074841e-04, -5.57412510e-04, ...,<br>           3.94155813e-06, -5.91928347e-06, -4.19962589e-06],<br>         [ 3.58245312e-03, -7.41473865e-04, -5.39145025e-04, ...,<br>           4.38314402e-07, -4.97896735e-07,  9.25795462e-07],<br>         [ 3.59026249e-03, -8.29241297e-04, -5.16846951e-04, ...,<br>           4.38314402e-07, -4.97896735e-07,  9.25795462e-07]],<br><br>        ...,<br><br>        [[ 3.36399395e-03, -7.46560225e-04, -5.22549206e-04, ...,<br>          -8.43172165e-06,  3.74451929e-06,  5.48384423e-06],<br>         [ 3.35459923e-03, -7.50162057e-04, -5.22376969e-04, ...,<br>          -8.43172165e-06,  3.74451929e-06,  5.48384423e-06],<br>         [ 3.30403261e-03, -7.66376266e-04, -5.03849355e-04, ...,<br>          -6.66029473e-06,  3.12408133e-06,  4.22947369e-06],<br>         [ 3.18350480e-03, -8.18486616e-04, -4.41012817e-04, ...,<br>          -8.94087407e-06,  3.01647492e-06,  4.12974168e-06],<br>         [ 3.04106064e-03, -9.14288044e-04, -3.53100011e-04, ...,<br>           9.36968991e-06, -2.91130323e-06, -5.61709203e-06],<br>         [ 2.93045538e-03, -9.97494208e-04, -2.76002305e-04, ...,<br>           9.36968991e-06, -2.91130323e-06, -5.61709203e-06]],<br><br>        [[ 3.33201466e-03, -6.65693660e-04, -5.38234832e-04, ...,<br>           1.97192003e-06,  1.71042245e-07, -1.61690014e-06],<br>         [ 3.33412271e-03, -6.87587191e-04, -5.33585611e-04, ...,<br>           1.97192003e-06,  1.71042245e-07, -1.61690014e-06],<br>         [ 3.31157236e-03, -7.51926040e-04, -5.00304624e-04, ...,<br>           1.86037437e-06, -2.79883648e-06, -3.34185188e-06],<br>         [ 3.22864158e-03, -8.45583738e-04, -4.23668127e-04, ...,<br>           1.33423064e-05, -4.04343973e-06, -6.14766986e-06],<br>         [ 3.10671143e-03, -9.51123657e-04, -3.31630086e-04, ...,<br>          -1.40128054e-06,  1.12709210e-06,  1.95759048e-06],<br>         [ 2.99397111e-03, -1.01274089e-03, -2.58435670e-04, ...,<br>          -1.40128054e-06,  1.12709210e-06,  1.95759048e-06]],<br><br>        [[ 3.06666549e-03, -1.13794627e-03, -3.47808993e-04, ...,<br>           1.97192003e-06,  1.71042245e-07, -1.61690014e-06],<br>         [ 3.07110650e-03, -1.13720901e-03, -3.47641093e-04, ...,<br>           1.97192003e-06,  1.71042245e-07, -1.61690014e-06],<br>         [ 3.07030417e-03, -1.12003589e-03, -3.41904379e-04, ...,<br>           1.86037437e-06, -2.79883648e-06, -3.34185188e-06],<br>         [ 3.03534791e-03, -1.07207801e-03, -3.28305468e-04, ...,<br>           1.33423064e-05, -4.04343973e-06, -6.14766986e-06],<br>         [ 2.93844682e-03, -9.94288479e-04, -3.13063589e-04, ...,<br>          -1.40128054e-06,  1.12709210e-06,  1.95759048e-06],<br>         [ 2.83285952e-03, -9.21817904e-04, -2.96976737e-04, ...,<br>          -1.40128054e-06,  1.12709210e-06,  1.95759048e-06]]]],<br>      shape=(14, 14, 6, 64))}<br>(14, 14, 6, 64)</pre>
   </details>

Tools Filemigrator
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Open
     - ✅
     - 3ms
   * - Update Meta
     - ✅
     - 3ms
   * - Open Old File
     - ✅
     - 4ms
   * - Open Old Irregular File
     - ✅
     - 3ms
   * - Column Migrator
     - ✅
     - 2ms
   * - Analyze
     - ✅
     - 2ms
   * - Migrate
     - ✅
     - 228ms

.. raw:: html

   <details>
      <summary>Log Test : Analyze</summary>
      <pre>.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Migrate</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No localization file in folder.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No tracking file in folder.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No MSD file in folder.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No Instant Diffusion file in folder.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No Fit file in folder.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No Astimagmatism 3D Model file in folder.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Localization file migrated.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Warning that the 'Height' metadata differs between several files to be migrated (128 VS 256). The first one (128) will be retained.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Tracking file migrated.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">MSD file migrated.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Instant Diffusion file migrated.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Fit file migrated.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Astimagmatism 3D Model file migrated.</span><span style="font-weight: bold"></span></pre>
   </details>

Tools Logger
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Logger
     - ✅
     - 2ms
   * - Logger Bad Use
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Logger</summary>
      <pre>[27-01-2026 14:42:11] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log<br>[27-01-2026 14:42:11] First message<br>[27-01-2026 14:42:11] <br>[27-01-2026 14:42:11] after blank<br>[27-01-2026 14:42:11] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Logger Bad Use</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:42:11] Aucun fichier à fermer.</span><span style="font-weight: bold"></span><br>[27-01-2026 14:42:11] Message without logger open<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-01-2026 14:42:11] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span></pre>
   </details>

Tools Monitoring
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Monitoring
     - ✅
     - 1.24s
   * - Monitoring Save
     - ✅
     - 6.64s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.64, 0.86, 1.02]<br>CPU Usage : [0.0, 0.0, 0.0, 0.0, 0.41875, 0.0]<br>GPU Usage : [0, 0, 0, 0, 0, 2]<br>Memory Usage : [620.53125, 620.53125, 620.53125, 620.53125, 620.53125, 620.55859375]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Monitoring Save</summary>
      <pre>Simulating high CPU usage for 2 seconds...<br>CPU simulation complete.<br>Aucun GPU CUDA disponible pour la simulation.<br>Allocating 50 MB of memory...<br>Memory allocated. Holding for 2 seconds...<br>Releasing memory.<br>Writing a file of size 1 MB...<br>File written. Holding for 2 seconds...<br>Deleting the file...<br>Disk I/O simulation complete.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Kaleido doesn't work so well need update. No Image Saved.</span><span style="font-weight: bold"></span></pre>
   </details>

Tools Utils
^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Add Extension
     - ✅
     - 1ms
   * - Add Suffix
     - ✅
     - 1ms
   * - Get Timestamp For Files
     - ✅
     - 1ms
   * - Get Last File
     - ✅
     - 3ms
   * - Extract Suffix
     - ✅
     - 1ms
   * - Load Dll
     - ✅
     - 2ms
   * - Print Error
     - ✅
     - 1ms
   * - Print Warning
     - ✅
     - 2ms
   * - Print Success
     - ✅
     - 2ms
   * - Format Time
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Get Timestamp For Files</summary>
      <pre>Timestamp with hour : 20260127_144219<br>Timestamp without hour : 20260127</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Get Last File</summary>
      <pre>C:\Git\palm-tracer\palm_tracer\_tests\input\File-03.txt<br>C:\Git\palm-tracer\palm_tracer\_tests\input\File-03.txt</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Load Dll</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\PALMTracer_File.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\PALMTracer_File.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Print Error</summary>
      <pre><span style="color: #aa0000"></span><span style="font-weight: bold; color: #aa0000">Message d'erreur</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Print Warning</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Message d'avertissement</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Print Success</summary>
      <pre><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Message de succes</span><span style="font-weight: bold"></span></pre>
   </details>

Ui Alignmentwidget
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 10ms
   * - Bad Load Tif
     - ✅
     - 27ms
   * - Bad Load Coef
     - ✅
     - 13ms
   * - Bad Compute
     - ✅
     - 11ms
   * - Compute
     - ✅
     - 12ms
   * - Bad Align
     - ✅
     - 7ms
   * - Align
     - ✅
     - 159ms

Ui Astigmatism3Dwidget
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 351ms
   * - Bad Load Loc
     - ✅
     - 106ms
   * - Bad Load Model
     - ✅
     - 82ms
   * - Bad Compute
     - ✅
     - 110ms
   * - Compute
     - ✅
     - 203ms
   * - Compute Z
     - ✅
     - 194ms
   * - Bad Estimate
     - ✅
     - 107ms
   * - Estimate
     - ✅
     - 197ms
   * - Estimate Backup
     - ✅
     - 191ms
   * - Sync Spin
     - ✅
     - 116ms
   * - Download
     - ✅
     - 153ms

Ui Filemigratorwidget
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 5ms
   * - Bad Load
     - ✅
     - 7ms
   * - Mirgate
     - ✅
     - 28ms

Ui Graphviewer
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 155ms
   * - Actualize
     - ✅
     - 842ms
   * - Reset Filtered
     - ✅
     - 379ms
   * - Update Filtered
     - ✅
     - 497ms
   * - Update Plot
     - ✅
     - 682ms
   * - Get Plot Data
     - ✅
     - 891ms
   * - Status
     - ✅
     - 158ms
   * - Tracks Source
     - ✅
     - 176ms

Ui Standalonewidget
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 2ms

Widget
^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 1.18s
   * - Widget On Load Setting
     - ✅
     - 712ms
   * - Widget Reset Setting
     - ✅
     - 913ms
   * - Widget Reset Layer
     - ✅
     - 1.43s
   * - Widget Get Actual Image
     - ✅
     - 1.45s
   * - Widget Add Detection Layers
     - ✅
     - 7.22s
   * - Widget Preview
     - ✅
     - 7.04s
   * - Widget Auto Threshold
     - ✅
     - 1.51s
   * - Widget Thread Process
     - ✅
     - 1.56s
   * - Widget After Close
     - ✅
     - 1.60s
   * - Viewer3D
     - ✅
     - 2.05s
   * - Viewerhr Load
     - ✅
     - 890ms
   * - Viewerhr Generate
     - ✅
     - 5.44s
   * - Viewerhr Already Configured
     - ✅
     - 2.52s

.. raw:: html

   <details>
      <summary>Log Test : Widget On Load Setting</summary>
      <pre>INFO: Chargement du fichier de configuration '.'.<br>WARNING: Erreur lors du chargement du fichier '.' : Le fichier "." est introuvable.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Reset Layer</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Get Actual Image</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Add Detection Layers</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">erreur lors de la suppression de l'ancien calque : Using glBindFramebuffer with no OpenGL context.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Preview</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br>INFO: Thread Process done<br>Preview des 142 points détectés (46 sur l'image actuelle, 48 sur l'image précédente, 48 sur l'image suivante).<br>INFO: Thread Process done<br>Preview des 142 points détectés (46 sur l'image actuelle, 48 sur l'image précédente, 48 sur l'image suivante).<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Erreur lors de la suppression de l'ancien calque : Using glBindFramebuffer with no OpenGL context.</span><span style="font-weight: bold"></span><br>INFO: Thread Process done</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Auto Threshold</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br>Auto Threshold : 63.95</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Thread Process</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br>INFO: Thread Process done<br>[27-01-2026 14:42:48] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144248.log<br>[27-01-2026 14:42:48] Commencer le traitement.<br>[27-01-2026 14:42:48] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:42:48] Paramètres sauvegardés.<br>[27-01-2026 14:42:48] Fichier Meta sauvegardé.<br>[27-01-2026 14:42:48] Localisation désactivé.<br>[27-01-2026 14:42:48] 	Aucune donnée de localisation pré-calculée.<br>[27-01-2026 14:42:48] Tracking désactivé.<br>[27-01-2026 14:42:48] 	Aucune donnée de tracking pré-calculée.<br>[27-01-2026 14:42:48] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:42:48] Visualisation haute résolution désactivée.<br>[27-01-2026 14:42:48] Visualisation graphique désactivée.<br>[27-01-2026 14:42:48] Génération de la galerie désactivée.<br>[27-01-2026 14:42:48] Traitement terminé.<br>[27-01-2026 14:42:48] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144248.log<br>INFO: Thread Process done<br>Auto Threshold : 63.95<br>INFO: Thread Process done</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget After Close</summary>
      <pre>INFO: Chargement du fichier de configuration 'C:\Users\tmonseigne\.palm_tracer\settings.json'.<br>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Viewer3D</summary>
      <pre>WARNING: Le fichier doit contenir les colonnes X, Y, Z et Integrated Intensity.<br>WARNING: erreur lors de la suppression de l'ancien calque : Using glBindFramebuffer with no OpenGL context.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Viewerhr Already Configured</summary>
      <pre>[27-01-2026 14:42:59] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144259.log<br>[27-01-2026 14:42:59] Commencer le traitement.<br>[27-01-2026 14:42:59] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-01-2026 14:42:59] Paramètres sauvegardés.<br>[27-01-2026 14:42:59] Fichier Meta sauvegardé.<br>[27-01-2026 14:42:59] Localisation activée.<br>[27-01-2026 14:42:59] 	Enregistrement du fichier de localisation<br>[27-01-2026 14:42:59] 		455 localisation(s) trouvée(s).<br>[27-01-2026 14:42:59] Tracking désactivé.<br>[27-01-2026 14:42:59] 	Chargement d'un tracking pré-calculée.<br>[27-01-2026 14:42:59] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20260127_144253.csv' chargé avec succès.<br>[27-01-2026 14:42:59] 		455 trajectoire(s) trouvée(s).<br>[27-01-2026 14:42:59] Calcul sur les trajectoires désactivé.<br>[27-01-2026 14:42:59] Visualisation haute résolution désactivée.<br>[27-01-2026 14:42:59] Visualisation graphique désactivée.<br>[27-01-2026 14:42:59] Génération de la galerie désactivée.<br>[27-01-2026 14:42:59] Traitement terminé.<br>[27-01-2026 14:42:59] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20260127_144259.log<br>Chargement du fichier de configuration 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\settings-20260127_144259.json'.<br>	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/localizations-20260127_144259.csv' chargé avec succès.<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/localizations_filtered-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/localizations_filtered-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_filtered-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_filtered-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking-reconnected-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking-reconnected-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_filtered_reconnected-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_filtered_reconnected-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_MSD-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_MSD-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_MSD-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_MSD-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_InstantD-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_InstantD-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_InstantD_filtered-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_InstantD_filtered-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_Fit-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_Fit-20260127_144259.csv'<br>	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/tracking_Fit_filtered-20260127_144259.csv' : [Errno 2] No such file or directory: 'C:\\Git\\palm-tracer\\palm_tracer\\_tests\\input/stack_PALM_Tracer/tracking_Fit_filtered-20260127_144259.csv'<br>	Pile chargé avec succès (taille : (10, 128, 256)).<br>INFO: Sauvegarde du fichier image.</pre>
   </details>

.. raw:: html

   </div>
