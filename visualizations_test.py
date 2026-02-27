import matplotlib.pyplot as plt
from fda_api import FDA_API

# FDA outcome codes for subplots
outcome_labels = {
    "1": "Recovered / Resolved",
    "2": "Recovering / Resolving",
    "3": "Not Recovered / Not Resolved",
    "4": "Recovered with Sequelae",
    "5": "Fatal",
    "6": "Unknown",
}

def plot_drugs_by_outcome(fda, limit=10):
    """
    plot the top drugs and frequency by reaction outcome
    """
    # create a 2x3 grid of subplots
    fig, axes = plt.subplots(2, 3, figsize=(14, 10))
    axes = axes.flatten()
    # plot each outcome in a subplot
    for i, (outcome_code, title) in enumerate(outcome_labels.items()):
        data = fda.get_fatal_drugs(limit, most_frequent=True, outcome=outcome_code)
        drugs = [d["drug"] for d in data]
        counts = [d["count"] for d in data]
        ax = axes[i]
        ax.bar(range(len(drugs)), counts, color="steelblue", edgecolor="navy", alpha=0.8)
        ax.set_xticks(range(len(drugs)))
        ax.set_xticklabels(drugs, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Frequency")
        ax.set_xlabel("Drug")
        ax.set_title(title)
        ax.tick_params(axis="x", labelsize=7)

    plt.suptitle("Top drugs and frequencyby reaction outcome", fontsize=12, y=1.02)
    plt.tight_layout()
    plt.show()


def create_visualizations(fda):
    plot_drugs_by_outcome(fda, limit=10)


def main():
    fda = FDA_API()
    create_visualizations(fda)


if __name__ == "__main__":
    main()