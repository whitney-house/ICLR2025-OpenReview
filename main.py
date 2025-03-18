"""
run fetch-data, analyse and plot here
"""
from fetch_data import Fetcher
from analyse import Analyser
from plot import BarPlot
from constants import ICLR_SUBMISSION_INVITATION

# define the data fetcher, analyser, plotter, file path
fetcher = Fetcher()
filepath = "data/papers.csv"
submissions = fetcher.fetch_papers(ICLR_SUBMISSION_INVITATION)
fetcher.process_papers(submissions, filepath)

# get the top data
analyser = Analyser(filepath)
top_institutions = analyser.top_calculations('Affiliations', k=10)
top_authors = analyser.top_calculations("Authors", k=10)

# plot and save
bar_plot = BarPlot()
bar_plot.plot(top_institutions, "Top 10 Institutions", save_path="plots/institutions.png")
bar_plot.plot(top_authors, "Top 10 Authors", save_path="plots/authors.png")
