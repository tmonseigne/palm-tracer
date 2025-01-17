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

51 tests collected, 51 passed ✅, 0 failed ❌ in 0:00:14s on 17/01/2025 at 18:18:30

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
     - 123ms
   * - Run Palm Image Dll
     - ✅
     - 64ms
   * - Run Palm Stack Dll
     - ✅
     - 281ms

.. raw:: html

   <details>
      <summary>Log Test : Load Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Palm Image Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Run Palm Stack Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
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
     - 355ms
   * - Process Only Localisation
     - ✅
     - 379ms
   * - Process Only Tracking
     - ✅
     - 276ms
   * - Process Only Visualization
     - ✅
     - 290ms
   * - Process All
     - ✅
     - 284ms

.. raw:: html

   <details>
      <summary>Log Test : Process No Input</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Localisation</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[17-01-2025 18:18:17] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log<br>[17-01-2025 18:18:17] Commencer le traitement.<br>[17-01-2025 18:18:17] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : False<br><br>[17-01-2025 18:18:17] Paramètres sauvegardés.<br>[17-01-2025 18:18:17] Fichier Meta sauvegardé.<br>[17-01-2025 18:18:17] Localisation désactivé.<br>[17-01-2025 18:18:17] 	Aucune donnée de localisation pré-calculée.<br>[17-01-2025 18:18:17] Tracking désactivé.<br>[17-01-2025 18:18:17] 	Aucune donnée de tracking pré-calculée.<br>[17-01-2025 18:18:17] Visualisation désactivée.<br>[17-01-2025 18:18:17] Traitement terminé.<br>[17-01-2025 18:18:17] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log<br>[17-01-2025 18:18:17] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log<br>[17-01-2025 18:18:17] Commencer le traitement.<br>[17-01-2025 18:18:17] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : True<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : False<br><br>[17-01-2025 18:18:17] Paramètres sauvegardés.<br>[17-01-2025 18:18:17] Fichier Meta sauvegardé.<br>[17-01-2025 18:18:17] Localisation commencée.<br>TODO PALM._palm_to_localisation_file<br>[17-01-2025 18:18:17] 	5222 localisation(s) trouvée(s).<br>[17-01-2025 18:18:17] Enregistrement du fichier de localisation<br>[17-01-2025 18:18:17] Tracking désactivé.<br>[17-01-2025 18:18:17] 	Aucune donnée de tracking pré-calculée.<br>[17-01-2025 18:18:17] Visualisation désactivée.<br>[17-01-2025 18:18:17] Traitement terminé.<br>[17-01-2025 18:18:17] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Tracking</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[17-01-2025 18:18:17] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log<br>[17-01-2025 18:18:17] Commencer le traitement.<br>[17-01-2025 18:18:17] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : True<br>  - Visualization :<br>    - Activate : False<br><br>[17-01-2025 18:18:17] Paramètres sauvegardés.<br>[17-01-2025 18:18:17] Fichier Meta sauvegardé.<br>[17-01-2025 18:18:17] Localisation désactivé.<br>[17-01-2025 18:18:17] 	Chargement d'une localisation pré-calculée.<br>[17-01-2025 18:18:17] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localisations-20251701_181817.csv' chargé avec succès.<br>[17-01-2025 18:18:17] 		5222 localisation(s) trouvée(s).<br>[17-01-2025 18:18:17] Tracking commencé.<br>TODO PALM.tracking<br>TODO _palm_to_tracking_file<br>[17-01-2025 18:18:17] Enregistrement du fichier de tracking.<br>[17-01-2025 18:18:17] Visualisation désactivée.<br>[17-01-2025 18:18:17] Traitement terminé.<br>[17-01-2025 18:18:17] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Visualization</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[17-01-2025 18:18:17] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log<br>[17-01-2025 18:18:17] Commencer le traitement.<br>[17-01-2025 18:18:17] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : True<br><br>[17-01-2025 18:18:17] Paramètres sauvegardés.<br>[17-01-2025 18:18:17] Fichier Meta sauvegardé.<br>[17-01-2025 18:18:17] Localisation désactivé.<br>[17-01-2025 18:18:17] 	Chargement d'une localisation pré-calculée.<br>[17-01-2025 18:18:17] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localisations-20251701_181817.csv' chargé avec succès.<br>[17-01-2025 18:18:17] 		5222 localisation(s) trouvée(s).<br>[17-01-2025 18:18:17] Tracking désactivé.<br>[17-01-2025 18:18:17] 	Chargement d'un tracking pré-calculée.<br>[17-01-2025 18:18:17] 	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20251701_181817.csv' : No columns to parse from file<br>[17-01-2025 18:18:17] Visualisation commencé.<br>TODO PALM.visualization<br>[17-01-2025 18:18:17] Enregistrement du fichier de visualisation.<br>[17-01-2025 18:18:17] Traitement terminé.<br>[17-01-2025 18:18:17] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process All</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[17-01-2025 18:18:17] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log<br>[17-01-2025 18:18:17] Commencer le traitement.<br>[17-01-2025 18:18:17] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : True<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : True<br>  - Visualization :<br>    - Activate : True<br><br>[17-01-2025 18:18:17] Paramètres sauvegardés.<br>[17-01-2025 18:18:17] Fichier Meta sauvegardé.<br>[17-01-2025 18:18:17] Localisation commencée.<br>TODO PALM._palm_to_localisation_file<br>[17-01-2025 18:18:18] 	5222 localisation(s) trouvée(s).<br>[17-01-2025 18:18:18] Enregistrement du fichier de localisation<br>[17-01-2025 18:18:18] Tracking commencé.<br>TODO PALM.tracking<br>TODO _palm_to_tracking_file<br>[17-01-2025 18:18:18] Enregistrement du fichier de tracking.<br>[17-01-2025 18:18:18] Visualisation commencé.<br>TODO PALM.visualization<br>[17-01-2025 18:18:18] Enregistrement du fichier de visualisation.<br>[17-01-2025 18:18:18] Traitement terminé.<br>[17-01-2025 18:18:18] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181817.log</pre>
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
     - 11ms

.. raw:: html

   <details>
      <summary>Log Test : Auto Threshold</summary>
      <pre>104.24780444414506</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Auto Threshold Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>103.61033392219885</pre>
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
     - 13ms
   * - Batch
     - ✅
     - 208ms
   * - Batch Get Path
     - ✅
     - 12ms
   * - Batch Get Stacks
     - ✅
     - 18ms
   * - Calibration
     - ✅
     - 188ms
   * - Localisation
     - ✅
     - 214ms
   * - Gaussian Fit
     - ✅
     - 185ms

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
     - 260ms

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
     - 151ms
   * - Create Setting From Dict Fail
     - ✅
     - 1ms
   * - Spin Int
     - ✅
     - 125ms
   * - Spin Float
     - ✅
     - 132ms
   * - Check Box
     - ✅
     - 4ms
   * - Combo
     - ✅
     - 3ms
   * - Browse File
     - ✅
     - 123ms
   * - File List
     - ✅
     - 5ms

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
     - 22ms
   * - Save Tif 2D
     - ✅
     - 7ms
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
      <pre>[17-01-2025 18:18:19] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log<br>[17-01-2025 18:18:19] First message<br>[17-01-2025 18:18:19] <br>[17-01-2025 18:18:19] after blank<br>[17-01-2025 18:18:19] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Logger Bad Use</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[17-01-2025 18:18:19] Aucun fichier à fermer.</span><span style="font-weight: bold"></span><br>[17-01-2025 18:18:19] Message without logger open<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[17-01-2025 18:18:19] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span></pre>
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
     - 4.51s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.63, 0.84, 1.05]<br>CPU Usage : [0.0, 0.4875, 0.0, 0.484375, 0.484375, 0.0]<br>Memory Usage : [222.01953125, 222.01953125, 222.0234375, 222.0234375, 222.02734375, 222.00390625]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
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
      <pre>Timestamp with hour : 20250117_181825<br>Timestamp without hour : 20250117</pre>
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
     - 3.05s
   * - Widget Reset Layer
     - ✅
     - 779ms
   * - Widget Auto Threshold
     - ✅
     - 669ms
   * - Widget Process
     - ✅
     - 574ms

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
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br>[17-01-2025 18:18:30] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181830.log<br>[17-01-2025 18:18:30] Commencer le traitement.<br>[17-01-2025 18:18:30] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 1.0<br>  - Tracking :<br>    - Activate : False<br>  - Visualization :<br>    - Activate : False<br><br>[17-01-2025 18:18:30] Paramètres sauvegardés.<br>[17-01-2025 18:18:30] Fichier Meta sauvegardé.<br>[17-01-2025 18:18:30] Localisation désactivé.<br>[17-01-2025 18:18:30] 	Chargement d'une localisation pré-calculée.<br>[17-01-2025 18:18:30] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localisations-20251701_181817.csv' chargé avec succès.<br>[17-01-2025 18:18:30] 		5222 localisation(s) trouvée(s).<br>[17-01-2025 18:18:30] Tracking désactivé.<br>[17-01-2025 18:18:30] 	Chargement d'un tracking pré-calculée.<br>[17-01-2025 18:18:30] 	Erreur lors du chargement du fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20251701_181817.csv' : No columns to parse from file<br>[17-01-2025 18:18:30] Visualisation désactivée.<br>[17-01-2025 18:18:30] Traitement terminé.<br>[17-01-2025 18:18:30] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20251701_181830.log</pre>
   </details>

.. raw:: html

   </div>
