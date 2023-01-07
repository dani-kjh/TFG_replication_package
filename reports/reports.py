import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
from scipy import stats
from scipy.stats import shapiro
import scikit_posthocs as sp
import cliffs_delta as cd


def generate_summary(data):
    summary_emissions_data = [["", "", "min", "max", "mean", "median", "std"]]
    mult = 1000
    for provider in data:
        new_row = [
            "emissions (g)",
            provider.cloud_provider[0],
            provider.emissions.min() * mult,
            provider.emissions.max() * mult,
            provider.emissions.mean() * mult,
            provider.emissions.median() * mult,
            provider.emissions.std() * mult,
        ]
        summary_emissions_data.append(new_row)
    with open("report_figures/summary_emissions.html", "w") as f:
        f.write(tabulate(summary_emissions_data, headers="firstrow", tablefmt="html"))
    summary_energy_data = [["", "", "min", "max", "mean", "median", "std"]]
    for provider in data:
        new_row = [
            "en (W)",
            provider.cloud_provider[0],
            provider.energy_consumed.min() * mult,
            provider.energy_consumed.max() * mult,
            provider.energy_consumed.mean() * mult,
            provider.energy_consumed.median() * mult,
            provider.energy_consumed.std() * mult,
        ]
        summary_energy_data.append(new_row)
    with open("report_figures/summary_energy.html", "w") as f:
        f.write(tabulate(summary_energy_data, headers="firstrow", tablefmt="html"))


def gen_normality_results(providers):
    sns.set(style="darkgrid")
    my_pal = {"aws": "skyblue", "azure": "olive", "heroku": "gold", "gcp": "teal"}
    df = pd.concat(providers, ignore_index=True)
    violin = sns.violinplot(x="cloud_provider", y="energy_consumed", data=df, scale="width", palette=my_pal)
    figure = violin.get_figure()
    figure.set_size_inches(14, 14)
    figure.savefig("report_figures/normality/violin_comb.png")

    fig, axs = plt.subplots(2, 2, figsize=(16, 12))

    sns.histplot(data=aws, x="emissions", kde=True, color="skyblue", ax=axs[0, 0]).set(title="Aws")
    sns.histplot(data=azure, x="emissions", kde=True, color="olive", ax=axs[0, 1]).set(title="Azure")
    sns.histplot(data=heroku, x="emissions", kde=True, color="gold", ax=axs[1, 0]).set(title="Heroku")
    sns.histplot(data=railway, x="emissions", kde=True, color="teal", ax=axs[1, 1]).set(title="Railway")

    fig.tight_layout()
    fig.savefig("report_figures/normality/histograms.png")

    sns.set(style="darkgrid")
    fig2, axs2 = plt.subplots(2, 2, figsize=(16, 12))

    sns.violinplot(x="cloud_provider", y="emissions", color="skyblue", data=aws, scale="width", ax=axs2[0, 0])
    sns.violinplot(x="cloud_provider", y="emissions", color="olive", data=azure, scale="width", ax=axs2[0, 1])
    sns.violinplot(x="cloud_provider", y="emissions", color="gold", data=heroku, scale="width", ax=axs2[1, 0])
    sns.violinplot(x="cloud_provider", y="emissions", color="teal", data=railway, scale="width", ax=axs2[1, 1])
    fig2.tight_layout()

    fig2.savefig("report_figures/normality/violinplots.png")

    shapiro_results = [
        [
            "",
            "test_stat",
            "p-value",
        ]
    ]
    for provider in providers:
        shapiro_test = shapiro(provider.emissions)
        new_row = [
            provider.cloud_provider[0],
            shapiro_test.statistic,
            shapiro_test.pvalue,
        ]
        shapiro_results.append(new_row)
    with open("report_figures/normality/shapiro.html", "w") as f:
        f.write(tabulate(shapiro_results, headers="firstrow", tablefmt="html"))
    print(tabulate(shapiro_results, headers="firstrow", tablefmt="fancy_grid"))


def test_significance(providers):
    groups = [providers[0].emissions, providers[1].emissions, providers[2].emissions, providers[3].emissions]

    kruskal = stats.kruskal(
        providers[0].emissions, providers[1].emissions, providers[2].emissions, providers[3].emissions
    )

    dunn = sp.posthoc_dunn(groups, p_adjust="bonferroni")
    with open("report_figures/significance/dunn.html", "w") as f:
        f.write(tabulate(dunn, showindex=False, headers=["aws", "azure", "heroku", "railway"], tablefmt="html"))
    cliff = cd.cliffs_delta(providers[2].emissions, providers[3].emissions)
    print(cliff)
    cliff_test = [
        ["aws-azure", cd.cliffs_delta(providers[0].emissions, providers[1].emissions)],
        ["aws-heroku", cd.cliffs_delta(providers[0].emissions, providers[2].emissions)],
        ["aws-railway", cd.cliffs_delta(providers[0].emissions, providers[3].emissions)],
        ["azure-heroku", cd.cliffs_delta(providers[1].emissions, providers[2].emissions)],
        ["azure-railway", cd.cliffs_delta(providers[1].emissions, providers[3].emissions)],
        ["heroku-railway", cd.cliffs_delta(providers[2].emissions, providers[3].emissions)],
    ]
    with open("report_figures/significance/cliff.html", "w") as f:
        f.write(
            tabulate(
                cliff_test,
                showindex=False,
                headers=[
                    "",
                    "test_statistic",
                    "tag",
                ],
                tablefmt="html",
            )
        )


azure = "../results/azure/2023-01-06-13.01.49/API_results.csv"
aws = "../results/aws/2023-01-06-13.05.23/API_results.csv"
railway = "../results/railway//2023-01-06-13.24.06/API_results.csv"
heroku = "../results/heroku/2023-01-06-13.15.31/API_results.csv"


sns.set(style="darkgrid")
azure = pd.read_csv(azure)
aws = pd.read_csv(aws)
heroku = pd.read_csv(heroku)
railway = pd.read_csv(railway)

results = [azure, aws, heroku, railway]

gen_normality_results(results)

test_significance(results)
