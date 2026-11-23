# OptiComm Lab — Animated Web App V2

**PBL Title:** Optical Signal Transmission & Visualization Using Python

OptiComm Lab is an interactive web application for simulating an optical communication link. It combines a Flask/Python simulation backend with a responsive HTML/CSS/JavaScript dashboard and animated optical transmission visuals.

## V2 Highlights

- Live animated transmission pipeline: Signal Generator → Optical TX → Fiber → Optical RX → Recovered Signal
- Moving optical particles and fiber beam animation
- Animated metric counters for loss, received power, SNR and BER
- Live link-health, received-power and noise-impact meters
- Quick experiment presets: Ideal Link, Balanced, Noisy Channel and Long Distance
- Interactive Chart.js waveform and engineering analysis charts
- Engineering interpretation generated from experiment parameters
- Local experiment history using browser localStorage
- Latest-vs-previous experiment comparison
- CSV export
- Print / Save as PDF using the browser print dialog
- Responsive layout for desktop and mobile
- ECE-focused theory and methodology section

## Architecture

```text
Browser UI
   ↓
HTML + CSS + JavaScript
   ↓
Flask REST API
   ↓
Python / NumPy Simulation Engine
   ↓
Signal Generation → Fiber Loss → Noise → Receiver Recovery
   ↓
JSON Results
   ↓
Interactive Charts + Metrics + Live Analysis
```

## Technology Stack

- Python
- Flask
- NumPy
- HTML5
- CSS3
- JavaScript
- Chart.js
- Browser LocalStorage

## Project Structure

```text
optical_signal_webapp/
├── app.py
├── simulation.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Run Locally on Windows PowerShell

### 1. Open the project

```powershell
cd C:\Users\ankul\Downloads\optical_signal_webapp
```

### 2. Activate the virtual environment

If your environment is named `.venv`:

```powershell
.\.venv\Scripts\Activate.ps1
```

If it is named `venv`:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the server

```powershell
python app.py
```

### 5. Open the app

```text
http://127.0.0.1:5000
```

## Main Experiments

### Digital Signal

Generates random binary information and evaluates the recovered bits using BER.

### Sine Signal

Generates a continuous sinusoidal signal and shows its degradation through the optical channel.

### Square Signal

Generates a square waveform for observing channel attenuation and noise effects.

## Engineering Parameters

### Fiber Loss

```text
Loss(dB) = α × L
```

where `α` is attenuation in dB/km and `L` is fiber length in km.

### Received Power

```text
Pr = Pt × 10^(-Loss/10)
```

### SNR

```text
SNR(dB) = 10 log10(Psignal / Pnoise)
```

### BER

```text
BER = Incorrect Bits / Total Bits
```

## PBL Demonstration Flow

For a live demonstration, start with **Ideal Link**, then run **Balanced**, then **Noisy Channel** and finally **Long Distance**. Compare the resulting SNR, BER, received power and waveform changes.

This makes the effect of optical attenuation and channel noise easy to explain during a PBL presentation or viva.

## Educational Note

This project is an educational simulation. It models important optical communication concepts but is not a replacement for a physical optical transmitter, receiver or laboratory measurement system.
