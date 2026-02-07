import numpy as np

def compute_sa_BNBC2020(Z, site_class, importance=1.0, damping_ratio=5):
    """
    Computes the Design Response Spectrum based on BNBC 2020 Figure 6.2.25 (Page 3195).
    """
    # Exact site-dependent parameters from BNBC Table 6.2.16
    config = {
        "SA": {"S": 1.0,  "TB": 0.05, "TC": 0.25, "TD": 1.2},
        "SB": {"S": 1.2,  "TB": 0.05, "TC": 0.35, "TD": 1.2},
        "SC": {"S": 1.15, "TB": 0.10, "TC": 0.45, "TD": 1.5},
        "SD": {"S": 1.35, "TB": 0.20, "TC": 0.85, "TD": 2.0},
        "SE": {"S": 1.40, "TB": 0.15, "TC": 0.50, "TD": 2.5}
    }
    
    p = config.get(site_class, config["SD"])
    
    # Damping correction factor (eta)
    eta = np.sqrt(10 / (5 + damping_ratio))
    eta = max(eta, 0.55) 

    periods = np.linspace(0.01, 4, 200)
    spectrum = np.zeros_like(periods)
    
    for i, T in enumerate(periods):
        # 4-branch mathematical logic from Figure 6.2.25
        if T <= p['TB']:
            sa = Z * p['S'] * (1 + (T / p['TB']) * (2.5 * eta - 1))
        elif T <= p['TC']:
            sa = 2.5 * Z * p['S'] * eta
        elif T <= p['TD']:
            sa = 2.5 * Z * p['S'] * eta * (p['TC'] / T)
        else:
            sa = 2.5 * Z * p['S'] * eta * (p['TC'] * p['TD'] / T**2)
        
        spectrum[i] = sa * importance
    
    return periods, spectrum