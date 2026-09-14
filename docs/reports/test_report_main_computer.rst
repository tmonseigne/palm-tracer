Test Report Main Computer
=========================

Environnement
-------------

.. list-table::

   * - Python
     - 3.14.6
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

864 tests collected, 864 passed ✅, 0 failed ❌, 0 skipped ⏭️ in 0:01:20s on 14/09/2026 at 16:58:56

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

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Reset Result</td><td>✅</td><td>198ms</td></tr>
   <tr><td>Clean Ui</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Getter Localization</td><td>✅</td><td>32ms</td></tr>
   <tr><td>Getter Beads</td><td>✅</td><td>64ms</td></tr>
   <tr><td>Getter Tracks</td><td>✅</td><td>34ms</td></tr>
   <tr><td>Getter Tracks Compute</td><td>✅</td><td>29ms</td></tr>
   <tr><td>Getter Path</td><td>✅</td><td>26ms</td></tr>
   <tr><td>Getter Stack</td><td>✅</td><td>21ms</td></tr>
   <tr><td>Getter Suffix</td><td>✅</td><td>22ms</td></tr>
   <tr><td>Load Bad Dll</td><td>✅</td><td>104ms</td></tr>
   <tr><td>Load Nothing</td><td>✅</td><td>36ms</td></tr>
   <tr><td>Load</td><td>✅</td><td>372ms</td></tr>
   <tr><td>Process No Input</td><td>✅</td><td>15ms</td></tr>
   <tr><td>Process Nothing</td><td>✅</td><td>1.62s</td></tr>
   <tr><td>Process Bad Dll</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Process Multiple Stack</td><td>✅</td><td>73ms</td></tr>
   <tr><td>Process Localization</td><td>✅</td><td>54ms</td></tr>
   <tr><td>Process Localization Z</td><td>✅</td><td>140ms</td></tr>
   <tr><td>Process Localization Spline Bad</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Process Localization Spline</td><td>✅</td><td>59ms</td></tr>
   <tr><td>Process Beads Extraction No Beads</td><td>✅</td><td>88ms</td></tr>
   <tr><td>Process Plane Discontinuous</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Process Beads Extraction</td><td>✅</td><td>146ms</td></tr>
   <tr><td>Process Tracking</td><td>✅</td><td>214ms</td></tr>
   <tr><td>Process Tracking Blinking</td><td>✅</td><td>188ms</td></tr>
   <tr><td>Process Tracks Compute</td><td>✅</td><td>518ms</td></tr>
   <tr><td>Process Gallery</td><td>✅</td><td>660ms</td></tr>
   <tr><td>Process Visualization Graph</td><td>✅</td><td>588ms</td></tr>
   <tr><td>Process Visualization Hr</td><td>✅</td><td>2.00s</td></tr>
   <tr><td>Process All</td><td>✅</td><td>510ms</td></tr>
   <tr><td>Get Astigmatism Model</td><td>✅</td><td>75ms</td></tr>
   <tr><td>Reset Filtered</td><td>✅</td><td>26ms</td></tr>
   <tr><td>Update Filtered</td><td>✅</td><td>195ms</td></tr>
   <tr><td>Save Filtered</td><td>✅</td><td>34ms</td></tr>
   <tr><td>Connect Filters Button</td><td>✅</td><td>232ms</td></tr>
   <tr><td>Filter Localization</td><td>✅</td><td>336ms</td></tr>
   <tr><td>Filter Tracks Compute</td><td>✅</td><td>687ms</td></tr>
   <tr><td>Graph</td><td>✅</td><td>457ms</td></tr>
   <tr><td>Get Graph Data</td><td>✅</td><td>40ms</td></tr>
   <tr><td>Get Graph Data Dual Tracks</td><td>✅</td><td>223ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Graph Data From Src — 18 cas</button></td><td>✅ 18/18</td><td>144ms</td></tr>
   <tr class="test-variant"><td>[localizations-missing-column]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[localizations-x]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[localization-count]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[empty-localizations]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[tracks-missing-column]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[length-scatter]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[lengths]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[on-durations]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[off-durations]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[unknown-length]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[msd-step-5]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[msd-step-9]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[instant-diffusion]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[fit-error]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[empty-tracks]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[empty-msd]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[empty-diffusion]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[empty-fit]</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Hr</td><td>✅</td><td>33ms</td></tr>
   <tr><td>Hr Filter</td><td>✅</td><td>12ms</td></tr>
   <tr><td>Hr Z Stack</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Hr Rotation</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Hr Stress</td><td>✅</td><td>65ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Track Stack — 6 cas</button></td><td>✅ 6/6</td><td>71ms</td></tr>
   <tr class="test-variant"><td>[addition-no-background]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[addition-with-background]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[maximum-no-background]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[maximum-with-background]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[minimum-no-background]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[minimum-with-background]</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Hr Track Stack Empty Roi</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Hr Track Stack Dimension Switch</td><td>✅</td><td>83ms</td></tr>
   <tr><td>Crop</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Crop Track Stack Rgb</td><td>✅</td><td>4ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Update Filtered</summary>
      <pre>[14-09-2026 16:57:58] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165758.log<br>[14-09-2026 16:57:58] Start Processing.<br>[14-09-2026 16:57:58] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[14-09-2026 16:57:58] Meta file saved.<br>[14-09-2026 16:57:58] Settings saved.<br>[14-09-2026 16:57:58] Localization load previous result (Timestamp : 20260101_000000).<br>[14-09-2026 16:57:58] 	File 'localizations-20260101_000000.csv' loaded successfully, 451 row(s) found.<br>[14-09-2026 16:57:58] Beads Extraction disabled.<br>[14-09-2026 16:57:58] Tracking disabled.<br>[14-09-2026 16:57:58] Blinking Reconnection disabled.<br>[14-09-2026 16:57:58] Tracks Compute disabled.<br>[14-09-2026 16:57:58] Gallery generation disabled.<br>[14-09-2026 16:57:58] Graphical visualization disabled.<br>[14-09-2026 16:57:58] High-resolution visualization disabled.<br>[14-09-2026 16:57:58] Processing complete.<br>[14-09-2026 16:57:58] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165758.log</pre>
   </details>

Processing Astigmatism3D
^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Z From Planes — 5 cas</button></td><td>✅ 5/5</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[symmetric-range]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[negative-range]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[positive-range]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[equal-bounds]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[identical-planes]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Z From Step — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[centered-odd-count]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[centered-even-count]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[no-centering]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Remove Multi Loc — 6 cas</button></td><td>✅ 6/6</td><td>12ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[missing-plane-column]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[single-point-per-plane]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[no-single-localization-plane]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[spatial-selection]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[bead-column]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Sigma Model</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Model Validity — 3 cas</button></td><td>✅ 3/3</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[correct-model]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reversed-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[different-model]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Model Projection Validity — 3 cas</button></td><td>✅ 3/3</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[correct-model]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[reversed-axes]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[different-model]</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Find Model Center</td><td>✅</td><td>2ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Remove Multi Loc [missing-plane-column]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Not all valid columns in localizations. Unable to remove ambiguous localizations reliably.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Remove Multi Loc [no-single-localization-plane]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">All planes contain multiple localizations. Unable to remove ambiguous localizations reliably.</span><span style="font-weight: bold"></span></pre>
   </details>

Processing Drift
^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Empty Data — 2 cas</button></td><td>✅ 2/2</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[bead-extraction]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[drift-computation]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Assign Tracks No Pairs</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Assign Tracks Skip Used Track</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Extract Bead Bad Input — 4 cas</button></td><td>✅ 4/4</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[negative-distance]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[missing-columns]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[non-consecutive-planes]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[single-plane]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Extract Beads No Match Returns Empty</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Extract Beads</td><td>✅</td><td>39ms</td></tr>
   <tr><td>Remove Beads</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Drift Bad Input — 3 cas</button></td><td>✅ 3/3</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing-columns]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[non-consecutive-planes]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[single-plane]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Get Drift</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Apply Drift Bad Input — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[incomplete-localizations]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[incomplete-drift]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Remove Drift</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Remove Drift Empty</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Chain Drift</td><td>✅</td><td>11ms</td></tr>
   <tr><td>Drift Correction</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Median Filter Centered</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Median Filter Invalid — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[even-window]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[3d-array]</td><td>✅</td><td>1ms</td></tr>
   </tbody>
   </table>

Processing Filtering
^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Filter Bad — 3 cas</button></td><td>✅ 3/3</td><td>88ms</td></tr>
   <tr class="test-variant"><td>[localizations]</td><td>✅</td><td>85ms</td></tr>
   <tr class="test-variant"><td>[tracks]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[track-computations]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Localization</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking — 4 cas</button></td><td>✅ 4/4</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[track-ids]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[length]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[track-ids-and-length]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[filters-disabled]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracks Compute — 8 cas</button></td><td>✅ 8/8</td><td>54ms</td></tr>
   <tr class="test-variant"><td>[intersection-without-criteria]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[active-criteria]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[missing-msd]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[missing-instant-diffusion]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[missing-fit]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[overly-restrictive-length]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[no-common-tracks]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[filters-disabled]</td><td>✅</td><td>13ms</td></tr>
   </tbody>
   </table>

Processing Gallery
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Make Gallery</td><td>✅</td><td>6ms</td></tr>
   </tbody>
   </table>

Processing Gaussianmixture
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Fit Two Components</td><td>✅</td><td>17ms</td></tr>
   <tr><td>Fit Is Generic</td><td>✅</td><td>11ms</td></tr>
   <tr><td>Make Curve</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Invalid Fit Parameters — 8 cas</button></td><td>✅ 8/8</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[zero-components]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[zero-iterations]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[zero-tolerance]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[zero-initializations]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[empty-data]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[more-components-than-samples]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[constant-data-two-components]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[constant-data-one-component]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Invalid Curve Parameters — 4 cas</button></td><td>✅ 4/4</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[insufficient-points]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[missing-bound]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[nan-bound]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[equal-bounds]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Initialize Centers Fallback</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Kmeans Iteration Limit</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Em Iteration Limit</td><td>✅</td><td>1ms</td></tr>
   </tbody>
   </table>

Processing Grapher
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Blank</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Histogram — 7 cas</button></td><td>✅ 7/7</td><td>200ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[fixed-bins]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[integer-values]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[two-rows]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-variant"><td>[two-columns]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[flattened-matrix]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[flattened-volume]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Histogram Curves — 7 cas</button></td><td>✅ 7/7</td><td>238ms</td></tr>
   <tr class="test-variant"><td>[all-options]</td><td>✅</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[kde]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[gaussian]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[gaussian-mixture]</td><td>✅</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[poisson]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[exponential]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[gaussian-counts]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Scatter — 5 cas</button></td><td>✅ 5/5</td><td>171ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[1d-data]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[two-rows]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[two-columns-with-limits]</td><td>✅</td><td>36ms</td></tr>
   <tr class="test-variant"><td>[mean-and-sigma]</td><td>✅</td><td>57ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Scatter Invalid — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[invalid-matrix]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[3d-volume]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cloud — 6 cas</button></td><td>✅ 6/6</td><td>251ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[infinite-values]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[two-rows]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[two-columns-with-limits]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[mean-and-sigma]</td><td>✅</td><td>120ms</td></tr>
   <tr class="test-variant"><td>[constant-data]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cloud Curves — 4 cas</button></td><td>✅ 4/4</td><td>234ms</td></tr>
   <tr class="test-variant"><td>[kde]</td><td>✅</td><td>132ms</td></tr>
   <tr class="test-variant"><td>[gaussian]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[poisson]</td><td>✅</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[exponential]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cloud Invalid — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[1d-data]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[invalid-matrix]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[3d-volume]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism3D — 6 cas</button></td><td>✅ 6/6</td><td>170ms</td></tr>
   <tr class="test-variant"><td>[curve]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[cross-without-points]</td><td>✅</td><td>34ms</td></tr>
   <tr class="test-variant"><td>[cross-with-points]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[slope-without-points]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[slope-with-points]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[unknown-mode]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism3D Invalid — 1 cas</button></td><td>✅ 1/1</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[invalid-model]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Histogram Poisson Distribution</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Histogram Exponential Distribution</td><td>✅</td><td>28ms</td></tr>
   <tr><td>Histogram Gaussian Mixture Distribution</td><td>✅</td><td>49ms</td></tr>
   </tbody>
   </table>

Processing Palm
^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Palm Dll Valid</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Palm Cpu Empty Result</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Palm Cpu Image — 60 cas</button></td><td>✅ 60/60</td><td>611ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-1]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-2]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-3]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-4]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-5]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-6]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-7]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-8]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-9]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-10]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-1]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-2]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-3]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-4]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-5]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-6]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-7]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-8]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-9]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-10]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-1]</td><td>✅</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-2]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-3]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-4]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-5]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-6]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-7]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-8]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-9]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-10]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-1]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-2]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-3]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-4]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-5]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-6]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-7]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-8]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-9]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-10]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-1]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-2]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-3]</td><td>✅</td><td>12ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-4]</td><td>✅</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-5]</td><td>✅</td><td>12ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-6]</td><td>✅</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-7]</td><td>✅</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-8]</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-9]</td><td>✅</td><td>12ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-10]</td><td>✅</td><td>12ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-1]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-2]</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-3]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-4]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-5]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-6]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-7]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-8]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-9]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-10]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Palm Cpu Stack — 12 cas</button></td><td>✅ 12/12</td><td>1.42s</td></tr>
   <tr class="test-variant"><td>[no-fit-with-watershed]</td><td>✅</td><td>132ms</td></tr>
   <tr class="test-variant"><td>[no-fit-no-watershed]</td><td>✅</td><td>131ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-with-watershed]</td><td>✅</td><td>143ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-no-watershed]</td><td>✅</td><td>128ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-with-watershed]</td><td>✅</td><td>142ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-no-watershed]</td><td>✅</td><td>128ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-with-watershed]</td><td>✅</td><td>153ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-no-watershed]</td><td>✅</td><td>140ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-with-watershed]</td><td>✅</td><td>154ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-no-watershed]</td><td>✅</td><td>135ms</td></tr>
   <tr class="test-variant"><td>[spline-with-watershed]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[spline-no-watershed]</td><td>✅</td><td>15ms</td></tr>
   <tr><td>Palm Cpu Stack Plane Selection</td><td>✅</td><td>86ms</td></tr>
   <tr><td>Palm Cpu Stack Dll Check Quadrant</td><td>✅</td><td>102ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cpu Auto Threshold — 10 cas</button></td><td>✅ 10/10</td><td>43ms</td></tr>
   <tr class="test-variant"><td>[plane-1]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[plane-2]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[plane-3]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[plane-4]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[plane-5]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[plane-6]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[plane-7]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[plane-8]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[plane-9]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[plane-10]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking — 12 cas</button></td><td>✅ 12/12</td><td>4.72s</td></tr>
   <tr class="test-variant"><td>[no-fit-with-watershed]</td><td>✅</td><td>489ms</td></tr>
   <tr class="test-variant"><td>[no-fit-no-watershed]</td><td>✅</td><td>492ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-with-watershed]</td><td>✅</td><td>486ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-no-watershed]</td><td>✅</td><td>485ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-with-watershed]</td><td>✅</td><td>483ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-no-watershed]</td><td>✅</td><td>454ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-with-watershed]</td><td>✅</td><td>475ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-no-watershed]</td><td>✅</td><td>447ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-with-watershed]</td><td>✅</td><td>458ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-no-watershed]</td><td>✅</td><td>452ms</td></tr>
   <tr class="test-variant"><td>[spline-with-watershed]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[spline-no-watershed]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Tracking Empty</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Tracking Discontinuous</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Blinking Reconnection — 3 cas</button></td><td>✅ 3/3</td><td>89ms</td></tr>
   <tr class="test-variant"><td>[stationary]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[diffusion]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[linear]</td><td>✅</td><td>28ms</td></tr>
   <tr><td>Blinking Reconnection Empty</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracks Compute — 2 cas</button></td><td>✅ 2/2</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[ind-3d-log-enabled]</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-variant"><td>[ind-3d-log-disabled]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracks Compute Fit Modes — 4 cas</button></td><td>✅ 4/4</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[no-fit]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[linear]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[power]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[exponential]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracks Compute Small Inputs — 3 cas</button></td><td>✅ 3/3</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[diffusion-without-msd]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[single-observation]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[no-observations]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Align</td><td>✅</td><td>550ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Wavelett — 5 cas</button></td><td>✅ 5/5</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[level-0]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[level-1]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[level-2]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[level-3]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[level-4]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism 3D Calibration — 2 cas</button></td><td>✅ 2/2</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[no-centering]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[centered-model]</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Astigmatism 3D Estimation</td><td>✅</td><td>3ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [no-fit-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-xy-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-sigma-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-sigma-xy-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-1]</summary>
      <pre>Theta mean: 4.11°, Theta median (robust) : 0.52°, Concentration R: 0.923<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-0_103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-2]</summary>
      <pre>Theta mean: -5.05°, Theta median (robust) : -1.63°, Concentration R: 0.892</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-3]</summary>
      <pre>Theta mean: -7.82°, Theta median (robust) : -0.76°, Concentration R: 0.858</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-4]</summary>
      <pre>Theta mean: 3.99°, Theta median (robust) : -0.59°, Concentration R: 0.900</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-5]</summary>
      <pre>Theta mean: 1.57°, Theta median (robust) : -0.23°, Concentration R: 0.851</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-6]</summary>
      <pre>Theta mean: -0.87°, Theta median (robust) : 0.07°, Concentration R: 0.848</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-7]</summary>
      <pre>Theta mean: -1.38°, Theta median (robust) : 0.78°, Concentration R: 0.933</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-8]</summary>
      <pre>Theta mean: 3.27°, Theta median (robust) : 0.13°, Concentration R: 0.813</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-9]</summary>
      <pre>Theta mean: 1.46°, Theta median (robust) : 0.43°, Concentration R: 0.917</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-10]</summary>
      <pre>Theta mean: 0.58°, Theta median (robust) : 0.03°, Concentration R: 0.896</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [no-fit-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [no-fit-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-theta-with-watershed]</summary>
      <pre>Theta mean: 0.04°, Theta median (robust) : 0.07°, Concentration R: 0.884<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-theta-no-watershed]</summary>
      <pre>Theta mean: -0.33°, Theta median (robust) : -0.04°, Concentration R: 0.887<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
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
      <summary>Log Test : Tracking [no-fit-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_0_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [no-fit-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_0_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_1_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_1_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_2_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_2_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 426 Points comparés, 426 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_3_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_3_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 428 Points comparés, 428 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-theta-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_True_4_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 435 Points comparés, 435 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-theta-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-tracking-103.6_False_4_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 416 Points comparés, 416 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [spline-with-watershed]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_True_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [spline-no-watershed]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\stack-localizations-103.6_False_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection [stationary]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-0.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection [diffusion]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-1.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection [linear]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking-blinking-2.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Compute [ind-3d-log-enabled]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-MSD-True.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-True.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Compute [ind-3d-log-disabled]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-MSD-False.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-False.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Compute Fit Modes [linear]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-1.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Compute Fit Modes [power]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-2.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracks Compute Fit Modes [exponential]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\palm_tracer\_tests\input\ref\tracking2-Fit-3.csv'</pre>
   </details>

Processing Parsing
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Rearrange Dataframe Columns — 2 cas</button></td><td>✅ 2/2</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[other-columns-preserved]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[selection-only]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Rearrange Dataframe Columns Missing</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Log10 Dataframe</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Degrees To Radians</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Radians To Degrees</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Wrap Angle</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Manage Theta</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Get Meta</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Get Meta Invalid</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Parse Irregular Array</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Irregular Array Invalid — 3 cas</button></td><td>✅ 3/3</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[2d-array]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[non-numeric-data]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[truncated-row]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Irregular Array Empty — 2 cas</button></td><td>✅ 2/2</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[empty-array]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[empty-row]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Result — 8 cas</button></td><td>✅ 8/8</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[localizations]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[tracks]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[astigmatism-model]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[msd]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[instant-diffusion]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[linear-fit-log]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[power-fit]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[exponential-fit]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Result Empty — 3 cas</button></td><td>✅ 3/3</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[localizations]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[tracks]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[fit]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Result Invalid — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[invalid-fit]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[unknown-type]</td><td>✅</td><td>1ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Manage Theta</summary>
      <pre>Theta mean: -16.32°, Theta median (robust) : 0.00°, Concentration R: 0.712</pre>
   </details>

Processing Renderer
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Set Size</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Localizations</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Localizations Gaussian</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Tracks</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Z Stack</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Z Stack Gaussian</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Rotation</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Rotation Gaussian</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Track Stack Timeline</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Empty And Scale — 4 cas</button></td><td>✅ 4/4</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[1d-array]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[missing-column]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[out-of-bounds]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Track Stack Scale</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Priority And Modes — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Track Stack Head Priority</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Raw — 4 cas</button></td><td>✅ 4/4</td><td>38ms</td></tr>
   <tr class="test-variant"><td>[maximum-nearest-neighbor]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[maximum-lanczos]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[minimum-nearest-neighbor]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[minimum-lanczos]</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Track Stack Raw Empty And 2D</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Raw Fade And Overlap — 3 cas</button></td><td>✅ 3/3</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Init Rendering — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Init Rendering Volume</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Finalize Rendering</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Finalize Track Stack</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Empty Background — 12 cas</button></td><td>✅ 12/12</td><td>11ms</td></tr>
   <tr class="test-variant"><td>[black-zero-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[black-negative-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[black-positive-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[gray-zero-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[gray-negative-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[gray-positive-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[lower-clipping-zero-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[lower-clipping-negative-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[lower-clipping-positive-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[upper-clipping-zero-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[upper-clipping-negative-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[upper-clipping-positive-infinite-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Empty Dimensions — 3 cas</button></td><td>✅ 3/3</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[no-planes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[no-rows]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[no-columns]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Finalize Track Stack Strided</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Drawing — 3 cas</button></td><td>✅ 3/3</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Finalize Track Stack Remainder</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Background Remainder — 3 cas</button></td><td>✅ 3/3</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[negative-background]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[one-wrap]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[two-wraps]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Rgb — 2 cas</button></td><td>✅ 2/2</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[viridis]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[magma]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Rgb Global Contrast — 2 cas</button></td><td>✅ 2/2</td><td>11ms</td></tr>
   <tr class="test-variant"><td>[black]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[gray]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Upscale Raw</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Upscale Raw Lanczos</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Upscale Raw Edge Cases — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[nearest-neighbor]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[lanczos]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Upscale Raw 2D — 4 cas</button></td><td>✅ 4/4</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[nearest-neighbor-ratio-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[nearest-neighbor-ratio-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[lanczos-ratio-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[lanczos-ratio-2]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Get Localization Colors</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Get Tracks Colors</td><td>✅</td><td>11ms</td></tr>
   <tr><td>Prepare Localizations</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Prepare Tracks</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Prepare Tracks Empty — 2 cas</button></td><td>✅ 2/2</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[empty-data]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[out-of-bounds]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Line Spans — 16 cas</button></td><td>✅ 16/16</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[forward-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[forward-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[forward-descending-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[forward-ascending-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[forward-line-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[forward-line-width-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[forward-point-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[forward-point-width-4]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-descending-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-ascending-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-line-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-line-width-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-point-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reverse-point-width-4]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Line Spans Clipping</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Line Spans Orientations — 32 cas</button></td><td>✅ 32/32</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-down-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-down-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-up-original-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-up-swapped-axes]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Line</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Crossing — 3 cas</button></td><td>✅ 3/3</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Width — 12 cas</button></td><td>✅ 12/12</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[sum-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[sum-width-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[sum-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[sum-width-4]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-4]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-4]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Point Width — 4 cas</button></td><td>✅ 4/4</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Draw Line Width Border</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Width Orientations — 42 cas</button></td><td>✅ 42/42</td><td>39ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-shallow-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-steep-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-left]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-up]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-shallow-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-steep-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-left]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-up]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-shallow-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-steep-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-left]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-up]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-shallow-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-steep-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-left]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-up]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-shallow-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-steep-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-left]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-up]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-diagonal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-shallow-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-steep-slope]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-left]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-up]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Alpha — 10 cas</button></td><td>✅ 10/10</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[sum-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[sum-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-higher-value-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-higher-value-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-lower-value-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-lower-value-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-higher-value-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-higher-value-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-lower-value-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-lower-value-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Alpha Initial Background — 6 cas</button></td><td>✅ 6/6</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[sum-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[sum-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-3]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Clamped Parameters — 9 cas</button></td><td>✅ 9/9</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[negative-alpha-negative-width]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[negative-alpha-zero-width]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[negative-alpha-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[partial-alpha-negative-width]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[partial-alpha-zero-width]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[partial-alpha-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[alpha-above-one-negative-width]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[alpha-above-one-zero-width]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[alpha-above-one-width-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Width Finalize — 9 cas</button></td><td>✅ 9/9</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[width-2-sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-2-minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-3-minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[width-4-minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Line Thick Empty Rows</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Gaussian</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Gaussian 3D</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Draw Track Blinks</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Track Empty Rows</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Track Short Fade Long Blink</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Track Hard Cutoff</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Overlap — 3 cas</button></td><td>✅ 3/3</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Thickness — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Track Stationary And Clipping</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Alpha Independent Of Geometry — 6 cas</button></td><td>✅ 6/6</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[stationary-departure-0]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[stationary-departure-9]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[horizontal-departure-0]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[horizontal-departure-9]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[diagonal-departure-0]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[diagonal-departure-9]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Heads Planes — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[negative-diameter]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[zero-diameter]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[diameter-1]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Heads Circles — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[diameter-2]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[diameter-4]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[diameter-5]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Track Heads Clipping</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Track Heads Priority</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Draw Track Heads Preserve Interior</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Renderer Atom</td><td>✅</td><td>2.94s</td></tr>
   <tr><td>Renderer Track Stack Spiral</td><td>✅</td><td>357ms</td></tr>
   <tr><td>Renderer Track Stack Spiral Raw</td><td>✅</td><td>3.40s</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Upscale Raw Edge Cases [nearest-neighbor]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Raw shape doesn't have expected dimensions for output background will be 0.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Upscale Raw Edge Cases [lanczos]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Raw shape doesn't have expected dimensions for output background will be 0.</span><span style="font-weight: bold"></span></pre>
   </details>

Processing Step
^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Object Creation</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Prepare Action — 9 cas</button></td><td>✅ 9/9</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[inactive-without-previous]</td><td>✅</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[active-without-previous]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[dirty-pipeline]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[inactive-with-dirty-pipeline]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[reactivation-through-reuse]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[both-groups-inactive]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[activation-without-previous-result]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[identical-parameters]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[different-parameters]</td><td>✅</td><td>10ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Object Creation</summary>
      <pre>Step : Step(group_name='name', keys=['key'], process_func=&lt;function test_object_creation.&lt;locals&gt;.f at 0x000001ED88FFEB90&gt;, filter_func=&lt;function test_object_creation.&lt;locals&gt;.f at 0x000001ED88FFEB90&gt;, allow_dirty=False, apply_filter=True)<br>Actions : StepAction.Compute,StepAction.Reuse,StepAction.Skip</pre>
   </details>

Results
^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Accessors</td><td>✅</td><td>22ms</td></tr>
   <tr><td>Active Results</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Dataframe Status — 5 cas</button></td><td>✅ 5/5</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[no-tracks]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[original-tracks-only]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[all-tracks-preserved]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[partially-filtered-tracks]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[reconnected-filtered-tracks]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Status</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Reset</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Load</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Save</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Interfaces</td><td>✅</td><td>47ms</td></tr>
   </tbody>
   </table>

Settings Groups
^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Base Group</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Batch</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Batch Get Path — 5 cas</button></td><td>✅ 5/5</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[no-files]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[first-file]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[second-file]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[all-files]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[merged-files]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Batch Get Stacks — 5 cas</button></td><td>✅ 5/5</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[no-stacks]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[selected-stack]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[separate-stacks]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[compatible-merge]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[invalid-dimensions]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Calibration</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Localization</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Localization Fit</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Gaussian Fit</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Gaussian Fit Z</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Spline Fit</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Beads</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Tracking</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Tracks Blinking Reconnection</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Tracks Computes</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Filters</td><td>✅</td><td>22ms</td></tr>
   <tr><td>Filters L</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Filters T</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Gallery</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Graph</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Graph Display</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Hr</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Hr Gaussian</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Hr 3D</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Hr Track Stack</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Visualization 3D</td><td>✅</td><td>12ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Batch</summary>
      <pre>- Activate : True<br>- Files : -1<br>- Mode : 0<br><br>{'Files': -1, 'Mode': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Batch Get Stacks [invalid-dimensions]</summary>
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
      <pre>- Activate : True<br>- Save : True<br>- Plane : Deactivate [1, 100000]<br>- ROI : 1<br>- Localization :<br>  - Activate : True<br>  - Z : Deactivate [-2000, 2000]<br>  - Intensity : Deactivate [0, 10000000]<br>  - Sigma X : Deactivate [0, 10]<br>  - Sigma Y : Deactivate [0, 10]<br>  - Circularity : Deactivate [0, 1.0]<br>  - Theta : Deactivate [-90, 90]<br>  - MSE XY : Deactivate [0, 1.0]<br>  - MSE Z : Deactivate [0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Track : <br>  - Length : Deactivate [1, 10000]<br>  - Instant D : Deactivate [-5, 5]<br>  - D Coeff : Deactivate [-5, 5]<br>  - Alpha : Deactivate [-10, 10]<br>  - Speed : Deactivate [0, 1.0]<br>  - Confinement : Deactivate [-10, 10]<br><br>{'Save': True, 'Plane': [1, 100000], 'ROI': 1, 'Localization Z': [-2000, 2000], 'Localization Intensity': [0, 10000000], 'Localization Sigma X': [0, 10], 'Localization Sigma Y': [0, 10], 'Localization Circularity': [0, 1.0], 'Localization Theta': [-90, 90], 'Localization MSE XY': [0, 1.0], 'Localization MSE Z': [0, 1.0], 'Tracks Track': '', 'Tracks Length': [1, 10000], 'Tracks Instant D': [-5, 5], 'Tracks D Coeff': [-5, 5], 'Tracks Alpha': [-10, 10], 'Tracks Speed': [0, 1.0], 'Tracks Confinement': [-10, 10]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters L</summary>
      <pre>- Activate : True<br>- Z : Deactivate [2, 9]<br>- Intensity : Deactivate [0, 10000000]<br>- Sigma X : Deactivate [0, 10]<br>- Sigma Y : Deactivate [0, 10]<br>- Circularity : Deactivate [0, 1.0]<br>- Theta : Deactivate [-90, 90]<br>- MSE XY : Deactivate [0, 1.0]<br>- MSE Z : Deactivate [0, 1.0]<br><br>{'Z': [2, 9], 'Intensity': [0, 10000000], 'Sigma X': [0, 10], 'Sigma Y': [0, 10], 'Circularity': [0, 1.0], 'Theta': [-90, 90], 'MSE XY': [0, 1.0], 'MSE Z': [0, 1.0]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters T</summary>
      <pre>- Activate : True<br>- Track : 1;3-4<br>- Length : Deactivate [1, 10000]<br>- Instant D : Deactivate [-5, 5]<br>- D Coeff : Deactivate [-5, 5]<br>- Alpha : Deactivate [-10, 10]<br>- Speed : Deactivate [0, 1.0]<br>- Confinement : Deactivate [-10, 10]<br><br>{'Track': '1;3-4', 'Length': [1, 10000], 'Instant D': [-5, 5], 'D Coeff': [-5, 5], 'Alpha': [-10, 10], 'Speed': [0, 1.0], 'Confinement': [-10, 10]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Gallery</summary>
      <pre>- Activate : True<br>- ROI Size : 11<br>- ROIs Per Line : 30<br><br>{'ROI Size': 11, 'ROIs Per Line': 30}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Graph</summary>
      <pre>- Activate : True<br>- Type : 1<br>- Source : 0<br>- Dual : False<br>- Source B : 0<br>- MSD Step : 1<br>- Display :<br>  - Activate : True<br>  - Limits : True<br>  - Sigma : False<br>  - Gauss : False<br>  - Gauss Mix : False<br>  - KDE : False<br>  - Poiss : False<br>  - Exp : False<br>  - Cumul : False<br>  - Log Scale : False<br>  - Count : False<br>  - Bins : 0<br><br>{'Type': 1, 'Source': 0, 'Dual': False, 'Source B': 0, 'MSD Step': 1, 'Display Limits': True, 'Display Sigma': False, 'Display Gauss': False, 'Display Gauss Mix': False, 'Display KDE': False, 'Display Poiss': False, 'Display Exp': False, 'Display Cumul': False, 'Display Log Scale': False, 'Display Count': False, 'Display Bins': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Graph Display</summary>
      <pre>- Activate : True<br>- Limits : False<br>- Sigma : False<br>- Gauss : False<br>- Gauss Mix : False<br>- KDE : False<br>- Poiss : False<br>- Exp : False<br>- Cumul : False<br>- Log Scale : False<br>- Count : False<br>- Bins : 0<br><br>{'Limits': False, 'Sigma': False, 'Gauss': False, 'Gauss Mix': False, 'KDE': False, 'Poiss': False, 'Exp': False, 'Cumul': False, 'Log Scale': False, 'Count': False, 'Bins': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Hr</summary>
      <pre>- Activate : True<br>- Dimension : 1<br>- Type : 0<br>- Source : 0<br>- Scaling : 1<br>- Color mode : 0<br>- Background : 0<br>- Ratio : 4<br>- Crop : True<br>- Remove Beads : True<br>- Drift Correction : True<br>- Smooth Drift : True<br>- Gaussian :<br>  - Activate : False<br>  - Intensity : 100<br>  - Fixed Intensity : False<br>  - Shape : 0<br>  - Size : 1<br>- 3D :<br>  - Activate : True<br>  - Z Step : 20<br>  - Axis : 1<br>  - Frames : 36<br>- T-Stack :<br>  - Activate : True<br>  - Head : 1<br>  - Width : 1<br>  - Length : -1<br>  - Fade : 0<br>  - Map : 0<br>  - Background : True<br>  - Upscale : 0<br><br>{'Dimension': 1, 'Type': 0, 'Source': 0, 'Scaling': 1, 'Color mode': 0, 'Background': 0, 'Ratio': 4, 'Crop': True, 'Remove Beads': True, 'Drift Correction': True, 'Smooth Drift': True, 'Gaussian Intensity': 100, 'Gaussian Fixed Intensity': False, 'Gaussian Shape': 0, 'Gaussian Size': 1, '3D Z Step': 20, '3D Axis': 1, '3D Frames': 36, 'T-Stack Head': 1, 'T-Stack Width': 1, 'T-Stack Length': -1, 'T-Stack Fade': 0, 'T-Stack Map': 0, 'T-Stack Background': True, 'T-Stack Upscale': 0}</pre>
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
      <summary>Log Test : Hr Track Stack</summary>
      <pre>- Activate : True<br>- Head : 5<br>- Width : 1<br>- Length : -1<br>- Fade : 0<br>- Map : 0<br>- Background : True<br>- Upscale : 0<br><br>{'Head': 5, 'Width': 1, 'Length': -1, 'Fade': 0, 'Map': 0, 'Background': True, 'Upscale': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Visualization 3D</summary>
      <pre>- Activate : True<br>- Point Size : 2<br>- Pixel Size : 160<br>- XY Scale : 1.0<br>- Z Scale : 1.0<br>- Remove Outliers : False<br><br>{'Point Size': 2, 'Pixel Size': 160, 'XY Scale': 1.0, 'Z Scale': 1.0, 'Remove Outliers': False}</pre>
   </details>

Settings Roimanager
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Rois</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Set Xy Roi</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Layer</td><td>✅</td><td>384ms</td></tr>
   <tr><td>Update Main</td><td>✅</td><td>42ms</td></tr>
   <tr><td>Update Hr</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Update Roi Selection</td><td>✅</td><td>14ms</td></tr>
   <tr><td>Dict</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Roi Limits</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Hr Box</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Filtering Dataframe</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Filtering Dataframe Concave Cross</td><td>✅</td><td>2ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Filtering Dataframe</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">ROI type 'line' does not define an area compatible with strict filtering.</span><span style="font-weight: bold"></span></pre>
   </details>

Settings Settings
^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Settings</td><td>✅</td><td>102ms</td></tr>
   <tr><td>Settings Group Getter</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Settings Signal</td><td>✅</td><td>11ms</td></tr>
   </tbody>
   </table>

Settings Types
^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Base Setting</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Base Check Setting — 4 cas</button></td><td>✅ 4/4</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[CheckInt]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[CheckIntSelection]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[CheckRangeFloat]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[CheckRangeInt]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Base Ui</td><td>✅</td><td>94ms</td></tr>
   <tr><td>Base Ui No Label</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Spin Int</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Spin Float</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Check Box</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Combo</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Browse File</td><td>✅</td><td>2ms</td></tr>
   <tr><td>File List</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Check Int</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Check Range Int</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Check Range Float</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Check Int Selection</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Button</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Button Group</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Sync</td><td>✅</td><td>10ms</td></tr>
   </tbody>
   </table>

Settings Types Signal
^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Connect And Emit Direct</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Disconnect</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Block Simple Coalescence Last Value</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Block Without Emits No Output</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Nested Blocks Emit Once At Outer Exit</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Emit Default None Coalesced</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Block Flags Reset After Flush</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Block Without Emit</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Blocked Returns Context Manager Instance</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Internal Block Begin End Paths</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Coalescence Overwrite Multiple Times</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Emit Direct After Previous Block</td><td>✅</td><td>1ms</td></tr>
   </tbody>
   </table>

Tools Fileio
^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Add Extension — 6 cas</button></td><td>✅ 6/6</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[existing-extension]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[multiple-dots]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[with-directories]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[extension-already-present]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[extension-with-dot]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Add Suffix — 2 cas</button></td><td>✅ 2/2</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[with-extension]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Timestamp For Files — 2 cas</button></td><td>✅ 2/2</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[with-time]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[date-only]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Last File — 2 cas</button></td><td>✅ 2/2</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[alphabetical-order]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[modification-time]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Last File Not Found — 2 cas</button></td><td>✅ 2/2</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing-directory]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[no-match]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Extract Suffix — 5 cas</button></td><td>✅ 5/5</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[empty-name]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[no-suffix]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[single-suffix]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[last-suffix]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cleanup Process — 4 cas</button></td><td>✅ 4/4</td><td>264ms</td></tr>
   <tr class="test-variant"><td>[empty-directory]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[administrative-files-only]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[result-still-present]</td><td>✅</td><td>234ms</td></tr>
   <tr class="test-variant"><td>[other-timestamp-preserved]</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Cleanup Process Missing Folder</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Load Dll</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Load Dll Missing</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Json Roundtrip</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Open Json Bad File</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tif Roundtrip — 2 cas</button></td><td>✅ 2/2</td><td>60ms</td></tr>
   <tr class="test-variant"><td>[stack]</td><td>✅</td><td>44ms</td></tr>
   <tr class="test-variant"><td>[2d-image]</td><td>✅</td><td>16ms</td></tr>
   <tr><td>Save Tif Rgb</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Save Tif Bad Stack — 4 cas</button></td><td>✅ 4/4</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[1d-array]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[5d-array]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[two-channels]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[four-channels]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Open Tif</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Tif Bad File — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[missing-file]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[invalid-dimensions]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Save Png — 3 cas</button></td><td>✅ 3/3</td><td>483ms</td></tr>
   <tr class="test-variant"><td>[normalization]</td><td>✅</td><td>285ms</td></tr>
   <tr class="test-variant"><td>[no-normalization]</td><td>✅</td><td>166ms</td></tr>
   <tr class="test-variant"><td>[black-image]</td><td>✅</td><td>32ms</td></tr>
   <tr><td>Save Png Color</td><td>✅</td><td>11ms</td></tr>
   <tr><td>Save Png Bad Sample</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Open Calibration Mat Bad File</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Open Calibration Mat</td><td>✅</td><td>4ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Load Dll Missing</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to load the DLL 'PALMTracer_File.dll':<br>	Could not find module 'C:\Git\palm-tracer\palm_tracer\DLL\PALMTracer_File.dll' (or one of its dependencies). Try using the full path with constructor syntax.</span><span style="font-weight: bold"></span></pre>
   </details>

Tools Filemigrator
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Open</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Invalid — 3 cas</button></td><td>✅ 3/3</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[directory-without-results]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[file-instead-of-directory]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[missing-directory]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Analyze</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Analyze Invalid — 1 cas</button></td><td>✅ 1/1</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[no-directory]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Migrate</td><td>✅</td><td>218ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Migrate Invalid — 1 cas</button></td><td>✅ 1/1</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[no-directory]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Update Meta</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Open Old File</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Old File Invalid — 2 cas</button></td><td>✅ 2/2</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[directory-instead-of-file]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[invalid-content]</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Open Old Irregular File</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Old Irregular File Invalid — 2 cas</button></td><td>✅ 2/2</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[directory-instead-of-file]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[invalid-content]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Column Migrator</td><td>✅</td><td>1ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Analyze</summary>
      <pre>.</pre>
   </details>

Tools Logger
^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Logger</td><td>✅</td><td>26ms</td></tr>
   <tr><td>Logger Bad Use</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Logger With Use</td><td>✅</td><td>2ms</td></tr>
   </tbody>
   </table>

Tools Monitoring
^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Monitoring</td><td>✅</td><td>3.08s</td></tr>
   <tr><td>Monitoring Draw Test Section</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Monitoring Draw</td><td>✅</td><td>32ms</td></tr>
   <tr><td>Monitoring Removes Samples Before First Test</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Monitoring Save</td><td>✅</td><td>6.27s</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>10 entrées.<br>Timestamps : [0.0, 0.21, 0.42, 0.63, 0.85, 2.02, 2.23, 2.44, 2.65, 2.86]<br>CPU Usage : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.484375, 0.484375, 0.0, 0.484375]<br>GPU Usage : [16, 16, 16, 3, 3, 0, 0, 0, 0, 0]<br>Memory Usage : [773.21484375, 773.21484375, 773.21484375, 773.21875, 773.21875, 773.22265625, 773.22265625, 773.22265625, 773.22265625, 773.22265625]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Monitoring Save</summary>
      <pre>Simulating high CPU usage for 2 seconds...<br>CPU simulation complete.<br>Aucun GPU CUDA disponible pour la simulation.<br>Allocating 50 MB of memory...<br>Memory allocated. Holding for 2 seconds...<br>Releasing memory.<br>Writing a file of size 1 MB...<br>File written. Holding for 2 seconds...<br>Deleting the file...<br>Disk I/O simulation complete.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Kaleido doesn't work so well need update. No Image Saved.</span><span style="font-weight: bold"></span></pre>
   </details>

Tools Ui
^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Add Setting Row</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Init Layout</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Container — 2 cas</button></td><td>✅ 2/2</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[tab]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[group]</td><td>✅</td><td>3ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Info Grid — 2 cas</button></td><td>✅ 2/2</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[no-units]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[with-units-and-tooltips]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Make File Info Group</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Make Path Label</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Path Label — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[string]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[path-object]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Make Vertical Scroll</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Separator — 2 cas</button></td><td>✅ 2/2</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[vertical]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[horizontal]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Spin — 2 cas</button></td><td>✅ 2/2</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[integer-with-buttons]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[decimal-without-buttons]</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Sync Button Group</td><td>✅</td><td>1ms</td></tr>
   <tr><td>Sync Spin</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Spin Limits — 4 cas</button></td><td>✅ 4/4</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[no-change]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minimum-only]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[maximum-only]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[both-bounds]</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Print Message — 3 cas</button></td><td>✅ 3/3</td><td>3ms</td></tr>
   <tr class="test-variant"><td>[error]</td><td>✅</td><td>2ms</td></tr>
   <tr class="test-variant"><td>[warning]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[success]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Format Time — 4 cas</button></td><td>✅ 4/4</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[zero-duration]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[seconds]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[minute-boundary]</td><td>✅</td><td>1ms</td></tr>
   <tr class="test-variant"><td>[hours-minutes-seconds]</td><td>✅</td><td>1ms</td></tr>
   </tbody>
   </table>

Ui Alignment
^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>95ms</td></tr>
   <tr><td>Bad Load Tif</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Bad Load Coef</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Bad Compute</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Compute</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Bad Align</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Align</td><td>✅</td><td>169ms</td></tr>
   </tbody>
   </table>

Ui Astigmatism3D
^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>316ms</td></tr>
   <tr><td>Sync Spin</td><td>✅</td><td>64ms</td></tr>
   <tr><td>Check Loc</td><td>✅</td><td>69ms</td></tr>
   <tr><td>Bad Load Loc</td><td>✅</td><td>51ms</td></tr>
   <tr><td>Bad Load Model</td><td>✅</td><td>51ms</td></tr>
   <tr><td>Bad Compute</td><td>✅</td><td>45ms</td></tr>
   <tr><td>Compute</td><td>✅</td><td>120ms</td></tr>
   <tr><td>Compute Mean Beads</td><td>✅</td><td>118ms</td></tr>
   <tr><td>Compute Remove Bead Col</td><td>✅</td><td>106ms</td></tr>
   <tr><td>Compute Remove Multi</td><td>✅</td><td>109ms</td></tr>
   <tr><td>Compute Z</td><td>✅</td><td>114ms</td></tr>
   <tr><td>Compute Center Z</td><td>✅</td><td>296ms</td></tr>
   <tr><td>Compute Bad Model</td><td>✅</td><td>118ms</td></tr>
   <tr><td>Bad Estimate</td><td>✅</td><td>46ms</td></tr>
   <tr><td>Estimate</td><td>✅</td><td>76ms</td></tr>
   <tr><td>Estimate Backup</td><td>✅</td><td>95ms</td></tr>
   <tr><td>Download</td><td>✅</td><td>65ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Download</summary>
      <pre>C:\Git\palm-tracer\palm_tracer\_tests\input\ref</pre>
   </details>

Ui Baseplotlywidget
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Creation</td><td>✅</td><td>14ms</td></tr>
   <tr><td>Update Plotly</td><td>✅</td><td>18ms</td></tr>
   <tr><td>Update Plotly No Js</td><td>✅</td><td>17ms</td></tr>
   <tr><td>Download Plotly</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Export Plotly</td><td>✅</td><td>19ms</td></tr>
   </tbody>
   </table>

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

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>3ms</td></tr>
   <tr><td>Bad Load</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Mirgate</td><td>✅</td><td>36ms</td></tr>
   </tbody>
   </table>

Ui Graphviewer
^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>79ms</td></tr>
   <tr><td>Results Status Automatic Update</td><td>✅</td><td>72ms</td></tr>
   <tr><td>Widget Double Creation</td><td>✅</td><td>125ms</td></tr>
   <tr><td>Change Type</td><td>✅</td><td>85ms</td></tr>
   <tr><td>Add Stack</td><td>✅</td><td>85ms</td></tr>
   <tr><td>Update Plot Localization</td><td>✅</td><td>157ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Add Stack</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span></pre>
   </details>

Ui Palmtracer
^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Creation</td><td>✅</td><td>968ms</td></tr>
   <tr><td>Filters Button</td><td>✅</td><td>1.06s</td></tr>
   <tr><td>Thread Process</td><td>✅</td><td>941ms</td></tr>
   <tr><td>On Load Setting</td><td>✅</td><td>1.58s</td></tr>
   <tr><td>Reset Setting</td><td>✅</td><td>1.53s</td></tr>
   <tr><td>Clean Layer</td><td>✅</td><td>1.05s</td></tr>
   <tr><td>Reset Layer</td><td>✅</td><td>948ms</td></tr>
   <tr><td>Add Detection Layers</td><td>✅</td><td>1.67s</td></tr>
   <tr><td>Get Actual Image</td><td>✅</td><td>1.15s</td></tr>
   <tr><td>Preview</td><td>✅</td><td>1.08s</td></tr>
   <tr><td>Auto Threshold</td><td>✅</td><td>878ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Filters Button</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span><br>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif (10, 128, 256) into Napari viewer.<br>[14-09-2026 16:58:35] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165835.log<br>[14-09-2026 16:58:35] Start Processing.<br>[14-09-2026 16:58:35] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[14-09-2026 16:58:35] Meta file saved.<br>[14-09-2026 16:58:35] Settings saved.<br>[14-09-2026 16:58:35] Localization enabled.<br>[14-09-2026 16:58:35] 	Saving the localization file (455 localization(s) found).<br>[14-09-2026 16:58:35] Beads Extraction disabled.<br>[14-09-2026 16:58:35] Tracking disabled.<br>[14-09-2026 16:58:35] Blinking Reconnection disabled.<br>[14-09-2026 16:58:35] Tracks Compute disabled.<br>[14-09-2026 16:58:35] Gallery generation disabled.<br>[14-09-2026 16:58:35] Graphical visualization disabled.<br>[14-09-2026 16:58:35] High-resolution visualization disabled.<br>[14-09-2026 16:58:35] Processing complete.<br>[14-09-2026 16:58:35] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165835.log<br>{'reset': &lt;PySide6.QtWidgets.QPushButton(0x1ed99da3ab0) at 0x000001ED8DCAEB00&gt;, 'update': &lt;PySide6.QtWidgets.QPushButton(0x1ed99da1a10) at 0x000001ED8DCAEAC0&gt;, 'save': &lt;PySide6.QtWidgets.QPushButton(0x1ed99da3c80) at 0x000001ED8DCAEA00&gt;}<br>- Activate : True<br>- Save : False<br>- Plane : Activate [1, 5]<br>- ROI : 1<br>- Localization :<br>  - Activate : True<br>  - Z : Deactivate [-2000, 2000]<br>  - Intensity : Deactivate [0, 10000000]<br>  - Sigma X : Deactivate [0, 10]<br>  - Sigma Y : Deactivate [0, 10]<br>  - Circularity : Deactivate [0, 1.0]<br>  - Theta : Deactivate [-90, 90]<br>  - MSE XY : Deactivate [0, 1.0]<br>  - MSE Z : Deactivate [0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Track : <br>  - Length : Deactivate [1, 10]<br>  - Instant D : Deactivate [-5, 5]<br>  - D Coeff : Deactivate [-5, 5]<br>  - Alpha : Deactivate [-10, 10]<br>  - Speed : Deactivate [0, 1.0]<br>  - Confinement : Deactivate [-10, 10]<br><br>[14-09-2026 16:58:35] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165835.log<br>[14-09-2026 16:58:35] Start Processing.<br>[14-09-2026 16:58:35] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[14-09-2026 16:58:35] Meta file saved.<br>[14-09-2026 16:58:35] Settings saved.<br>[14-09-2026 16:58:35] Localization load previous result (Timestamp : 20260914_165835).<br>[14-09-2026 16:58:35] 	File 'localizations-20260914_165835.csv' loaded successfully, 455 row(s) found.<br>[14-09-2026 16:58:35] 		Filtering of file 242 row(s) instead of 455: 213 deletion(s).<br>[14-09-2026 16:58:35] Beads Extraction disabled.<br>[14-09-2026 16:58:35] Tracking disabled.<br>[14-09-2026 16:58:35] Blinking Reconnection disabled.<br>[14-09-2026 16:58:35] Tracks Compute disabled.<br>[14-09-2026 16:58:35] Gallery generation disabled.<br>[14-09-2026 16:58:35] Graphical visualization disabled.<br>[14-09-2026 16:58:35] High-resolution visualization disabled.<br>[14-09-2026 16:58:35] Processing complete.<br>[14-09-2026 16:58:35] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165835.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Thread Process</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span><br>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif (10, 128, 256) into Napari viewer.<br>[14-09-2026 16:58:36] Log opened : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165836.log<br>[14-09-2026 16:58:36] Start Processing.<br>[14-09-2026 16:58:36] Output folder: C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer<br>[14-09-2026 16:58:36] Meta file saved.<br>[14-09-2026 16:58:36] Settings saved.<br>[14-09-2026 16:58:36] Localization load previous result (Timestamp : 20260914_165835).<br>[14-09-2026 16:58:36] 	File 'localizations-20260914_165835.csv' loaded successfully, 455 row(s) found.<br>[14-09-2026 16:58:36] Beads Extraction disabled.<br>[14-09-2026 16:58:36] Tracking disabled.<br>[14-09-2026 16:58:36] Blinking Reconnection disabled.<br>[14-09-2026 16:58:36] Tracks Compute disabled.<br>[14-09-2026 16:58:36] Gallery generation disabled.<br>[14-09-2026 16:58:36] Graphical visualization disabled.<br>[14-09-2026 16:58:36] High-resolution visualization disabled.<br>[14-09-2026 16:58:36] Processing complete.<br>[14-09-2026 16:58:36] Log closed : C:\Git\palm-tracer\palm_tracer\_tests\input\stack_PALM_Tracer\log-20260914_165836.log<br>Auto Threshold: 63.95</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Get Actual Image</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span><br>INFO: Loaded C:\Git\palm-tracer\palm_tracer\_tests\input\stack.tif (10, 128, 256) into Napari viewer.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Preview</summary>
      <pre>Preview of plane 4 : 142 detected points (46 on the current frame, 48 on the previous frame, 48 on the next frame).</pre>
   </details>

Ui Resultsui
^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Creation</td><td>✅</td><td>2ms</td></tr>
   <tr><td>Update Status</td><td>✅</td><td>1ms</td></tr>
   </tbody>
   </table>

Ui Viewer3D
^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>474ms</td></tr>
   <tr><td>Viewer3D</td><td>✅</td><td>492ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Viewer3D</summary>
      <pre>WARNING: The file must contain the columns X, Y, Z, and Integrated Intensity.</pre>
   </details>

Ui Viewerhr
^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>647ms</td></tr>
   <tr><td>Results Status Automatic Update</td><td>✅</td><td>671ms</td></tr>
   <tr><td>Widget Double Creation</td><td>✅</td><td>1.14s</td></tr>
   <tr><td>Check Beads</td><td>✅</td><td>619ms</td></tr>
   <tr><td>Add Stack</td><td>✅</td><td>673ms</td></tr>
   <tr><td>Actualize</td><td>✅</td><td>663ms</td></tr>
   <tr><td>Save</td><td>✅</td><td>628ms</td></tr>
   <tr><td>Screenshot</td><td>✅</td><td>470ms</td></tr>
   <tr><td>Change Type</td><td>✅</td><td>657ms</td></tr>
   <tr><td>Generate Bad</td><td>✅</td><td>654ms</td></tr>
   <tr><td>Generate</td><td>✅</td><td>756ms</td></tr>
   <tr><td>Visualization Layer Rgb Transitions</td><td>✅</td><td>67ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Widget Creation</summary>
      <pre>WARNING: No stack processed loaded.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Results Status Automatic Update</summary>
      <pre>WARNING: No stack processed loaded.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Widget Double Creation</summary>
      <pre>WARNING: No stack processed loaded.<br>WARNING: No stack processed loaded.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Check Beads</summary>
      <pre>WARNING: No stack processed loaded.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Actualize</summary>
      <pre>WARNING: No stack processed loaded.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Save</summary>
      <pre>WARNING: No stack processed loaded.<br>INFO: Image file saved successfully.<br>INFO: Image file saved successfully.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Screenshot</summary>
      <pre>WARNING: No stack processed loaded.<br>INFO: Screenshot saved successfully.</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Change Type</summary>
      <pre>WARNING: No stack processed loaded.</pre>
   </details>

.. raw:: html

   <style>
   .test-results .test-group button {
       font: inherit; font-weight: bold; color: inherit; background: transparent;
       border: 0; padding: 0; cursor: pointer; text-align: left;
   }
   .test-results .test-group button::before { content: "▶ "; }
   .test-results .test-group button[aria-expanded="true"]::before { content: "▼ "; }
   .test-results .test-variant td:first-child { padding-left: 2em; }
   .test-results tr[hidden] { display: none; }
   .test-page table.docutils.test-results tbody > tr > td { background-color: white; }
   .test-page table.docutils.test-results tbody > tr.test-row-odd > td { background-color: #f3f6f6; }
   </style>
   <script>
   (() => {
       const page = document.currentScript.closest('.test-page');
       // Recalculer l'alternance uniquement sur les lignes visibles.
       const stripeTable = table => {
           let index = 0;
           table.querySelectorAll('tbody > tr').forEach(row => {
               row.classList.toggle('test-row-odd', !row.hidden && index % 2 === 0);
               if (!row.hidden) { index += 1; }
           });
       };
       page.querySelectorAll('.test-group button').forEach(button => {
           const rows = [];
           let next = button.closest('tr').nextElementSibling;
           while (next && next.classList.contains('test-variant')) {
               rows.push(next);
               next = next.nextElementSibling;
           }
           const setExpanded = expanded => {
               button.setAttribute('aria-expanded', String(expanded));
               rows.forEach(row => { row.hidden = !expanded; });
           };
           setExpanded(false);
           button.addEventListener('click', () => {
               setExpanded(button.getAttribute('aria-expanded') !== 'true');
               stripeTable(button.closest('table'));
           });
       });
       page.querySelectorAll('.test-results').forEach(stripeTable);
   })();
   </script>
   </div>
