import numpy as np


def generate_signal(signal_type="Digital", n_bits=40, samples_per_bit=80,
                    frequency=5, duration=1.0, sample_rate=1000):
    if signal_type == "Digital":
        bits = np.random.randint(0, 2, n_bits)
        signal = np.repeat(bits, samples_per_bit).astype(float)
        t = np.arange(len(signal)) / sample_rate
        return t, signal, bits

    t = np.arange(0, duration, 1 / sample_rate)
    if signal_type == "Sine":
        signal = 0.5 * (np.sin(2 * np.pi * frequency * t) + 1)
    elif signal_type == "Square":
        signal = 0.5 * (np.sign(np.sin(2 * np.pi * frequency * t)) + 1)
    else:
        raise ValueError("Unsupported signal type")
    return t, signal, None


def apply_fiber(signal, length_km, attenuation_db_per_km):
    loss_db = length_km * attenuation_db_per_km
    power_factor = 10 ** (-loss_db / 10)
    amplitude_factor = np.sqrt(power_factor)
    return signal * amplitude_factor, loss_db, power_factor


def add_gaussian_noise(signal, noise_percent):
    noise_std = (noise_percent / 100.0) * max(np.std(signal), 1e-9)
    return signal + np.random.normal(0, noise_std, size=signal.shape)


def recover_digital(received, threshold=0.5, samples_per_bit=80):
    bits = []
    recovered = np.zeros_like(received)
    n_bits = len(received) // samples_per_bit

    for i in range(n_bits):
        chunk = received[i * samples_per_bit:(i + 1) * samples_per_bit]
        bit = int(np.mean(chunk) >= threshold)
        bits.append(bit)
        recovered[i * samples_per_bit:(i + 1) * samples_per_bit] = bit
    return recovered, np.array(bits)


def calculate_snr(clean, received):
    noise = received - clean
    signal_power = np.mean(clean ** 2)
    noise_power = np.mean(noise ** 2)
    if noise_power <= 0:
        return float("inf")
    return 10 * np.log10(signal_power / noise_power)


def calculate_ber(original_bits, recovered_bits):
    if original_bits is None or recovered_bits is None:
        return None
    n = min(len(original_bits), len(recovered_bits))
    return float(np.mean(original_bits[:n] != recovered_bits[:n]))


def received_power_mw(tx_power_mw, loss_db):
    return tx_power_mw * 10 ** (-loss_db / 10)


def run_simulation(signal_type="Digital", length_km=10,
                   attenuation_db_per_km=0.2, noise_percent=5,
                   transmitted_power_mw=10):
    t, original, bits = generate_signal(signal_type)
    after_fiber, loss_db, power_factor = apply_fiber(
        original, length_km, attenuation_db_per_km
    )
    noisy_rx = add_gaussian_noise(after_fiber, noise_percent)

    if signal_type == "Digital":
        recovered, recovered_bits = recover_digital(noisy_rx)
    else:
        recovered, recovered_bits = noisy_rx.copy(), None

    snr = calculate_snr(after_fiber, noisy_rx)
    ber = calculate_ber(bits, recovered_bits)

    return {
        "t": t,
        "original": original,
        "after_fiber": after_fiber,
        "noisy_rx": noisy_rx,
        "recovered": recovered,
        "loss_db": loss_db,
        "power_factor": power_factor,
        "snr_db": snr,
        "ber": ber,
        "rx_power_mw": received_power_mw(transmitted_power_mw, loss_db),
    }


def power_vs_distance(max_distance_km, step_km, tx_power_mw, attenuation):
    distances = np.arange(0, max_distance_km + step_km, step_km)
    powers = received_power_mw(tx_power_mw, distances * attenuation)
    return distances, powers


def ber_vs_noise(noise_values, length_km, attenuation, tx_power, trials=4):
    values = []
    for noise in noise_values:
        trial = []
        for _ in range(trials):
            r = run_simulation("Digital", length_km, attenuation, noise, tx_power)
            if r["ber"] is not None:
                trial.append(r["ber"])
        values.append(np.mean(trial) if trial else np.nan)
    return np.array(values)
