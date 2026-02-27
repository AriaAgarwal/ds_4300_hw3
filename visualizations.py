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
        data = fda.get_drugs_by_outcome(limit, most_frequent=True, outcome=outcome_code)
        drugs = [d["drug"] for d in data]
        counts = [d["fatal_count"] for d in data]
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

    return drugs, counts

def create_visualizations(fda):

    recovered = fda.get_drugs_by_outcome(10, True, "1")
    print("HIIII API CALL", recovered)
    fatal = fda.get_drugs_by_outcome(10, True, "5")
    #print(fatal)

    common_reactions = fda.get_common_reactions_by_sex(10)
    #print(common_reactions)

    outcomes_by_age = fda.get_outcomes_by_age_bucket(10)
    #print(outcomes_by_age)

    drugs, counts = plot_drugs_by_outcome(fda, limit=10)
    print("HI DRUGS:", drugs)
    print("HI COUNTS:", counts)


def main():
    fda = FDA_API()
    create_visualizations(fda)


if __name__ == "__main__":
    main()