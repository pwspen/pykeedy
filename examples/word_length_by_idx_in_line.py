from pykeedy import VMS
from pykeedy.utils import barplot
from collections import defaultdict

paragraph_lines = VMS.from_loci(
    [locus for locus in VMS.get().loci if locus.is_paragraph()]
).to_lines()

lines_by_word = [line.split(".") for line in paragraph_lines]

lines_by_word = [line for line in lines_by_word if len(line) > 5]
lengths = [len(line) for line in lines_by_word]
avg_line_length = sum(lengths) / len(lengths)
stddev_line_length = (
    sum((len - avg_line_length) ** 2 for len in lengths) / len(lengths)
) ** 0.5

word_lengths_by_idx = defaultdict(list)

for line in lines_by_word:
    for idx, word in enumerate(line):
        word_lengths_by_idx[idx].append(len(word))

results = {
    idx: sum(lengths) / len(lengths) for idx, lengths in word_lengths_by_idx.items()
}


def custom(plt):
    plt.ylim(3, 6)
    plt.grid(True, axis="y")  # It's plt.grid(), not plt.show_grid()


barplot(
    results,
    ax_names=(
        f"Word Index (Avg num words in line= {avg_line_length:.2f}, stddev= {stddev_line_length:.2f})",
        "Average Length",
    ),
    n_max=int(avg_line_length + stddev_line_length + 5),
    fname="word_length_by_idx_in_line.png",
    customize_fn=custom,
)
