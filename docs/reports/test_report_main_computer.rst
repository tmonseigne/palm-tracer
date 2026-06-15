Test Report Main Computer
=========================

Environnement
-------------

.. list-table::

   * - Python
     - 3.14.5
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

270 tests collected, 270 passed ✅, 0 failed ❌, 0 skipped ⏭️ in 0:00:58s on 15/06/2026 at 10:08:48

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
   * - Reset Result
     - ✅
     - 39ms
   * - Getter Localization
     - ✅
     - 13ms
   * - Getter Beads
     - ✅
     - 5ms
   * - Getter Tracks
     - ✅
     - 9ms
   * - Getter Tracks Compute
     - ✅
     - 4ms
   * - Get Status
     - ✅
     - 14ms
   * - Getter Path
     - ✅
     - 3ms
   * - Getter Stack
     - ✅
     - 139ms
   * - Getter Suffix
     - ✅
     - 4ms
   * - Load Bad Dll
     - ✅
     - 8ms
   * - Load Nothing
     - ✅
     - 5ms
   * - Load
     - ✅
     - 102ms
   * - Process No Input
     - ✅
     - 4ms
   * - Process Nothing
     - ✅
     - 286ms
   * - Process Bad Dll
     - ✅
     - 4ms
   * - Process Multiple Stack
     - ✅
     - 39ms
   * - Process Localization
     - ✅
     - 32ms
   * - Process Localization Z
     - ✅
     - 83ms
   * - Process Localization Spline Bad
     - ✅
     - 16ms
   * - Process Localization Spline
     - ✅
     - 35ms
   * - Process Beads Extraction No Beads
     - ✅
     - 49ms
   * - Process Plane Discontinuous
     - ✅
     - 7ms
   * - Process Beads Extraction
     - ✅
     - 49ms
   * - Process Tracking
     - ✅
     - 38ms
   * - Process Tracking Blinking
     - ✅
     - 33ms
   * - Process Tracks Compute
     - ✅
     - 2.14s
   * - Process Gallery
     - ✅
     - 37ms
   * - Process Visualization Graph
     - ✅
     - 82ms
   * - Process Visualization Hr
     - ✅
     - 2.53s
   * - Process All
     - ✅
     - 127ms
   * - Reset Filtered
     - ✅
     - 7ms
   * - Update Filtered
     - ✅
     - 55ms
   * - Save Filtered
     - ✅
     - 11ms
   * - Connect Filters Button
     - ✅
     - 134ms
   * - Filter Localization
     - ✅
     - 1.12s
   * - Filter Tracks Compute
     - ✅
     - 2.18s
   * - Graph
     - ✅
     - 75ms
   * - Get Graph Data
     - ✅
     - 16ms
   * - Get Graph Data From Src
     - ✅
     - 52ms
   * - Crop
     - ✅
     - 17ms
   * - Hr
     - ✅
     - 47ms
   * - Hr Z Stack
     - ✅
     - 7ms
   * - Hr Rotation
     - ✅
     - 7ms
   * - Hr Stress
     - ✅
     - 57ms
   * - Get Astigmatism Model
     - ✅
     - 11ms

.. raw:: html

   <details>
      <summary>Log Test : Update Filtered</summary>
      <pre>[15-06-2026 10:08:03] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100803.log<br>[15-06-2026 10:08:03] Start Processing.<br>[15-06-2026 10:08:03] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[15-06-2026 10:08:03] Meta file saved.<br>[15-06-2026 10:08:03] Settings saved.<br>[15-06-2026 10:08:03] Localization load previous result (Timestamp : 20260101_000000).<br>[15-06-2026 10:08:03] 	File 'localizations-20260101_000000.csv' loaded successfully, 451 row(s) found.<br>[15-06-2026 10:08:03] Beads Extraction disabled.<br>[15-06-2026 10:08:03] Tracking disabled.<br>[15-06-2026 10:08:03] Blinking Reconnection disabled.<br>[15-06-2026 10:08:03] Tracks Compute disabled.<br>[15-06-2026 10:08:03] Gallery generation disabled.<br>[15-06-2026 10:08:03] Graphical visualization disabled.<br>[15-06-2026 10:08:03] High-resolution visualization disabled.<br>[15-06-2026 10:08:03] Processing complete.<br>[15-06-2026 10:08:03] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100803.log</pre>
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
     - 10ms
   * - Get Z From Step
     - ✅
     - 7ms
   * - Remove Multi Loc
     - ✅
     - 19ms
   * - Sigma Model
     - ✅
     - 3ms
   * - Model Validity
     - ✅
     - 7ms
   * - Model Projection Validity
     - ✅
     - 16ms
   * - Find Model Center
     - ✅
     - 12ms

.. raw:: html

   <details>
      <summary>Log Test : Remove Multi Loc</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Not all valid columns in localizations. Unable to remove ambiguous localizations reliably.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">All planes contain multiple localizations. Unable to remove ambiguous localizations reliably.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Model Projection Validity</summary>
      <pre>{'rmse_z': 5.777646505663858, 'mae_z': 4.527265453090619, 'p95_abs_z': 11.402280456091262, 'bias_z': 0.034926985397079696, 'std_z': 5.777540934524036, 'mean_dist': 0.015979049334594875, 'p95_dist': 0.03907161488826703, 'slope_mean': 0.003993454737472619}<br>{'rmse_z': 577.3147040352493, 'mae_z': 499.9443888777755, 'p95_abs_z': 950.0000000000001, 'bias_z': 7.395319063812727, 'std_z': 577.2673356004581, 'mean_dist': 0.02749131099862401, 'p95_dist': 0.09899871427527444, 'slope_mean': 0.003993454737472619}<br>{'rmse_z': 763.5196346175319, 'mae_z': 749.5955591118224, 'p95_abs_z': 975.0050010002001, 'bias_z': 20.59999999999995, 'std_z': 763.2416867850505, 'mean_dist': 1.592075248599287, 'p95_dist': 2.2654090960555444, 'slope_mean': 0.00156321987547227}</pre>
   </details>

Processing Drift
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Extract Bead Bad Input
     - ✅
     - 16ms
   * - Extract Beads No Match Returns Empty
     - ✅
     - 3ms
   * - Assign Tracks No Pairs
     - ✅
     - 3ms
   * - Assign Tracks Skip Used Track
     - ✅
     - 3ms
   * - Extract Beads
     - ✅
     - 45ms
   * - Remove Beads
     - ✅
     - 7ms
   * - Get Drift Bad Input
     - ✅
     - 15ms
   * - Get Drift
     - ✅
     - 25ms
   * - Apply Drift Bad Input
     - ✅
     - 8ms
   * - Remove Drift
     - ✅
     - 12ms
   * - Chain Drift
     - ✅
     - 13ms
   * - Drift Correction
     - ✅
     - 18ms
   * - Median Filter Centered
     - ✅
     - 9ms

Processing Filtering
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Filter Bad
     - ✅
     - 34ms
   * - Localization
     - ✅
     - 12ms
   * - Tracking
     - ✅
     - 22ms
   * - Tracks Compute
     - ✅
     - 86ms

Processing Gallery
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Make Gallery
     - ✅
     - 49ms

Processing Grapher
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Blank
     - ✅
     - 28ms
   * - Histogram
     - ✅
     - 381ms
   * - Scatter
     - ✅
     - 193ms
   * - Cloud
     - ✅
     - 706ms
   * - Astigmatism3D
     - ✅
     - 163ms

Processing Palm
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Palm Dll Valid
     - ✅
     - 2ms
   * - Palm Cpu Empty Result
     - ✅
     - 4ms
   * - Palm Cpu Image
     - ✅
     - 905ms
   * - Palm Cpu Stack
     - ✅
     - 1.61s
   * - Palm Cpu Stack Plane Selection
     - ✅
     - 92ms
   * - Palm Cpu Stack Dll Check Quadrant
     - ✅
     - 228ms
   * - Cpu Auto Threshold
     - ✅
     - 37ms
   * - Tracking
     - ✅
     - 4.97s
   * - Tracking Discontinuous
     - ✅
     - 33ms
   * - Blinking Reconnection
     - ✅
     - 152ms
   * - Tracks Compute
     - ✅
     - 35ms
   * - Align
     - ✅
     - 635ms
   * - Wavelett
     - ✅
     - 30ms
   * - Astigmatism 3D Calibration
     - ✅
     - 11ms
   * - Astigmatism 3D Estimation
     - ✅
     - 8ms

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Theta mean: 4.11°, Theta median (robust) : 0.52°, Concentration R: 0.923<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Theta mean: -5.05°, Theta median (robust) : -1.63°, Concentration R: 0.892<br>Theta mean: -7.82°, Theta median (robust) : -0.76°, Concentration R: 0.858<br>Theta mean: 3.99°, Theta median (robust) : -0.59°, Concentration R: 0.900<br>Theta mean: 1.57°, Theta median (robust) : -0.23°, Concentration R: 0.851<br>Theta mean: -0.87°, Theta median (robust) : 0.07°, Concentration R: 0.848<br>Theta mean: -1.38°, Theta median (robust) : 0.78°, Concentration R: 0.933<br>Theta mean: 3.27°, Theta median (robust) : 0.13°, Concentration R: 0.813<br>Theta mean: 1.46°, Theta median (robust) : 0.43°, Concentration R: 0.917<br>Theta mean: 0.58°, Theta median (robust) : 0.03°, Concentration R: 0.896</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Theta mean: 0.04°, Theta median (robust) : 0.07°, Concentration R: 0.884<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Theta mean: -0.33°, Theta median (robust) : -0.04°, Concentration R: 0.887<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack Plane Selection</summary>
      <pre>Theta mean: -0.53°, Theta median (robust) : -0.05°, Concentration R: 0.876<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-plane_select-103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 227 Points comparés, 227 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack Dll Check Quadrant</summary>
      <pre>Theta mean: -1.19°, Theta median (robust) : -0.02°, Concentration R: 0.868<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 269 Points comparés, 269 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_0_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_1_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_2_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_3_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_4_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 435 Points comparés, 435 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_0_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_1_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_2_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 426 Points comparés, 426 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_3_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 428 Points comparés, 428 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_4_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 416 Points comparés, 416 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-0.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-1.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span><br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-2.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Compute</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-MSD-True.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-True.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-MSD-False.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-False.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-1.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-2.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-3.csv'</pre>
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
   * - Rearrange Dataframe Columns
     - ✅
     - 10ms
   * - Log10 Dataframe
     - ✅
     - 4ms
   * - Degrees To Radians
     - ✅
     - 5ms
   * - Radians To Degrees
     - ✅
     - 5ms
   * - Wrap Angle
     - ✅
     - 4ms
   * - Manage Theta
     - ✅
     - 3ms
   * - Parse Irregular Array
     - ✅
     - 9ms
   * - Parse Result
     - ✅
     - 27ms

.. raw:: html

   <details>
      <summary>Log Test : Manage Theta</summary>
      <pre>Theta mean: -16.32°, Theta median (robust) : 0.00°, Concentration R: 0.712</pre>
   </details>

Processing Renderer
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Set Size
     - ✅
     - 7ms
   * - Get Localization Colors
     - ✅
     - 5ms
   * - Get Tracks Colors
     - ✅
     - 17ms
   * - Prepare Data
     - ✅
     - 1ms
   * - Draw Line
     - ✅
     - 7ms
   * - Draw Gaussian
     - ✅
     - 4ms
   * - Draw Gaussian 3D
     - ✅
     - 4ms
   * - Localizations
     - ✅
     - 18ms
   * - Localizations Gaussian
     - ✅
     - 10ms
   * - Tracks
     - ✅
     - 13ms
   * - Z Stack
     - ✅
     - 16ms
   * - Z Stack Gaussian
     - ✅
     - 9ms
   * - Rotation
     - ✅
     - 14ms
   * - Rotation Gaussian
     - ✅
     - 6ms
   * - Renderer Atom
     - ✅
     - 2.20s

Processing Step
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Object Creation
     - ✅
     - 1ms
   * - Prepare Action
     - ✅
     - 21ms

.. raw:: html

   <details>
      <summary>Log Test : Object Creation</summary>
      <pre>Step : Step(group_name='name', keys=['key'], process_func=&lt;function test_object_creation.&lt;locals&gt;.f at 0x0000020E87C09220&gt;, filter_func=&lt;function test_object_creation.&lt;locals&gt;.f at 0x0000020E87C09220&gt;, allow_dirty=False, apply_filter=True)<br>Actions : StepAction.Compute,StepAction.Reuse,StepAction.Skip</pre>
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
     - 15ms
   * - Batch Get Path
     - ✅
     - 16ms
   * - Batch Get Stacks
     - ✅
     - 19ms
   * - Calibration
     - ✅
     - 3ms
   * - Localization
     - ✅
     - 14ms
   * - Localization Fit
     - ✅
     - 7ms
   * - Gaussian Fit
     - ✅
     - 5ms
   * - Gaussian Fit Z
     - ✅
     - 6ms
   * - Spline Fit
     - ✅
     - 3ms
   * - Beads
     - ✅
     - 2ms
   * - Tracking
     - ✅
     - 4ms
   * - Tracks Blinking Reconnection
     - ✅
     - 3ms
   * - Tracks Computes
     - ✅
     - 3ms
   * - Filters
     - ✅
     - 25ms
   * - Filters L
     - ✅
     - 8ms
   * - Filters T
     - ✅
     - 5ms
   * - Gallery
     - ✅
     - 3ms
   * - Graph
     - ✅
     - 7ms
   * - Graph Display
     - ✅
     - 2ms
   * - Hr
     - ✅
     - 11ms
   * - Hr Gaussian
     - ✅
     - 3ms
   * - Hr 3D
     - ✅
     - 3ms
   * - Visualization 3D
     - ✅
     - 3ms

.. raw:: html

   <details>
      <summary>Log Test : Batch</summary>
      <pre>- Activate : True<br>- Files : -1<br>- Mode : 0<br><br>{'Files': -1, 'Mode': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Batch Get Stacks</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Error when concatenating stacks (they will be processed independently):<br>ValueError: all the input array dimensions except for the concatenation axis must match exactly, but along dimension 1, the array at index 0 has size 128 and the array at index 1 has size 256</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Calibration</summary>
      <pre>- Activate : True<br>- Pixel Size : 0.32<br>- Exposure : 0.05<br>- Intensity : 0.012<br><br>{'Pixel Size': 0.32, 'Exposure': 0.05, 'Intensity': 0.012}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Localization</summary>
      <pre>- Activate : True<br>- Preview : True<br>- Threshold : 90.0<br>- Auto Threshold : True<br>- ROI Shape : 0<br>- ROI Size : 7<br>- Watershed : True<br>- Fit : 0<br>- Gaussian Fit :<br>  - Activate : True<br>  - Mode : 0<br>  - Sigma : 1.0<br>  - Theta : 0.0<br>  - Z : False<br>  - Z max : 500<br>  - Model : <br>- Spline Fit :<br>  - Activate : True<br>  - Sensor : 0<br>  - Variance Map : <br>  - File : <br><br>{'Preview': True, 'Threshold': 90.0, 'Auto Threshold': True, 'ROI Shape': 0, 'ROI Size': 7, 'Watershed': True, 'Fit': 0, 'Gaussian Fit Mode': 0, 'Gaussian Fit Sigma': 1.0, 'Gaussian Fit Theta': 0.0, 'Gaussian Fit Z': False, 'Gaussian Fit Z max': 500, 'Gaussian Fit Model': '', 'Spline Fit Sensor': 0, 'Spline Fit Variance Map': '', 'Spline Fit File': ''}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gaussian Fit</summary>
      <pre>- Activate : True<br>- Mode : 2<br>- Sigma : 1.0<br>- Theta : 0.0<br>- Z : False<br>- Z max : 500<br>- Model : <br><br>{'Mode': 2, 'Sigma': 1.0, 'Theta': 0.0, 'Z': False, 'Z max': 500, 'Model': ''}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Spline Fit</summary>
      <pre>- Activate : True<br>- Sensor : 1<br>- Variance Map : <br>- File : <br><br>{'Sensor': 1, 'Variance Map': '', 'File': ''}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Beads</summary>
      <pre>- Activate : True<br>- Max Distance : 2<br>- 3D : False<br><br>{'Max Distance': 2, '3D': False}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking</summary>
      <pre>- Activate : True<br>- Max Distance : 2<br><br>{'Max Distance': 2}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Blinking Reconnection</summary>
      <pre>- Activate : True<br>- Mode : 1<br>- Max Duration : 1<br>- Max Distance : 1.0<br><br>{'Mode': 1, 'Max Duration': 1, 'Max Distance': 1.0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Computes</summary>
      <pre>- Activate : True<br>- MSD : True<br>- Instant Diffusion : False<br>- Fit Length : 4<br>- 3D : False<br>- Log Scale : False<br>- Fit : 0<br><br>{'MSD': True, 'Instant Diffusion': False, 'Fit Length': 4, '3D': False, 'Log Scale': False, 'Fit': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters</summary>
      <pre>- Activate : True<br>- Save : True<br>- Plane : Deactivate [1, 100000]<br>- Localization :<br>  - Activate : True<br>  - X : Deactivate [0, 100000]<br>  - Y : Deactivate [0, 100000]<br>  - Z : Deactivate [-2000, 2000]<br>  - Intensity : Deactivate [0, 10000000]<br>  - Sigma X : Deactivate [0, 10]<br>  - Sigma Y : Deactivate [0, 10]<br>  - Circularity : Deactivate [0, 1.0]<br>  - Theta : Deactivate [-90, 90]<br>  - MSE XY : Deactivate [0, 1.0]<br>  - MSE Z : Deactivate [0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Length : Deactivate [1, 10000]<br>  - Instant D : Deactivate [-5, 5]<br>  - D Coeff : Deactivate [-5, 5]<br>  - Alpha : Deactivate [-10, 10]<br>  - Speed : Deactivate [0, 1.0]<br>  - Confinement : Deactivate [-10, 10]<br><br>{'Save': True, 'Plane': [1, 100000], 'Localization X': [0, 100000], 'Localization Y': [0, 100000], 'Localization Z': [-2000, 2000], 'Localization Intensity': [0, 10000000], 'Localization Sigma X': [0, 10], 'Localization Sigma Y': [0, 10], 'Localization Circularity': [0, 1.0], 'Localization Theta': [-90, 90], 'Localization MSE XY': [0, 1.0], 'Localization MSE Z': [0, 1.0], 'Tracks Length': [1, 10000], 'Tracks Instant D': [-5, 5], 'Tracks D Coeff': [-5, 5], 'Tracks Alpha': [-10, 10], 'Tracks Speed': [0, 1.0], 'Tracks Confinement': [-10, 10]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters L</summary>
      <pre>- Activate : True<br>- X : Deactivate [2, 9]<br>- Y : Deactivate [0, 100000]<br>- Z : Deactivate [-2000, 2000]<br>- Intensity : Deactivate [0, 10000000]<br>- Sigma X : Deactivate [0, 10]<br>- Sigma Y : Deactivate [0, 10]<br>- Circularity : Deactivate [0, 1.0]<br>- Theta : Deactivate [-90, 90]<br>- MSE XY : Deactivate [0, 1.0]<br>- MSE Z : Deactivate [0, 1.0]<br><br>{'X': [2, 9], 'Y': [0, 100000], 'Z': [-2000, 2000], 'Intensity': [0, 10000000], 'Sigma X': [0, 10], 'Sigma Y': [0, 10], 'Circularity': [0, 1.0], 'Theta': [-90, 90], 'MSE XY': [0, 1.0], 'MSE Z': [0, 1.0]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters T</summary>
      <pre>- Activate : True<br>- Length : Deactivate [2, 3]<br>- Instant D : Deactivate [-5, 5]<br>- D Coeff : Deactivate [-5, 5]<br>- Alpha : Deactivate [-10, 10]<br>- Speed : Deactivate [0, 1.0]<br>- Confinement : Deactivate [-10, 10]<br><br>{'Length': [2, 3], 'Instant D': [-5, 5], 'D Coeff': [-5, 5], 'Alpha': [-10, 10], 'Speed': [0, 1.0], 'Confinement': [-10, 10]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gallery</summary>
      <pre>- Activate : True<br>- ROI Size : 11<br>- ROIs Per Line : 30<br><br>{'ROI Size': 11, 'ROIs Per Line': 30}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Graph</summary>
      <pre>- Activate : True<br>- Type : 1<br>- Source : 0<br>- Dual : False<br>- Source B : 0<br>- MSD Step : 1<br>- Display :<br>  - Activate : True<br>  - Limits : True<br>  - Sigma : False<br>  - Gauss : False<br>  - KDE : False<br>  - Cumul : False<br>  - Log Scale : False<br><br>{'Type': 1, 'Source': 0, 'Dual': False, 'Source B': 0, 'MSD Step': 1, 'Display Limits': True, 'Display Sigma': False, 'Display Gauss': False, 'Display KDE': False, 'Display Cumul': False, 'Display Log Scale': False}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Graph Display</summary>
      <pre>- Activate : True<br>- Limits : False<br>- Sigma : False<br>- Gauss : False<br>- KDE : False<br>- Cumul : False<br>- Log Scale : False<br><br>{'Limits': False, 'Sigma': False, 'Gauss': False, 'KDE': False, 'Cumul': False, 'Log Scale': False}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Hr</summary>
      <pre>- Activate : True<br>- Dimension : 1<br>- Type : 0<br>- Source : 0<br>- Color mode : 0<br>- Ratio : 4<br>- Crop : True<br>- Remove Beads : True<br>- Drift Correction : True<br>- Smooth Drift : True<br>- Gaussian :<br>  - Activate : False<br>  - Intensity : 100<br>  - Fixed Intensity : False<br>  - Shape : 0<br>  - Size : 1<br>- 3D :<br>  - Activate : True<br>  - Z Step : 20<br>  - Axis : 1<br>  - Frames : 36<br><br>{'Dimension': 1, 'Type': 0, 'Source': 0, 'Color mode': 0, 'Ratio': 4, 'Crop': True, 'Remove Beads': True, 'Drift Correction': True, 'Smooth Drift': True, 'Gaussian Intensity': 100, 'Gaussian Fixed Intensity': False, 'Gaussian Shape': 0, 'Gaussian Size': 1, '3D Z Step': 20, '3D Axis': 1, '3D Frames': 36}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Hr Gaussian</summary>
      <pre>- Activate : True<br>- Intensity : 10<br>- Fixed Intensity : False<br>- Shape : 0<br>- Size : 1<br><br>{'Intensity': 10, 'Fixed Intensity': False, 'Shape': 0, 'Size': 1}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Hr 3D</summary>
      <pre>- Activate : True<br>- Z Step : 10<br>- Axis : 1<br>- Frames : 36<br><br>{'Z Step': 10, 'Axis': 1, 'Frames': 36}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Visualization 3D</summary>
      <pre>- Activate : True<br>- Point Size : 2<br>- Pixel Size : 160<br>- XY Scale : 1.0<br>- Z Scale : 1.0<br>- Remove Outliers : False<br><br>{'Point Size': 2, 'Pixel Size': 160, 'XY Scale': 1.0, 'Z Scale': 1.0, 'Remove Outliers': False}</pre>
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
     - 25ms
   * - Settings Group Getter
     - ✅
     - 14ms
   * - Settings Signal
     - ✅
     - 10ms

Settings Types
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Base Setting
     - ✅
     - 2ms
   * - Base Ui
     - ✅
     - 99ms
   * - Base Ui No Label
     - ✅
     - 1ms
   * - Spin Int
     - ✅
     - 8ms
   * - Spin Float
     - ✅
     - 1ms
   * - Check Box
     - ✅
     - 3ms
   * - Combo
     - ✅
     - 3ms
   * - Browse File
     - ✅
     - 5ms
   * - File List
     - ✅
     - 10ms
   * - Check Range Int
     - ✅
     - 13ms
   * - Check Range Float
     - ✅
     - 12ms
   * - Button
     - ✅
     - 3ms
   * - Button Group
     - ✅
     - 3ms
   * - Sync
     - ✅
     - 10ms

Settings Types Signal
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Connect And Emit Direct
     - ✅
     - 2ms
   * - Disconnect
     - ✅
     - 6ms
   * - Block Simple Coalescence Last Value
     - ✅
     - 2ms
   * - Block Without Emits No Output
     - ✅
     - 2ms
   * - Nested Blocks Emit Once At Outer Exit
     - ✅
     - 3ms
   * - Emit Default None Coalesced
     - ✅
     - 2ms
   * - Block Flags Reset After Flush
     - ✅
     - 3ms
   * - Block Without Emit
     - ✅
     - 4ms
   * - Blocked Returns Context Manager Instance
     - ✅
     - 2ms
   * - Internal Block Begin End Paths
     - ✅
     - 2ms
   * - Coalescence Overwrite Multiple Times
     - ✅
     - 2ms
   * - Emit Direct After Previous Block
     - ✅
     - 3ms

Tools Fileio
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Add Extension
     - ✅
     - 5ms
   * - Add Suffix
     - ✅
     - 3ms
   * - Get Timestamp For Files
     - ✅
     - 2ms
   * - Get Last File
     - ✅
     - 3ms
   * - Extract Suffix
     - ✅
     - 9ms
   * - Cleanup Process
     - ✅
     - 2ms
   * - Load Dll
     - ✅
     - 4ms
   * - Save Json
     - ✅
     - 2ms
   * - Open Json
     - ✅
     - 21ms
   * - Open Json Bad File
     - ✅
     - 2ms
   * - Save Tif
     - ✅
     - 3ms
   * - Save Tif 2D
     - ✅
     - 2ms
   * - Save Tif Bad Stack
     - ✅
     - 2ms
   * - Open Tif
     - ✅
     - 58ms
   * - Open Tif Bad File
     - ✅
     - 5ms
   * - Save Png
     - ✅
     - 4ms
   * - Save Png Color
     - ✅
     - 9ms
   * - Save Png Bad Sample
     - ✅
     - 2ms
   * - Open Calibration Mat Bad File
     - ✅
     - 2ms
   * - Open Calibration Mat
     - ✅
     - 3ms

.. raw:: html

   <details>
      <summary>Log Test : Get Timestamp For Files</summary>
      <pre>Timestamp with hour : 20260615_100820<br>Timestamp without hour : 20260615</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Get Last File</summary>
      <pre>C:\Git\palm-tracer\palm_tracer\_tests\input\File-03.txt<br>C:\Git\palm-tracer\palm_tracer\_tests\input\File-03.txt</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Load Dll</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to load the DLL 'PALMTracer_File.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\PALMTracer_File.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span></pre>
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
     - 13ms
   * - Update Meta
     - ✅
     - 11ms
   * - Open Old File
     - ✅
     - 34ms
   * - Open Old Irregular File
     - ✅
     - 25ms
   * - Column Migrator
     - ✅
     - 4ms
   * - Analyze
     - ✅
     - 9ms
   * - Migrate
     - ✅
     - 247ms

.. raw:: html

   <details>
      <summary>Log Test : Analyze</summary>
      <pre>.</pre>
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
     - 11ms
   * - Logger Bad Use
     - ✅
     - 5ms
   * - Logger With Use
     - ✅
     - 9ms

Tools Monitoring
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Monitoring
     - ✅
     - 3.09s
   * - Monitoring Save
     - ✅
     - 6.21s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>10 entrées.<br>Timestamps : [0.0, 0.21, 0.41, 0.63, 0.84, 2.01, 2.22, 2.43, 2.64, 2.85]<br>CPU Usage : [0.4875, 0.0, 0.0, 0.4875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]<br>GPU Usage : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]<br>Memory Usage : [780.7734375, 780.77734375, 780.77734375, 780.77734375, 780.78125, 780.7890625, 780.7890625, 780.7890625, 780.7890625, 780.7890625]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Monitoring Save</summary>
      <pre>Simulating high CPU usage for 2 seconds...<br>CPU simulation complete.<br>Aucun GPU CUDA disponible pour la simulation.<br>Allocating 50 MB of memory...<br>Memory allocated. Holding for 2 seconds...<br>Releasing memory.<br>Writing a file of size 1 MB...<br>File written. Holding for 2 seconds...<br>Deleting the file...<br>Disk I/O simulation complete.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Kaleido doesn't work so well need update. No Image Saved.</span><span style="font-weight: bold"></span></pre>
   </details>

Tools Ui
^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Builders
     - ✅
     - 23ms
   * - Builders Spin
     - ✅
     - 7ms
   * - Sync Spin
     - ✅
     - 7ms
   * - Sync Button Group
     - ✅
     - 14ms
   * - Print Error
     - ✅
     - 1ms
   * - Print Warning
     - ✅
     - 1ms
   * - Print Success
     - ✅
     - 1ms
   * - Format Time
     - ✅
     - 2ms

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

Ui Alignment
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 97ms
   * - Bad Load Tif
     - ✅
     - 7ms
   * - Bad Load Coef
     - ✅
     - 12ms
   * - Bad Compute
     - ✅
     - 4ms
   * - Compute
     - ✅
     - 8ms
   * - Bad Align
     - ✅
     - 8ms
   * - Align
     - ✅
     - 183ms

Ui Astigmatism3D
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 208ms
   * - Bad Load Loc
     - ✅
     - 256ms
   * - Bad Load Model
     - ✅
     - 54ms
   * - Bad Compute
     - ✅
     - 49ms
   * - Check Loc
     - ✅
     - 67ms
   * - Compute
     - ✅
     - 125ms
   * - Compute Mean Beads
     - ✅
     - 120ms
   * - Compute Remove Bead Col
     - ✅
     - 111ms
   * - Compute Remove Multi
     - ✅
     - 109ms
   * - Compute Z
     - ✅
     - 117ms
   * - Compute Center Z
     - ✅
     - 116ms
   * - Compute Bad Model
     - ✅
     - 120ms
   * - Bad Estimate
     - ✅
     - 57ms
   * - Estimate
     - ✅
     - 84ms
   * - Estimate Backup
     - ✅
     - 423ms
   * - Sync Spin
     - ✅
     - 268ms
   * - Download
     - ✅
     - 77ms

.. raw:: html

   <details>
      <summary>Log Test : Download</summary>
      <pre>C:\Git\palm-tracer\palm_tracer\_tests\input\ref</pre>
   </details>

Ui Baseplotlywidget
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Creation
     - ✅
     - 14ms
   * - Update Plotly
     - ✅
     - 18ms
   * - Update Plotly No Js
     - ✅
     - 19ms
   * - Download Plotly
     - ✅
     - 19ms
   * - Export Plotly
     - ✅
     - 21ms

.. raw:: html

   <details>
      <summary>Log Test : Download Plotly</summary>
      <pre>C:\Git\palm-tracer\palm_tracer\_tests\output<br>C:\Git\palm-tracer\palm_tracer\_tests\output</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Export Plotly</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No figures to export.</span><span style="font-weight: bold"></span></pre>
   </details>

Ui Filemigrator
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 3ms
   * - Bad Load
     - ✅
     - 6ms
   * - Mirgate
     - ✅
     - 34ms

Ui Graphviewer
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 58ms
   * - Widget Double Creation
     - ✅
     - 94ms
   * - Add Stack
     - ✅
     - 73ms
   * - Change Type
     - ✅
     - 76ms
   * - Update Plot Localization
     - ✅
     - 155ms

.. raw:: html

   <details>
      <summary>Log Test : Add Stack</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span></pre>
   </details>

Ui Palmtracer
^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 922ms
   * - Widget On Load Setting
     - ✅
     - 445ms
   * - Widget Reset Setting
     - ✅
     - 450ms
   * - Widget Reset Layer
     - ✅
     - 824ms
   * - Widget Get Actual Image
     - ✅
     - 516ms
   * - Widget Add Detection Layers
     - ✅
     - 1.48s
   * - Widget Preview
     - ✅
     - 615ms
   * - Widget Roi Filter Layer
     - ✅
     - 713ms
   * - Widget Auto Threshold
     - ✅
     - 553ms
   * - Widget Thread Process
     - ✅
     - 600ms
   * - Widget Keyblocker
     - ✅
     - 841ms
   * - Filters Button
     - ✅
     - 702ms

.. raw:: html

   <details>
      <summary>Log Test : Widget Get Actual Image</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Roi Filter Layer</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Thread Process</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif into Napari viewer.<br>[15-06-2026 10:08:41] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100841.log<br>[15-06-2026 10:08:41] Start Processing.<br>[15-06-2026 10:08:41] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[15-06-2026 10:08:41] Meta file saved.<br>[15-06-2026 10:08:41] Settings saved.<br>[15-06-2026 10:08:41] Localization disabled.<br>[15-06-2026 10:08:41] Beads Extraction disabled.<br>[15-06-2026 10:08:41] Tracking disabled.<br>[15-06-2026 10:08:41] Blinking Reconnection disabled.<br>[15-06-2026 10:08:41] Tracks Compute disabled.<br>[15-06-2026 10:08:41] Gallery generation disabled.<br>[15-06-2026 10:08:41] Graphical visualization disabled.<br>[15-06-2026 10:08:41] High-resolution visualization disabled.<br>[15-06-2026 10:08:41] Processing complete.<br>[15-06-2026 10:08:41] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100841.log<br>Auto Threshold: 63.95</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Keyblocker</summary>
      <pre>INFO: Loading the setting file 'C:\Users\tmonseigne\.palm_tracer\settings.json'.<br>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters Button</summary>
      <pre>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif into Napari viewer.<br>[15-06-2026 10:08:42] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100842.log<br>[15-06-2026 10:08:42] Start Processing.<br>[15-06-2026 10:08:42] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[15-06-2026 10:08:42] Meta file saved.<br>[15-06-2026 10:08:42] Settings saved.<br>[15-06-2026 10:08:42] Localization enabled.<br>[15-06-2026 10:08:42] 	Saving the localization file (455 localization(s) found).<br>[15-06-2026 10:08:42] Beads Extraction disabled.<br>[15-06-2026 10:08:42] Tracking disabled.<br>[15-06-2026 10:08:42] Blinking Reconnection disabled.<br>[15-06-2026 10:08:42] Tracks Compute disabled.<br>[15-06-2026 10:08:42] Gallery generation disabled.<br>[15-06-2026 10:08:42] Graphical visualization disabled.<br>[15-06-2026 10:08:42] High-resolution visualization disabled.<br>[15-06-2026 10:08:42] Processing complete.<br>[15-06-2026 10:08:42] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100842.log<br>{'reset': &lt;PySide6.QtWidgets.QPushButton(0x20ea9a1c3f0) at 0x0000020E91E09D80&gt;, 'update': &lt;PySide6.QtWidgets.QPushButton(0x20ea9a1ea00) at 0x0000020E91E09E80&gt;, 'save': &lt;PySide6.QtWidgets.QPushButton(0x20ea9a1e0f0) at 0x0000020E91E09C00&gt;}<br>[15-06-2026 10:08:42] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100842.log<br>[15-06-2026 10:08:42] Start Processing.<br>- Activate : True<br>- Save : False<br>- Plane : Activate [1, 5]<br>- Localization :<br>  - Activate : True<br>  - X : Deactivate [0, 256]<br>  - Y : Deactivate [0, 128]<br>  - Z : Deactivate [-2000, 2000]<br>  - Intensity : Deactivate [0, 10000000]<br>  - Sigma X : Deactivate [0, 10]<br>  - Sigma Y : Deactivate [0, 10]<br>  - Circularity : Deactivate [0, 1.0]<br>  - Theta : Deactivate [-90, 90]<br>  - MSE XY : Deactivate [0, 1.0]<br>  - MSE Z : Deactivate [0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Length : Deactivate [1, 10]<br>  - Instant D : Deactivate [-5, 5]<br>  - D Coeff : Deactivate [-5, 5]<br>  - Alpha : Deactivate [-10, 10]<br>  - Speed : Deactivate [0, 1.0]<br>  - Confinement : Deactivate [-10, 10]<br><br>[15-06-2026 10:08:42] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[15-06-2026 10:08:42] Meta file saved.<br>[15-06-2026 10:08:42] Settings saved.<br>[15-06-2026 10:08:42] Localization load previous result (Timestamp : 20260615_100842).<br>[15-06-2026 10:08:42] 	File 'localizations-20260615_100842.csv' loaded successfully, 455 row(s) found.<br>[15-06-2026 10:08:42] 		Filtering of file 242 row(s) instead of 455: 213 deletion(s).<br>[15-06-2026 10:08:42] Beads Extraction disabled.<br>[15-06-2026 10:08:42] Tracking disabled.<br>[15-06-2026 10:08:42] Blinking Reconnection disabled.<br>[15-06-2026 10:08:42] Tracks Compute disabled.<br>[15-06-2026 10:08:42] Gallery generation disabled.<br>[15-06-2026 10:08:42] Graphical visualization disabled.<br>[15-06-2026 10:08:42] High-resolution visualization disabled.<br>[15-06-2026 10:08:42] Processing complete.<br>[15-06-2026 10:08:42] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260615_100842.log</pre>
   </details>

Ui Viewer3D
^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 344ms
   * - Viewer3D
     - ✅
     - 537ms

.. raw:: html

   <details>
      <summary>Log Test : Viewer3D</summary>
      <pre>WARNING: The file must contain the columns X, Y, Z, and Integrated Intensity.</pre>
   </details>

Ui Viewerhr
^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Widget Creation
     - ✅
     - 378ms
   * - Widget Double Creation
     - ✅
     - 78ms
   * - Add Stack
     - ✅
     - 363ms
   * - Change Type
     - ✅
     - 362ms
   * - Actualize
     - ✅
     - 357ms
   * - Save
     - ✅
     - 367ms
   * - Screenshot
     - ✅
     - 375ms
   * - Check Beads
     - ✅
     - 365ms
   * - Generate Bad
     - ✅
     - 656ms
   * - Generate
     - ✅
     - 437ms

.. raw:: html

   <details>
      <summary>Log Test : Save</summary>
      <pre>INFO: Image file saved successfully.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Screenshot</summary>
      <pre>INFO: Screenshot saved successfully.</pre>
   </details>

.. raw:: html

   </div>
