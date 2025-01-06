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
     - Unknown Processor (2.2 GHz - 24 Cores (32 Logical))
   * - RAM
     - 63.69 GB
   * - GPU
     - NVIDIA GeForce RTX 4090 Laptop GPU (Memory: 16376.0MB)

Summary
-------

32 tests collected, 32 passed ✅, 0 failed ❌ in 0:00:16s on 06/01/2025 at 12:34:16

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

Settings Groups
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Base Group
     - ✅
     - 100ms
   * - Batch
     - ✅
     - 9ms
   * - Calibration
     - ✅
     - 216ms
   * - Localisation
     - ✅
     - 169ms
   * - Gaussian Fit
     - ✅
     - 176ms

.. raw:: html

   <details>
      <summary>Log Test : Batch</summary>
      <pre>- Activate : False<br>- Files : -1<br>- Mode : 0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Calibration</summary>
      <pre>- Activate : False<br>- Pixel Size : 320<br>- Exposure : 50<br>- Intensity : 0.012</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Localisation</summary>
      <pre>- Activate : False<br>- Preview : True<br>- Threshold : 90.0<br>- ROI Size : 7<br>- Watershed : True<br>- Mode : 0<br>- Gaussian Fit :<br>  - Activate : False<br>  - Sigma : 1.0<br>  - Sigma Fixed : False<br>  - Theta : 1.0<br>  - Theta Fixed : False</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gaussian Fit</summary>
      <pre>- Activate : False<br>- Sigma : 2.0<br>- Sigma Fixed : False<br>- Theta : 1.0<br>- Theta Fixed : False</pre>
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
     - 243ms

.. raw:: html

   <details>
      <summary>Log Test : Settings</summary>
      <pre>Settings :<br>  - Batch :<br>    - Activate : False<br>    - Files : -1<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : False<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : False<br>      - Sigma : 1.0<br>      - Sigma Fixed : False<br>      - Theta : 1.0<br>      - Theta Fixed : False</pre>
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
     - 234ms
   * - Create Setting From Dict Fail
     - ✅
     - 1ms
   * - Spin Int
     - ✅
     - 201ms
   * - Spin Float
     - ✅
     - 208ms
   * - Check Box
     - ✅
     - 3ms
   * - Combo
     - ✅
     - 2ms
   * - Browse File
     - ✅
     - 184ms
   * - File List
     - ✅
     - 3ms

Tools Monitoring
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Monitoring
     - ✅
     - 1.42s
   * - Monitoring Save
     - ✅
     - 6.76s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.64, 0.85, 1.07]<br>CPU Usage : [0.0, 0.51875, 0.44375, 0.446875, 0.446875, 0.0]<br>Memory Usage : [210.828125, 210.83203125, 210.83203125, 210.83203125, 210.83203125, 210.80859375]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
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
      <pre>-20250106_123410<br>-20250106</pre>
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

Reader
^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Reader
     - ✅
     - 33ms
   * - Get Reader Pass
     - ✅
     - 1ms

Sample Data
^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Something
     - ✅
     - 1ms

Widget
^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 3.42s
   * - Widget On Click
     - ✅
     - 573ms
   * - Threshold Autogenerate Widget
     - ✅
     - 1ms
   * - Threshold Magic Widget
     - ✅
     - 816ms
   * - Image Threshold Widget
     - ✅
     - 847ms
   * - Example Q Widget
     - ✅
     - 569ms

.. raw:: html

   <details>
      <summary>Log Test : Widget On Click</summary>
      <pre>napari has 1 layers<br>Settings :<br>  - Batch :<br>    - Activate : False<br>    - Files : -1<br>    - Mode : 0<br>  - Calibration :<br>    - Activate : False<br>    - Pixel Size : 160<br>    - Exposure : 50<br>    - Intensity : 0.012<br>  - Localisation :<br>    - Activate : False<br>    - Preview : False<br>    - Threshold : 90.0<br>    - ROI Size : 7<br>    - Watershed : True<br>    - Mode : 0<br>    - Gaussian Fit :<br>      - Activate : False<br>      - Sigma : 1.0<br>      - Sigma Fixed : False<br>      - Theta : 1.0<br>      - Theta Fixed : False</pre>
   </details>

Writer
^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Something
     - ✅
     - 1ms

.. raw:: html

   </div>
