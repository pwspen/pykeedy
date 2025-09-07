from pykeedy.utils import seriesplot, load_corpus
from pykeedy.analysis import length_distribution

# Plot the distribution of word lengths in the VMS

texts = load_corpus(include_vms=True)

tokens = {name: length_distribution(text.to_words()) for name, text in texts.items()}
types = {
    name: length_distribution(set(text.to_words())) for name, text in texts.items()
}

for name, text in texts.items():
    words = text.to_words()
    maxlen = max(len(word) for word in words) if words else 0
    print(name)
    lens_to_print = 5
    while lens_to_print:
        words_this_len = [word for word in words if len(word) == maxlen]
        if words_this_len:
            print(f"len={maxlen}: {words_this_len}")
            lens_to_print -= 1
        maxlen -= 1
    print("\n\n")


def custom(plt):
    plt.yscale("log")
    plt.grid(True, axis="y")


seriesplot(
    tokens,
    ax_names=("Word length", "Count"),
    fname="word_token_lengths.png",
    customize_fn=custom,
)
seriesplot(
    types,
    ax_names=("Word length", "Count"),
    fname="word_type_lengths.png",
    customize_fn=custom,
)
