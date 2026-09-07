# Real-Time ECG Signal Processing & HRV Extraction Pipeline

A Python-based digital signal processing (DSP) pipeline designed to ingest noisy physiological data, isolate the QRS complex, and calculate clinical-grade Heart Rate Variability (HRV) metrics.

## The Engineering Problem
Raw electrocardiogram (ECG) data acquired from medical sensors is inherently corrupted by baseline wander (patient respiration) and high-frequency noise (powerline interference and muscle tremors). Before diagnostic algorithms can analyze the heartbeat, the signal must be digitally filtered without distorting the underlying morphology of the cardiac wave.

## Solution Architecture
This module programmatically fetches raw waveform data from the PhysioNet MIT-BIH Arrhythmia Database and applies the following pipeline:

1. **Digital Filtering:** Applies a 0.5Hz – 40Hz Zero-Phase Butterworth Bandpass Filter (`scipy.signal.filtfilt`). Zero-phase filtering is critical to prevent time-shifting of the QRS complex.
2. **Topological Feature Extraction:** Detects R-peaks using amplitude thresholds and physiological distance constraints (preventing false positives from T-waves or physiological impossibilities).
3. **Clinical Metrics:** Derives instantaneous Heart Rate (BPM) and Heart Rate Variability (HRV) using the RMSSD (Root Mean Square of Successive Differences) time-domain metric.
4. **Data Visualization:** Generates a synchronized dual-plot visualizing the morphological ECG alongside an HRV Tachogram.

## Tech Stack
* **Language:** Python 3
* **DSP & Math:** `SciPy`, `NumPy`
* **Physiological Data:** `wfdb` (Waveform Database package)
* **Visualization:** `Matplotlib`

## Installation and Execution

1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/ecg-pipeline-hrv.git](https://github.com/YourUsername/ecg-pipeline-hrv.git)