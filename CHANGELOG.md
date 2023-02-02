# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.1.2 (2023-02-02)

### Fixed

- Log message of `LoggedStopper` caused `FormatError`

## 1.1.1 (2023-01-31)

### Fixed

- Log message of `ThresholdTrialStopper` exchanged above/below

## 1.1.0 (2023-01-30)

### Deprecated

- All stoppers are now imported directly from `rt_stoppers_contrib`

## Added

- All stoppers now show a log message when stopping trials or experiments
- `LoggedStopper` to add logging to existing stoppers
- `NoImprovementTrialStopper` now accepts epoch-dependent settings
