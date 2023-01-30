<div align="center">

# Additional stoppers for ray tune

![logo](https://user-images.githubusercontent.com/13602468/207724747-2f86dc4d-0c09-4d8f-9e7f-37614a0dab9d.png)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-BADGE:END -->
<!-- [![Documentation Status](https://readthedocs.org/projects/ray-tune-stoppers-contrib/badge/?version=latest)](https://ray-tune-stoppers-contrib.readthedocs.io/) -->
<!-- [![Pypi status](https://badge.fury.io/py/ray-tune-stoppers-contrib.svg)](https://pypi.org/project/ray-tune-stoppers-contrib/) -->

[![Documentation Status](https://readthedocs.org/projects/ray-tune-stoppers-contrib/badge/?version=latest)](https://ray-tune-stoppers-contrib.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/klieret/ray-tune-stoppers-contrib/main.svg)](https://results.pre-commit.ci/latest/github/klieret/ray-tune-stoppers-contrib/main)
[![Python package](https://github.com/klieret/ray-tune-stoppers-contrib/actions/workflows/test.yaml/badge.svg)](https://github.com/klieret/ray-tune-stoppers-contrib/actions/workflows/test.yaml)
[![Check Markdown links](https://github.com/klieret/ray-tune-stoppers-contrib/actions/workflows/check-links.yaml/badge.svg)](https://github.com/klieret/ray-tune-stoppers-contrib/actions/workflows/check-links.yaml)
[![codecov](https://codecov.io/github/klieret/ray-tune-stoppers-contrib/branch/main/graph/badge.svg?token=6MQZ4LODE5)](https://codecov.io/github/klieret/ray-tune-stoppers-contrib)
[![gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![PR welcome](https://img.shields.io/badge/PR-Welcome-%23FF8300.svg)](https://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project)

</div>

## 📝 Description

[Ray tune][ray-tune] is a tool for scalable hyperparameter tuning for machine learning applications.
For intelligent hyperperameter optimization, trials that are performing inadequately should be stopped early.
Part of this can be done by schedulers such as [ASHA][asha-paper], but additional explicit stopping criteria are useful as well.

For example, a trial that has converged and is no longer producing better results, but is still outperforming all other running trials, will not be stopped by ASHA.
Ray tune currently only provides three different stoppers: a plateau stopper, a maximum iterations stopper, and a timeout stopper.

This module aims to foster a greater variety of community maintained contributed stopping mechanisms.

## 📦 Installation

```bash
pip3 install rt_stoppers_contrib
```

## 🔥 Using it

For a full list of the stoppers offered, see the the [documentation][doc-all-stoppers].

Using any of the stoppers is as easy as

```python3
from rt_stoppers_contrib import NoImprovementTrialStopper

tuner = tune.Tuner(
    tune.Trainable,
    tune_config=...,
    run_config=air.RunConfig(stop=NoImprovementTrialStopper("my_metric"))
)
```

For more information, refer to the [documentation][docs].

## 🧰 Development setup

```bash
pip3 install pre-commit
cd <this repository>
pre-commit install
gitmoji -i
```

## 💖 Contributing

Your help is greatly appreciated! Suggestions, bug reports and feature requests are best opened as [github issues](https://github.com/klieret/ray-tune-stoppers-contrib/issues). You are also very welcome to submit a [pull request](https://github.com/klieret/ray-tune-stoppers-contrib/pulls)!

Bug reports and pull requests are credited with the help of the [allcontributors bot](https://allcontributors.org/).

<!-- ## ✨ Contributors -->
<!--  -->
<!-- Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)): -->
<!--  -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!--  -->
<!-- This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome! -->

## ⚖️ License

See [LICENSE](LICENSE.txt) for more information. The logo is built from the official [ray-tune][ray-tune] logo
together with [this stop sign][stop-sign] (CC 4.0).

[ray-tune]: https://docs.ray.io/en/latest/tune/index.html
[asha-paper]: https://arxiv.org/abs/1810.05934
[docs]: https://ray-tune-stoppers-contrib.readthedocs.io/
[stop-sign]: https://commons.wikimedia.org/wiki/File:Stop-sign.jpg
[doc-all-stoppers]: https://ray-tune-stoppers-contrib.readthedocs.io/en/latest/autoapi/rt_stoppers_contrib/index.html
