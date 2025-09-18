import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# -----------------------------
# Plant Growth Stress Simulator
# -----------------------------

def simulate_growth(days=30, gravity=1.0, radiation=0.0, nutrients=1.0, light=1.0):
    """
    Simulate plant growth under space stressors.
    
    Parameters:
        days (int): number of days to simulate
        gravity (float): 1.0 = Earth, 0.38 = Mars, 0.16 = Moon, 0.0 = microgravity
        radiation (float): 0.0 = none, 1.0 = high radiation
        nutrients (float): 0.0 = no nutrients, 1.0 = full nutrients
        light (float): 0.0 = darkness, 1.0 = full light
    """
    growth = [1.0]  # initial size
    health = 1.0    # plant health (0–1)
    
    for day in range(1, days + 1):
        # Base growth rate
        rate = 0.2 * gravity * nutrients * light
        
        # Radiation reduces health
        health -= 0.01 * radiation
        health = max(0.0, health)
        
        # Growth formula (simple exponential with stress factor)
        new_size = growth[-1] + rate * health * np.random.uniform(0.8, 1.2)
        growth.append(max(new_size, 0.0))
    
    return np.array(growth)


def run_simulation():
    # Define scenarios
    scenarios = {
        "Earth (Control)": {"gravity": 1.0, "radiation": 0.0, "nutrients": 1.0, "light": 1.0},
        "Moon + Radiation": {"gravity": 0.16, "radiation": 0.5, "nutrients": 0.8, "light": 1.0},
        "Mars + Low Nutrients": {"gravity": 0.38, "radiation": 0.2, "nutrients": 0.5, "light": 0.9},
        "ISS Microgravity": {"gravity": 0.0, "radiation": 0.3, "nutrients": 1.0, "light": 1.0}
    }

    results = {}
    days = 30

    # Run each scenario
    for name, params in scenarios.items():
        growth = simulate_growth(days=days, **params)
        results[name] = growth

    # Save results as CSV
    df = pd.DataFrame(results)
    os.makedirs("examples", exist_ok=True)
    df.to_csv("examples/growth_data.csv", index_label="Day")
    print("Simulation data saved to examples/growth_data.csv")

    # Plot results
    plt.figure(figsize=(8, 5))
    for name, growth in results.items():
        plt.plot(range(days + 1), growth, label=name)

    plt.title("Plant Growth Under Spaceflight Stressors")
    plt.xlabel("Days")
    plt.ylabel("Plant Size (relative units)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plot
    plot_path = "examples/growth_curve.png"
    plt.savefig(plot_path)
    plt.show()
    print(f"Growth curve plot saved to {plot_path}")


if __name__ == "__main__":
    run_simulation()
