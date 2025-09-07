from pykeedy.analysis import conditional_entropy
from pykeedy import VMS
from pykeedy.utils import seriesplot, load_corpus
from pykeedy.crypt import naibbe_encrypt_to_object

analyze = load_corpus(include_vms=True)
analyze["naturalis_enc"] = naibbe_encrypt_to_object(
    analyze["naturalis"].to_text(), return_object=True
)

entropies = {
    f"{name}": [
        (n, conditional_entropy(text.to_text(), n, exclude_containing=[".", " ", "\n"]))
        for n in range(1, 20)
    ]
    for name, text in analyze.items()
}
entropies["VMS_cuva"] = [
    (
        n,
        conditional_entropy(
            VMS.to_text(alphabet="cuva"), n, exclude_containing=[".", " ", "\n"]
        ),
    )
    for n in range(1, 20)
]

seriesplot(entropies)
