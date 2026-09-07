import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks


# --- DSP & Analysis Functions ---

def fetch_ecg(record_name='103', sampto=3000):  # Increased sample slightly for better visualization
    """Downloads an ECG record from PhysioNet."""
    record = wfdb.rdrecord(record_name, sampto=sampto, pn_dir='mitdb')
    raw_signal = record.p_signal[:, 0]
    fs = record.fs
    time = np.arange(raw_signal.size) / fs
    return raw_signal, time, fs


def butter_bandpass_filter(data, fs):
    """Applies a 0.5Hz to 40Hz Butterworth bandpass filter."""
    nyquist = 0.5 * fs
    low, high = 0.5 / nyquist, 40.0 / nyquist
    b, a = butter(4, [low, high], btype='band')
    return filtfilt(b, a, data)


def detect_r_peaks(clean_signal, fs):
    """Finds R-peaks with physiological distance constraints."""
    min_dist = int(0.35 * fs)  # Adjusted slightly for potentially faster heart rates
    peaks, _ = find_peaks(clean_signal, distance=min_dist, height=0.4)
    return peaks


def calculate_clinical_metrics(r_peaks, fs):
    """Calculates instantaneous heart rate and HRV RMSSD."""
    # 1. Heart Rate Calculation
    rr_intervals_sec = np.diff(r_peaks) / fs
    average_bpm = np.mean(60.0 / rr_intervals_sec)

    # 2. HRV Calculation (RMSSD)
    rr_intervals_ms = rr_intervals_sec * 1000
    rmssd = np.sqrt(np.mean(np.diff(rr_intervals_ms) ** 2))

    return rr_intervals_sec, average_bpm, rmssd


# --- Visualization Function ---

def plot_ecg_and_hrv(time, clean_signal, r_peaks, rr_sec):
    """
    Creates a composite visualization: Filtered ECG with Peaks
    and the HRV Tachogram aligned on a shared x-axis.
    """
    # Define how to plot the R-R data against time (align interval to the second beat)
    # We ignore the first beat, because there is no interval before it.
    hrv_time_axis = time[r_peaks[1:]]

    # Initialize the stacked plot area (shared x-axis is critical here)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # --- Top Plot: ECG + R-Peaks ---
    ax1.plot(time, clean_signal, color='#1f77b4', linewidth=1, label='Filtered ECG (0.5-40 Hz)')
    # Marker 'ro' = red circles
    ax1.plot(time[r_peaks], clean_signal[r_peaks], 'ro', markersize=6, label='Detected R-Peaks')

    ax1.set_title('ECG Peak Detection')
    ax1.set_ylabel('Amplitude (mV)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper right')

    # --- Bottom Plot: HRV Tachogram ---
    # We use a 'step' plot here because R-R intervals are discrete events, not smooth data.
    # Convert RR seconds to ms for y-axis
    ax2.step(hrv_time_axis, rr_sec * 1000, where='post', color='#ff7f0e', linewidth=1.5, label='R-R Interval Dynamics')

    # Add scattered points on top of the step line for clarity
    ax2.scatter(hrv_time_axis, rr_sec * 1000, color='#ff7f0e', s=20)

    ax2.set_title('HRV Tachogram (R-R Interval over Time)')
    ax2.set_ylabel('R-R Interval (ms)')
    ax2.set_xlabel('Time (seconds)')
    ax2.grid(True, linestyle='--', alpha=0.7)

    # Set y-axis limits to clearly show variability (typically 600ms to 1200ms for resting adults)
    ax2.set_ylim(600, 1100)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


# --- Main Execution Block ---

if __name__ == "__main__":
    # 1. Fetch, Filter, and Detect
    raw_sig, time, fs = fetch_ecg(record_name='103')  # increased sample slightly
    clean_sig = butter_bandpass_filter(raw_sig, fs)
    r_peaks = detect_r_peaks(clean_sig, fs)

    # 2. Calculate Metrics
    rr_sec, avg_bpm, rmssd = calculate_clinical_metrics(r_peaks, fs)

    # 3. Print Clinical Report to Terminal
    print("\n" + "=" * 30)
    print("=== CLINICAL ECG REPORT ===")
    print("=" * 30)
    print(f"Record Analyzed:  MIT-BIH 103")
    print(f"Total Beats:      {len(r_peaks)}")
    print(f"Average HR:       {avg_bpm:.1f} BPM")
    print(f"HRV (RMSSD):      {rmssd:.1f} ms")
    print("=" * 30 + "\n")

    # 4. Generate Visualization
    print("Generating visualization... close plot window to end program.")
    plot_ecg_and_hrv(time, clean_sig, r_peaks, rr_sec)