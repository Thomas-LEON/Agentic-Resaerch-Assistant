# Research Report on large language models

## arXiv Papers

### Lost in Translation: Large Language Models in Non-English Content
  Analysis

  In recent years, large language models (e.g., Open AI's GPT-4, Meta's LLaMa,
Google's PaLM) have become the dominant approach for building AI systems to
analyze and generate language online. However, the automated systems that
increasingly mediate our interactions online -- such as chatbots, content
moderation systems, and search engines -- are primarily designed for and work
far more effectively in English than in the world's other 7,000 languages.
Recently, researchers and technology companies have attempted to extend the
capabilities of large language models into languages other than English by
building what are called multilingual language models.
  In this paper, we explain how these multilingual language models work and
explore their capabilities and limits. Part I provides a simple technical
explanation of how large language models work, why there is a gap in available
data between English and other languages, and how multilingual language models
attempt to bridge that gap. Part II accounts for the challenges of doing
content analysis with large language models in general and multilingual
language models in particular. Part III offers recommendations for companies,
researchers, and policymakers to keep in mind when considering researching,
developing and deploying large and multilingual language models.


### Cedille: A large autoregressive French language model

  Scaling up the size and training of autoregressive language models has
enabled novel ways of solving Natural Language Processing tasks using zero-shot
and few-shot learning. While extreme-scale language models such as GPT-3 offer
multilingual capabilities, zero-shot learning for languages other than English
remain largely unexplored. Here, we introduce Cedille, a large open source
auto-regressive language model, specifically trained for the French language.
Our results show that Cedille outperforms existing French language models and
is competitive with GPT-3 on a range of French zero-shot benchmarks.
Furthermore, we provide an in-depth comparison of the toxicity exhibited by
these models, showing that Cedille marks an improvement in language model
safety thanks to dataset filtering.


### How Good are Commercial Large Language Models on African Languages?

  Recent advancements in Natural Language Processing (NLP) has led to the
proliferation of large pretrained language models. These models have been shown
to yield good performance, using in-context learning, even on unseen tasks and
languages. They have also been exposed as commercial APIs as a form of
language-model-as-a-service, with great adoption. However, their performance on
African languages is largely unknown. We present a preliminary analysis of
commercial large language models on two tasks (machine translation and text
classification) across eight African languages, spanning different language
families and geographical areas. Our results suggest that commercial language
models produce below-par performance on African languages. We also find that
they perform better on text classification than machine translation. In
general, our findings present a call-to-action to ensure African languages are
well represented in commercial large language models, given their growing
popularity.


### Goldfish: Monolingual Language Models for 350 Languages

  For many low-resource languages, the only available language models are large
multilingual models trained on many languages simultaneously. However, using
FLORES perplexity as a metric, we find that these models perform worse than
bigrams for many languages (e.g. 24% of languages in XGLM 4.5B; 43% in BLOOM
7.1B). To facilitate research that focuses on low-resource languages, we
pre-train and release Goldfish, a suite of monolingual autoregressive
Transformer language models up to 125M parameters for 350 languages. The
Goldfish reach lower FLORES perplexities than BLOOM, XGLM, and MaLA-500 on 98
of 204 FLORES languages, despite each Goldfish model being over 10x smaller.
However, the Goldfish significantly underperform larger multilingual models on
reasoning benchmarks, suggesting that for low-resource languages,
multilinguality primarily improves general reasoning abilities rather than
basic text generation. We release models trained on 5MB (350 languages), 10MB
(288 languages), 100MB (166 languages), and 1GB (83 languages) of text data
where available. The Goldfish models are available as baselines, fine-tuning
sources, or augmentations to existing models in low-resource NLP research, and
they are further useful for crosslinguistic studies requiring maximally
comparable models across languages.


### Modelling Language

  This paper argues that large language models have a valuable scientific role
to play in serving as scientific models of a language. Linguistic study should
not only be concerned with the cognitive processes behind linguistic
competence, but also with language understood as an external, social entity.
Once this is recognized, the value of large language models as scientific
models becomes clear. This paper defends this position against a number of
arguments to the effect that language models provide no linguistic insight. It
also draws upon recent work in philosophy of science to show how large language
models could serve as scientific models.
