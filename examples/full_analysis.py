# ruff: noqa
from pykeedy import VMS
from pykeedy.analyze import run_full_analysis

# run_full_analysis is an extremely powerful function that can run any combination of analyses on all of the available manuscripts
# respective example files noted below
# run_full_analysis(
#     voynich=VMS.get(),  # Any Manuscript object
#     comparison_texts_dir=None,  # None means use default corpus, see load_corpus.py
#     comparison_text_names=None,  # text names to filter to
#     output_dir="../full_analysis",
#     add_encrypted=True,  # naibbe_entropy.py
#     run_entropy=True,  # entropy_comparison.py
#     run_ngram_freqs=True,  # char_and_word_ngram_freqs.py
#     ngram_max_n=3,  # " "
#     run_cooccurence=True,  # char_and_word_cooccurrence_heatmap.py
#     run_word_lengths=True,  # word_length.py
#     run_positions=True,  # word_positions.py
# )
# This will apply all of these analyses to the VMS + all available plaintexts,
# and save all the resulting pngs in a folder called "full_analysis_results",
# along with a manifest.json file that can then be parsed to display the results in any format
# Takes about 45 seconds to run with current corpus of 4 manuscripts

from pykeedy.parse_analysis import analysis_to_md  #
# Here is one such parser

analysis_to_md(
    manifest_path="../full_analysis/manifest.json",
    output_markdown_fname="../analysis_summary.md",
    md_to_imgs_path="./full_analysis",
)
# So running this file from inside the 'examples directory will
# re-generate both '/full_analysis' and 'analysis_summary.md'.
# (minus minor changes made to 'analysis_summary.md' for clarity)
