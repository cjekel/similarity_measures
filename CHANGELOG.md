# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2019-08-14
### Changed
- fixed broken links in README !

## [0.3.2] - 2019-08-14
### Changed
- fixed bug in similaritymeasures.dtw_path(), where dtw path would always go from [1, 1] to [0, 0]

## [0.3.1] - 2019-08-08
### Changed
- Repo name shortened to just similarity_measures

## [0.3.0] - 2019-02-07
### Added
- Fréchet distance now supports any minkowski distance!
### Changed
- Fréchet distance now supports N-D data!
- Add notes to Fréchet and DTW about support of N-D data in readme.
### Removed
- euc_dist function has been removed

## [0.2.3] - 2018-12-10
### Changed
- fixed image link in README.rst for pypi.org
- fix unicode Fréchet distance

## [0.2.2] - 2018-12-09
### Changed
- dtw function docstring now specifies number of data points and dimensions

## [0.2.1] - 2018-12-08
### Added
- dtw path function
- dtw function can now take all distance metrics in scipy.spatial.distance.cdist
- add test functions for dtw_path
- add test functions for passing distance metrics in dtw
### Changed
- dtw function now outputs cumulative distance matrix

## [0.2.0] - 2018-12-07
### Added
- dtw function for Dynamic Time warping!
- New test curves for sphere and simple three points
- dtw example fits in notebook
- Changelog
### Changed
- Docstrings now follow numpydoc
- Added dtw examples to README

## [0.1.2] - 2018-12-06
### Changed
- Fix README.rst issues on pypi.org

## [0.1.1] - 2018-07-15
### Added
- Initial project release
