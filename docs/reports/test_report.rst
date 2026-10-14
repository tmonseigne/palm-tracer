Test Report
===========

Environnement
-------------

.. list-table::

   * - Python
     - 3.14.8
   * - Platform
     - Windows-11-10.0.26300-SP0
   * - JAVA_HOME
     - C:\Program Files\OpenJDK\jdk-26.0.2.1
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

1458 tests collected, 1458 passed ✅, 0 failed ❌, 0 skipped ⏭️ in 0:03:58s on 14/10/2026 at 11:21:53

Monitoring
----------

.. raw:: html

   <div style="position: relative; width: 100%; height: 620px; max-width: 100%; margin: 0 0 1em 0; padding:0;">
     <iframe src="monitoring.html"
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
   <tr><td>Reset Result</td><td>✅</td><td>97ms</td></tr>
   <tr><td>Clean Ui</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Getter Path</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Getter Stack</td><td>✅</td><td>24ms</td></tr>
   <tr><td>Getter Suffix</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Save Setting Group Missing File — 2 cas</button></td><td>✅ 2/2</td><td>125ms</td></tr>
   <tr class="test-variant"><td>[hr]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[filters]</td><td>✅</td><td>66ms</td></tr>
   <tr><td>Getter Localization</td><td>✅</td><td>36ms</td></tr>
   <tr><td>Getter Beads</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Getter Tracks</td><td>✅</td><td>27ms</td></tr>
   <tr><td>Getter Track Analysis</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Missing Dll — 2 cas</button></td><td>✅ 2/2</td><td>55ms</td></tr>
   <tr class="test-variant"><td>[load-results]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[run-pipeline]</td><td>✅</td><td>27ms</td></tr>
   <tr><td>Load Nothing</td><td>✅</td><td>74ms</td></tr>
   <tr><td>Load</td><td>✅</td><td>303ms</td></tr>
   <tr><td>Load Stack Error</td><td>✅</td><td>113ms</td></tr>
   <tr><td>Process No Input</td><td>✅</td><td>61ms</td></tr>
   <tr><td>Process Nothing</td><td>✅</td><td>1.88s</td></tr>
   <tr><td>Process Multiple Stack</td><td>✅</td><td>349ms</td></tr>
   <tr><td>Process All</td><td>✅</td><td>1.26s</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Process Step Recomputes After Reuse Error — 2 cas</button></td><td>✅ 2/2</td><td>149ms</td></tr>
   <tr class="test-variant"><td>[unreadable-csv]</td><td>✅</td><td>64ms</td></tr>
   <tr class="test-variant"><td>[rename-denied]</td><td>✅</td><td>85ms</td></tr>
   <tr><td>Process Localization</td><td>✅</td><td>309ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Process Localization Z — 2 cas</button></td><td>✅ 2/2</td><td>1.08s</td></tr>
   <tr class="test-variant"><td>[specific-model]</td><td>✅</td><td>556ms</td></tr>
   <tr class="test-variant"><td>[default-model]</td><td>✅</td><td>520ms</td></tr>
   <tr><td>Process Localization Spline Bad</td><td>✅</td><td>158ms</td></tr>
   <tr><td>Process Localization Spline</td><td>✅</td><td>267ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Astigmatism Model — 5 cas</button></td><td>✅ 5/5</td><td>443ms</td></tr>
   <tr class="test-variant"><td>[explicit-path]</td><td>✅</td><td>80ms</td></tr>
   <tr class="test-variant"><td>[output-folder]</td><td>✅</td><td>111ms</td></tr>
   <tr class="test-variant"><td>[parent-folder]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[user-folder]</td><td>✅</td><td>62ms</td></tr>
   <tr class="test-variant"><td>[missing-model]</td><td>✅</td><td>121ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Astigmatism Model Invalid User Backup — 2 cas</button></td><td>✅ 2/2</td><td>481ms</td></tr>
   <tr class="test-variant"><td>[invalid-shape]</td><td>✅</td><td>45ms</td></tr>
   <tr class="test-variant"><td>[unreadable-csv]</td><td>✅</td><td>436ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Astigmatism Model Default Only — 4 cas</button></td><td>✅ 4/4</td><td>334ms</td></tr>
   <tr class="test-variant"><td>[valid-default]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[missing-default]</td><td>✅</td><td>70ms</td></tr>
   <tr class="test-variant"><td>[invalid-default]</td><td>✅</td><td>118ms</td></tr>
   <tr class="test-variant"><td>[unreadable-default]</td><td>✅</td><td>78ms</td></tr>
   <tr><td>Process Beads Extraction No Beads</td><td>✅</td><td>303ms</td></tr>
   <tr><td>Process Plane Discontinuous</td><td>✅</td><td>84ms</td></tr>
   <tr><td>Process Beads Extraction</td><td>✅</td><td>332ms</td></tr>
   <tr><td>Process Tracking</td><td>✅</td><td>393ms</td></tr>
   <tr><td>Process Tracking Blinking</td><td>✅</td><td>345ms</td></tr>
   <tr><td>Process Track Analysis</td><td>✅</td><td>936ms</td></tr>
   <tr><td>Reset Filtered</td><td>✅</td><td>61ms</td></tr>
   <tr><td>Reset Filtered Saves Only Filters</td><td>✅</td><td>155ms</td></tr>
   <tr><td>Update Filtered</td><td>✅</td><td>368ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Button Does Not Accumulate Filters — 3 cas</button></td><td>✅ 3/3</td><td>555ms</td></tr>
   <tr class="test-variant"><td>[localizations-plane]</td><td>✅</td><td>186ms</td></tr>
   <tr class="test-variant"><td>[tracks-plane]</td><td>✅</td><td>190ms</td></tr>
   <tr class="test-variant"><td>[tracks-id]</td><td>✅</td><td>178ms</td></tr>
   <tr><td>Update Filtered Saves Only Filters</td><td>✅</td><td>93ms</td></tr>
   <tr><td>Save Filtered</td><td>✅</td><td>158ms</td></tr>
   <tr><td>Connect Filters Button</td><td>✅</td><td>519ms</td></tr>
   <tr><td>Filter Localization</td><td>✅</td><td>552ms</td></tr>
   <tr><td>Filter Track Analysis</td><td>✅</td><td>1.00s</td></tr>
   <tr><td>Process Gallery</td><td>✅</td><td>1.08s</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Graph — 77 cas</button></td><td>✅ 77/77</td><td>19.02s</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Integrated Intensity]</td><td>✅</td><td>398ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Sigma X]</td><td>✅</td><td>282ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Sigma Y]</td><td>✅</td><td>377ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Circularity]</td><td>✅</td><td>202ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Theta]</td><td>✅</td><td>164ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-X]</td><td>✅</td><td>231ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Y]</td><td>✅</td><td>240ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Z]</td><td>✅</td><td>226ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Surface]</td><td>✅</td><td>212ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-MSE XY]</td><td>✅</td><td>244ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-MSE Z]</td><td>✅</td><td>228ms</td></tr>
   <tr class="test-variant"><td>[histogram-localizations-Count per Plane]</td><td>✅</td><td>227ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Length]</td><td>✅</td><td>247ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Length On]</td><td>✅</td><td>247ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Length Off]</td><td>✅</td><td>248ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-MSD]</td><td>✅</td><td>239ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Instant D]</td><td>✅</td><td>236ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Total Intensity]</td><td>✅</td><td>272ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-D(0) (\u03bcm\xb2/s)]</td><td>✅</td><td>224ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-MSD(0) (\u03bcm\xb2)]</td><td>✅</td><td>187ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-MSE(0)]</td><td>✅</td><td>247ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-A (\u03bcm\xb2/s)]</td><td>✅</td><td>226ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-B (\u03bcm\xb2)]</td><td>✅</td><td>230ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-MSE]</td><td>✅</td><td>234ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Alpha]</td><td>✅</td><td>251ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Average Speed (Last-First)(\u03bcm/s)]</td><td>✅</td><td>261ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-A (\u03bcm\xb2)]</td><td>✅</td><td>242ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-B (s)]</td><td>✅</td><td>223ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-C (\u03bcm\xb2)]</td><td>✅</td><td>217ms</td></tr>
   <tr class="test-variant"><td>[histogram-tracks-Confinement Radius (\u03bcm)]</td><td>✅</td><td>229ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Integrated Intensity]</td><td>✅</td><td>242ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Sigma X]</td><td>✅</td><td>246ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Sigma Y]</td><td>✅</td><td>225ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Circularity]</td><td>✅</td><td>236ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Theta]</td><td>✅</td><td>227ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-X]</td><td>✅</td><td>247ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Y]</td><td>✅</td><td>253ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Z]</td><td>✅</td><td>245ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Surface]</td><td>✅</td><td>187ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-MSE XY]</td><td>✅</td><td>272ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-MSE Z]</td><td>✅</td><td>252ms</td></tr>
   <tr class="test-variant"><td>[scatter-localizations-Count per Plane]</td><td>✅</td><td>257ms</td></tr>
   <tr class="test-variant"><td>[scatter-tracks-Integrated Intensity]</td><td>✅</td><td>263ms</td></tr>
   <tr class="test-variant"><td>[scatter-tracks-Integrated Intensity Mean]</td><td>✅</td><td>280ms</td></tr>
   <tr class="test-variant"><td>[scatter-tracks-MSD]</td><td>✅</td><td>250ms</td></tr>
   <tr class="test-variant"><td>[scatter-tracks-MSD Mean]</td><td>✅</td><td>205ms</td></tr>
   <tr class="test-variant"><td>[scatter-tracks-Instant D]</td><td>✅</td><td>194ms</td></tr>
   <tr class="test-variant"><td>[scatter-tracks-Instant D Mean]</td><td>✅</td><td>182ms</td></tr>
   <tr class="test-variant"><td>[scatter-tracks-Track Count]</td><td>✅</td><td>285ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Integrated Intensity]</td><td>✅</td><td>235ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Sigma X]</td><td>✅</td><td>211ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Sigma Y]</td><td>✅</td><td>241ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Circularity]</td><td>✅</td><td>237ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Theta]</td><td>✅</td><td>246ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-X]</td><td>✅</td><td>283ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Y]</td><td>✅</td><td>270ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Z]</td><td>✅</td><td>263ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-Surface]</td><td>✅</td><td>232ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-MSE XY]</td><td>✅</td><td>263ms</td></tr>
   <tr class="test-variant"><td>[dual-localizations-MSE Z]</td><td>✅</td><td>246ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Length]</td><td>✅</td><td>288ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Length On]</td><td>✅</td><td>262ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Length Off]</td><td>✅</td><td>286ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Instant D]</td><td>✅</td><td>258ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Total Intensity]</td><td>✅</td><td>261ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-D(0) (\u03bcm\xb2/s)]</td><td>✅</td><td>240ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-MSD(0) (\u03bcm\xb2)]</td><td>✅</td><td>342ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-MSE(0)]</td><td>✅</td><td>258ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-A (\u03bcm\xb2/s)]</td><td>✅</td><td>239ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-B (\u03bcm\xb2)]</td><td>✅</td><td>325ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-MSE]</td><td>✅</td><td>266ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Alpha]</td><td>✅</td><td>232ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Average Speed (Last-First)(\u03bcm/s)]</td><td>✅</td><td>231ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-A (\u03bcm\xb2)]</td><td>✅</td><td>251ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-B (s)]</td><td>✅</td><td>233ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-C (\u03bcm\xb2)]</td><td>✅</td><td>242ms</td></tr>
   <tr class="test-variant"><td>[dual-tracks-Confinement Radius (\u03bcm)]</td><td>✅</td><td>245ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Log Data — 2 cas</button></td><td>✅ 2/2</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[linear]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[logarithmic]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Graph Data Dual Localizations — 2 cas</button></td><td>✅ 2/2</td><td>97ms</td></tr>
   <tr class="test-variant"><td>[paired-values]</td><td>✅</td><td>58ms</td></tr>
   <tr class="test-variant"><td>[missing-source]</td><td>✅</td><td>39ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Graph Data Dual Tracks — 3 cas</button></td><td>✅ 3/3</td><td>386ms</td></tr>
   <tr class="test-variant"><td>[total-duration]</td><td>✅</td><td>150ms</td></tr>
   <tr class="test-variant"><td>[present-duration]</td><td>✅</td><td>100ms</td></tr>
   <tr class="test-variant"><td>[absent-duration]</td><td>✅</td><td>136ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Graph Data Dual Tracks Empty — 2 cas</button></td><td>✅ 2/2</td><td>92ms</td></tr>
   <tr class="test-variant"><td>[incompatible-dimensions]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[no-common-track]</td><td>✅</td><td>52ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Graph Data From Src — 5 cas</button></td><td>✅ 5/5</td><td>212ms</td></tr>
   <tr class="test-variant"><td>[localizations-histogram]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[localizations-scatter]</td><td>✅</td><td>84ms</td></tr>
   <tr class="test-variant"><td>[tracks-histogram]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[tracks-scatter]</td><td>✅</td><td>34ms</td></tr>
   <tr class="test-variant"><td>[tracks-dual]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Localization Graph Data — 6 cas</button></td><td>✅ 6/6</td><td>314ms</td></tr>
   <tr class="test-variant"><td>[linear-histogram]</td><td>✅</td><td>41ms</td></tr>
   <tr class="test-variant"><td>[linear-scatter]</td><td>✅</td><td>84ms</td></tr>
   <tr class="test-variant"><td>[linear-dual]</td><td>✅</td><td>38ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-histogram]</td><td>✅</td><td>38ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-scatter]</td><td>✅</td><td>34ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-dual]</td><td>✅</td><td>78ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Localization Graph Data Count — 2 cas</button></td><td>✅ 2/2</td><td>71ms</td></tr>
   <tr class="test-variant"><td>[histogram]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[scatter]</td><td>✅</td><td>31ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Localization Graph Data Empty — 2 cas</button></td><td>✅ 2/2</td><td>66ms</td></tr>
   <tr class="test-variant"><td>[histogram]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[scatter]</td><td>✅</td><td>31ms</td></tr>
   <tr><td>Get Localization Graph Data Missing Column</td><td>✅</td><td>116ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Scatter Data — 8 cas</button></td><td>✅ 8/8</td><td>424ms</td></tr>
   <tr class="test-variant"><td>[linear-per-track-msd]</td><td>✅</td><td>49ms</td></tr>
   <tr class="test-variant"><td>[linear-per-track-instant-diffusion]</td><td>✅</td><td>42ms</td></tr>
   <tr class="test-variant"><td>[linear-mean-msd]</td><td>✅</td><td>39ms</td></tr>
   <tr class="test-variant"><td>[linear-mean-instant-diffusion]</td><td>✅</td><td>83ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-per-track-msd]</td><td>✅</td><td>42ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-per-track-instant-diffusion]</td><td>✅</td><td>41ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-mean-msd]</td><td>✅</td><td>42ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-mean-instant-diffusion]</td><td>✅</td><td>87ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Scatter Data Metadata — 6 cas</button></td><td>✅ 6/6</td><td>273ms</td></tr>
   <tr class="test-variant"><td>[linear-intensity]</td><td>✅</td><td>34ms</td></tr>
   <tr class="test-variant"><td>[linear-mean-intensity]</td><td>✅</td><td>39ms</td></tr>
   <tr class="test-variant"><td>[linear-count]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-intensity]</td><td>✅</td><td>51ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-mean-intensity]</td><td>✅</td><td>75ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-count]</td><td>✅</td><td>42ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Scatter Data Empty — 4 cas</button></td><td>✅ 4/4</td><td>172ms</td></tr>
   <tr class="test-variant"><td>[msd]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[mean-diffusion]</td><td>✅</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[intensity]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[count]</td><td>✅</td><td>76ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Scatter Data Missing Columns — 4 cas</button></td><td>✅ 4/4</td><td>156ms</td></tr>
   <tr class="test-variant"><td>[missing-step]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[missing-track-id]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[missing-intensity]</td><td>✅</td><td>43ms</td></tr>
   <tr class="test-variant"><td>[missing-plane]</td><td>✅</td><td>41ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Scatter Data Unknown Source — 2 cas</button></td><td>✅ 2/2</td><td>93ms</td></tr>
   <tr class="test-variant"><td>[unknown-source]</td><td>✅</td><td>36ms</td></tr>
   <tr class="test-variant"><td>[unsupported-mean]</td><td>✅</td><td>58ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Graph Data — 3 cas</button></td><td>✅ 3/3</td><td>260ms</td></tr>
   <tr class="test-variant"><td>[msd-step-5]</td><td>✅</td><td>70ms</td></tr>
   <tr class="test-variant"><td>[instant-diffusion]</td><td>✅</td><td>121ms</td></tr>
   <tr class="test-variant"><td>[fit-error]</td><td>✅</td><td>69ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Graph Data Empty — 3 cas</button></td><td>✅ 3/3</td><td>162ms</td></tr>
   <tr class="test-variant"><td>[msd]</td><td>✅</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[diffusion]</td><td>✅</td><td>87ms</td></tr>
   <tr class="test-variant"><td>[fit]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Graph Data Missing Column — 2 cas</button></td><td>✅ 2/2</td><td>200ms</td></tr>
   <tr class="test-variant"><td>[missing-msd-step]</td><td>✅</td><td>76ms</td></tr>
   <tr class="test-variant"><td>[missing-fit-column]</td><td>✅</td><td>123ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Graph Data Options — 24 cas</button></td><td>✅ 24/24</td><td>966ms</td></tr>
   <tr class="test-variant"><td>[linear-histogram-instant-diffusion]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[linear-histogram-diffusion]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-variant"><td>[linear-histogram-diffusion-slope]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[linear-histogram-msd]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-variant"><td>[linear-histogram-length]</td><td>✅</td><td>72ms</td></tr>
   <tr class="test-variant"><td>[linear-histogram-fit-error]</td><td>✅</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[linear-dual-instant-diffusion]</td><td>✅</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[linear-dual-diffusion]</td><td>✅</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[linear-dual-diffusion-slope]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[linear-dual-msd]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[linear-dual-length]</td><td>✅</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[linear-dual-fit-error]</td><td>✅</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-histogram-instant-diffusion]</td><td>✅</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-histogram-diffusion]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-histogram-diffusion-slope]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-histogram-msd]</td><td>✅</td><td>36ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-histogram-length]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-histogram-fit-error]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-dual-instant-diffusion]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-dual-diffusion]</td><td>✅</td><td>87ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-dual-diffusion-slope]</td><td>✅</td><td>34ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-dual-msd]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-dual-length]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-dual-fit-error]</td><td>✅</td><td>42ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Length Data — 4 cas</button></td><td>✅ 4/4</td><td>402ms</td></tr>
   <tr class="test-variant"><td>[legacy-track-duration-pairs]</td><td>✅</td><td>124ms</td></tr>
   <tr class="test-variant"><td>[total-duration]</td><td>✅</td><td>80ms</td></tr>
   <tr class="test-variant"><td>[present-segments]</td><td>✅</td><td>116ms</td></tr>
   <tr class="test-variant"><td>[absent-segments]</td><td>✅</td><td>81ms</td></tr>
   <tr><td>Get Track Length Data Empty</td><td>✅</td><td>35ms</td></tr>
   <tr><td>Get Track Length Data Unknown Source</td><td>✅</td><td>119ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Length Data Without Absence — 2 cas</button></td><td>✅ 2/2</td><td>94ms</td></tr>
   <tr class="test-variant"><td>[durations]</td><td>✅</td><td>44ms</td></tr>
   <tr class="test-variant"><td>[track-duration-pairs]</td><td>✅</td><td>50ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Intensity Data — 4 cas</button></td><td>✅ 4/4</td><td>271ms</td></tr>
   <tr class="test-variant"><td>[linear-per-track]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[linear-mean]</td><td>✅</td><td>112ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-per-track]</td><td>✅</td><td>45ms</td></tr>
   <tr class="test-variant"><td>[logarithmic-mean]</td><td>✅</td><td>74ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Track Count Data — 2 cas</button></td><td>✅ 2/2</td><td>155ms</td></tr>
   <tr class="test-variant"><td>[linear]</td><td>✅</td><td>87ms</td></tr>
   <tr class="test-variant"><td>[logarithmic]</td><td>✅</td><td>68ms</td></tr>
   <tr><td>Process Visualization Graph</td><td>✅</td><td>566ms</td></tr>
   <tr><td>Hr</td><td>✅</td><td>443ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Filtered Plot Data — 8 cas</button></td><td>✅ 8/8</td><td>764ms</td></tr>
   <tr class="test-variant"><td>[excluded-points-raw-2d]</td><td>✅</td><td>118ms</td></tr>
   <tr class="test-variant"><td>[excluded-points-raw-z-stack]</td><td>✅</td><td>78ms</td></tr>
   <tr class="test-variant"><td>[excluded-points-corrected-2d]</td><td>✅</td><td>92ms</td></tr>
   <tr class="test-variant"><td>[excluded-points-corrected-z-stack]</td><td>✅</td><td>124ms</td></tr>
   <tr class="test-variant"><td>[all-kept-raw-2d]</td><td>✅</td><td>77ms</td></tr>
   <tr class="test-variant"><td>[all-kept-raw-z-stack]</td><td>✅</td><td>122ms</td></tr>
   <tr class="test-variant"><td>[all-kept-corrected-2d]</td><td>✅</td><td>76ms</td></tr>
   <tr class="test-variant"><td>[all-kept-corrected-z-stack]</td><td>✅</td><td>77ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Localization Z Source — 2 cas</button></td><td>✅ 2/2</td><td>148ms</td></tr>
   <tr class="test-variant"><td>[unfiltered]</td><td>✅</td><td>93ms</td></tr>
   <tr class="test-variant"><td>[filtered]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Filtered Points All Removed As Beads — 2 cas</button></td><td>✅ 2/2</td><td>166ms</td></tr>
   <tr class="test-variant"><td>[raw]</td><td>✅</td><td>62ms</td></tr>
   <tr class="test-variant"><td>[corrected]</td><td>✅</td><td>103ms</td></tr>
   <tr><td>Hr Filter</td><td>✅</td><td>138ms</td></tr>
   <tr><td>Hr Track Crossing Roi</td><td>✅</td><td>124ms</td></tr>
   <tr><td>Hr Empty Roi 3D</td><td>✅</td><td>83ms</td></tr>
   <tr><td>Hr Z Stack</td><td>✅</td><td>129ms</td></tr>
   <tr><td>Hr Rotation</td><td>✅</td><td>97ms</td></tr>
   <tr><td>Hr Stress</td><td>✅</td><td>560ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Track Stack — 6 cas</button></td><td>✅ 6/6</td><td>650ms</td></tr>
   <tr class="test-variant"><td>[addition-no-background]</td><td>✅</td><td>71ms</td></tr>
   <tr class="test-variant"><td>[addition-with-background]</td><td>✅</td><td>84ms</td></tr>
   <tr class="test-variant"><td>[maximum-no-background]</td><td>✅</td><td>111ms</td></tr>
   <tr class="test-variant"><td>[maximum-with-background]</td><td>✅</td><td>211ms</td></tr>
   <tr class="test-variant"><td>[minimum-no-background]</td><td>✅</td><td>78ms</td></tr>
   <tr class="test-variant"><td>[minimum-with-background]</td><td>✅</td><td>95ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Track Stack Empty Roi — 2 cas</button></td><td>✅ 2/2</td><td>160ms</td></tr>
   <tr class="test-variant"><td>[full-field]</td><td>✅</td><td>105ms</td></tr>
   <tr class="test-variant"><td>[auto-crop]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Track Stack Crop Background — 3 cas</button></td><td>✅ 3/3</td><td>231ms</td></tr>
   <tr class="test-variant"><td>[uniform-background]</td><td>✅</td><td>57ms</td></tr>
   <tr class="test-variant"><td>[raw-background]</td><td>✅</td><td>99ms</td></tr>
   <tr class="test-variant"><td>[black-background]</td><td>✅</td><td>75ms</td></tr>
   <tr><td>Hr Track Stack Dimension Switch</td><td>✅</td><td>137ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Data Crop — 8 cas</button></td><td>✅ 8/8</td><td>1.29s</td></tr>
   <tr class="test-variant"><td>[2d-spots]</td><td>✅</td><td>141ms</td></tr>
   <tr class="test-variant"><td>[2d-fixed-size]</td><td>✅</td><td>156ms</td></tr>
   <tr class="test-variant"><td>[2d-isotropic]</td><td>✅</td><td>180ms</td></tr>
   <tr class="test-variant"><td>[2d-anisotropic]</td><td>✅</td><td>166ms</td></tr>
   <tr class="test-variant"><td>[z-stack-spots]</td><td>✅</td><td>169ms</td></tr>
   <tr class="test-variant"><td>[z-stack-fixed-size]</td><td>✅</td><td>172ms</td></tr>
   <tr class="test-variant"><td>[z-stack-isotropic]</td><td>✅</td><td>125ms</td></tr>
   <tr class="test-variant"><td>[z-stack-anisotropic]</td><td>✅</td><td>182ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Tracks Data Crop — 12 cas</button></td><td>✅ 12/12</td><td>1.90s</td></tr>
   <tr class="test-variant"><td>[full-field-tracks-2d]</td><td>✅</td><td>73ms</td></tr>
   <tr class="test-variant"><td>[full-field-track-stack]</td><td>✅</td><td>172ms</td></tr>
   <tr class="test-variant"><td>[full-field-raw-background]</td><td>✅</td><td>210ms</td></tr>
   <tr class="test-variant"><td>[full-field-large-heads]</td><td>✅</td><td>168ms</td></tr>
   <tr class="test-variant"><td>[full-field-wide-tails]</td><td>✅</td><td>158ms</td></tr>
   <tr class="test-variant"><td>[full-field-wide-raw]</td><td>✅</td><td>241ms</td></tr>
   <tr class="test-variant"><td>[partial-roi-tracks-2d]</td><td>✅</td><td>117ms</td></tr>
   <tr class="test-variant"><td>[partial-roi-track-stack]</td><td>✅</td><td>147ms</td></tr>
   <tr class="test-variant"><td>[partial-roi-raw-background]</td><td>✅</td><td>137ms</td></tr>
   <tr class="test-variant"><td>[partial-roi-large-heads]</td><td>✅</td><td>153ms</td></tr>
   <tr class="test-variant"><td>[partial-roi-wide-tails]</td><td>✅</td><td>132ms</td></tr>
   <tr class="test-variant"><td>[partial-roi-wide-raw]</td><td>✅</td><td>191ms</td></tr>
   <tr><td>Crop</td><td>✅</td><td>103ms</td></tr>
   <tr><td>Crop Track Stack Rgb</td><td>✅</td><td>40ms</td></tr>
   <tr><td>Process Visualization Hr</td><td>✅</td><td>3.57s</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Get Astigmatism Model Invalid User Backup [unreadable-csv]</summary>
      <pre><span style="color: #aa0000"></span><span style="font-weight: bold; color: #aa0000">Unable to read the model file: Error tokenizing data. C error: EOF inside string starting at row 0.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Get Astigmatism Model Default Only [unreadable-default]</summary>
      <pre><span style="color: #aa0000"></span><span style="font-weight: bold; color: #aa0000">Unable to read the model file: Error tokenizing data. C error: EOF inside string starting at row 0.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Update Filtered</summary>
      <pre>[14-10-2026 11:18:12] Log opened : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_update_filtered0\stack_PALM_Tracer\log-20261014_111812.log<br>[14-10-2026 11:18:12] Start Processing.<br>[14-10-2026 11:18:12] Output folder: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_update_filtered0\stack_PALM_Tracer<br>[14-10-2026 11:18:13] Meta file saved.<br>[14-10-2026 11:18:13] Settings saved.<br>[14-10-2026 11:18:13] Localization load previous result (Timestamp : 20260101_000000).<br>[14-10-2026 11:18:13] 	File 'localizations-20260101_000000.csv' loaded successfully, 451 row(s) found.<br>[14-10-2026 11:18:13] Beads Extraction disabled.<br>[14-10-2026 11:18:13] Tracking disabled.<br>[14-10-2026 11:18:13] Blinking Reconnection disabled.<br>[14-10-2026 11:18:13] Track Analysis disabled.<br>[14-10-2026 11:18:13] Gallery generation disabled.<br>[14-10-2026 11:18:13] Graphical visualization disabled.<br>[14-10-2026 11:18:13] High-resolution visualization disabled.<br>[14-10-2026 11:18:13] Processing complete.<br>[14-10-2026 11:18:13] Log closed : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_update_filtered0\stack_PALM_Tracer\log-20261014_111812.log</pre>
   </details>

Processing Astigmatism3D
^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Z From Planes — 5 cas</button></td><td>✅ 5/5</td><td>132ms</td></tr>
   <tr class="test-variant"><td>[symmetric-range]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[negative-range]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[positive-range]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[equal-bounds]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[identical-planes]</td><td>✅</td><td>61ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Z From Step — 3 cas</button></td><td>✅ 3/3</td><td>44ms</td></tr>
   <tr class="test-variant"><td>[centered-odd-count]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[centered-even-count]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[no-centering]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Remove Multi Loc — 6 cas</button></td><td>✅ 6/6</td><td>159ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[missing-plane-column]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[single-point-per-plane]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[no-single-localization-plane]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[spatial-selection]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[bead-column]</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Sigma Model</td><td>✅</td><td>12ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Model Validity — 3 cas</button></td><td>✅ 3/3</td><td>56ms</td></tr>
   <tr class="test-variant"><td>[correct-model]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[reversed-axes]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[different-model]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Model Projection Validity — 3 cas</button></td><td>✅ 3/3</td><td>157ms</td></tr>
   <tr class="test-variant"><td>[correct-model]</td><td>✅</td><td>76ms</td></tr>
   <tr class="test-variant"><td>[reversed-axes]</td><td>✅</td><td>50ms</td></tr>
   <tr class="test-variant"><td>[different-model]</td><td>✅</td><td>31ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Model Projection Astigmatism — 10 cas</button></td><td>✅ 10/10</td><td>292ms</td></tr>
   <tr class="test-variant"><td>[small-pixels-separated-minima]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[small-pixels-reversed-axes]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[small-pixels-coincident-minima]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[small-pixels-minima-at-domain-edges]</td><td>✅</td><td>58ms</td></tr>
   <tr class="test-variant"><td>[small-pixels-asymmetric-model]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[large-pixels-separated-minima]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[large-pixels-reversed-axes]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[large-pixels-coincident-minima]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[large-pixels-minima-at-domain-edges]</td><td>✅</td><td>58ms</td></tr>
   <tr class="test-variant"><td>[large-pixels-asymmetric-model]</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Find Model Center</td><td>✅</td><td>28ms</td></tr>
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
   <tr class="test-group"><td><button type="button" aria-expanded="true">Empty Data — 2 cas</button></td><td>✅ 2/2</td><td>38ms</td></tr>
   <tr class="test-variant"><td>[bead-extraction]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[drift-computation]</td><td>✅</td><td>18ms</td></tr>
   <tr><td>Assign Tracks No Pairs</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Assign Tracks Skip Used Track</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Extract Bead Bad Input — 4 cas</button></td><td>✅ 4/4</td><td>116ms</td></tr>
   <tr class="test-variant"><td>[negative-distance]</td><td>✅</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[missing-columns]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-variant"><td>[non-consecutive-planes]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[single-plane]</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Extract Beads No Match Returns Empty</td><td>✅</td><td>34ms</td></tr>
   <tr><td>Extract Beads</td><td>✅</td><td>283ms</td></tr>
   <tr><td>Remove Beads</td><td>✅</td><td>34ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Drift Bad Input — 3 cas</button></td><td>✅ 3/3</td><td>98ms</td></tr>
   <tr class="test-variant"><td>[missing-columns]</td><td>✅</td><td>58ms</td></tr>
   <tr class="test-variant"><td>[non-consecutive-planes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[single-plane]</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Get Drift</td><td>✅</td><td>81ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Apply Drift Bad Input — 2 cas</button></td><td>✅ 2/2</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[incomplete-localizations]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[incomplete-drift]</td><td>✅</td><td>17ms</td></tr>
   <tr><td>Remove Drift</td><td>✅</td><td>97ms</td></tr>
   <tr><td>Remove Drift Empty</td><td>✅</td><td>15ms</td></tr>
   <tr><td>Chain Drift</td><td>✅</td><td>81ms</td></tr>
   <tr><td>Drift Correction</td><td>✅</td><td>151ms</td></tr>
   <tr><td>Median Filter Centered</td><td>✅</td><td>45ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Median Filter Invalid — 2 cas</button></td><td>✅ 2/2</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[even-window]</td><td>✅</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[3d-array]</td><td>✅</td><td>12ms</td></tr>
   </tbody>
   </table>

Processing Filtering
^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Filter Bad — 3 cas</button></td><td>✅ 3/3</td><td>62ms</td></tr>
   <tr class="test-variant"><td>[localizations]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[tracks]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[track-analysis]</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Localization</td><td>✅</td><td>72ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking — 4 cas</button></td><td>✅ 4/4</td><td>105ms</td></tr>
   <tr class="test-variant"><td>[track-ids]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[length]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[track-ids-and-length]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[filters-disabled]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking Plane — 3 cas</button></td><td>✅ 3/3</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[inclusive-planes]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[plane-disabled]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[filters-disabled]</td><td>✅</td><td>19ms</td></tr>
   <tr><td>Tracking Plane Before Length</td><td>✅</td><td>27ms</td></tr>
   <tr><td>Tracking Plane Empty</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking Time Inside Roi — 7 cas</button></td><td>✅ 7/7</td><td>221ms</td></tr>
   <tr class="test-variant"><td>[fully-outside]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[fully-inside]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[any-occupancy]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[positive-occupancy]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-variant"><td>[partially-inside]</td><td>✅</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[not-fully-inside]</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[roi-disabled]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking Ignores Roi Without Percentage — 2 cas</button></td><td>✅ 2/2</td><td>53ms</td></tr>
   <tr class="test-variant"><td>[no-other-filter]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[length-active]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Analysis — 8 cas</button></td><td>✅ 8/8</td><td>411ms</td></tr>
   <tr class="test-variant"><td>[intersection-without-criteria]</td><td>✅</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[active-criteria]</td><td>✅</td><td>53ms</td></tr>
   <tr class="test-variant"><td>[missing-msd]</td><td>✅</td><td>47ms</td></tr>
   <tr class="test-variant"><td>[missing-instant-diffusion]</td><td>✅</td><td>45ms</td></tr>
   <tr class="test-variant"><td>[missing-fit]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[overly-restrictive-length]</td><td>✅</td><td>39ms</td></tr>
   <tr class="test-variant"><td>[no-common-tracks]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[filters-disabled]</td><td>✅</td><td>85ms</td></tr>
   </tbody>
   </table>

Processing Gallery
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Make Gallery</td><td>✅</td><td>40ms</td></tr>
   </tbody>
   </table>

Processing Gaussianmixture
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Fit Two Components</td><td>✅</td><td>107ms</td></tr>
   <tr><td>Fit Is Generic</td><td>✅</td><td>115ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Invalid Fit Parameters — 8 cas</button></td><td>✅ 8/8</td><td>183ms</td></tr>
   <tr class="test-variant"><td>[zero-components]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[zero-iterations]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[zero-tolerance]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[zero-initializations]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[empty-data]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[more-components-than-samples]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[constant-data-two-components]</td><td>✅</td><td>12ms</td></tr>
   <tr class="test-variant"><td>[constant-data-one-component]</td><td>✅</td><td>72ms</td></tr>
   <tr><td>Em Iteration Limit</td><td>✅</td><td>17ms</td></tr>
   <tr><td>Component Probability Densities</td><td>✅</td><td>17ms</td></tr>
   <tr><td>Make Curve</td><td>✅</td><td>43ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Invalid Curve Parameters — 4 cas</button></td><td>✅ 4/4</td><td>71ms</td></tr>
   <tr class="test-variant"><td>[insufficient-points]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[missing-bound]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[nan-bound]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[equal-bounds]</td><td>✅</td><td>17ms</td></tr>
   <tr><td>Initialize Centers Fallback</td><td>✅</td><td>18ms</td></tr>
   <tr><td>Kmeans Iteration Limit</td><td>✅</td><td>25ms</td></tr>
   </tbody>
   </table>

Processing Grapher
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Blank</td><td>✅</td><td>135ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Histogram — 7 cas</button></td><td>✅ 7/7</td><td>1.66s</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>209ms</td></tr>
   <tr class="test-variant"><td>[fixed-bins]</td><td>✅</td><td>286ms</td></tr>
   <tr class="test-variant"><td>[integer-values]</td><td>✅</td><td>303ms</td></tr>
   <tr class="test-variant"><td>[two-rows]</td><td>✅</td><td>160ms</td></tr>
   <tr class="test-variant"><td>[two-columns]</td><td>✅</td><td>204ms</td></tr>
   <tr class="test-variant"><td>[flattened-matrix]</td><td>✅</td><td>182ms</td></tr>
   <tr class="test-variant"><td>[flattened-volume]</td><td>✅</td><td>311ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Histogram Curves — 7 cas</button></td><td>✅ 7/7</td><td>2.76s</td></tr>
   <tr class="test-variant"><td>[all-options]</td><td>✅</td><td>1.32s</td></tr>
   <tr class="test-variant"><td>[kde]</td><td>✅</td><td>399ms</td></tr>
   <tr class="test-variant"><td>[gaussian]</td><td>✅</td><td>214ms</td></tr>
   <tr class="test-variant"><td>[gaussian-mixture]</td><td>✅</td><td>261ms</td></tr>
   <tr class="test-variant"><td>[poisson]</td><td>✅</td><td>167ms</td></tr>
   <tr class="test-variant"><td>[exponential]</td><td>✅</td><td>195ms</td></tr>
   <tr class="test-variant"><td>[gaussian-counts]</td><td>✅</td><td>203ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Histogram Fit Limit — 32 cas</button></td><td>✅ 32/32</td><td>4.40s</td></tr>
   <tr class="test-variant"><td>[zero-density-kde]</td><td>✅</td><td>111ms</td></tr>
   <tr class="test-variant"><td>[zero-density-gaussian]</td><td>✅</td><td>156ms</td></tr>
   <tr class="test-variant"><td>[zero-density-poisson]</td><td>✅</td><td>143ms</td></tr>
   <tr class="test-variant"><td>[zero-density-exponential]</td><td>✅</td><td>89ms</td></tr>
   <tr class="test-variant"><td>[zero-counts-kde]</td><td>✅</td><td>167ms</td></tr>
   <tr class="test-variant"><td>[zero-counts-gaussian]</td><td>✅</td><td>111ms</td></tr>
   <tr class="test-variant"><td>[zero-counts-poisson]</td><td>✅</td><td>141ms</td></tr>
   <tr class="test-variant"><td>[zero-counts-exponential]</td><td>✅</td><td>117ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-density-kde]</td><td>✅</td><td>152ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-density-gaussian]</td><td>✅</td><td>116ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-density-poisson]</td><td>✅</td><td>145ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-density-exponential]</td><td>✅</td><td>117ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-counts-kde]</td><td>✅</td><td>164ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-counts-gaussian]</td><td>✅</td><td>78ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-counts-poisson]</td><td>✅</td><td>153ms</td></tr>
   <tr class="test-variant"><td>[zero-cumulative-counts-exponential]</td><td>✅</td><td>123ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-density-kde]</td><td>✅</td><td>162ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-density-gaussian]</td><td>✅</td><td>155ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-density-poisson]</td><td>✅</td><td>122ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-density-exponential]</td><td>✅</td><td>168ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-counts-kde]</td><td>✅</td><td>133ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-counts-gaussian]</td><td>✅</td><td>166ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-counts-poisson]</td><td>✅</td><td>149ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-counts-exponential]</td><td>✅</td><td>110ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-density-kde]</td><td>✅</td><td>167ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-density-gaussian]</td><td>✅</td><td>120ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-density-poisson]</td><td>✅</td><td>158ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-density-exponential]</td><td>✅</td><td>112ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-counts-kde]</td><td>✅</td><td>141ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-counts-gaussian]</td><td>✅</td><td>165ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-counts-poisson]</td><td>✅</td><td>133ms</td></tr>
   <tr class="test-variant"><td>[diffusion-floor-cumulative-counts-exponential]</td><td>✅</td><td>159ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Histogram Fit Limit Without Distribution — 3 cas</button></td><td>✅ 3/3</td><td>423ms</td></tr>
   <tr class="test-variant"><td>[all-excluded]</td><td>✅</td><td>160ms</td></tr>
   <tr class="test-variant"><td>[one-admissible-value]</td><td>✅</td><td>106ms</td></tr>
   <tr class="test-variant"><td>[constant-admissible-values]</td><td>✅</td><td>156ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Histogram Gaussian Mixture Components — 4 cas</button></td><td>✅ 4/4</td><td>1.13s</td></tr>
   <tr class="test-variant"><td>[all-values-density]</td><td>✅</td><td>162ms</td></tr>
   <tr class="test-variant"><td>[all-values-cumulative]</td><td>✅</td><td>207ms</td></tr>
   <tr class="test-variant"><td>[positive-values-density]</td><td>✅</td><td>403ms</td></tr>
   <tr class="test-variant"><td>[positive-values-cumulative]</td><td>✅</td><td>355ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Scatter — 6 cas</button></td><td>✅ 6/6</td><td>1.42s</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>173ms</td></tr>
   <tr class="test-variant"><td>[no-valid-points]</td><td>✅</td><td>182ms</td></tr>
   <tr class="test-variant"><td>[1d-data]</td><td>✅</td><td>235ms</td></tr>
   <tr class="test-variant"><td>[two-rows]</td><td>✅</td><td>173ms</td></tr>
   <tr class="test-variant"><td>[two-columns-with-limits]</td><td>✅</td><td>213ms</td></tr>
   <tr class="test-variant"><td>[mean-and-sigma]</td><td>✅</td><td>448ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Scatter Multiple Curves — 2 cas</button></td><td>✅ 2/2</td><td>277ms</td></tr>
   <tr class="test-variant"><td>[default-names]</td><td>✅</td><td>156ms</td></tr>
   <tr class="test-variant"><td>[explicit-names]</td><td>✅</td><td>122ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Scatter Invalid — 4 cas</button></td><td>✅ 4/4</td><td>72ms</td></tr>
   <tr class="test-variant"><td>[invalid-matrix]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[3d-volume]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[missing-curve-name]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[extra-curve-name]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cloud — 6 cas</button></td><td>✅ 6/6</td><td>1.85s</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>134ms</td></tr>
   <tr class="test-variant"><td>[infinite-values]</td><td>✅</td><td>187ms</td></tr>
   <tr class="test-variant"><td>[two-rows]</td><td>✅</td><td>210ms</td></tr>
   <tr class="test-variant"><td>[two-columns-with-limits]</td><td>✅</td><td>188ms</td></tr>
   <tr class="test-variant"><td>[mean-and-sigma]</td><td>✅</td><td>923ms</td></tr>
   <tr class="test-variant"><td>[constant-data]</td><td>✅</td><td>208ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cloud Curves — 4 cas</button></td><td>✅ 4/4</td><td>1.45s</td></tr>
   <tr class="test-variant"><td>[kde]</td><td>✅</td><td>789ms</td></tr>
   <tr class="test-variant"><td>[gaussian]</td><td>✅</td><td>232ms</td></tr>
   <tr class="test-variant"><td>[poisson]</td><td>✅</td><td>214ms</td></tr>
   <tr class="test-variant"><td>[exponential]</td><td>✅</td><td>212ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cloud Invalid — 3 cas</button></td><td>✅ 3/3</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[1d-data]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[invalid-matrix]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[3d-volume]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism3D — 6 cas</button></td><td>✅ 6/6</td><td>1.33s</td></tr>
   <tr class="test-variant"><td>[curve]</td><td>✅</td><td>222ms</td></tr>
   <tr class="test-variant"><td>[cross-without-points]</td><td>✅</td><td>228ms</td></tr>
   <tr class="test-variant"><td>[cross-with-points]</td><td>✅</td><td>260ms</td></tr>
   <tr class="test-variant"><td>[slope-without-points]</td><td>✅</td><td>201ms</td></tr>
   <tr class="test-variant"><td>[slope-with-points]</td><td>✅</td><td>294ms</td></tr>
   <tr class="test-variant"><td>[unknown-mode]</td><td>✅</td><td>127ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism3D Invalid — 1 cas</button></td><td>✅ 1/1</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[invalid-model]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism3D Filters Z Limits — 4 cas</button></td><td>✅ 4/4</td><td>1.46s</td></tr>
   <tr class="test-variant"><td>[small-range-cross]</td><td>✅</td><td>222ms</td></tr>
   <tr class="test-variant"><td>[small-range-slope]</td><td>✅</td><td>137ms</td></tr>
   <tr class="test-variant"><td>[large-range-cross]</td><td>✅</td><td>947ms</td></tr>
   <tr class="test-variant"><td>[large-range-slope]</td><td>✅</td><td>153ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism3D Without Valid Points — 4 cas</button></td><td>✅ 4/4</td><td>598ms</td></tr>
   <tr class="test-variant"><td>[empty-data-cross]</td><td>✅</td><td>198ms</td></tr>
   <tr class="test-variant"><td>[empty-data-slope]</td><td>✅</td><td>95ms</td></tr>
   <tr class="test-variant"><td>[all-excluded-cross]</td><td>✅</td><td>193ms</td></tr>
   <tr class="test-variant"><td>[all-excluded-slope]</td><td>✅</td><td>112ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism3D Cross Guides — 4 cas</button></td><td>✅ 4/4</td><td>744ms</td></tr>
   <tr class="test-variant"><td>[separated-minima]</td><td>✅</td><td>177ms</td></tr>
   <tr class="test-variant"><td>[reversed-axes]</td><td>✅</td><td>178ms</td></tr>
   <tr class="test-variant"><td>[coincident-minima]</td><td>✅</td><td>171ms</td></tr>
   <tr class="test-variant"><td>[asymmetric-minima]</td><td>✅</td><td>218ms</td></tr>
   <tr><td>Histogram Poisson Distribution</td><td>✅</td><td>164ms</td></tr>
   <tr><td>Histogram Exponential Distribution</td><td>✅</td><td>226ms</td></tr>
   <tr><td>Histogram Gaussian Mixture Distribution</td><td>✅</td><td>370ms</td></tr>
   </tbody>
   </table>

Processing Palm
^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Palm Dll Valid</td><td>✅</td><td>16ms</td></tr>
   <tr><td>Palm Cpu Empty Result</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Palm Cpu Image — 60 cas</button></td><td>✅ 60/60</td><td>5.30s</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-1]</td><td>✅</td><td>238ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-2]</td><td>✅</td><td>41ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-3]</td><td>✅</td><td>42ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-4]</td><td>✅</td><td>45ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-5]</td><td>✅</td><td>80ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-6]</td><td>✅</td><td>42ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-7]</td><td>✅</td><td>41ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-8]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-9]</td><td>✅</td><td>84ms</td></tr>
   <tr class="test-variant"><td>[no-fit-plane-10]</td><td>✅</td><td>43ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-1]</td><td>✅</td><td>239ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-2]</td><td>✅</td><td>51ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-3]</td><td>✅</td><td>54ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-4]</td><td>✅</td><td>106ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-5]</td><td>✅</td><td>53ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-6]</td><td>✅</td><td>53ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-7]</td><td>✅</td><td>51ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-8]</td><td>✅</td><td>101ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-9]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-plane-10]</td><td>✅</td><td>52ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-1]</td><td>✅</td><td>261ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-2]</td><td>✅</td><td>90ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-3]</td><td>✅</td><td>61ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-4]</td><td>✅</td><td>60ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-5]</td><td>✅</td><td>116ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-6]</td><td>✅</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-7]</td><td>✅</td><td>64ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-8]</td><td>✅</td><td>53ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-9]</td><td>✅</td><td>66ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-plane-10]</td><td>✅</td><td>53ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-1]</td><td>✅</td><td>245ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-2]</td><td>✅</td><td>75ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-3]</td><td>✅</td><td>57ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-4]</td><td>✅</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-5]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-6]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-7]</td><td>✅</td><td>73ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-8]</td><td>✅</td><td>94ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-9]</td><td>✅</td><td>69ms</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-plane-10]</td><td>✅</td><td>69ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-1]</td><td>✅</td><td>375ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-2]</td><td>✅</td><td>128ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-3]</td><td>✅</td><td>101ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-4]</td><td>✅</td><td>100ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-5]</td><td>✅</td><td>121ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-6]</td><td>✅</td><td>127ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-7]</td><td>✅</td><td>113ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-8]</td><td>✅</td><td>83ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-9]</td><td>✅</td><td>137ms</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-plane-10]</td><td>✅</td><td>91ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-1]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-2]</td><td>✅</td><td>93ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-3]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-4]</td><td>✅</td><td>57ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-5]</td><td>✅</td><td>60ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-6]</td><td>✅</td><td>58ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-7]</td><td>✅</td><td>64ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-8]</td><td>✅</td><td>61ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-9]</td><td>✅</td><td>88ms</td></tr>
   <tr class="test-variant"><td>[spline-plane-10]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Palm Cpu Stack — 12 cas</button></td><td>✅ 12/12</td><td>17.53s</td></tr>
   <tr class="test-variant"><td>[no-fit-with-watershed]</td><td>✅</td><td>1.77s</td></tr>
   <tr class="test-variant"><td>[no-fit-no-watershed]</td><td>✅</td><td>1.49s</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-with-watershed]</td><td>✅</td><td>1.44s</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-no-watershed]</td><td>✅</td><td>2.37s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-with-watershed]</td><td>✅</td><td>1.66s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-no-watershed]</td><td>✅</td><td>1.73s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-with-watershed]</td><td>✅</td><td>1.73s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-no-watershed]</td><td>✅</td><td>1.74s</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-with-watershed]</td><td>✅</td><td>1.76s</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-no-watershed]</td><td>✅</td><td>1.63s</td></tr>
   <tr class="test-variant"><td>[spline-with-watershed]</td><td>✅</td><td>123ms</td></tr>
   <tr class="test-variant"><td>[spline-no-watershed]</td><td>✅</td><td>81ms</td></tr>
   <tr><td>Palm Cpu Stack Plane Selection</td><td>✅</td><td>957ms</td></tr>
   <tr><td>Palm Cpu Stack Dll Check Quadrant</td><td>✅</td><td>1.30s</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cpu Auto Threshold — 10 cas</button></td><td>✅ 10/10</td><td>550ms</td></tr>
   <tr class="test-variant"><td>[plane-1]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[plane-2]</td><td>✅</td><td>57ms</td></tr>
   <tr class="test-variant"><td>[plane-3]</td><td>✅</td><td>95ms</td></tr>
   <tr class="test-variant"><td>[plane-4]</td><td>✅</td><td>49ms</td></tr>
   <tr class="test-variant"><td>[plane-5]</td><td>✅</td><td>44ms</td></tr>
   <tr class="test-variant"><td>[plane-6]</td><td>✅</td><td>39ms</td></tr>
   <tr class="test-variant"><td>[plane-7]</td><td>✅</td><td>118ms</td></tr>
   <tr class="test-variant"><td>[plane-8]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-variant"><td>[plane-9]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[plane-10]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking — 12 cas</button></td><td>✅ 12/12</td><td>55.77s</td></tr>
   <tr class="test-variant"><td>[no-fit-with-watershed]</td><td>✅</td><td>6.84s</td></tr>
   <tr class="test-variant"><td>[no-fit-no-watershed]</td><td>✅</td><td>5.28s</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-with-watershed]</td><td>✅</td><td>6.53s</td></tr>
   <tr class="test-variant"><td>[gaussian-xy-no-watershed]</td><td>✅</td><td>5.57s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-with-watershed]</td><td>✅</td><td>5.64s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-no-watershed]</td><td>✅</td><td>6.45s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-with-watershed]</td><td>✅</td><td>6.40s</td></tr>
   <tr class="test-variant"><td>[gaussian-sigma-xy-no-watershed]</td><td>✅</td><td>5.86s</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-with-watershed]</td><td>✅</td><td>5.39s</td></tr>
   <tr class="test-variant"><td>[gaussian-theta-no-watershed]</td><td>✅</td><td>1.79s</td></tr>
   <tr class="test-variant"><td>[spline-with-watershed]</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-variant"><td>[spline-no-watershed]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracking Empty — 2 cas</button></td><td>✅ 2/2</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[zero-localizations]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[empty-data]</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Tracking Discontinuous</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Blinking Reconnection — 3 cas</button></td><td>✅ 3/3</td><td>316ms</td></tr>
   <tr class="test-variant"><td>[stationary]</td><td>✅</td><td>101ms</td></tr>
   <tr class="test-variant"><td>[diffusion]</td><td>✅</td><td>83ms</td></tr>
   <tr class="test-variant"><td>[linear]</td><td>✅</td><td>132ms</td></tr>
   <tr><td>Blinking Reconnection Empty</td><td>✅</td><td>13ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Analysis — 2 cas</button></td><td>✅ 2/2</td><td>116ms</td></tr>
   <tr class="test-variant"><td>[ind-3d-enabled]</td><td>✅</td><td>61ms</td></tr>
   <tr class="test-variant"><td>[ind-3d-disabled]</td><td>✅</td><td>56ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Analysis Fit Modes — 4 cas</button></td><td>✅ 4/4</td><td>179ms</td></tr>
   <tr class="test-variant"><td>[no-fit]</td><td>✅</td><td>58ms</td></tr>
   <tr class="test-variant"><td>[linear]</td><td>✅</td><td>40ms</td></tr>
   <tr class="test-variant"><td>[power]</td><td>✅</td><td>41ms</td></tr>
   <tr class="test-variant"><td>[exponential]</td><td>✅</td><td>41ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Analysis Small Inputs — 3 cas</button></td><td>✅ 3/3</td><td>140ms</td></tr>
   <tr class="test-variant"><td>[diffusion-without-msd]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-variant"><td>[single-observation]</td><td>✅</td><td>78ms</td></tr>
   <tr class="test-variant"><td>[no-observations]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Align — 3 cas</button></td><td>✅ 3/3</td><td>1.48s</td></tr>
   <tr class="test-variant"><td>[identity]</td><td>✅</td><td>376ms</td></tr>
   <tr class="test-variant"><td>[upsampling]</td><td>✅</td><td>928ms</td></tr>
   <tr class="test-variant"><td>[transposition]</td><td>✅</td><td>179ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Wavelet — 5 cas</button></td><td>✅ 5/5</td><td>259ms</td></tr>
   <tr class="test-variant"><td>[level-0]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[level-1]</td><td>✅</td><td>43ms</td></tr>
   <tr class="test-variant"><td>[level-2]</td><td>✅</td><td>86ms</td></tr>
   <tr class="test-variant"><td>[level-3]</td><td>✅</td><td>44ms</td></tr>
   <tr class="test-variant"><td>[level-4]</td><td>✅</td><td>38ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Astigmatism 3D Calibration — 2 cas</button></td><td>✅ 2/2</td><td>71ms</td></tr>
   <tr class="test-variant"><td>[no-centering]</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-variant"><td>[centered-model]</td><td>✅</td><td>36ms</td></tr>
   <tr><td>Astigmatism 3D Estimation</td><td>✅</td><td>74ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [no-fit-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-0_103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-xy-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-0_103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-sigma-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-0_103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-sigma-xy-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-0_103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Image [gaussian-theta-plane-1]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-0_103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 51 Points comparés, 51 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [no-fit-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_True_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [no-fit-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_False_0_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_True_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_False_1_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_True_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_False_2_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_True_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-sigma-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_False_3_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-theta-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack [gaussian-theta-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_False_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack Plane Selection</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-plane_select-103.6_True_4_1.0_0.0_7.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 227 Points comparés, 227 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Palm Cpu Stack Dll Check Quadrant</summary>
      <pre><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 269 Points comparés, 269 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [no-fit-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_True_0_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [no-fit-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_False_0_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_True_1_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_False_1_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 429 Points comparés, 429 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_True_2_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_False_2_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 426 Points comparés, 426 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-xy-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_True_3_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 451 Points comparés, 451 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-sigma-xy-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_False_3_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 428 Points comparés, 428 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-theta-with-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_True_4_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 435 Points comparés, 435 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [gaussian-theta-no-watershed]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\stack-tracking-103.6_False_4_1.0_0.0_7-5.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 416 Points comparés, 416 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [spline-with-watershed]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_True_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Tracking [spline-no-watershed]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Fichier de localisations 'C:\Git\palm-tracer\tests\input\ref\stack-localizations-103.6_False_5_1.0_0.0_7.csv' indisponible.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection [stationary]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking-blinking-0.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection [diffusion]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking-blinking-1.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Blinking Reconnection [linear]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking-blinking-2.csv'<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Comparaison terminée : 18 Points comparés, 18 Points identiques (100.00%)</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Track Analysis [ind-3d-enabled]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking2-MSD-True.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking2-Fit-True.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Track Analysis [ind-3d-disabled]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking2-MSD-False.csv'<br>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking2-Fit-False.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Track Analysis Fit Modes [linear]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking2-Fit-1.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Track Analysis Fit Modes [power]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking2-Fit-2.csv'</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Track Analysis Fit Modes [exponential]</summary>
      <pre>Comparaison avec : 'C:\Git\palm-tracer\tests\input\ref\tracking2-Fit-3.csv'</pre>
   </details>

Processing Parsing
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Rearrange Dataframe Columns — 2 cas</button></td><td>✅ 2/2</td><td>50ms</td></tr>
   <tr class="test-variant"><td>[other-columns-preserved]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[selection-only]</td><td>✅</td><td>26ms</td></tr>
   <tr><td>Rearrange Dataframe Columns Missing</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Log10 Dataframe</td><td>✅</td><td>27ms</td></tr>
   <tr><td>Degrees To Radians</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Radians To Degrees</td><td>✅</td><td>61ms</td></tr>
   <tr><td>Wrap Angle</td><td>✅</td><td>22ms</td></tr>
   <tr><td>Manage Theta</td><td>✅</td><td>19ms</td></tr>
   <tr><td>Get Meta</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Get Meta Invalid</td><td>✅</td><td>18ms</td></tr>
   <tr><td>Parse Irregular Array</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Irregular Array Invalid — 3 cas</button></td><td>✅ 3/3</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[2d-array]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[non-numeric-data]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[truncated-row]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Irregular Array Empty — 2 cas</button></td><td>✅ 2/2</td><td>79ms</td></tr>
   <tr class="test-variant"><td>[empty-array]</td><td>✅</td><td>60ms</td></tr>
   <tr class="test-variant"><td>[empty-row]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Result — 8 cas</button></td><td>✅ 8/8</td><td>219ms</td></tr>
   <tr class="test-variant"><td>[localizations]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[tracks]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[astigmatism-model]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[msd]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[instant-diffusion]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[linear-fit]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[power-fit]</td><td>✅</td><td>61ms</td></tr>
   <tr class="test-variant"><td>[exponential-fit]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Result Empty — 3 cas</button></td><td>✅ 3/3</td><td>69ms</td></tr>
   <tr class="test-variant"><td>[localizations]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[tracks]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[fit]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Parse Result Invalid — 2 cas</button></td><td>✅ 2/2</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[invalid-fit]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[unknown-type]</td><td>✅</td><td>13ms</td></tr>
   </tbody>
   </table>

Processing Renderer
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Set Size</td><td>✅</td><td>14ms</td></tr>
   <tr><td>Localizations</td><td>✅</td><td>56ms</td></tr>
   <tr><td>Localizations Gaussian</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Tracks</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tracks Crossing — 3 cas</button></td><td>✅ 3/3</td><td>47ms</td></tr>
   <tr class="test-variant"><td>[addition]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>15ms</td></tr>
   <tr><td>Z Stack</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Z Stack Gaussian</td><td>✅</td><td>30ms</td></tr>
   <tr><td>Rotation</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Rotation Data Crop — 12 cas</button></td><td>✅ 12/12</td><td>3.31s</td></tr>
   <tr class="test-variant"><td>[spots-x]</td><td>✅</td><td>192ms</td></tr>
   <tr class="test-variant"><td>[spots-y]</td><td>✅</td><td>194ms</td></tr>
   <tr class="test-variant"><td>[spots-z]</td><td>✅</td><td>1.08s</td></tr>
   <tr class="test-variant"><td>[fixed-x]</td><td>✅</td><td>239ms</td></tr>
   <tr class="test-variant"><td>[fixed-y]</td><td>✅</td><td>169ms</td></tr>
   <tr class="test-variant"><td>[fixed-z]</td><td>✅</td><td>176ms</td></tr>
   <tr class="test-variant"><td>[isotropic-x]</td><td>✅</td><td>227ms</td></tr>
   <tr class="test-variant"><td>[isotropic-y]</td><td>✅</td><td>228ms</td></tr>
   <tr class="test-variant"><td>[isotropic-z]</td><td>✅</td><td>197ms</td></tr>
   <tr class="test-variant"><td>[anisotropic-x]</td><td>✅</td><td>179ms</td></tr>
   <tr class="test-variant"><td>[anisotropic-y]</td><td>✅</td><td>220ms</td></tr>
   <tr class="test-variant"><td>[anisotropic-z]</td><td>✅</td><td>208ms</td></tr>
   <tr><td>Rotation Gaussian</td><td>✅</td><td>26ms</td></tr>
   <tr><td>Track Stack Timeline</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Track Stack Crossing Bounds</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Empty And Scale — 4 cas</button></td><td>✅ 4/4</td><td>149ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[1d-array]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[missing-column]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[out-of-bounds]</td><td>✅</td><td>72ms</td></tr>
   <tr><td>Track Stack Scale</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Priority And Modes — 3 cas</button></td><td>✅ 3/3</td><td>60ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Track Stack Head Priority</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Raw — 4 cas</button></td><td>✅ 4/4</td><td>251ms</td></tr>
   <tr class="test-variant"><td>[maximum-nearest-neighbor]</td><td>✅</td><td>51ms</td></tr>
   <tr class="test-variant"><td>[maximum-lanczos]</td><td>✅</td><td>84ms</td></tr>
   <tr class="test-variant"><td>[minimum-nearest-neighbor]</td><td>✅</td><td>60ms</td></tr>
   <tr class="test-variant"><td>[minimum-lanczos]</td><td>✅</td><td>57ms</td></tr>
   <tr><td>Track Stack Raw Empty And 2D</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Track Stack Raw Fade And Overlap — 3 cas</button></td><td>✅ 3/3</td><td>152ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>76ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Init Rendering — 3 cas</button></td><td>✅ 3/3</td><td>56ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>19ms</td></tr>
   <tr><td>Init Rendering Volume</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Finalize Rendering</td><td>✅</td><td>54ms</td></tr>
   <tr><td>Finalize Track Stack</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Empty Background — 12 cas</button></td><td>✅ 12/12</td><td>318ms</td></tr>
   <tr class="test-variant"><td>[black-zero-background]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[black-negative-infinite-background]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[black-positive-infinite-background]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[gray-zero-background]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[gray-negative-infinite-background]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[gray-positive-infinite-background]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[lower-clipping-zero-background]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[lower-clipping-negative-infinite-background]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[lower-clipping-positive-infinite-background]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[upper-clipping-zero-background]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[upper-clipping-negative-infinite-background]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[upper-clipping-positive-infinite-background]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Empty Dimensions — 3 cas</button></td><td>✅ 3/3</td><td>111ms</td></tr>
   <tr class="test-variant"><td>[no-planes]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[no-rows]</td><td>✅</td><td>64ms</td></tr>
   <tr class="test-variant"><td>[no-columns]</td><td>✅</td><td>24ms</td></tr>
   <tr><td>Finalize Track Stack Strided</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Drawing — 3 cas</button></td><td>✅ 3/3</td><td>72ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>24ms</td></tr>
   <tr><td>Finalize Track Stack Remainder</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Background Remainder — 3 cas</button></td><td>✅ 3/3</td><td>110ms</td></tr>
   <tr class="test-variant"><td>[negative-background]</td><td>✅</td><td>65ms</td></tr>
   <tr class="test-variant"><td>[one-wrap]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[two-wraps]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Rgb — 2 cas</button></td><td>✅ 2/2</td><td>96ms</td></tr>
   <tr class="test-variant"><td>[viridis]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[magma]</td><td>✅</td><td>47ms</td></tr>
   <tr><td>Finalize Track Stack Rgb Rejects Short Lut</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Finalize Track Stack Rgb Global Contrast — 2 cas</button></td><td>✅ 2/2</td><td>156ms</td></tr>
   <tr class="test-variant"><td>[black]</td><td>✅</td><td>95ms</td></tr>
   <tr class="test-variant"><td>[gray]</td><td>✅</td><td>61ms</td></tr>
   <tr><td>Upscale Raw</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Upscale Raw Lanczos</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Upscale Raw Edge Cases — 2 cas</button></td><td>✅ 2/2</td><td>85ms</td></tr>
   <tr class="test-variant"><td>[nearest-neighbor]</td><td>✅</td><td>64ms</td></tr>
   <tr class="test-variant"><td>[lanczos]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Upscale Raw 2D — 4 cas</button></td><td>✅ 4/4</td><td>85ms</td></tr>
   <tr class="test-variant"><td>[nearest-neighbor-ratio-1]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[nearest-neighbor-ratio-2]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[lanczos-ratio-1]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[lanczos-ratio-2]</td><td>✅</td><td>23ms</td></tr>
   <tr><td>Get Localization Colors</td><td>✅</td><td>32ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Localization Z Colors — 3 cas</button></td><td>✅ 3/3</td><td>106ms</td></tr>
   <tr class="test-variant"><td>[mixed-sign]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[positive]</td><td>✅</td><td>61ms</td></tr>
   <tr class="test-variant"><td>[negative]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Localization Constant Z Colors — 3 cas</button></td><td>✅ 3/3</td><td>66ms</td></tr>
   <tr class="test-variant"><td>[negative]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[zero]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[positive]</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Get Tracks Colors</td><td>✅</td><td>143ms</td></tr>
   <tr><td>Prepare Localizations</td><td>✅</td><td>22ms</td></tr>
   <tr><td>Prepare Tracks</td><td>✅</td><td>19ms</td></tr>
   <tr><td>Prepare Tracks Empty</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Line Spans — 16 cas</button></td><td>✅ 16/16</td><td>385ms</td></tr>
   <tr class="test-variant"><td>[forward-horizontal]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[forward-vertical]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[forward-descending-diagonal]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[forward-ascending-diagonal]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[forward-line-width-3]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[forward-line-width-2]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[forward-point-width-3]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[forward-point-width-4]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[reverse-horizontal]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[reverse-vertical]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[reverse-descending-diagonal]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[reverse-ascending-diagonal]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[reverse-line-width-3]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[reverse-line-width-2]</td><td>✅</td><td>57ms</td></tr>
   <tr class="test-variant"><td>[reverse-point-width-3]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[reverse-point-width-4]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Line Spans Empty — 5 cas</button></td><td>✅ 5/5</td><td>91ms</td></tr>
   <tr class="test-variant"><td>[zero-height]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[zero-width]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[negative-coordinates]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[outside-right]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[outside-corner]</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Line Spans Clipping</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Line Spans Width Clamping — 3 cas</button></td><td>✅ 3/3</td><td>86ms</td></tr>
   <tr class="test-variant"><td>[negative-width]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-variant"><td>[zero-width]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[unit-width]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Line Spans Orientations — 32 cas</button></td><td>✅ 32/32</td><td>792ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-down-original-axes]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-down-swapped-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-up-original-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-1-right-up-swapped-axes]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-down-original-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-down-swapped-axes]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-up-original-axes]</td><td>✅</td><td>56ms</td></tr>
   <tr class="test-variant"><td>[width-1-left-up-swapped-axes]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-down-original-axes]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-down-swapped-axes]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-up-original-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-2-right-up-swapped-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-down-original-axes]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-down-swapped-axes]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-up-original-axes]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[width-2-left-up-swapped-axes]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-down-original-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-down-swapped-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-up-original-axes]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-3-right-up-swapped-axes]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-down-original-axes]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-down-swapped-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-up-original-axes]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[width-3-left-up-swapped-axes]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-down-original-axes]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-down-swapped-axes]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-up-original-axes]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4-right-up-swapped-axes]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-down-original-axes]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-down-swapped-axes]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-up-original-axes]</td><td>✅</td><td>62ms</td></tr>
   <tr class="test-variant"><td>[width-4-left-up-swapped-axes]</td><td>✅</td><td>24ms</td></tr>
   <tr><td>Draw Line</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Crossing — 3 cas</button></td><td>✅ 3/3</td><td>65ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Width — 12 cas</button></td><td>✅ 12/12</td><td>372ms</td></tr>
   <tr class="test-variant"><td>[sum-width-1]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[sum-width-2]</td><td>✅</td><td>74ms</td></tr>
   <tr class="test-variant"><td>[sum-width-3]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[sum-width-4]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-1]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-2]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-3]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-4]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-1]</td><td>✅</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-2]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-3]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-4]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Point Width — 4 cas</button></td><td>✅ 4/4</td><td>137ms</td></tr>
   <tr class="test-variant"><td>[width-1]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-2]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-3]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4]</td><td>✅</td><td>67ms</td></tr>
   <tr><td>Draw Line Width Border</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Width Orientations — 42 cas</button></td><td>✅ 42/42</td><td>1.17s</td></tr>
   <tr class="test-variant"><td>[width-2-forward-diagonal]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-shallow-slope]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-steep-slope]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-left]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-up]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-vertical]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-2-forward-horizontal]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-diagonal]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-shallow-slope]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-steep-slope]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-left]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-up]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-vertical]</td><td>✅</td><td>64ms</td></tr>
   <tr class="test-variant"><td>[width-2-reverse-horizontal]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-diagonal]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-shallow-slope]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-steep-slope]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-left]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-up]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-vertical]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[width-3-forward-horizontal]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-diagonal]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-shallow-slope]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-steep-slope]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-left]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-up]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-vertical]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[width-3-reverse-horizontal]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-diagonal]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-shallow-slope]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-steep-slope]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-left]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-up]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-vertical]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[width-4-forward-horizontal]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-diagonal]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-shallow-slope]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-steep-slope]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-left]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-up]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-vertical]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4-reverse-horizontal]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Alpha — 10 cas</button></td><td>✅ 10/10</td><td>288ms</td></tr>
   <tr class="test-variant"><td>[sum-width-1]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[sum-width-3]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[maximum-higher-value-width-1]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[maximum-higher-value-width-3]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[maximum-lower-value-width-1]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[maximum-lower-value-width-3]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[minimum-higher-value-width-1]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[minimum-higher-value-width-3]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[minimum-lower-value-width-1]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[minimum-lower-value-width-3]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Alpha Initial Background — 6 cas</button></td><td>✅ 6/6</td><td>176ms</td></tr>
   <tr class="test-variant"><td>[sum-width-1]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[sum-width-3]</td><td>✅</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-1]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[maximum-width-3]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-1]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[minimum-width-3]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Clamped Parameters — 9 cas</button></td><td>✅ 9/9</td><td>235ms</td></tr>
   <tr class="test-variant"><td>[negative-alpha-negative-width]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[negative-alpha-zero-width]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[negative-alpha-width-1]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[partial-alpha-negative-width]</td><td>✅</td><td>65ms</td></tr>
   <tr class="test-variant"><td>[partial-alpha-zero-width]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[partial-alpha-width-1]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[alpha-above-one-negative-width]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[alpha-above-one-zero-width]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[alpha-above-one-width-1]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Line Width Finalize — 9 cas</button></td><td>✅ 9/9</td><td>254ms</td></tr>
   <tr class="test-variant"><td>[width-2-sum]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-2-maximum]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[width-2-minimum]</td><td>✅</td><td>66ms</td></tr>
   <tr class="test-variant"><td>[width-3-sum]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[width-3-maximum]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[width-3-minimum]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4-sum]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[width-4-maximum]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[width-4-minimum]</td><td>✅</td><td>27ms</td></tr>
   <tr><td>Draw Line Thick Empty Rows</td><td>✅</td><td>22ms</td></tr>
   <tr><td>Draw Gaussian</td><td>✅</td><td>28ms</td></tr>
   <tr><td>Draw Gaussian 3D</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Gaussian Overlap — 6 cas</button></td><td>✅ 6/6</td><td>182ms</td></tr>
   <tr class="test-variant"><td>[addition-2d]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[addition-3d]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[maximum-2d]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[maximum-3d]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[minimum-2d]</td><td>✅</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[minimum-3d]</td><td>✅</td><td>16ms</td></tr>
   <tr><td>Draw Track Blinks</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Draw Track Empty Rows</td><td>✅</td><td>21ms</td></tr>
   <tr><td>Draw Track Short Fade Long Blink</td><td>✅</td><td>21ms</td></tr>
   <tr><td>Draw Track Hard Cutoff</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Overlap — 3 cas</button></td><td>✅ 3/3</td><td>64ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Thickness — 3 cas</button></td><td>✅ 3/3</td><td>118ms</td></tr>
   <tr class="test-variant"><td>[sum]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[maximum]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[minimum]</td><td>✅</td><td>24ms</td></tr>
   <tr><td>Draw Track Stationary</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Without Drawing — 6 cas</button></td><td>✅ 6/6</td><td>185ms</td></tr>
   <tr class="test-variant"><td>[empty-track]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[single-point]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[after-volume]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[before-volume]</td><td>✅</td><td>68ms</td></tr>
   <tr class="test-variant"><td>[outside-image]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[disabled-tail]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Alpha Independent Of Geometry — 6 cas</button></td><td>✅ 6/6</td><td>198ms</td></tr>
   <tr class="test-variant"><td>[stationary-departure-0]</td><td>✅</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[stationary-departure-9]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[horizontal-departure-0]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[horizontal-departure-9]</td><td>✅</td><td>27ms</td></tr>
   <tr class="test-variant"><td>[diagonal-departure-0]</td><td>✅</td><td>69ms</td></tr>
   <tr class="test-variant"><td>[diagonal-departure-9]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Heads Planes — 3 cas</button></td><td>✅ 3/3</td><td>78ms</td></tr>
   <tr class="test-variant"><td>[negative-diameter]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[zero-diameter]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[diameter-1]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Heads Circles — 3 cas</button></td><td>✅ 3/3</td><td>90ms</td></tr>
   <tr class="test-variant"><td>[diameter-2]</td><td>✅</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[diameter-4]</td><td>✅</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[diameter-5]</td><td>✅</td><td>37ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Draw Track Heads Clipping — 2 cas</button></td><td>✅ 2/2</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[empty-track]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[outside-volume]</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Draw Track Heads Priority</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Draw Track Heads Preserve Interior</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Renderer Track Crossing Roi Diamond</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Renderer Atom</td><td>✅</td><td>3.86s</td></tr>
   <tr><td>Renderer Track Stack Spiral</td><td>✅</td><td>265ms</td></tr>
   <tr><td>Renderer Track Stack Spiral Raw</td><td>✅</td><td>2.70s</td></tr>
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
   <tr class="test-group"><td><button type="button" aria-expanded="true">Filter Aliases — 2 cas</button></td><td>✅ 2/2</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[single-dataframe]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[track-analysis]</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Object Creation</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Prepare Action — 9 cas</button></td><td>✅ 9/9</td><td>62ms</td></tr>
   <tr class="test-variant"><td>[inactive-without-previous]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[active-without-previous]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[dirty-pipeline]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[inactive-with-dirty-pipeline]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[reactivation-through-reuse]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[both-groups-inactive]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[activation-without-previous-result]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[identical-parameters]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[different-parameters]</td><td>✅</td><td>16ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Object Creation</summary>
      <pre>Step : Step(group_name='name', keys=['key'], process_func=&lt;function test_object_creation.&lt;locals&gt;.f at 0x0000024C5F5012D0&gt;, filter_func=&lt;function test_object_creation.&lt;locals&gt;.f at 0x0000024C5F5012D0&gt;, allow_dirty=False, apply_filter=True)<br>Actions : StepAction.Compute,StepAction.Reuse,StepAction.Skip</pre>
   </details>

Results
^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Accessors</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Load</td><td>✅</td><td>33ms</td></tr>
   <tr><td>Reset</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Name Normalization — 3 cas</button></td><td>✅ 3/3</td><td>83ms</td></tr>
   <tr class="test-variant"><td>[tiff-file]</td><td>✅</td><td>57ms</td></tr>
   <tr class="test-variant"><td>[multiple-suffixes]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>18ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Name Results Folder — 2 cas</button></td><td>✅ 2/2</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[same-stack-path]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[same-name-different-folder]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Active Results</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Status</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Dataframe Status — 5 cas</button></td><td>✅ 5/5</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[no-tracks]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[original-tracks-only]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[all-tracks-preserved]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[partially-filtered-tracks]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[reconnected-filtered-tracks]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Dataframe Status Counts Unique Tracks</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Save</td><td>✅</td><td>35ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Results Folder Unavailable — 2 cas</button></td><td>✅ 2/2</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[unset-folder]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing-folder]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Results Folder Button — 3 cas</button></td><td>✅ 3/3</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[existing-folder]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[missing-folder]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[unset-folder]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Clear Button — 7 cas</button></td><td>✅ 7/7</td><td>70ms</td></tr>
   <tr class="test-variant"><td>[localizations]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[beads]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[tracks]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[reconnected-tracks]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[msd]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[instant-diffusion]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[msd-fit]</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Interfaces</td><td>✅</td><td>9ms</td></tr>
   </tbody>
   </table>

Settings Groups
^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Group Contract — 13 cas</button></td><td>✅ 13/13</td><td>102ms</td></tr>
   <tr class="test-variant"><td>[calibration]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[gaussian-fit]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[spline-fit]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[beads]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[tracking]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[blinking]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[track-analysis]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gallery]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[graph-display]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[hr-gaussian]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[hr-3d]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[hr-track-stack]</td><td>✅</td><td>13ms</td></tr>
   <tr class="test-variant"><td>[visualization-3d]</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Base Group</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Base Group Tostring Range — 4 cas</button></td><td>✅ 4/4</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[inactive-float-range]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[inactive-integer-range]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[active-float-range]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[active-integer-range]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Batch</td><td>✅</td><td>83ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Batch Get Path — 5 cas</button></td><td>✅ 5/5</td><td>25ms</td></tr>
   <tr class="test-variant"><td>[no-files]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[first-file]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[second-file]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[all-files]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[merged-files]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Batch Get Stacks — 5 cas</button></td><td>✅ 5/5</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[no-stacks]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[selected-stack]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[separate-stacks]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[compatible-merge]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[invalid-dimensions]</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Localization</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Localization Fit — 4 cas</button></td><td>✅ 4/4</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[no-fit-without-ui]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[no-fit-with-ui]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[gaussian-fit-without-ui]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[gaussian-fit-with-ui]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Localization Spline Missing File — 2 cas</button></td><td>✅ 2/2</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[without-ui]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[with-ui]</td><td>✅</td><td>12ms</td></tr>
   <tr><td>Gaussian Fit Z</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Gaussian Fit Default Model — 2 cas</button></td><td>✅ 2/2</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[specific-model]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[default-model]</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Filters</td><td>✅</td><td>27ms</td></tr>
   <tr><td>Filters L</td><td>✅</td><td>12ms</td></tr>
   <tr><td>Filters T</td><td>✅</td><td>11ms</td></tr>
   <tr><td>Graph</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Hr</td><td>✅</td><td>28ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [calibration]</summary>
      <pre>- Activate : True<br>- Pixel Size : 0.32<br>- Exposure : 0.05<br>- Intensity : 0.012<br><br>{'Pixel Size': 0.32, 'Exposure': 0.05, 'Intensity': 0.012}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [gaussian-fit]</summary>
      <pre>- Activate : True<br>- Mode : 2<br>- Sigma : 1.0<br>- Theta : 0.0<br>- Z : False<br>- Z max : 500<br>- Model : <br>- Default Model : False<br><br>{'Mode': 2, 'Sigma': 1.0, 'Theta': 0.0, 'Z': False, 'Z max': 500, 'Model': '', 'Default Model': False}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [spline-fit]</summary>
      <pre>- Activate : True<br>- Sensor : 1<br>- Variance Map : <br>- File : <br><br>{'Sensor': 1, 'Variance Map': '', 'File': ''}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [beads]</summary>
      <pre>- Activate : True<br>- Max Distance : 2<br>- 3D : False<br><br>{'Max Distance': 2, '3D': False}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [tracking]</summary>
      <pre>- Activate : True<br>- Max Distance : 2<br><br>{'Max Distance': 2}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [blinking]</summary>
      <pre>- Activate : True<br>- Mode : 1<br>- Max Duration : 1<br>- Max Distance : 1.0<br><br>{'Mode': 1, 'Max Duration': 1, 'Max Distance': 1.0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [track-analysis]</summary>
      <pre>- Activate : True<br>- MSD : True<br>- Instant Diffusion : False<br>- Fit Length : 4<br>- Fit : 0<br>- 3D : False<br><br>{'MSD': True, 'Instant Diffusion': False, 'Fit Length': 4, 'Fit': 0, '3D': False}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [gallery]</summary>
      <pre>- Activate : True<br>- ROI Size : 11<br>- ROIs Per Line : 30<br><br>{'ROI Size': 11, 'ROIs Per Line': 30}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [graph-display]</summary>
      <pre>- Activate : True<br>- Limits : False<br>- Sigma : False<br>- Gauss : False<br>- Gauss Mix : False<br>- KDE : False<br>- Poiss : False<br>- Exp : False<br>- Cumul : False<br>- Log Scale : False<br>- Count : False<br>- Bins : 0<br><br>{'Limits': False, 'Sigma': False, 'Gauss': False, 'Gauss Mix': False, 'KDE': False, 'Poiss': False, 'Exp': False, 'Cumul': False, 'Log Scale': False, 'Count': False, 'Bins': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [hr-gaussian]</summary>
      <pre>- Activate : True<br>- Intensity : 10<br>- Fixed Intensity : False<br>- Shape : 0<br>- Size : 1<br><br>{'Intensity': 10, 'Fixed Intensity': False, 'Shape': 0, 'Size': 1}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [hr-3d]</summary>
      <pre>- Activate : True<br>- Z Step : 10<br>- Axis : 1<br>- Frames : 36<br><br>{'Z Step': 10, 'Axis': 1, 'Frames': 36}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [hr-track-stack]</summary>
      <pre>- Activate : True<br>- Head : 5<br>- Width : 1<br>- Length : -1<br>- Fade : 0<br>- Map : 0<br>- Background : True<br>- Upscale : 0<br><br>{'Head': 5, 'Width': 1, 'Length': -1, 'Fade': 0, 'Map': 0, 'Background': True, 'Upscale': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Group Contract [visualization-3d]</summary>
      <pre>- Activate : True<br>- Point Size : 2<br>- Pixel Size : 160<br>- XY Scale : 1.0<br>- Z Scale : 1.0<br>- Remove Outliers : False<br><br>{'Point Size': 2, 'Pixel Size': 160, 'XY Scale': 1.0, 'Z Scale': 1.0, 'Remove Outliers': False}</pre>
   </details>

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
      <summary>Log Test : Localization</summary>
      <pre>- Activate : True<br>- Preview : True<br>- Threshold : 90.0<br>- Auto Threshold : True<br>- ROI Shape : 0<br>- ROI Size : 7<br>- Watershed : True<br>- Fit : 0<br>- Gaussian Fit :<br>  - Activate : True<br>  - Mode : 0<br>  - Sigma : 1.0<br>  - Theta : 0.0<br>  - Z : False<br>  - Z max : 500<br>  - Model : <br>  - Default Model : False<br>- Spline Fit :<br>  - Activate : True<br>  - Sensor : 0<br>  - Variance Map : <br>  - File : <br><br>{'Preview': True, 'Threshold': 90.0, 'Auto Threshold': True, 'ROI Shape': 0, 'ROI Size': 7, 'Watershed': True, 'Fit': 0, 'Gaussian Fit Mode': 0, 'Gaussian Fit Sigma': 1.0, 'Gaussian Fit Theta': 0.0, 'Gaussian Fit Z': False, 'Gaussian Fit Z max': 500, 'Gaussian Fit Model': '', 'Gaussian Fit Default Model': False, 'Spline Fit Sensor': 0, 'Spline Fit Variance Map': '', 'Spline Fit File': ''}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters</summary>
      <pre>- Activate : True<br>- Save : True<br>- Plane : Deactivate [1, 100000]<br>- ROI : 1<br>- Localization :<br>  - Activate : True<br>  - Z : Deactivate [-2000, 2000]<br>  - Intensity : Deactivate [0, 10000000]<br>  - Sigma X : Deactivate [0, 10]<br>  - Sigma Y : Deactivate [0, 10]<br>  - Circularity : Deactivate [0, 1.0]<br>  - Theta : Deactivate [-90, 90]<br>  - MSE XY : Deactivate [0, 1.0]<br>  - MSE Z : Deactivate [0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Track : <br>  - Length : Deactivate [1, 10000]<br>  - Time Inside ROI : Deactivate [0, 100]<br>  - Instant D : Deactivate [-5, 5]<br>  - D Coeff : Deactivate [-5, 5]<br>  - Alpha : Deactivate [-10, 10]<br>  - Speed : Deactivate [0, 1.0]<br>  - Confinement : Deactivate [-10, 10]<br><br>{'Save': True, 'Plane': [1, 100000], 'ROI': 1, 'Localization Z': [-2000, 2000], 'Localization Intensity': [0, 10000000], 'Localization Sigma X': [0, 10], 'Localization Sigma Y': [0, 10], 'Localization Circularity': [0, 1.0], 'Localization Theta': [-90, 90], 'Localization MSE XY': [0, 1.0], 'Localization MSE Z': [0, 1.0], 'Tracks Track': '', 'Tracks Length': [1, 10000], 'Tracks Time Inside ROI': [0, 100], 'Tracks Instant D': [-5, 5], 'Tracks D Coeff': [-5, 5], 'Tracks Alpha': [-10, 10], 'Tracks Speed': [0, 1.0], 'Tracks Confinement': [-10, 10]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters L</summary>
      <pre>- Activate : True<br>- Z : Deactivate [2, 9]<br>- Intensity : Deactivate [0, 10000000]<br>- Sigma X : Deactivate [0, 10]<br>- Sigma Y : Deactivate [0, 10]<br>- Circularity : Deactivate [0, 1.0]<br>- Theta : Deactivate [-90, 90]<br>- MSE XY : Deactivate [0, 1.0]<br>- MSE Z : Deactivate [0, 1.0]<br><br>{'Z': [2, 9], 'Intensity': [0, 10000000], 'Sigma X': [0, 10], 'Sigma Y': [0, 10], 'Circularity': [0, 1.0], 'Theta': [-90, 90], 'MSE XY': [0, 1.0], 'MSE Z': [0, 1.0]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Filters T</summary>
      <pre>- Activate : True<br>- Track : 1;3-4<br>- Length : Deactivate [1, 10000]<br>- Time Inside ROI : Deactivate [0, 100]<br>- Instant D : Deactivate [-5, 5]<br>- D Coeff : Deactivate [-5, 5]<br>- Alpha : Deactivate [-10, 10]<br>- Speed : Deactivate [0, 1.0]<br>- Confinement : Deactivate [-10, 10]<br><br>{'Track': '1;3-4', 'Length': [1, 10000], 'Time Inside ROI': [0, 100], 'Instant D': [-5, 5], 'D Coeff': [-5, 5], 'Alpha': [-10, 10], 'Speed': [0, 1.0], 'Confinement': [-10, 10]}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Graph</summary>
      <pre>- Activate : True<br>- Mode : 1<br>- Type : 0<br>- Source : 0<br>- Source B : 0<br>- MSD Step : 1<br>- Display :<br>  - Activate : True<br>  - Limits : False<br>  - Sigma : False<br>  - Gauss : False<br>  - Gauss Mix : False<br>  - KDE : False<br>  - Poiss : False<br>  - Exp : False<br>  - Cumul : False<br>  - Log Scale : False<br>  - Count : False<br>  - Bins : 0<br><br>{'Mode': 1, 'Type': 0, 'Source': 0, 'Source B': 0, 'MSD Step': 1, 'Display Limits': False, 'Display Sigma': False, 'Display Gauss': False, 'Display Gauss Mix': False, 'Display KDE': False, 'Display Poiss': False, 'Display Exp': False, 'Display Cumul': False, 'Display Log Scale': False, 'Display Count': False, 'Display Bins': 0}</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Hr</summary>
      <pre>- Activate : True<br>- Dimension : 1<br>- Type : 0<br>- Source : 0<br>- Scaling : 1<br>- Color mode : 0<br>- Background : 0<br>- Ratio : 4<br>- Crop : True<br>- Remove Beads : True<br>- Drift Correction : True<br>- Smooth Drift : True<br>- Gaussian :<br>  - Activate : False<br>  - Intensity : 100<br>  - Fixed Intensity : False<br>  - Shape : 0<br>  - Size : 1<br>- 3D :<br>  - Activate : True<br>  - Z Step : 20<br>  - Axis : 1<br>  - Frames : 36<br>- T-Stack :<br>  - Activate : True<br>  - Head : 1<br>  - Width : 1<br>  - Length : -1<br>  - Fade : 0<br>  - Map : 0<br>  - Background : True<br>  - Upscale : 0<br><br>{'Dimension': 1, 'Type': 0, 'Source': 0, 'Scaling': 1, 'Color mode': 0, 'Background': 0, 'Ratio': 4, 'Crop': True, 'Remove Beads': True, 'Drift Correction': True, 'Smooth Drift': True, 'Gaussian Intensity': 100, 'Gaussian Fixed Intensity': False, 'Gaussian Shape': 0, 'Gaussian Size': 1, '3D Z Step': 20, '3D Axis': 1, '3D Frames': 36, 'T-Stack Head': 1, 'T-Stack Width': 1, 'T-Stack Length': -1, 'T-Stack Fade': 0, 'T-Stack Map': 0, 'T-Stack Background': True, 'T-Stack Upscale': 0}</pre>
   </details>

Settings Roimanager
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Layer</td><td>✅</td><td>554ms</td></tr>
   <tr><td>Rois</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Set Xy Roi</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update From Layer Mismatched Lengths — 4 cas</button></td><td>✅ 4/4</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[missing-data-main-layer]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[missing-data-hr-layer]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing-type-main-layer]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing-type-hr-layer]</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Update Main</td><td>✅</td><td>36ms</td></tr>
   <tr><td>Update Hr</td><td>✅</td><td>12ms</td></tr>
   <tr><td>Update Roi Selection</td><td>✅</td><td>17ms</td></tr>
   <tr><td>Dict</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Roi Limits</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Limits — 4 cas</button></td><td>✅ 4/4</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[outside]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[crossing]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[not-fully-inside]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[fully-inside]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Hr Data Intersection — 2 cas</button></td><td>✅ 2/2</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[image-edge]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[disjoint]</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Hr Box</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Data Box — 4 cas</button></td><td>✅ 4/4</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[spots]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[fixed-size]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[isotropic]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[anisotropic]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Data Box Reset — 4 cas</button></td><td>✅ 4/4</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[disabled]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[empty-data]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[nonfinite-data]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing-column]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Data Box Invalid Gaussian — 10 cas</button></td><td>✅ 10/10</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[missing-sigma-x]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing-sigma-y]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[nan-sigma]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[infinite-sigma]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[nan-size]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[infinite-size]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[zero-size]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[negative-size]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[zero-mean-sigma]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[negative-max-sigma]</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Data Box Intersection And Reset</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Filtering Dataframe</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Filtering Dataframe Concave Cross</td><td>✅</td><td>6ms</td></tr>
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
   <tr><td>Settings</td><td>✅</td><td>31ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Settings Batch Filter Limits — 4 cas</button></td><td>✅ 4/4</td><td>76ms</td></tr>
   <tr class="test-variant"><td>[first-stack]</td><td>✅</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[selected-stack]</td><td>✅</td><td>26ms</td></tr>
   <tr class="test-variant"><td>[separate-files-max]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[all-in-one]</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Settings Batch Filter Limits After List Change</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Settings Batch Reuses Tif Metadata</td><td>✅</td><td>11ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Settings Group Getter — 11 cas</button></td><td>✅ 11/11</td><td>78ms</td></tr>
   <tr class="test-variant"><td>[batch]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[calibration]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[localization]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[beads]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[tracking]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[blinking]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[track-analysis]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[gallery]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[graph]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[high-resolution]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-variant"><td>[filters]</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Settings Signal</td><td>✅</td><td>17ms</td></tr>
   </tbody>
   </table>

Settings Types
^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Base Setting</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Base Check Setting — 4 cas</button></td><td>✅ 4/4</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[integer]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[integer-selection]</td><td>✅</td><td>4ms</td></tr>
   <tr class="test-variant"><td>[float-range]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[integer-range]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Base Ui — 2 cas</button></td><td>✅ 2/2</td><td>84ms</td></tr>
   <tr class="test-variant"><td>[with-label]</td><td>✅</td><td>79ms</td></tr>
   <tr class="test-variant"><td>[no-label]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Spin Int</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Spin Float</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Check Box</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Combo</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Color Map</td><td>✅</td><td>14ms</td></tr>
   <tr><td>Color Map Picker Replaces Temporary Entry</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Color Map Rejects Invalid Custom Color</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Color Map Picker Cancel</td><td>✅</td><td>113ms</td></tr>
   <tr><td>Color Map Updates Picker Without Button</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Color Map Get Lut — 3 cas</button></td><td>✅ 3/3</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[default-uint16]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[zero]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[custom-uint8]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Color Map Get Lut Rejects Negative Maximum</td><td>✅</td><td>4ms</td></tr>
   <tr><td>Browse File</td><td>✅</td><td>77ms</td></tr>
   <tr><td>File List</td><td>✅</td><td>16ms</td></tr>
   <tr><td>File List Adds Sorted Batch Without Reordering Existing Items</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">File List Emits Final Selection Once — 2 cas</button></td><td>✅ 2/2</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[dialog]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[paths]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>File List Add Files Syncs Views</td><td>✅</td><td>100ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">File List Add Files Ignores Invalid Paths — 3 cas</button></td><td>✅ 3/3</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[empty]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[directory]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[missing]</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Check Int</td><td>✅</td><td>91ms</td></tr>
   <tr><td>Check Range Int</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Check Range Float</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Int Selection Validator — 4 cas</button></td><td>✅ 4/4</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[empty-selection]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[whitespace]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[integer-ranges]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[invalid-character]</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Int Selection Validator Parse Error</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Check Int Selection</td><td>✅</td><td>76ms</td></tr>
   <tr><td>Button</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Button Group</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Sync</td><td>✅</td><td>15ms</td></tr>
   </tbody>
   </table>

Settings Types Signal
^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Connect And Emit Direct</td><td>✅</td><td>5ms</td></tr>
   <tr><td>Disconnect</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Disconnect Unavailable Signal — 4 cas</button></td><td>✅ 4/4</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[already-disconnected-single-slot]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[already-disconnected-all-slots]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[destroyed-object-single-slot]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[destroyed-object-all-slots]</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Blocked Returns Context Manager Instance</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Block Simple Coalescence Last Value — 2 cas</button></td><td>✅ 2/2</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[successive-values]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[repeated-overwrites]</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Block Without Emits No Output</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Nested Blocks Emit Once At Outer Exit</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Emit Default None Coalesced</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Block Flags Reset After Flush</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Block Without Emit</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Emit Direct After Previous Block</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Internal Block Begin End Paths</td><td>✅</td><td>7ms</td></tr>
   </tbody>
   </table>

Tools Fileio
^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Add Extension — 6 cas</button></td><td>✅ 6/6</td><td>45ms</td></tr>
   <tr class="test-variant"><td>[existing-extension]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[multiple-dots]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[with-directories]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[extension-already-present]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[extension-with-dot]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Add Suffix — 2 cas</button></td><td>✅ 2/2</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[with-extension]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Timestamp For Files — 2 cas</button></td><td>✅ 2/2</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[with-time]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[date-only]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Last File — 2 cas</button></td><td>✅ 2/2</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[alphabetical-order]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[modification-time]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Last File Not Found — 2 cas</button></td><td>✅ 2/2</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[missing-directory]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[no-match]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Get Last File Io Error — 2 cas</button></td><td>✅ 2/2</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[directory-unreadable]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[file-disappeared]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Extract Suffix — 5 cas</button></td><td>✅ 5/5</td><td>38ms</td></tr>
   <tr class="test-variant"><td>[empty-name]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[no-suffix]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[single-suffix]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[last-suffix]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Cleanup Process — 4 cas</button></td><td>✅ 4/4</td><td>36ms</td></tr>
   <tr class="test-variant"><td>[empty-directory]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[administrative-files-only]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[result-still-present]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[other-timestamp-preserved]</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Cleanup Process Missing Folder</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Cleanup Process Delete Error</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Load Dll</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Load Dll Missing</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Json Roundtrip</td><td>✅</td><td>37ms</td></tr>
   <tr><td>Open Json Bad File</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tif Roundtrip — 2 cas</button></td><td>✅ 2/2</td><td>93ms</td></tr>
   <tr class="test-variant"><td>[stack]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-variant"><td>[2d-image]</td><td>✅</td><td>38ms</td></tr>
   <tr><td>Save Tif Rgb</td><td>✅</td><td>45ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Save Tif Bad Stack — 4 cas</button></td><td>✅ 4/4</td><td>45ms</td></tr>
   <tr class="test-variant"><td>[1d-array]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[5d-array]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[two-channels]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[four-channels]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Read Tif Shape — 2 cas</button></td><td>✅ 2/2</td><td>54ms</td></tr>
   <tr class="test-variant"><td>[single-image]</td><td>✅</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[stack]</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Read Tif Shape Single Image</td><td>✅</td><td>29ms</td></tr>
   <tr><td>Open Tif</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Tif Read Errors — 4 cas</button></td><td>✅ 4/4</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[shape-missing-file]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[shape-invalid-dimensions]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[pixels-missing-file]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[pixels-invalid-dimensions]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Save Png — 3 cas</button></td><td>✅ 3/3</td><td>72ms</td></tr>
   <tr class="test-variant"><td>[normalization]</td><td>✅</td><td>21ms</td></tr>
   <tr class="test-variant"><td>[no-normalization]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[black-image]</td><td>✅</td><td>31ms</td></tr>
   <tr><td>Save Png Color</td><td>✅</td><td>20ms</td></tr>
   <tr><td>Save Png Bad Sample</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Open Calibration Mat</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Open Calibration Mat Bad File</td><td>✅</td><td>7ms</td></tr>
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
   <tr><td>Open</td><td>✅</td><td>12ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Invalid — 3 cas</button></td><td>✅ 3/3</td><td>28ms</td></tr>
   <tr class="test-variant"><td>[directory-without-results]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[file-instead-of-directory]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[missing-directory]</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Analyze</td><td>✅</td><td>11ms</td></tr>
   <tr><td>Migrate</td><td>✅</td><td>117ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Operation Without Directory — 2 cas</button></td><td>✅ 2/2</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[analyze]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[migrate]</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Update Meta</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Open Old File</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Old File Invalid — 2 cas</button></td><td>✅ 2/2</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[directory-instead-of-file]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[invalid-content]</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Open Old Irregular File</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Open Old Irregular File Invalid — 2 cas</button></td><td>✅ 2/2</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[directory-instead-of-file]</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-variant"><td>[invalid-content]</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Column Migrator</td><td>✅</td><td>10ms</td></tr>
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
   <tr><td>Logger</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Logger Reopen</td><td>✅</td><td>29ms</td></tr>
   <tr><td>Logger Open Error</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Logger Close Error — 3 cas</button></td><td>✅ 3/3</td><td>38ms</td></tr>
   <tr class="test-variant"><td>[write-failed]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[flush-failed]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[close-failed]</td><td>✅</td><td>22ms</td></tr>
   <tr><td>Logger Bad Use</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Logger Add Error — 2 cas</button></td><td>✅ 2/2</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[write-failed]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[flush-failed]</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Logger With Use</td><td>✅</td><td>10ms</td></tr>
   </tbody>
   </table>

Tools Ui
^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Add Setting Row</td><td>✅</td><td>61ms</td></tr>
   <tr><td>Init Layout</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Container — 2 cas</button></td><td>✅ 2/2</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[tab]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[group]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Info Grid — 2 cas</button></td><td>✅ 2/2</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[no-units]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[with-units-and-tooltips]</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Make File Info Group</td><td>✅</td><td>9ms</td></tr>
   <tr><td>Make Path Label</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Path Label — 2 cas</button></td><td>✅ 2/2</td><td>18ms</td></tr>
   <tr class="test-variant"><td>[string]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[path-object]</td><td>✅</td><td>10ms</td></tr>
   <tr><td>Make Vertical Scroll</td><td>✅</td><td>10ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Separator — 2 cas</button></td><td>✅ 2/2</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[vertical]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[horizontal]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Make Spin — 2 cas</button></td><td>✅ 2/2</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[integer-with-buttons]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[decimal-without-buttons]</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Sync Button Group</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Sync Spin</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Spin Limits — 4 cas</button></td><td>✅ 4/4</td><td>47ms</td></tr>
   <tr class="test-variant"><td>[no-change]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[minimum-only]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[maximum-only]</td><td>✅</td><td>9ms</td></tr>
   <tr class="test-variant"><td>[both-bounds]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Print Message — 3 cas</button></td><td>✅ 3/3</td><td>24ms</td></tr>
   <tr class="test-variant"><td>[error]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[warning]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[success]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Format Time — 4 cas</button></td><td>✅ 4/4</td><td>33ms</td></tr>
   <tr class="test-variant"><td>[zero-duration]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[seconds]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[minute-boundary]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[hours-minutes-seconds]</td><td>✅</td><td>8ms</td></tr>
   </tbody>
   </table>

Ui Alignment
^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>47ms</td></tr>
   <tr><td>Bad Load Tif</td><td>✅</td><td>12ms</td></tr>
   <tr><td>Bad Compute</td><td>✅</td><td>11ms</td></tr>
   <tr><td>Compute</td><td>✅</td><td>12ms</td></tr>
   <tr><td>Bad Load Coef</td><td>✅</td><td>14ms</td></tr>
   <tr><td>Bad Align</td><td>✅</td><td>13ms</td></tr>
   <tr><td>Align</td><td>✅</td><td>198ms</td></tr>
   </tbody>
   </table>

Ui Astigmatism3D
^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>323ms</td></tr>
   <tr><td>Sync Spin</td><td>✅</td><td>72ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Sanity Check Filters Z Limits — 2 cas</button></td><td>✅ 2/2</td><td>121ms</td></tr>
   <tr class="test-variant"><td>[small-range]</td><td>✅</td><td>62ms</td></tr>
   <tr class="test-variant"><td>[large-range]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Sanity Check Without Valid Points — 2 cas</button></td><td>✅ 2/2</td><td>116ms</td></tr>
   <tr class="test-variant"><td>[empty-data]</td><td>✅</td><td>59ms</td></tr>
   <tr class="test-variant"><td>[all-excluded]</td><td>✅</td><td>56ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Plot Modes — 3 cas</button></td><td>✅ 3/3</td><td>221ms</td></tr>
   <tr class="test-variant"><td>[cross-section]</td><td>✅</td><td>93ms</td></tr>
   <tr class="test-variant"><td>[slope]</td><td>✅</td><td>65ms</td></tr>
   <tr class="test-variant"><td>[sigma-curves]</td><td>✅</td><td>63ms</td></tr>
   <tr><td>Check Loc</td><td>✅</td><td>94ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Bad Load Loc — 2 cas</button></td><td>✅ 2/2</td><td>104ms</td></tr>
   <tr class="test-variant"><td>[calibration-tab]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-variant"><td>[estimation-tab]</td><td>✅</td><td>49ms</td></tr>
   <tr><td>Estimation Load Does Not Calibrate</td><td>✅</td><td>120ms</td></tr>
   <tr><td>Bad Load Model</td><td>✅</td><td>48ms</td></tr>
   <tr><td>Compute Without Calibration Data</td><td>✅</td><td>73ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Compute On Localization Load — 5 cas</button></td><td>✅ 5/5</td><td>869ms</td></tr>
   <tr class="test-variant"><td>[original-z]</td><td>✅</td><td>147ms</td></tr>
   <tr class="test-variant"><td>[mean-beads]</td><td>✅</td><td>272ms</td></tr>
   <tr class="test-variant"><td>[single-bead]</td><td>✅</td><td>139ms</td></tr>
   <tr class="test-variant"><td>[plane-z-flipped]</td><td>✅</td><td>134ms</td></tr>
   <tr class="test-variant"><td>[uncentered]</td><td>✅</td><td>178ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Compute On Parameter Change — 9 cas</button></td><td>✅ 9/9</td><td>1.94s</td></tr>
   <tr class="test-variant"><td>[pixel-size]</td><td>✅</td><td>222ms</td></tr>
   <tr class="test-variant"><td>[z-limit]</td><td>✅</td><td>221ms</td></tr>
   <tr class="test-variant"><td>[plane-interval]</td><td>✅</td><td>220ms</td></tr>
   <tr class="test-variant"><td>[z-from-plane]</td><td>✅</td><td>208ms</td></tr>
   <tr class="test-variant"><td>[center-z]</td><td>✅</td><td>228ms</td></tr>
   <tr class="test-variant"><td>[flip-z]</td><td>✅</td><td>209ms</td></tr>
   <tr class="test-variant"><td>[one-bead]</td><td>✅</td><td>216ms</td></tr>
   <tr class="test-variant"><td>[synced-pixel-size]</td><td>✅</td><td>208ms</td></tr>
   <tr class="test-variant"><td>[synced-z-limit]</td><td>✅</td><td>207ms</td></tr>
   <tr><td>Compute Reuses Original Z</td><td>✅</td><td>626ms</td></tr>
   <tr><td>Compute User Backup Unavailable</td><td>✅</td><td>107ms</td></tr>
   <tr><td>Compute Remove Multi</td><td>✅</td><td>172ms</td></tr>
   <tr><td>Compute Missing Plane</td><td>✅</td><td>174ms</td></tr>
   <tr><td>Compute Missing Plane With Option Enabled</td><td>✅</td><td>136ms</td></tr>
   <tr><td>Compute Bad Model</td><td>✅</td><td>193ms</td></tr>
   <tr><td>Set Default Model Without Model</td><td>✅</td><td>73ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Set Default Model — 2 cas</button></td><td>✅ 2/2</td><td>549ms</td></tr>
   <tr class="test-variant"><td>[enable-after-model]</td><td>✅</td><td>327ms</td></tr>
   <tr class="test-variant"><td>[enable-before-model]</td><td>✅</td><td>222ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Estimate Default Model — 4 cas</button></td><td>✅ 4/4</td><td>817ms</td></tr>
   <tr class="test-variant"><td>[valid-default]</td><td>✅</td><td>86ms</td></tr>
   <tr class="test-variant"><td>[missing-default]</td><td>✅</td><td>55ms</td></tr>
   <tr class="test-variant"><td>[invalid-default]</td><td>✅</td><td>605ms</td></tr>
   <tr class="test-variant"><td>[unreadable-default]</td><td>✅</td><td>71ms</td></tr>
   <tr><td>Bad Estimate</td><td>✅</td><td>55ms</td></tr>
   <tr><td>Estimate</td><td>✅</td><td>80ms</td></tr>
   <tr><td>Estimate Backup</td><td>✅</td><td>88ms</td></tr>
   <tr><td>Download</td><td>✅</td><td>73ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Compute Reuses Original Z</summary>
      <pre>Selected file: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_compute_reuses_original_z0\astigmatism_3d_calibration.csv.<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">CSV loaded successfully with 94 points and 11 columns.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">There are 47 planes and 2 beads in file.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X  272.605512  326.110313 -0.069073  0.029962  689.731919<br>Y -246.225834  352.659451  0.704618 -0.283028  708.933430<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X  272.605512  326.110313 -0.069073  0.029962  689.731919<br>Y -246.225834  352.659451  0.704618 -0.283028  708.933430<br>Average model:<br>           Z0           W        C3        C4           A<br>X  272.605512  326.110313 -0.069073  0.029962  689.731919<br>Y -246.225834  352.659451  0.704618 -0.283028  708.933430<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  689.731919<br>Y  246.225834  352.659451 -0.704618 -0.283028  708.933430<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  689.731919<br>Y  246.225834  352.659451 -0.704618 -0.283028  708.933430<br>Average model:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  689.731919<br>Y  246.225834  352.659451 -0.704618 -0.283028  708.933430<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  724.218515<br>Y  246.225834  352.659450 -0.704618 -0.283028  744.380101<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  724.218515<br>Y  246.225834  352.659450 -0.704618 -0.283028  744.380101<br>Average model:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  724.218515<br>Y  246.225834  352.659450 -0.704618 -0.283028  744.380101<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  689.731919<br>Y  246.225834  352.659451 -0.704618 -0.283028  708.933430<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  689.731919<br>Y  246.225834  352.659451 -0.704618 -0.283028  708.933430<br>Average model:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  689.731919<br>Y  246.225834  352.659451 -0.704618 -0.283028  708.933430<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X  272.605512  326.110313 -0.069073  0.029962  689.731919<br>Y -246.225834  352.659451  0.704618 -0.283028  708.933430<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X  272.605512  326.110313 -0.069073  0.029962  689.731919<br>Y -246.225834  352.659451  0.704618 -0.283028  708.933430<br>Average model:<br>           Z0           W        C3        C4           A<br>X  272.605512  326.110313 -0.069073  0.029962  689.731919<br>Y -246.225834  352.659451  0.704618 -0.283028  708.933430<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Set Default Model [enable-after-model]</summary>
      <pre>Selected file: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_set_default_model_enable_0\astigmatism_3d_calibration.csv.<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">CSV loaded successfully with 94 points and 11 columns.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">There are 47 planes and 2 beads in file.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  551.785536<br>Y  246.225834  352.659450 -0.704618 -0.283028  567.146743<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  551.785536<br>Y  246.225834  352.659450 -0.704618 -0.283028  567.146743<br>Average model:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  551.785536<br>Y  246.225834  352.659450 -0.704618 -0.283028  567.146743<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Default model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -408.908268  489.165469  0.069073  0.029962  551.785536<br>Y  369.338751  528.989175 -0.704618 -0.283028  567.146743<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -408.908268  489.165469  0.069073  0.029962  551.785536<br>Y  369.338751  528.989175 -0.704618 -0.283028  567.146743<br>Average model:<br>           Z0           W        C3        C4           A<br>X -408.908268  489.165469  0.069073  0.029962  551.785536<br>Y  369.338751  528.989175 -0.704618 -0.283028  567.146743<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Default model saved successfully.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -545.211024  652.220626  0.069073  0.029962  551.785536<br>Y  492.451668  705.318900 -0.704618 -0.283028  567.146743<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -545.211024  652.220626  0.069073  0.029962  551.785536<br>Y  492.451668  705.318900 -0.704618 -0.283028  567.146743<br>Average model:<br>           Z0           W        C3        C4           A<br>X -545.211024  652.220626  0.069073  0.029962  551.785536<br>Y  492.451668  705.318900 -0.704618 -0.283028  567.146743<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Set Default Model [enable-before-model]</summary>
      <pre>Selected file: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_set_default_model_enable_1\astigmatism_3d_calibration.csv.<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">CSV loaded successfully with 94 points and 11 columns.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">There are 47 planes and 2 beads in file.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  551.785536<br>Y  246.225834  352.659450 -0.704618 -0.283028  567.146743<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  551.785536<br>Y  246.225834  352.659450 -0.704618 -0.283028  567.146743<br>Average model:<br>           Z0           W        C3        C4           A<br>X -272.605512  326.110313  0.069073  0.029962  551.785536<br>Y  246.225834  352.659450 -0.704618 -0.283028  567.146743<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Default model saved successfully.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -408.908268  489.165469  0.069073  0.029962  551.785536<br>Y  369.338751  528.989175 -0.704618 -0.283028  567.146743<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -408.908268  489.165469  0.069073  0.029962  551.785536<br>Y  369.338751  528.989175 -0.704618 -0.283028  567.146743<br>Average model:<br>           Z0           W        C3        C4           A<br>X -408.908268  489.165469  0.069073  0.029962  551.785536<br>Y  369.338751  528.989175 -0.704618 -0.283028  567.146743<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Default model saved successfully.</span><span style="font-weight: bold"></span><br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span><br>Model for bead 1:<br>           Z0           W        C3        C4           A<br>X -545.211024  652.220626  0.069073  0.029962  551.785536<br>Y  492.451668  705.318900 -0.704618 -0.283028  567.146743<br>Model for bead 2:<br>           Z0           W        C3        C4           A<br>X -545.211024  652.220626  0.069073  0.029962  551.785536<br>Y  492.451668  705.318900 -0.704618 -0.283028  567.146743<br>Average model:<br>           Z0           W        C3        C4           A<br>X -545.211024  652.220626  0.069073  0.029962  551.785536<br>Y  492.451668  705.318900 -0.704618 -0.283028  567.146743<br><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Model saved successfully.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Estimate Default Model [valid-default]</summary>
      <pre><span style="color: #00aa00"></span><span style="font-weight: bold; color: #00aa00">Localization file with estimation saved successfully.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Estimate Default Model [missing-default]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Can't estimate without correct model file loaded.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Estimate Default Model [invalid-default]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Can't estimate without correct model file loaded.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Estimate Default Model [unreadable-default]</summary>
      <pre><span style="color: #aa0000"></span><span style="font-weight: bold; color: #aa0000">Unable to read the model file: Error tokenizing data. C error: EOF inside string starting at row 0.</span><span style="font-weight: bold"></span><br><span style="color: #aa0000"></span><span style="font-weight: bold; color: #aa0000">Unable to read the model file: Error tokenizing data. C error: EOF inside string starting at row 0.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Can't estimate without correct model file loaded.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Download</summary>
      <pre>C:\Git\palm-tracer\tests\input\ref</pre>
   </details>

Ui Basenapari
^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Initialization Preserves References — 2 cas</button></td><td>✅ 2/2</td><td>32ms</td></tr>
   <tr class="test-variant"><td>[new-instance]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[shared-instance]</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Target Preserves Root Window — 2 cas</button></td><td>✅ 2/2</td><td>39ms</td></tr>
   <tr class="test-variant"><td>[docked]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[floating]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Filter Follows Visibility — 2 cas</button></td><td>✅ 2/2</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[drops-disabled]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[drops-enabled]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Delivers Local Files Once — 8 cas</button></td><td>✅ 8/8</td><td>131ms</td></tr>
   <tr class="test-variant"><td>[single-file-root-window]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[single-file-child-widget]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[single-file-only-root-window]</td><td>✅</td><td>19ms</td></tr>
   <tr class="test-variant"><td>[single-file-only-child-widget]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[multiple-files-root-window]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[multiple-files-child-widget]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[local-and-remote-root-window]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[local-and-remote-child-widget]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Rejects Invalid Files — 5 cas</button></td><td>✅ 5/5</td><td>79ms</td></tr>
   <tr class="test-variant"><td>[multiple-files]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[local-and-remote]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[directory]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[missing-file]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[blocked-widget]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Preserves Unrelated Events — 3 cas</button></td><td>✅ 3/3</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[other-window]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[remote-url]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[internal-text]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Ignores Inactive Target — 3 cas</button></td><td>✅ 3/3</td><td>154ms</td></tr>
   <tr class="test-variant"><td>[hidden-window]</td><td>✅</td><td>17ms</td></tr>
   <tr class="test-variant"><td>[deleted-window]</td><td>✅</td><td>122ms</td></tr>
   <tr class="test-variant"><td>[non-widget-receiver]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Filter Handles Deleted Window — 2 cas</button></td><td>✅ 2/2</td><td>30ms</td></tr>
   <tr class="test-variant"><td>[hide-after-destruction]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[show-after-destruction]</td><td>✅</td><td>15ms</td></tr>
   <tr><td>Drop Filter Handles Parent Destruction</td><td>✅</td><td>16ms</td></tr>
   <tr><td>Drop Requires Specialized Handler</td><td>✅</td><td>14ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Layer — 4 cas</button></td><td>✅ 4/4</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[preserve-hidden]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[preserve-visible]</td><td>✅</td><td>6ms</td></tr>
   <tr class="test-variant"><td>[force-visible]</td><td>✅</td><td>5ms</td></tr>
   <tr class="test-variant"><td>[force-hidden]</td><td>✅</td><td>6ms</td></tr>
   <tr><td>Update Layer Restores Visibility On Error</td><td>✅</td><td>6ms</td></tr>
   </tbody>
   </table>

Ui Baseplotlywidget
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Creation</td><td>✅</td><td>19ms</td></tr>
   <tr><td>Webengine Import Fallback</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Web Widget Without Engine — 6 cas</button></td><td>✅ 6/6</td><td>99ms</td></tr>
   <tr class="test-variant"><td>[load-page-webengine-disabled]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[load-page-text-view]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[update-figure-webengine-disabled]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[update-figure-text-view]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[connect-signals-webengine-disabled]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[connect-signals-text-view]</td><td>✅</td><td>15ms</td></tr>
   <tr><td>Load Plotly Page Missing Script</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Plotly — 2 cas</button></td><td>✅ 2/2</td><td>42ms</td></tr>
   <tr class="test-variant"><td>[local-script]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[missing-script]</td><td>✅</td><td>21ms</td></tr>
   <tr><td>Download Plotly</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Export Without Engine — 4 cas</button></td><td>✅ 4/4</td><td>63ms</td></tr>
   <tr class="test-variant"><td>[download-image-webengine-disabled]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[download-image-text-view]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[export-button-webengine-disabled]</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-variant"><td>[export-button-text-view]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Export Plotly — 6 cas</button></td><td>✅ 6/6</td><td>134ms</td></tr>
   <tr class="test-variant"><td>[png]</td><td>✅</td><td>20ms</td></tr>
   <tr class="test-variant"><td>[svg]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[webp]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[html]</td><td>✅</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[pdf]</td><td>✅</td><td>23ms</td></tr>
   <tr class="test-variant"><td>[fallback-png]</td><td>✅</td><td>25ms</td></tr>
   <tr><td>Export Write Error</td><td>✅</td><td>16ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Close Web Widget — 2 cas</button></td><td>✅ 2/2</td><td>31ms</td></tr>
   <tr class="test-variant"><td>[missing-page]</td><td>✅</td><td>15ms</td></tr>
   <tr class="test-variant"><td>[existing-page]</td><td>✅</td><td>16ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Download Plotly</summary>
      <pre>C:\Git\palm-tracer\tests\output<br>C:\Git\palm-tracer\tests\output</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Export Plotly [png]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No figures to export.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Export Plotly [svg]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No figures to export.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Export Plotly [webp]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No figures to export.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Export Plotly [html]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No figures to export.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Export Plotly [pdf]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No figures to export.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Export Plotly [fallback-png]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No figures to export.</span><span style="font-weight: bold"></span></pre>
   </details>

Ui Filemigrator
^^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Bad Load</td><td>✅</td><td>8ms</td></tr>
   <tr><td>Migrate</td><td>✅</td><td>30ms</td></tr>
   <tr><td>Migrate Error</td><td>✅</td><td>8ms</td></tr>
   </tbody>
   </table>

Ui Graphviewer
^^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>74ms</td></tr>
   <tr><td>Results Status Automatic Update</td><td>✅</td><td>75ms</td></tr>
   <tr><td>Widget Double Creation</td><td>✅</td><td>125ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Drop Ignores Inactive Target — 3 cas</button></td><td>✅ 3/3</td><td>145ms</td></tr>
   <tr class="test-variant"><td>[hidden-window]</td><td>✅</td><td>51ms</td></tr>
   <tr class="test-variant"><td>[deleted-window]</td><td>✅</td><td>49ms</td></tr>
   <tr class="test-variant"><td>[non-widget-receiver]</td><td>✅</td><td>44ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Drop Loads Latest Results And Redraws — 4 cas</button></td><td>✅ 4/4</td><td>190ms</td></tr>
   <tr class="test-variant"><td>[window]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[action-button]</td><td>✅</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[scroll-viewport]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[graph-area]</td><td>✅</td><td>47ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Drop Rejects Invalid Batch — 4 cas</button></td><td>✅ 4/4</td><td>183ms</td></tr>
   <tr class="test-variant"><td>[multiple-files]</td><td>✅</td><td>47ms</td></tr>
   <tr class="test-variant"><td>[local-and-remote]</td><td>✅</td><td>47ms</td></tr>
   <tr class="test-variant"><td>[directory]</td><td>✅</td><td>44ms</td></tr>
   <tr class="test-variant"><td>[missing-file]</td><td>✅</td><td>45ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Drop Preserves Unrelated Events — 3 cas</button></td><td>✅ 3/3</td><td>136ms</td></tr>
   <tr class="test-variant"><td>[other-window]</td><td>✅</td><td>47ms</td></tr>
   <tr class="test-variant"><td>[remote-url]</td><td>✅</td><td>43ms</td></tr>
   <tr class="test-variant"><td>[internal-text]</td><td>✅</td><td>46ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Drop Follows Visibility — 2 cas</button></td><td>✅ 2/2</td><td>99ms</td></tr>
   <tr class="test-variant"><td>[drops-disabled]</td><td>✅</td><td>50ms</td></tr>
   <tr class="test-variant"><td>[drops-enabled]</td><td>✅</td><td>49ms</td></tr>
   <tr><td>Change Type</td><td>✅</td><td>93ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Add Stack Uses Dropped Results Folder — 3 cas</button></td><td>✅ 3/3</td><td>138ms</td></tr>
   <tr class="test-variant"><td>[only-one]</td><td>✅</td><td>48ms</td></tr>
   <tr class="test-variant"><td>[each-file]</td><td>✅</td><td>46ms</td></tr>
   <tr class="test-variant"><td>[all-in-one]</td><td>✅</td><td>45ms</td></tr>
   <tr><td>Update Plot Localization</td><td>✅</td><td>348ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Add Stack Uses Dropped Results Folder [only-one]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to read batch stack depth: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\tmonseigne\\AppData\\Local\\Temp\\pytest-of-tmonseigne\\pytest-182\\test_add_stack_uses_dropped_re0\\first.tif'</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Add Stack Uses Dropped Results Folder [each-file]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to read batch stack depth: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\tmonseigne\\AppData\\Local\\Temp\\pytest-of-tmonseigne\\pytest-182\\test_add_stack_uses_dropped_re1\\first.tif'</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to read batch stack depth: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\tmonseigne\\AppData\\Local\\Temp\\pytest-of-tmonseigne\\pytest-182\\test_add_stack_uses_dropped_re1\\first.tif'</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to read batch stack depth: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\tmonseigne\\AppData\\Local\\Temp\\pytest-of-tmonseigne\\pytest-182\\test_add_stack_uses_dropped_re1\\first.tif'</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Add Stack Uses Dropped Results Folder [all-in-one]</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to read batch stack depth: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\tmonseigne\\AppData\\Local\\Temp\\pytest-of-tmonseigne\\pytest-182\\test_add_stack_uses_dropped_re2\\first.tif'</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to read batch stack depth: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\tmonseigne\\AppData\\Local\\Temp\\pytest-of-tmonseigne\\pytest-182\\test_add_stack_uses_dropped_re2\\first.tif'</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Unable to read batch stack depth: [WinError 2] Le fichier spécifié est introuvable: 'C:\\Users\\tmonseigne\\AppData\\Local\\Temp\\pytest-of-tmonseigne\\pytest-182\\test_add_stack_uses_dropped_re2\\first.tif'</span><span style="font-weight: bold"></span></pre>
   </details>

Ui Palmtracer
^^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Creation</td><td>✅</td><td>148ms</td></tr>
   <tr><td>Threading Import Fallback</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Filters Button</td><td>✅</td><td>594ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Drop Adds Files From Window — 2 cas</button></td><td>✅ 2/2</td><td>304ms</td></tr>
   <tr class="test-variant"><td>[single-file]</td><td>✅</td><td>140ms</td></tr>
   <tr class="test-variant"><td>[multiple-files]</td><td>✅</td><td>164ms</td></tr>
   <tr><td>Drop Rejects Files During Processing</td><td>✅</td><td>227ms</td></tr>
   <tr><td>Thread Process</td><td>✅</td><td>458ms</td></tr>
   <tr><td>Load Setting Restores Values</td><td>✅</td><td>251ms</td></tr>
   <tr><td>Load Setting Invalid Json</td><td>✅</td><td>222ms</td></tr>
   <tr><td>On Load Setting</td><td>✅</td><td>210ms</td></tr>
   <tr><td>Reset Setting</td><td>✅</td><td>267ms</td></tr>
   <tr><td>Clean Layer</td><td>✅</td><td>484ms</td></tr>
   <tr><td>Reset Layer</td><td>✅</td><td>253ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Reset Layer Error — 2 cas</button></td><td>✅ 2/2</td><td>289ms</td></tr>
   <tr class="test-variant"><td>[unreadable-stack]</td><td>✅</td><td>139ms</td></tr>
   <tr class="test-variant"><td>[selection-failed]</td><td>✅</td><td>150ms</td></tr>
   <tr><td>Add Detection Layers</td><td>✅</td><td>917ms</td></tr>
   <tr><td>Get Actual Image</td><td>✅</td><td>246ms</td></tr>
   <tr><td>Preview</td><td>✅</td><td>629ms</td></tr>
   <tr><td>Preview Fit Error</td><td>✅</td><td>142ms</td></tr>
   <tr><td>Preview Plane Filter Uses Stack Plane</td><td>✅</td><td>513ms</td></tr>
   <tr><td>Auto Threshold</td><td>✅</td><td>254ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Filters Button</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span><br>[14-10-2026 11:21:20] Log opened : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_filters_button0\stack_PALM_Tracer\log-20261014_112120.log<br>[14-10-2026 11:21:20] Start Processing.<br>[14-10-2026 11:21:20] Output folder: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_filters_button0\stack_PALM_Tracer<br>[14-10-2026 11:21:20] Meta file saved.<br>[14-10-2026 11:21:20] Settings saved.<br>[14-10-2026 11:21:20] Localization enabled.<br>[14-10-2026 11:21:20] 	Saving the localization file (455 localization(s) found).<br>[14-10-2026 11:21:20] Beads Extraction disabled.<br>[14-10-2026 11:21:20] Tracking disabled.<br>[14-10-2026 11:21:20] Blinking Reconnection disabled.<br>[14-10-2026 11:21:20] Track Analysis disabled.<br>[14-10-2026 11:21:20] Gallery generation disabled.<br>[14-10-2026 11:21:20] Graphical visualization disabled.<br>[14-10-2026 11:21:20] High-resolution visualization disabled.<br>[14-10-2026 11:21:20] Processing complete.<br>[14-10-2026 11:21:20] Log closed : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_filters_button0\stack_PALM_Tracer\log-20261014_112120.log<br>{'reset': &lt;PySide6.QtWidgets.QPushButton(0x24c90588e00) at 0x0000024C8BF42D40&gt;, 'update': &lt;PySide6.QtWidgets.QPushButton(0x24c90587100) at 0x0000024C8BC74540&gt;, 'save': &lt;PySide6.QtWidgets.QPushButton(0x24c905872d0) at 0x0000024C8BC743C0&gt;}<br>[14-10-2026 11:21:20] Log opened : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_filters_button0\stack_PALM_Tracer\log-20261014_112120.log<br>[14-10-2026 11:21:20] Start Processing.<br>[14-10-2026 11:21:20] Output folder: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_filters_button0\stack_PALM_Tracer<br>[14-10-2026 11:21:20] Meta file saved.<br>[14-10-2026 11:21:20] Settings saved.<br>- Activate : True<br>- Save : False<br>- Plane : Activate [1, 5]<br>- ROI : 1<br>- Localization :<br>  - Activate : True<br>  - Z : Deactivate [-2000, 2000]<br>  - Intensity : Deactivate [0, 10000000]<br>  - Sigma X : Deactivate [0, 10]<br>  - Sigma Y : Deactivate [0, 10]<br>  - Circularity : Deactivate [0, 1.0]<br>  - Theta : Deactivate [-90, 90]<br>  - MSE XY : Deactivate [0, 1.0]<br>  - MSE Z : Deactivate [0, 1.0]<br>- Tracks :<br>  - Activate : True<br>  - Track : <br>  - Length : Deactivate [1, 10]<br>  - Time Inside ROI : Deactivate [0, 100]<br>  - Instant D : Deactivate [-5, 5]<br>  - D Coeff : Deactivate [-5, 5]<br>  - Alpha : Deactivate [-10, 10]<br>  - Speed : Deactivate [0, 1.0]<br>  - Confinement : Deactivate [-10, 10]<br>[14-10-2026 11:21:20] Localization load previous result (Timestamp : 20261014_112120).<br><br>[14-10-2026 11:21:20] 	File 'localizations-20261014_112120.csv' loaded successfully, 455 row(s) found.<br>[14-10-2026 11:21:20] 		Filtering of file 242 row(s) instead of 455: 213 deletion(s).<br>[14-10-2026 11:21:20] Beads Extraction disabled.<br>[14-10-2026 11:21:20] Tracking disabled.<br>[14-10-2026 11:21:20] Blinking Reconnection disabled.<br>[14-10-2026 11:21:20] Track Analysis disabled.<br>[14-10-2026 11:21:20] Gallery generation disabled.<br>[14-10-2026 11:21:20] Graphical visualization disabled.<br>[14-10-2026 11:21:20] High-resolution visualization disabled.<br>[14-10-2026 11:21:20] Processing complete.<br>[14-10-2026 11:21:20] Log closed : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_filters_button0\stack_PALM_Tracer\log-20261014_112120.log</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Thread Process</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span><br>[14-10-2026 11:21:21] Log opened : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_thread_process0\stack_PALM_Tracer\log-20261014_112121.log<br>[14-10-2026 11:21:21] Start Processing.<br>[14-10-2026 11:21:21] Output folder: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_thread_process0\stack_PALM_Tracer<br>[14-10-2026 11:21:21] Meta file saved.<br>[14-10-2026 11:21:21] Settings saved.<br>[14-10-2026 11:21:21] Localization disabled.<br>[14-10-2026 11:21:21] Beads Extraction disabled.<br>[14-10-2026 11:21:21] Tracking disabled.<br>[14-10-2026 11:21:21] Blinking Reconnection disabled.<br>[14-10-2026 11:21:21] Track Analysis disabled.<br>[14-10-2026 11:21:21] Gallery generation disabled.<br>[14-10-2026 11:21:21] Graphical visualization disabled.<br>[14-10-2026 11:21:21] High-resolution visualization disabled.<br>[14-10-2026 11:21:21] Processing complete.<br>[14-10-2026 11:21:21] Log closed : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_thread_process0\stack_PALM_Tracer\log-20261014_112121.log<br>Auto Threshold: 63.95</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Get Actual Image</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Preview Plane Filter Uses Stack Plane</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">No valid settings file to load.</span><span style="font-weight: bold"></span><br>Preview of plane 4 : 46 detected points (46 on the current frame, 0 on the previous frame, 0 on the next frame).<br>Preview of plane 4 : 142 detected points (46 on the current frame, 48 on the previous frame, 48 on the next frame).<br>Preview of plane 4 : 142 detected points (46 on the current frame, 48 on the previous frame, 48 on the next frame).<br>Preview of plane 4 : 142 detected points (46 on the current frame, 48 on the previous frame, 48 on the next frame).</pre>
   </details>

Ui Resultsui
^^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Creation</td><td>✅</td><td>7ms</td></tr>
   <tr><td>Update Status</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">File Display — 3 cas</button></td><td>✅ 3/3</td><td>22ms</td></tr>
   <tr class="test-variant"><td>[tiff-file]</td><td>✅</td><td>8ms</td></tr>
   <tr class="test-variant"><td>[multiple-suffixes]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[no-extension]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Update Results Folder — 4 cas</button></td><td>✅ 4/4</td><td>29ms</td></tr>
   <tr class="test-variant"><td>[existing-folder]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[missing-folder]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[file-instead-of-folder]</td><td>✅</td><td>7ms</td></tr>
   <tr class="test-variant"><td>[unset-folder]</td><td>✅</td><td>7ms</td></tr>
   </tbody>
   </table>

Ui Viewer3D
^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>28ms</td></tr>
   <tr><td>Viewer3D</td><td>✅</td><td>46ms</td></tr>
   </tbody>
   </table>

Ui Viewerhr
^^^^^^^^^^^

.. raw:: html

   <table class="docutils align-default test-results">
   <thead><tr><th>Test Name / Parameters</th><th>Status</th><th>Duration</th></tr></thead>
   <tbody>
   <tr><td>Widget Creation</td><td>✅</td><td>88ms</td></tr>
   <tr><td>Layer Styles Follow Shared Configuration</td><td>✅</td><td>321ms</td></tr>
   <tr><td>Results Status Automatic Update</td><td>✅</td><td>111ms</td></tr>
   <tr><td>Widget Double Creation</td><td>✅</td><td>408ms</td></tr>
   <tr><td>Stack Drop Loads Latest Results And Actualizes</td><td>✅</td><td>147ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Drop Rejects Multiple Urls — 2 cas</button></td><td>✅ 2/2</td><td>287ms</td></tr>
   <tr class="test-variant"><td>[multiple-files]</td><td>✅</td><td>148ms</td></tr>
   <tr class="test-variant"><td>[local-and-remote]</td><td>✅</td><td>139ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Stack Drop Loads Latest Results From Dropped Stack — 6 cas</button></td><td>✅ 6/6</td><td>2.15s</td></tr>
   <tr class="test-variant"><td>[standalone-hr-only-one]</td><td>✅</td><td>228ms</td></tr>
   <tr class="test-variant"><td>[standalone-hr-each-file]</td><td>✅</td><td>212ms</td></tr>
   <tr class="test-variant"><td>[standalone-hr-all-in-one]</td><td>✅</td><td>199ms</td></tr>
   <tr class="test-variant"><td>[shared-main-widget-only-one]</td><td>✅</td><td>500ms</td></tr>
   <tr class="test-variant"><td>[shared-main-widget-each-file]</td><td>✅</td><td>512ms</td></tr>
   <tr class="test-variant"><td>[shared-main-widget-all-in-one]</td><td>✅</td><td>499ms</td></tr>
   <tr><td>Stack Drop Preserves Active Load Context</td><td>✅</td><td>147ms</td></tr>
   <tr><td>Stack Drop Releases Load Guard After Error</td><td>✅</td><td>154ms</td></tr>
   <tr><td>Check Beads</td><td>✅</td><td>128ms</td></tr>
   <tr><td>Add Stack</td><td>✅</td><td>425ms</td></tr>
   <tr><td>Actualize</td><td>✅</td><td>85ms</td></tr>
   <tr><td>Save</td><td>✅</td><td>90ms</td></tr>
   <tr><td>Screenshot</td><td>✅</td><td>1.28s</td></tr>
   <tr><td>Change Type</td><td>✅</td><td>91ms</td></tr>
   <tr><td>Generate Bad</td><td>✅</td><td>103ms</td></tr>
   <tr><td>Generate</td><td>✅</td><td>320ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Generate Filtered Points — 8 cas</button></td><td>✅ 8/8</td><td>2.32s</td></tr>
   <tr class="test-variant"><td>[keep-beads-raw-2d]</td><td>✅</td><td>259ms</td></tr>
   <tr class="test-variant"><td>[keep-beads-raw-z-stack]</td><td>✅</td><td>286ms</td></tr>
   <tr class="test-variant"><td>[keep-beads-corrected-2d]</td><td>✅</td><td>264ms</td></tr>
   <tr class="test-variant"><td>[keep-beads-corrected-z-stack]</td><td>✅</td><td>258ms</td></tr>
   <tr class="test-variant"><td>[remove-beads-raw-2d]</td><td>✅</td><td>283ms</td></tr>
   <tr class="test-variant"><td>[remove-beads-raw-z-stack]</td><td>✅</td><td>269ms</td></tr>
   <tr class="test-variant"><td>[remove-beads-corrected-2d]</td><td>✅</td><td>333ms</td></tr>
   <tr class="test-variant"><td>[remove-beads-corrected-z-stack]</td><td>✅</td><td>369ms</td></tr>
   <tr class="test-group"><td><button type="button" aria-expanded="true">Generate Clears Filtered Points In Other Modes — 2 cas</button></td><td>✅ 2/2</td><td>1.03s</td></tr>
   <tr class="test-variant"><td>[tracking]</td><td>✅</td><td>561ms</td></tr>
   <tr class="test-variant"><td>[rotation]</td><td>✅</td><td>466ms</td></tr>
   <tr><td>Generate Preserves Render Limits</td><td>✅</td><td>518ms</td></tr>
   <tr><td>Generate Restores Box Without Image</td><td>✅</td><td>1.57s</td></tr>
   <tr><td>Generate Render And Roi Transitions</td><td>✅</td><td>9.05s</td></tr>
   <tr><td>Rotation Preserves Hidden Roi</td><td>✅</td><td>853ms</td></tr>
   <tr><td>Visualization Layer Rgb Transitions</td><td>✅</td><td>265ms</td></tr>
   </tbody>
   </table>

.. raw:: html

   <details>
      <summary>Log Test : Stack Drop Loads Latest Results From Dropped Stack [standalone-hr-only-one]</summary>
      <pre>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r5\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r5\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Stack Drop Loads Latest Results From Dropped Stack [standalone-hr-each-file]</summary>
      <pre>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r6\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r6\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Stack Drop Loads Latest Results From Dropped Stack [standalone-hr-all-in-one]</summary>
      <pre>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r7\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r7\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Stack Drop Loads Latest Results From Dropped Stack [shared-main-widget-only-one]</summary>
      <pre>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r8\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r8\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).<br>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r8\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r8\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Stack Drop Loads Latest Results From Dropped Stack [shared-main-widget-each-file]</summary>
      <pre>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r9\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r9\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).<br>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r9\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r9\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Stack Drop Loads Latest Results From Dropped Stack [shared-main-widget-all-in-one]</summary>
      <pre>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r10\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r10\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).<br>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r10\dropped_PALM_Tracer\settings-20260102_000000.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_stack_drop_loads_latest_r10\dropped_PALM_Tracer' folder with the timestamp 20260102_000000.<br>	File 'localizations' loaded successfully.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).</pre>
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

   <details>
      <summary>Log Test : Generate Render And Roi Transitions</summary>
      <pre>[14-10-2026 11:21:38] Log opened : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_generate_render_and_roi_t0\stack_PALM_Tracer\log-20261014_112138.log<br>[14-10-2026 11:21:38] Start Processing.<br>[14-10-2026 11:21:38] Output folder: C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_generate_render_and_roi_t0\stack_PALM_Tracer<br>[14-10-2026 11:21:38] Meta file saved.<br>[14-10-2026 11:21:38] Settings saved.<br>[14-10-2026 11:21:38] Localization disabled.<br>[14-10-2026 11:21:38] Beads Extraction disabled.<br>[14-10-2026 11:21:38] Tracking disabled.<br>[14-10-2026 11:21:38] Blinking Reconnection disabled.<br>[14-10-2026 11:21:38] Track Analysis disabled.<br>[14-10-2026 11:21:38] Gallery generation disabled.<br>[14-10-2026 11:21:38] Graphical visualization disabled.<br>[14-10-2026 11:21:38] High-resolution visualization disabled.<br>[14-10-2026 11:21:38] Processing complete.<br>[14-10-2026 11:21:38] Log closed : C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_generate_render_and_roi_t0\stack_PALM_Tracer\log-20261014_112138.log<br>Loading setting file 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_generate_render_and_roi_t0\stack_PALM_Tracer\settings-20261014_112138.json'.<br>	Loading files from the 'C:\Users\tmonseigne\AppData\Local\Temp\pytest-of-tmonseigne\pytest-182\test_generate_render_and_roi_t0\stack_PALM_Tracer' folder with the timestamp 20261014_112138.<br>	File 'localizations' not found.<br>	File 'localizations_filtered' not found.<br>	File 'localizations_corrected' not found.<br>	File 'localizations_corrected_filtered' not found.<br>	File 'beads' not found.<br>	File 'tracking' not found.<br>	File 'tracking_filtered' not found.<br>	File 'tracking_reconnected' not found.<br>	File 'tracking_reconnected_filtered' not found.<br>	File 'tracking_MSD' not found.<br>	File 'tracking_MSD_filtered' not found.<br>	File 'tracking_InstantD' not found.<br>	File 'tracking_InstantD_filtered' not found.<br>	File 'tracking_Fit' not found.<br>	File 'tracking_Fit_filtered' not found.<br>	Stack loaded successfully (size: (10, 128, 256)).</pre>
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
