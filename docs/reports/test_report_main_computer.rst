Test Report Main Computer
=========================

Environnement
-------------

.. list-table::

   * - Python
     - 3.12.6
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

42 tests collected, 42 passed ✅, 0 failed ❌ in 0:00:14s on 15/01/2025 at 14:47:36

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
   * - Get Gaussian Mode
     - ✅
     - 123ms
   * - Get Max Points
     - ✅
     - 1ms
   * - Parse Palm Result
     - ✅
     - 2ms
   * - Load Dll
     - ✅
     - 21ms
   * - Run Palm Image Dll
     - ✅
     - 39ms
   * - Run Palm Stack Dll
     - ✅
     - 272ms

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

Processing Threshold
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Auto Threshold
     - ✅
     - 3ms
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
     - 8ms
   * - Batch
     - ✅
     - 6ms
   * - Calibration
     - ✅
     - 201ms
   * - Localisation
     - ✅
     - 156ms
   * - Gaussian Fit
     - ✅
     - 144ms

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
      <pre>- Activate : True<br>- Preview : True<br>- Threshold : 90.0<br>- ROI Size : 7<br>- Watershed : True<br>- Mode : 0<br>- Gaussian Fit :<br>  - Activate : False<br>  - Sigma : 1.0<br>  - Sigma Fixed : False<br>  - Theta : 1.0<br>  - Theta Fixed : False</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gaussian Fit</summary>
      <pre>- Activate : True<br>- Sigma : 2.0<br>- Sigma Fixed : False<br>- Theta : 1.0<br>- Theta Fixed : False</pre>
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
     - 161ms

.. raw:: html

   <details>
      <summary>Log Test : Settings</summary>
      <pre>Settings :<br>  - Batch :<br>    - Activate : True<br>    - Files : -1<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : True<br>    - Pixel Size : 320<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : False<br>      - Sigma : 1.0<br>      - Sigma Fixed : False<br>      - Theta : 1.0<br>      - Theta Fixed : False</pre>
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
     - 170ms
   * - Create Setting From Dict Fail
     - ✅
     - 1ms
   * - Spin Int
     - ✅
     - 161ms
   * - Spin Float
     - ✅
     - 180ms
   * - Check Box
     - ✅
     - 2ms
   * - Combo
     - ✅
     - 2ms
   * - Browse File
     - ✅
     - 163ms
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
     - 10ms
   * - Save Tif 2D
     - ✅
     - 8ms
   * - Save Tif Bad Stack
     - ✅
     - 1ms
   * - Open Tif
     - ✅
     - 9ms
   * - Open Tif Bad File
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
     - 17ms
   * - Logger Bad Use
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Logger</summary>
      <pre>[15-01-2025 14:47:23] : Log ouvert : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log<br>[15-01-2025 14:47:23] First message<br>[15-01-2025 14:47:23] <br>[15-01-2025 14:47:23] after blank<br>[15-01-2025 14:47:23] Log fermé : C:\Git\palm-tracer\palm_tracer\_tests\output/test_logger.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Logger Bad Use</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[15-01-2025 14:47:23] Aucun fichier à fermer.</span><span style="font-weight: bold"></span><br>[15-01-2025 14:47:23] Message without logger open<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">[15-01-2025 14:47:23] Aucun fichier de log ouvert pour écrire.</span><span style="font-weight: bold"></span></pre>
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
     - 6.71s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.63, 0.84, 1.04]<br>CPU Usage : [0.0, 0.446875, 0.525, 0.0, 0.0, 0.525]<br>Memory Usage : [222.28515625, 222.28515625, 222.28515625, 222.2890625, 222.29296875, 222.26953125]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Monitoring Save</summary>
      <pre>Simulating high CPU usage for 2 seconds...<br>CPU simulation complete.<br>Allocating 50 MB of memory...<br>Memory allocated. Holding for 2 seconds...<br>Releasing memory.<br>Writing a file of size 10 MB...<br>File written. Holding for 2 seconds...<br>Deleting the file...<br>Disk I/O simulation complete.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Kaleido doesn't work so well need update. No Image Saved.</span><span style="font-weight: bold"></span></pre>
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
   * - Print Error
     - ✅
     - 1ms
   * - Print Warning
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Get Timestamp For Files</summary>
      <pre>-20250115_144731<br>-20250115</pre>
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
     - 4.11s
   * - Widget Process
     - ✅
     - 601ms

.. raw:: html

   <details>
      <summary>Log Test : Widget Creation</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Process</summary>
      <pre>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\CPU_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\GPU_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Impossible de charger la DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\Live_PALM.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span><br>DLL 'C:\Git\palm-tracer\palm_tracer\DLL\Tracking_PALM.dll' chargée.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier en preview.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   </div>
