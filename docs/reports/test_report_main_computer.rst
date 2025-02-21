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

57 tests collected, 57 passed ✅, 0 failed ❌ in 0:00:18s on 21/02/2025 at 10:52:50

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
     - 120ms
   * - Run Palm Image Dll
     - ✅
     - 350ms
   * - Run Palm Stack Dll
     - ✅
     - 316ms
   * - Run Palm Stack Dll Check Quadrant
     - ✅
     - 58ms
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
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\stack-localizations-103.6_True_2_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
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
     - 319ms
   * - Process Only Localization
     - ✅
     - 313ms
   * - Process Only Tracking
     - ✅
     - 308ms
   * - Process Only Visualization
     - ✅
     - 290ms
   * - Process All
     - ✅
     - 369ms

.. raw:: html

   <details>
      <summary>Log Test : Process No Input</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Localization</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[21-02-2025 10:52:33] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105233.log<br>[21-02-2025 10:52:33] Commencer le traitement.<br>[21-02-2025 10:52:33] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>  - Tracking :<br>    - Activate : False<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - Visualization :<br>    - Activate : False<br>    - Ratio : 2<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : 1<br>    - Intensity : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : 0<br>      - Sigma X : 0<br>      - Sigma Y : 0<br>      - Circularity : 0<br>      - Z : 0<br>    - Tracks :<br>      - Activate : True<br>      - Length : 0<br>      - D Coeff : 0<br>      - Instant D : 0<br>      - Speed : 0<br>      - Alpha : 0<br>      - Confinement : 0<br><br>[21-02-2025 10:52:33] Paramètres sauvegardés.<br>[21-02-2025 10:52:33] Fichier Meta sauvegardé.<br>[21-02-2025 10:52:33] Localisation désactivé.<br>[21-02-2025 10:52:33] 	Chargement d'une localisation pré-calculée.<br>[21-02-2025 10:52:33] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252102_103923.csv' chargé avec succès.<br>[21-02-2025 10:52:33] 		342 localisation(s) trouvée(s).<br>[21-02-2025 10:52:33] Tracking désactivé.<br>[21-02-2025 10:52:33] 	Chargement d'un tracking pré-calculée.<br>[21-02-2025 10:52:33] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252002_153520.csv' chargé avec succès.<br>[21-02-2025 10:52:33] 		342 tracking(s) trouvée(s).<br>[21-02-2025 10:52:33] Visualisation désactivée.<br>[21-02-2025 10:52:33] Traitement terminé.<br>[21-02-2025 10:52:33] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105233.log<br>[21-02-2025 10:52:33] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105233.log<br>[21-02-2025 10:52:33] Commencer le traitement.<br>[21-02-2025 10:52:33] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : True<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>  - Tracking :<br>    - Activate : False<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - Visualization :<br>    - Activate : False<br>    - Ratio : 2<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : 1<br>    - Intensity : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : 0<br>      - Sigma X : 0<br>      - Sigma Y : 0<br>      - Circularity : 0<br>      - Z : 0<br>    - Tracks :<br>      - Activate : True<br>      - Length : 0<br>      - D Coeff : 0<br>      - Instant D : 0<br>      - Speed : 0<br>      - Alpha : 0<br>      - Confinement : 0<br><br>[21-02-2025 10:52:33] Paramètres sauvegardés.<br>[21-02-2025 10:52:33] Fichier Meta sauvegardé.<br>[21-02-2025 10:52:33] Localisation commencée.<br>[21-02-2025 10:52:33] 	Enregistrement du fichier de localisation<br>[21-02-2025 10:52:33] 		373 localisation(s) trouvée(s).<br>[21-02-2025 10:52:33] Tracking désactivé.<br>[21-02-2025 10:52:33] 	Chargement d'un tracking pré-calculée.<br>[21-02-2025 10:52:33] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252002_153520.csv' chargé avec succès.<br>[21-02-2025 10:52:33] 		373 tracking(s) trouvée(s).<br>[21-02-2025 10:52:33] Visualisation désactivée.<br>[21-02-2025 10:52:33] Traitement terminé.<br>[21-02-2025 10:52:33] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105233.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Tracking</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[21-02-2025 10:52:33] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105233.log<br>[21-02-2025 10:52:33] Commencer le traitement.<br>[21-02-2025 10:52:33] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>  - Tracking :<br>    - Activate : True<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - Visualization :<br>    - Activate : False<br>    - Ratio : 2<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : 1<br>    - Intensity : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : 0<br>      - Sigma X : 0<br>      - Sigma Y : 0<br>      - Circularity : 0<br>      - Z : 0<br>    - Tracks :<br>      - Activate : True<br>      - Length : 0<br>      - D Coeff : 0<br>      - Instant D : 0<br>      - Speed : 0<br>      - Alpha : 0<br>      - Confinement : 0<br><br>[21-02-2025 10:52:33] Paramètres sauvegardés.<br>[21-02-2025 10:52:33] Fichier Meta sauvegardé.<br>[21-02-2025 10:52:33] Localisation désactivé.<br>[21-02-2025 10:52:33] 	Chargement d'une localisation pré-calculée.<br>[21-02-2025 10:52:33] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252102_105233.csv' chargé avec succès.<br>[21-02-2025 10:52:33] 		373 localisation(s) trouvée(s).<br>[21-02-2025 10:52:33] Tracking commencé.<br>[21-02-2025 10:52:34] 	Enregistrement du fichier de tracking.<br>[21-02-2025 10:52:34] 		373 tracking(s) trouvé(s).<br>[21-02-2025 10:52:34] Visualisation désactivée.<br>[21-02-2025 10:52:34] Traitement terminé.<br>[21-02-2025 10:52:34] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105233.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process Only Visualization</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[21-02-2025 10:52:34] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105234.log<br>[21-02-2025 10:52:34] Commencer le traitement.<br>[21-02-2025 10:52:34] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>  - Tracking :<br>    - Activate : False<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - Visualization :<br>    - Activate : True<br>    - Ratio : 2<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : 1<br>    - Intensity : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : 0<br>      - Sigma X : 0<br>      - Sigma Y : 0<br>      - Circularity : 0<br>      - Z : 0<br>    - Tracks :<br>      - Activate : True<br>      - Length : 0<br>      - D Coeff : 0<br>      - Instant D : 0<br>      - Speed : 0<br>      - Alpha : 0<br>      - Confinement : 0<br><br>[21-02-2025 10:52:34] Paramètres sauvegardés.<br>[21-02-2025 10:52:34] Fichier Meta sauvegardé.<br>[21-02-2025 10:52:34] Localisation désactivé.<br>[21-02-2025 10:52:34] 	Chargement d'une localisation pré-calculée.<br>[21-02-2025 10:52:34] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252102_105233.csv' chargé avec succès.<br>[21-02-2025 10:52:34] 		373 localisation(s) trouvée(s).<br>[21-02-2025 10:52:34] Tracking désactivé.<br>[21-02-2025 10:52:34] 	Chargement d'un tracking pré-calculée.<br>[21-02-2025 10:52:34] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252102_105233.csv' chargé avec succès.<br>[21-02-2025 10:52:34] 		373 tracking(s) trouvée(s).<br>[21-02-2025 10:52:34] Visualisation commencé.<br>[21-02-2025 10:52:34] 	Enregistrement du fichier de visualisation.<br>[21-02-2025 10:52:34] Traitement terminé.<br>[21-02-2025 10:52:34] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105234.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Process All</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>[21-02-2025 10:52:34] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105234.log<br>[21-02-2025 10:52:34] Commencer le traitement.<br>[21-02-2025 10:52:34] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : True<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>  - Tracking :<br>    - Activate : True<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - Visualization :<br>    - Activate : True<br>    - Ratio : 2<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : 1<br>    - Intensity : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : 0<br>      - Sigma X : 0<br>      - Sigma Y : 0<br>      - Circularity : 0<br>      - Z : 0<br>    - Tracks :<br>      - Activate : True<br>      - Length : 0<br>      - D Coeff : 0<br>      - Instant D : 0<br>      - Speed : 0<br>      - Alpha : 0<br>      - Confinement : 0<br><br>[21-02-2025 10:52:34] Paramètres sauvegardés.<br>[21-02-2025 10:52:34] Fichier Meta sauvegardé.<br>[21-02-2025 10:52:34] Localisation commencée.<br>[21-02-2025 10:52:34] 	Enregistrement du fichier de localisation<br>[21-02-2025 10:52:34] 		373 localisation(s) trouvée(s).<br>[21-02-2025 10:52:34] Tracking commencé.<br>[21-02-2025 10:52:34] 	Enregistrement du fichier de tracking.<br>[21-02-2025 10:52:34] 		373 tracking(s) trouvé(s).<br>[21-02-2025 10:52:34] Visualisation commencé.<br>[21-02-2025 10:52:34] 	Enregistrement du fichier de visualisation.<br>[21-02-2025 10:52:34] Traitement terminé.<br>[21-02-2025 10:52:34] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105234.log<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
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
     - 117ms

.. raw:: html

   <details>
      <summary>Log Test : Auto Threshold Dll</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500"><br>====================<br>Aucune comparaison avec Metamorph dans ce test.<br>====================<br></span><span style="font-weight: bold"></span></pre>
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
     - 236ms
   * - Batch Get Path
     - ✅
     - 3ms
   * - Batch Get Stacks
     - ✅
     - 7ms
   * - Calibration
     - ✅
     - 264ms
   * - Localization
     - ✅
     - 201ms
   * - Gaussian Fit
     - ✅
     - 205ms
   * - Spline Fit
     - ✅
     - 2ms
   * - Filtering
     - ✅
     - 200ms
   * - Filtering Gf
     - ✅
     - 186ms
   * - Filtering T
     - ✅
     - 217ms

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
      <pre>- Activate : True<br>- Preview : True<br>- Threshold : 90.0<br>- ROI Size : 7<br>- Watershed : True<br>- Mode : 0<br>- Gaussian Fit :<br>  - Activate : True<br>  - Mode : 1<br>  - Sigma : 1.0<br>  - Theta : 0.0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gaussian Fit</summary>
      <pre>- Activate : True<br>- Mode : 2<br>- Sigma : 1.0<br>- Theta : 0.0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering</summary>
      <pre>- Activate : True<br>- Plane : 2<br>- Intensity : 0<br>- Gaussian Fit :<br>  - Activate : True<br>  - Chi² : 0<br>  - Sigma X : 0<br>  - Sigma Y : 0<br>  - Circularity : 0<br>  - Z : 0<br>- Tracks :<br>  - Activate : True<br>  - Length : 0<br>  - D Coeff : 0<br>  - Instant D : 0<br>  - Speed : 0<br>  - Alpha : 0<br>  - Confinement : 0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering Gf</summary>
      <pre>- Activate : True<br>- Chi² : 2<br>- Sigma X : 0<br>- Sigma Y : 0<br>- Circularity : 0<br>- Z : 0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filtering T</summary>
      <pre>- Activate : True<br>- Length : 2<br>- D Coeff : 0<br>- Instant D : 0<br>- Speed : 0<br>- Alpha : 0<br>- Confinement : 0</pre>
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
     - 219ms

.. raw:: html

   <details>
      <summary>Log Test : Settings</summary>
      <pre>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : -1<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 320<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>  - Tracking :<br>    - Activate : False<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - Visualization :<br>    - Activate : False<br>    - Ratio : 2<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : 1<br>    - Intensity : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : 0<br>      - Sigma X : 0<br>      - Sigma Y : 0<br>      - Circularity : 0<br>      - Z : 0<br>    - Tracks :<br>      - Activate : True<br>      - Length : 0<br>      - D Coeff : 0<br>      - Instant D : 0<br>      - Speed : 0<br>      - Alpha : 0<br>      - Confinement : 0</pre>
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
     - 261ms
   * - Create Setting From Dict Fail
     - ✅
     - 1ms
   * - Spin Int
     - ✅
     - 193ms
   * - Spin Float
     - ✅
     - 176ms
   * - Check Box
     - ✅
     - 3ms
   * - Combo
     - ✅
     - 2ms
   * - Browse File
     - ✅
     - 166ms
   * - File List
     - ✅
     - 3ms

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
     - 2ms
   * - Logger Bad Use
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Logger</summary>
      <pre>[21-02-2025 10:52:37] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log<br>[21-02-2025 10:52:37] First message<br>[21-02-2025 10:52:37] <br>[21-02-2025 10:52:37] after blank<br>[21-02-2025 10:52:37] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Logger Bad Use</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[21-02-2025 10:52:37] Aucun fichier à fermer.</span><span style="font-weight: bold"></span><br>[21-02-2025 10:52:37] Message without logger open<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[21-02-2025 10:52:37] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span></pre>
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
     - 1.46s
   * - Monitoring Save
     - ✅
     - 4.94s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.63, 0.84, 1.05]<br>CPU Usage : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]<br>Memory Usage : [220.41796875, 220.421875, 220.421875, 220.42578125, 220.42578125, 220.40625]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
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
      <pre>Timestamp with hour : 20250221_105243<br>Timestamp without hour : 20250221</pre>
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
     - 5.03s
   * - Widget Reset Layer
     - ✅
     - 729ms
   * - Widget Auto Threshold
     - ✅
     - 596ms
   * - Widget Process
     - ✅
     - 517ms

.. raw:: html

   <details>
      <summary>Log Test : Widget Creation</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Reset Layer</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Auto Threshold</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Process</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' chargée.<br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br>Loaded C:\Git\palm-tracer\palm_tracer\_tests\input/stack.tif into Napari viewer.<br>[21-02-2025 10:52:50] Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105250.log<br>[21-02-2025 10:52:50] Commencer le traitement.<br>[21-02-2025 10:52:50] Dossier de sortie : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer<br>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : 0<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localization :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Mode : 1<br>      - Sigma : 1.0<br>      - Theta : 0.0<br>  - Tracking :<br>    - Activate : False<br>    - Max Distance : 5.0<br>    - Min Length : 1.0<br>    - Decrease : 10.0<br>    - Cost Birth : 0.5<br>  - Visualization :<br>    - Activate : False<br>    - Ratio : 2<br>    - Source : 0<br>  - Filtering :<br>    - Activate : True<br>    - Plane : 1<br>    - Intensity : 0<br>    - Gaussian Fit :<br>      - Activate : True<br>      - Chi² : 0<br>      - Sigma X : 0<br>      - Sigma Y : 0<br>      - Circularity : 0<br>      - Z : 0<br>    - Tracks :<br>      - Activate : True<br>      - Length : 0<br>      - D Coeff : 0<br>      - Instant D : 0<br>      - Speed : 0<br>      - Alpha : 0<br>      - Confinement : 0<br><br>[21-02-2025 10:52:50] Paramètres sauvegardés.<br>[21-02-2025 10:52:50] Fichier Meta sauvegardé.<br>[21-02-2025 10:52:50] Localisation désactivé.<br>[21-02-2025 10:52:50] 	Chargement d'une localisation pré-calculée.<br>[21-02-2025 10:52:50] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\localizations-20252102_105234.csv' chargé avec succès.<br>[21-02-2025 10:52:50] 		373 localisation(s) trouvée(s).<br>[21-02-2025 10:52:50] Tracking désactivé.<br>[21-02-2025 10:52:50] 	Chargement d'un tracking pré-calculée.<br>[21-02-2025 10:52:50] 	Fichier 'C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer\tracking-20252102_105234.csv' chargé avec succès.<br>[21-02-2025 10:52:50] 		373 tracking(s) trouvée(s).<br>[21-02-2025 10:52:50] Visualisation désactivée.<br>[21-02-2025 10:52:50] Traitement terminé.<br>[21-02-2025 10:52:50] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\input/stack_PALM_Tracer/log-20252102_105250.log</pre>
   </details>

.. raw:: html

   </div>
