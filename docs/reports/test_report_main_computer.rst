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
     - Unknown Processor (2.2 GHz - 24 Cores (32 Logical))
   * - RAM
     - 63.69 GB
   * - GPU
     - NVIDIA GeForce RTX 4090 Laptop GPU (Memory: 16376.0MB)

Summary
-------

51 tests collected, 51 passed ✅, 0 failed ❌ in 0:00:19s on 30/01/2025 at 15:11:59

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

Processing Dll
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Load Dll
     - ✅
     - 291ms
   * - Run Palm Image Dll
     - ✅
     - 64ms
   * - Run Palm Stack Dll
     - ✅
     - 335ms

.. raw:: html

   <details>
      <summary>Log Test : Load Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Palm Image Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Palm Stack Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

Processing Palm
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Process No Input
     - ✅
     - 389ms
   * - Process Only Localisation
     - ✅
     - 284ms
   * - Process Only Tracking
     - ✅
     - 206ms
   * - Process Only Visualization
     - ✅
     - 277ms
   * - Process All
     - ✅
     - 279ms

.. raw:: html

   <details>
      <summary>Log Test : Process No Input</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Localisation</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[30-01-2025 15:11:41] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br>[30-01-2025 15:11:41] Commencer le traitement.<br>[30-01-2025 15:11:41] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : False<br><br>[30-01-2025 15:11:41] Paramètres sauvegardés.<br>[30-01-2025 15:11:41] Fichier Meta sauvegardé.<br>[30-01-2025 15:11:41] Localisation désactivé.<br>[30-01-2025 15:11:41] 	Chargement d'une localisation pré-calculée.<br>[30-01-2025 15:11:41] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localisations-20252201_151621.csv' chargé avec succès.<br>[30-01-2025 15:11:41] 		5222 localisation(s) trouvée(s).<br>[30-01-2025 15:11:41] Tracking désactivé.<br>[30-01-2025 15:11:41] 	Chargement d'un tracking pré-calculée.<br>[30-01-2025 15:11:41] 	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252201_151621.csv' : No columns to parse from file<br>[30-01-2025 15:11:41] Visualisation désactivée.<br>[30-01-2025 15:11:41] Traitement terminé.<br>[30-01-2025 15:11:41] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br>[30-01-2025 15:11:41] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br>[30-01-2025 15:11:41] Commencer le traitement.<br>[30-01-2025 15:11:41] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : True<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : False<br><br>[30-01-2025 15:11:41] Paramètres sauvegardés.<br>[30-01-2025 15:11:41] Fichier Meta sauvegardé.<br>[30-01-2025 15:11:41] Localisation commencée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO PALM._palm_to_localisation_file</span><span style="font-weight: bold"></span><br>[30-01-2025 15:11:41] 	4849 localisation(s) trouvée(s).<br>[30-01-2025 15:11:41] Enregistrement du fichier de localisation<br>[30-01-2025 15:11:41] Tracking désactivé.<br>[30-01-2025 15:11:41] 	Chargement d'un tracking pré-calculée.<br>[30-01-2025 15:11:41] 	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252201_151621.csv' : No columns to parse from file<br>[30-01-2025 15:11:41] Visualisation désactivée.<br>[30-01-2025 15:11:41] Traitement terminé.<br>[30-01-2025 15:11:41] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Tracking</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[30-01-2025 15:11:41] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br>[30-01-2025 15:11:41] Commencer le traitement.<br>[30-01-2025 15:11:41] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : True<br>  - Visualization :<br>    - Activate : False<br><br>[30-01-2025 15:11:41] Paramètres sauvegardés.<br>[30-01-2025 15:11:41] Fichier Meta sauvegardé.<br>[30-01-2025 15:11:41] Localisation désactivé.<br>[30-01-2025 15:11:41] 	Chargement d'une localisation pré-calculée.<br>[30-01-2025 15:11:41] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localisations-20253001_151141.csv' chargé avec succès.<br>[30-01-2025 15:11:41] 		4849 localisation(s) trouvée(s).<br>[30-01-2025 15:11:41] Tracking commencé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO PALM.tracking</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO _palm_to_tracking_file</span><span style="font-weight: bold"></span><br>[30-01-2025 15:11:41] Enregistrement du fichier de tracking.<br>[30-01-2025 15:11:41] Visualisation désactivée.<br>[30-01-2025 15:11:41] Traitement terminé.<br>[30-01-2025 15:11:41] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Visualization</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[30-01-2025 15:11:41] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br>[30-01-2025 15:11:41] Commencer le traitement.<br>[30-01-2025 15:11:41] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : True<br><br>[30-01-2025 15:11:41] Paramètres sauvegardés.<br>[30-01-2025 15:11:41] Fichier Meta sauvegardé.<br>[30-01-2025 15:11:41] Localisation désactivé.<br>[30-01-2025 15:11:41] 	Chargement d'une localisation pré-calculée.<br>[30-01-2025 15:11:41] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localisations-20253001_151141.csv' chargé avec succès.<br>[30-01-2025 15:11:41] 		4849 localisation(s) trouvée(s).<br>[30-01-2025 15:11:41] Tracking désactivé.<br>[30-01-2025 15:11:41] 	Chargement d'un tracking pré-calculée.<br>[30-01-2025 15:11:41] 	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20253001_151141.csv' : No columns to parse from file<br>[30-01-2025 15:11:41] Visualisation commencé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO PALM.visualization</span><span style="font-weight: bold"></span><br>[30-01-2025 15:11:41] Enregistrement du fichier de visualisation.<br>[30-01-2025 15:11:41] Traitement terminé.<br>[30-01-2025 15:11:41] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151141.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process All</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[30-01-2025 15:11:42] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151142.log<br>[30-01-2025 15:11:42] Commencer le traitement.<br>[30-01-2025 15:11:42] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : True<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : True<br>  - Visualization :<br>    - Activate : True<br><br>[30-01-2025 15:11:42] Paramètres sauvegardés.<br>[30-01-2025 15:11:42] Fichier Meta sauvegardé.<br>[30-01-2025 15:11:42] Localisation commencée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO PALM._palm_to_localisation_file</span><span style="font-weight: bold"></span><br>[30-01-2025 15:11:42] 	4849 localisation(s) trouvée(s).<br>[30-01-2025 15:11:42] Enregistrement du fichier de localisation<br>[30-01-2025 15:11:42] Tracking commencé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO PALM.tracking</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO _palm_to_tracking_file</span><span style="font-weight: bold"></span><br>[30-01-2025 15:11:42] Enregistrement du fichier de tracking.<br>[30-01-2025 15:11:42] Visualisation commencé.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">TODO PALM.visualization</span><span style="font-weight: bold"></span><br>[30-01-2025 15:11:42] Enregistrement du fichier de visualisation.<br>[30-01-2025 15:11:42] Traitement terminé.<br>[30-01-2025 15:11:42] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151142.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
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
     - 15ms

.. raw:: html

   <details>
      <summary>Log Test : Auto Threshold</summary>
      <pre>104.24780444414506</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Auto Threshold Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>103.61033392219885<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

Settings Groups
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Base Group
     - ✅
     - 3ms
   * - Batch
     - ✅
     - 195ms
   * - Batch Get Path
     - ✅
     - 6ms
   * - Batch Get Stacks
     - ✅
     - 8ms
   * - Calibration
     - ✅
     - 210ms
   * - Localisation
     - ✅
     - 200ms
   * - Gaussian Fit
     - ✅
     - 187ms

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
      <summary>Log Test : Localisation</summary>
      <pre>- Activate : True<br>- Preview : True<br>- Threshold : 90.0<br>- ROI Size : 7<br>- Watershed : True<br>- Mode : 0<br>- Gaussian Fit :<br>  - Activate : True<br>  - Mode : 1<br>  - Sigma : 1.0<br>  - Theta : 1.0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gaussian Fit</summary>
      <pre>- Activate : True<br>- Mode : 2<br>- Sigma : 1.0<br>- Theta : 1.0</pre>
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
     - 223ms

.. raw:: html

   <details>
      <summary>Log Test : Settings</summary>
      <pre>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : -1<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 320<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : False</pre>
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
     - 159ms
   * - Create Setting From Dict Fail
     - ✅
     - 1ms
   * - Spin Int
     - ✅
     - 158ms
   * - Spin Float
     - ✅
     - 179ms
   * - Check Box
     - ✅
     - 2ms
   * - Combo
     - ✅
     - 2ms
   * - Browse File
     - ✅
     - 183ms
   * - File List
     - ✅
     - 2ms

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
     - 8ms
   * - Save Tif 2D
     - ✅
     - 6ms
   * - Save Tif Bad Stack
     - ✅
     - 1ms
   * - Open Tif
     - ✅
     - 8ms
   * - Open Tif Bad File
     - ✅
     - 1ms
   * - Save  Png
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
     - 1ms
   * - Logger Bad Use
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Logger</summary>
      <pre>[30-01-2025 15:11:44] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log<br>[30-01-2025 15:11:44] First message<br>[30-01-2025 15:11:44] <br>[30-01-2025 15:11:44] after blank<br>[30-01-2025 15:11:44] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Logger Bad Use</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[30-01-2025 15:11:44] Aucun fichier à fermer.</span><span style="font-weight: bold"></span><br>[30-01-2025 15:11:44] Message without logger open<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[30-01-2025 15:11:44] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span></pre>
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
     - 1.38s
   * - Monitoring Save
     - ✅
     - 4.93s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.63, 0.84, 1.05]<br>CPU Usage : [0.0, 0.0, 0.4875, 0.484375, 0.0, 0.484375]<br>Memory Usage : [222.5390625, 222.54296875, 222.54296875, 222.54296875, 222.54296875, 222.51953125]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
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
     - 0ms

.. raw:: html

   <details>
      <summary>Log Test : Get Timestamp For Files</summary>
      <pre>Timestamp with hour : 20250130_151150<br>Timestamp without hour : 20250130</pre>
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
     - 7.17s
   * - Widget Reset Layer
     - ✅
     - 838ms
   * - Widget Auto Threshold
     - ✅
     - 676ms
   * - Widget Process
     - ✅
     - 573ms

.. raw:: html

   <details>
      <summary>Log Test : Widget Creation</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Reset Layer</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Auto Threshold</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Process</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br>[30-01-2025 15:11:59] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151159.log<br>[30-01-2025 15:11:59] Commencer le traitement.<br>[30-01-2025 15:11:59] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : False<br><br>[30-01-2025 15:11:59] Paramètres sauvegardés.<br>[30-01-2025 15:11:59] Fichier Meta sauvegardé.<br>[30-01-2025 15:11:59] Localisation désactivé.<br>[30-01-2025 15:11:59] 	Chargement d'une localisation pré-calculée.<br>[30-01-2025 15:11:59] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localisations-20253001_151142.csv' chargé avec succès.<br>[30-01-2025 15:11:59] 		4849 localisation(s) trouvée(s).<br>[30-01-2025 15:11:59] Tracking désactivé.<br>[30-01-2025 15:11:59] 	Chargement d'un tracking pré-calculée.<br>[30-01-2025 15:11:59] 	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20253001_151142.csv' : No columns to parse from file<br>[30-01-2025 15:11:59] Visualisation désactivée.<br>[30-01-2025 15:11:59] Traitement terminé.<br>[30-01-2025 15:11:59] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20253001_151159.log</pre>
   </details>

.. raw:: html

   </div>
