# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.1.0

### Deprecated

- ALl stoppers are now imported directly from `rt_stoppers_contrib`

## Added

- `LoggedStopper` to add logging to existing stoppers
- `NoImprovementTrialStopper` now accepts epoch-dependent settings
