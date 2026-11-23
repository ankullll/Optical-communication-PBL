from flask import Flask, render_template, request, jsonify, Response
import io
import csv
import numpy as np

from simulation import run_simulation, power_vs_distance, ber_vs_noise

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/simulate")
def simulate():
    data = request.get_json(force=True)

    signal = data.get("signal", "Digital")
    length = float(data.get("length", 10))
    attenuation = float(data.get("attenuation", 0.2))
    noise = float(data.get("noise", 5))
    power = float(data.get("power", 10))

    if min(length, attenuation, noise, power) < 0:
        return jsonify({"error": "Values cannot be negative."}), 400
    if power == 0:
        return jsonify({"error": "Transmitted power must be greater than zero."}), 400

    result = run_simulation(
        signal_type=signal,
        length_km=length,
        attenuation_db_per_km=attenuation,
        noise_percent=noise,
        transmitted_power_mw=power,
    )

    # Keep the payload reasonably small for the browser.
    max_points = 1200
    idx = np.linspace(0, len(result["t"]) - 1, min(max_points, len(result["t"]))).astype(int)

    payload = {
        "time": result["t"][idx].tolist(),
        "original": result["original"][idx].tolist(),
        "after_fiber": result["after_fiber"][idx].tolist(),
        "noisy_rx": result["noisy_rx"][idx].tolist(),
        "recovered": result["recovered"][idx].tolist(),
        "metrics": {
            "loss_db": result["loss_db"],
            "rx_power_mw": result["rx_power_mw"],
            "snr_db": None if np.isinf(result["snr_db"]) else result["snr_db"],
            "ber": result["ber"],
        },
    }

    distances, powers = power_vs_distance(
        max(50, length * 1.5), 0.5, power, attenuation
    )
    payload["power_curve"] = {
        "distance": distances.tolist(),
        "power": powers.tolist()
    }

    noise_values = np.arange(0, 31, 2.5)
    bers = ber_vs_noise(noise_values, length, attenuation, power, trials=4)
    payload["ber_curve"] = {
        "noise": noise_values.tolist(),
        "ber": [None if np.isnan(x) else float(x) for x in bers]
    }

    return jsonify(payload)


@app.post("/api/export")
def export():
    data = request.get_json(force=True)
    result = run_simulation(
        signal_type=data.get("signal", "Digital"),
        length_km=float(data.get("length", 10)),
        attenuation_db_per_km=float(data.get("attenuation", 0.2)),
        noise_percent=float(data.get("noise", 5)),
        transmitted_power_mw=float(data.get("power", 10)),
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["OptiComm Lab - Experiment Results"])
    writer.writerow(["Signal Type", data.get("signal", "Digital")])
    writer.writerow(["Fiber Length (km)", data.get("length", 10)])
    writer.writerow(["Attenuation (dB/km)", data.get("attenuation", 0.2)])
    writer.writerow(["Noise (%)", data.get("noise", 5)])
    writer.writerow(["Tx Power (mW)", data.get("power", 10)])
    writer.writerow(["Fiber Loss (dB)", result["loss_db"]])
    writer.writerow(["Rx Power (mW)", result["rx_power_mw"]])
    writer.writerow(["SNR (dB)", result["snr_db"]])
    writer.writerow(["BER", result["ber"]])
    writer.writerow([])
    writer.writerow(["Time", "Original", "After Fiber", "Noisy RX", "Recovered"])

    for row in zip(
        result["t"], result["original"], result["after_fiber"],
        result["noisy_rx"], result["recovered"]
    ):
        writer.writerow(row)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=optical_experiment.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)
