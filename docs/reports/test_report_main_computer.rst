Test Report Main Computer
=========================

Environnement
-------------

.. list-table::

   * - Python
     - 3.13.1
   * - Platform
     - Windows-11-10.0.26100-SP0
   * - JAVA_HOME
     - C:\Program Files\OpenJDK\jdk-22.0.2
   * - System
     - Windows
   * - CPU
     - Unknown Processor (1.466 GHz - 24 Cores (32 Logical))
   * - RAM
     - 63.69 GB
   * - GPU
     - NVIDIA GeForce RTX 4090 Laptop GPU (Memory: 16376.0MB)

Summary
-------

72 tests collected, 72 passed ✅, 0 failed ❌ in 0:00:18s on 27/02/2025 at 12:05:30

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
   * - Process No Input
     - ✅
     - 1.51s
   * - Process Nothing
     - ✅
     - 130ms
   * - Process Multiple Stack
     - ✅
     - 121ms
   * - Process Only Localization
     - ✅
     - 142ms
   * - Process Only Tracking
     - ✅
     - 113ms
   * - Process Only Visualization Hr
     - ✅
     - 190ms
   * - Process Only Visualization Graph
     - ✅
     - 637ms
   * - Process All
     - ✅
     - 300ms

.. raw:: html

   <details>
      <summary>Log Test : Process No Input</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Nothing</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[27-02-2025 12:05:14] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Commencer le traitement.<br>[27-02-2025 12:05:14] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:14] Paramètres sauvegardés.<br>[27-02-2025 12:05:14] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:14] Localisation désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de localisation pré-calculée.<br>[27-02-2025 12:05:14] Tracking désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de tracking pré-calculée.<br>[27-02-2025 12:05:14] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:14] Visualisation graphique désactivée.<br>[27-02-2025 12:05:14] Traitement terminé.<br>[27-02-2025 12:05:14] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Commencer le traitement.<br>[27-02-2025 12:05:14] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:14] Paramètres sauvegardés.<br>[27-02-2025 12:05:14] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:14] Localisation désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de localisation pré-calculée.<br>[27-02-2025 12:05:14] Tracking désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de tracking pré-calculée.<br>[27-02-2025 12:05:14] Visualisation haute résolution activée.<br>[27-02-2025 12:05:14] 	Aucun fichier de localisation pour la visualisation.<br>[27-02-2025 12:05:14] Visualisation graphique désactivée.<br>[27-02-2025 12:05:14] Traitement terminé.<br>[27-02-2025 12:05:14] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Multiple Stack</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[27-02-2025 12:05:14] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Commencer le traitement.<br>[27-02-2025 12:05:14] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:14] Paramètres sauvegardés.<br>[27-02-2025 12:05:14] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:14] Localisation désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de localisation pré-calculée.<br>[27-02-2025 12:05:14] Tracking désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de tracking pré-calculée.<br>[27-02-2025 12:05:14] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:14] Visualisation graphique désactivée.<br>[27-02-2025 12:05:14] Traitement terminé.<br>[27-02-2025 12:05:14] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_quadrant_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Commencer le traitement.<br>[27-02-2025 12:05:14] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_quadrant_PALM_Tracer<br>[27-02-2025 12:05:14] Paramètres sauvegardés.<br>[27-02-2025 12:05:14] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:14] Localisation désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de localisation pré-calculée.<br>[27-02-2025 12:05:14] Tracking désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de tracking pré-calculée.<br>[27-02-2025 12:05:14] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:14] Visualisation graphique désactivée.<br>[27-02-2025 12:05:14] Traitement terminé.<br>[27-02-2025 12:05:14] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_quadrant_PALM_Tracer/log-20252702_120514.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Localization</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[27-02-2025 12:05:14] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Commencer le traitement.<br>[27-02-2025 12:05:14] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:14] Paramètres sauvegardés.<br>[27-02-2025 12:05:14] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:14] Localisation activée.<br>[27-02-2025 12:05:14] 	Enregistrement du fichier de localisation<br>[27-02-2025 12:05:14] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:14] Tracking désactivé.<br>[27-02-2025 12:05:14] 	Aucune donnée de tracking pré-calculée.<br>[27-02-2025 12:05:14] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:14] Visualisation graphique désactivée.<br>[27-02-2025 12:05:14] Traitement terminé.<br>[27-02-2025 12:05:14] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Tracking</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[27-02-2025 12:05:14] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Commencer le traitement.<br>[27-02-2025 12:05:14] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:14] Paramètres sauvegardés.<br>[27-02-2025 12:05:14] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:14] Localisation désactivé.<br>[27-02-2025 12:05:14] 	Chargement d'une localisation pré-calculée.<br>[27-02-2025 12:05:14] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:14] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:14] Tracking activé.<br>[27-02-2025 12:05:14] 	Enregistrement du fichier de tracking.<br>[27-02-2025 12:05:14] 		373 tracking(s) trouvé(s).<br>[27-02-2025 12:05:14] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:14] Visualisation graphique désactivée.<br>[27-02-2025 12:05:14] Traitement terminé.<br>[27-02-2025 12:05:14] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Visualization Hr</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[27-02-2025 12:05:14] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br>[27-02-2025 12:05:14] Commencer le traitement.<br>[27-02-2025 12:05:14] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:14] Paramètres sauvegardés.<br>[27-02-2025 12:05:14] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:14] Localisation désactivé.<br>[27-02-2025 12:05:14] 	Chargement d'une localisation pré-calculée.<br>[27-02-2025 12:05:14] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:14] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:14] Tracking désactivé.<br>[27-02-2025 12:05:14] 	Chargement d'un tracking pré-calculée.<br>[27-02-2025 12:05:14] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:14] 		373 tracking(s) trouvée(s).<br>[27-02-2025 12:05:14] Visualisation haute résolution activée.<br>[27-02-2025 12:05:14] 	Enregistrement du fichier de visualisation haute résolution (x2, s0).<br>[27-02-2025 12:05:14] Visualisation graphique désactivée.<br>[27-02-2025 12:05:14] Traitement terminé.<br>[27-02-2025 12:05:14] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120514.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Visualization Graph</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[27-02-2025 12:05:15] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br>[27-02-2025 12:05:15] Commencer le traitement.<br>[27-02-2025 12:05:15] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:15] Paramètres sauvegardés.<br>[27-02-2025 12:05:15] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:15] Localisation désactivé.<br>[27-02-2025 12:05:15] 	Chargement d'une localisation pré-calculée.<br>[27-02-2025 12:05:15] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:15] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:15] Tracking désactivé.<br>[27-02-2025 12:05:15] 	Chargement d'un tracking pré-calculée.<br>[27-02-2025 12:05:15] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:15] 		373 tracking(s) trouvée(s).<br>[27-02-2025 12:05:15] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:15] Visualisation graphique activée.<br>[27-02-2025 12:05:15] 	Enregistrement du fichier de visualisation graphique.<br>[27-02-2025 12:05:15] Traitement terminé.<br>[27-02-2025 12:05:15] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span><br>[27-02-2025 12:05:15] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br>[27-02-2025 12:05:15] Commencer le traitement.<br>[27-02-2025 12:05:15] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:15] Paramètres sauvegardés.<br>[27-02-2025 12:05:15] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:15] Localisation désactivé.<br>[27-02-2025 12:05:15] 	Chargement d'une localisation pré-calculée.<br>[27-02-2025 12:05:15] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:15] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:15] Tracking désactivé.<br>[27-02-2025 12:05:15] 	Chargement d'un tracking pré-calculée.<br>[27-02-2025 12:05:15] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:15] 		373 tracking(s) trouvée(s).<br>[27-02-2025 12:05:15] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:15] Visualisation graphique activée.<br>[27-02-2025 12:05:15] 	Enregistrement du fichier de visualisation graphique.<br>[27-02-2025 12:05:15] Traitement terminé.<br>[27-02-2025 12:05:15] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span><br>[27-02-2025 12:05:15] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br>[27-02-2025 12:05:15] Commencer le traitement.<br>[27-02-2025 12:05:15] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:15] Paramètres sauvegardés.<br>[27-02-2025 12:05:15] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:15] Localisation désactivé.<br>[27-02-2025 12:05:15] 	Chargement d'une localisation pré-calculée.<br>[27-02-2025 12:05:15] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:15] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:15] Tracking désactivé.<br>[27-02-2025 12:05:15] 	Chargement d'un tracking pré-calculée.<br>[27-02-2025 12:05:15] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252702_120514.csv' chargé avec succès.<br>[27-02-2025 12:05:15] 		373 tracking(s) trouvée(s).<br>[27-02-2025 12:05:15] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:15] Visualisation graphique activée.<br>[27-02-2025 12:05:15] 	Enregistrement du fichier de visualisation graphique.<br>[27-02-2025 12:05:15] Traitement terminé.<br>[27-02-2025 12:05:15] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process All</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[27-02-2025 12:05:15] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br>[27-02-2025 12:05:15] Commencer le traitement.<br>[27-02-2025 12:05:15] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:15] Paramètres sauvegardés.<br>[27-02-2025 12:05:15] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:15] Localisation activée.<br>[27-02-2025 12:05:15] 	Enregistrement du fichier de localisation<br>[27-02-2025 12:05:15] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:15] Tracking activé.<br>[27-02-2025 12:05:15] 	Enregistrement du fichier de tracking.<br>[27-02-2025 12:05:15] 		373 tracking(s) trouvé(s).<br>[27-02-2025 12:05:15] Visualisation haute résolution activée.<br>[27-02-2025 12:05:15] 	Enregistrement du fichier de visualisation haute résolution (x2, s0).<br>[27-02-2025 12:05:15] Visualisation graphique activée.<br>[27-02-2025 12:05:15] 	Enregistrement du fichier de visualisation graphique.<br>[27-02-2025 12:05:15] Traitement terminé.<br>[27-02-2025 12:05:15] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120515.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

Processing Dll
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Rearrange Dataframe Columns
     - ✅
     - 2ms
   * - Load Dll
     - ✅
     - 2ms
   * - Run Palm Image Dll
     - ✅
     - 340ms
   * - Run Palm Stack Dll
     - ✅
     - 298ms
   * - Run Palm Stack Dll Check Quadrant
     - ✅
     - 54ms
   * - Run Tracking Dll
     - ✅
     - 2ms

.. raw:: html

   <details>
      <summary>Log Test : Load Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Palm Image Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Palm Stack Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Palm Stack Dll Check Quadrant</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Tracking Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\stack-localizations-103.6_True_0_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
   </details>

Processing Threshold
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Auto Threshold
     - ✅
     - 2ms
   * - Auto Threshold Dll
     - ✅
     - 109ms

.. raw:: html

   <details>
      <summary>Log Test : Auto Threshold Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

Processing Visualization
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Hr Visualization
     - ✅
     - 36ms
   * - Hr Visualization Bad Input
     - ✅
     - 3ms
   * - Plot Histogram
     - ✅
     - 387ms
   * - Plot Histogram Bad Input
     - ✅
     - 104ms
   * - Plot Violin
     - ✅
     - 572ms
   * - Plot Violin Bad Input
     - ✅
     - 52ms
   * - Plot Heatmap
     - ✅
     - 278ms
   * - Plot Heatmap Bad Input
     - ✅
     - 50ms

Settings Groups
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Base Group
     - ✅
     - 74ms
   * - Batch
     - ✅
     - 72ms
   * - Batch Get Path
     - ✅
     - 71ms
   * - Batch Get Stacks
     - ✅
     - 75ms
   * - Calibration
     - ✅
     - 81ms
   * - Localization
     - ✅
     - 76ms
   * - Gaussian Fit
     - ✅
     - 72ms
   * - Spline Fit
     - ✅
     - 80ms
   * - Filtering
     - ✅
     - 78ms
   * - Filtering Gf
     - ✅
     - 74ms
   * - Filtering T
     - ✅
     - 181ms

.. raw:: html

   <details>
      <summary>Log Test : Batch</summary>
      <pre>- Activate : True<br>- Files : -1<br>- Mode : 0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Calibration</summary>
      <pre>- Activate : True<br>- Pixel Size : 320<br>- Exposure : 50<br>- Intensity : 0.012</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Localization</summary>
      <pre>- Activate : True<br>- Preview : True<br>- Threshold : 90.0<br>- ROI Size : 7<br>- Watershed : True<br>- Mode : 0<br>- Gaussian Fit :<br>  - Activate : True<br>  - Mode : 1<br>  - Sigma : 1.0<br>  - Theta : 0.0<br>- Spline Fit :<br>  - Activate : True<br>  - Peak : 1.0<br>  - Cut-Off : 1.0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gaussian Fit</summary>
      <pre>- Activate : True<br>- Mode : 2<br>- Sigma : 1.0<br>- Theta : 0.0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Spline Fit</summary>
      <pre>- Activate : True<br>- Peak : 2.0<br>- Cut-Off : 1.0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering</summary>
      <pre>- Activate : True<br>- Plane : [2, 3]<br>- Intensity : [1, 100]<br>- Gaussian Fit :<br>  - Activate : True<br>  - Chi² : [0.0, 1.0]<br>  - Sigma X : [0.0, 1.0]<br>  - Sigma Y : [0.0, 1.0]<br>  - Circularity : [0.0, 1.0]<br>  - Z : [-1.0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Length : [1, 100]<br>  - D Coeff : [0, 5]<br>  - Instant D : [0, 5]<br>  - Speed : [0.0, 1.0]<br>  - Alpha : [-1.0, 1.0]<br>  - Confinement : [-1.0, 1.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering Gf</summary>
      <pre>- Activate : True<br>- Chi² : [1.0, 2.0]<br>- Sigma X : [0.0, 1.0]<br>- Sigma Y : [0.0, 1.0]<br>- Circularity : [0.0, 1.0]<br>- Z : [-1.0, 1.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering T</summary>
      <pre>- Activate : True<br>- Length : [2, 3]<br>- D Coeff : [0, 5]<br>- Instant D : [0, 5]<br>- Speed : [0.0, 1.0]<br>- Alpha : [-1.0, 1.0]<br>- Confinement : [-1.0, 1.0]</pre>
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
     - 93ms

.. raw:: html

   <details>
      <summary>Log Test : Settings</summary>
      <pre>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : -1<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 320<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>    - Spline Fit :<br>      - Activate : True<br>      - Peak : 1.0<br>      - Cut-Off : 1.0<br>  - Tracking :<br>    - Activate : False<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - VisualizationHR :<br>    - Activate : False<br>    - Ratio : 2<br>    - Source : 0<br>  - VisualizationGraph :<br>    - Activate : False<br>    - Mode : 0<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : [1, 100]<br>    - Intensity : [1, 100]<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : [0.0, 1.0]<br>      - Sigma X : [0.0, 1.0]<br>      - Sigma Y : [0.0, 1.0]<br>      - Circularity : [0.0, 1.0]<br>      - Z : [-1.0, 1.0]<br>    - Tracks :<br>      - Activate : True<br>      - Length : [1, 100]<br>      - D Coeff : [0, 5]<br>      - Instant D : [0, 5]<br>      - Speed : [0.0, 1.0]<br>      - Alpha : [-1.0, 1.0]<br>      - Confinement : [-1.0, 1.0]</pre>
   </details>

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
     - 72ms
   * - Create Setting From Dict Fail
     - ✅
     - 69ms
   * - Spin Int
     - ✅
     - 80ms
   * - Spin Float
     - ✅
     - 70ms
   * - Check Box
     - ✅
     - 76ms
   * - Combo
     - ✅
     - 71ms
   * - Browse File
     - ✅
     - 70ms
   * - File List
     - ✅
     - 77ms
   * - Check Range Int
     - ✅
     - 72ms
   * - Check Range Float
     - ✅
     - 70ms

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
     - 7ms
   * - Save Tif 2D
     - ✅
     - 6ms
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
     - 3ms
   * - Save Png Bad Sample
     - ✅
     - 1ms

Tools Logger
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Logger
     - ✅
     - 16ms
   * - Logger Bad Use
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Logger</summary>
      <pre>[27-02-2025 12:05:20] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log<br>[27-02-2025 12:05:20] First message<br>[27-02-2025 12:05:20] <br>[27-02-2025 12:05:20] after blank<br>[27-02-2025 12:05:20] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Logger Bad Use</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-02-2025 12:05:20] Aucun fichier à fermer.</span><span style="font-weight: bold"></span><br>[27-02-2025 12:05:20] Message without logger open<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[27-02-2025 12:05:20] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span></pre>
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
     - 1.35s
   * - Monitoring Save
     - ✅
     - 5.06s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.63, 0.84, 1.01]<br>CPU Usage : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]<br>Memory Usage : [332.0625, 332.0625, 332.0625, 332.0625, 332.0625, 332.0390625]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Monitoring Save</summary>
      <pre>Simulating high CPU usage for 2 seconds...<br>CPU simulation complete.<br>Allocating 50 MB of memory...<br>Memory allocated. Holding for 1 seconds...<br>Releasing memory.<br>Writing a file of size 1 MB...<br>File written. Holding for 1 seconds...<br>Deleting the file...<br>Disk I/O simulation complete.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Kaleido doesn't work so well need update. No Image Saved.</span><span style="font-weight: bold"></span></pre>
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
     - 1ms
   * - Print Error
     - ✅
     - 1ms
   * - Print Warning
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Get Timestamp For Files</summary>
      <pre>Timestamp with hour : 20250227_120526<br>Timestamp without hour : 20250227</pre>
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

Widget
^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 1.55s
   * - Widget Reset Layer
     - ✅
     - 873ms
   * - Widget Auto Threshold
     - ✅
     - 492ms
   * - Widget Process
     - ✅
     - 534ms
   * - Widget Bad Dll
     - ✅
     - 628ms

.. raw:: html

   <details>
      <summary>Log Test : Widget Creation</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Reset Layer</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier sélectionné.</span><span style="font-weight: bold"></span><br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Auto Threshold</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier en preview.</span><span style="font-weight: bold"></span><br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Process</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier en preview.</span><span style="font-weight: bold"></span><br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br>[27-02-2025 12:05:29] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120529.log<br>[27-02-2025 12:05:29] Commencer le traitement.<br>[27-02-2025 12:05:29] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>[27-02-2025 12:05:29] Paramètres sauvegardés.<br>[27-02-2025 12:05:29] Fichier Meta sauvegardé.<br>[27-02-2025 12:05:29] Localisation désactivé.<br>[27-02-2025 12:05:29] 	Chargement d'une localisation pré-calculée.<br>[27-02-2025 12:05:29] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252702_120515.csv' chargé avec succès.<br>[27-02-2025 12:05:29] 		373 localisation(s) trouvée(s).<br>[27-02-2025 12:05:29] Tracking désactivé.<br>[27-02-2025 12:05:29] 	Chargement d'un tracking pré-calculée.<br>[27-02-2025 12:05:29] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252702_120515.csv' chargé avec succès.<br>[27-02-2025 12:05:29] 		373 tracking(s) trouvée(s).<br>[27-02-2025 12:05:29] Visualisation haute résolution désactivée.<br>[27-02-2025 12:05:29] Visualisation graphique désactivée.<br>[27-02-2025 12:05:29] Traitement terminé.<br>[27-02-2025 12:05:29] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252702_120529.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Bad Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Process non effectué car DLL manquantes.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   </div>
