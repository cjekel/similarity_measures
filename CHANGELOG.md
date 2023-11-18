# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2023-11-18

### Changed
- `curve_length_measure` now supports curves with negative means! Thanks to a contribution by [Schmetzler](https://github.com/Schmetzler) in [PR37](https://github.com/cjekel/similarity_measures/pull/37)

## [1.0.0] - 2023-10-07

### Changed
- `area_between_two_curves` now correctly calculates the area of four points that form a triangle (where two of the four points are the same). Thanks to a contribution by [mcnick](https://github.com/mcnick) in [PR35](https://github.com/cjekel/similarity_measures/pull/35). Note that this change may result in different area values from previous versions. Cases where this will happen is if one curve had a perfectly straight line between three points, or if one curve had the exact same data point twice.

## [0.7.0] - 2023-01-14

### Changed

- `frechet_dist` now uses scipy cdist to calculate the distances between points
-  `frechet_dist` should be significantly faster due to cdist thanks to a contribution by [nucccc](https://github.com/nucccc)

## [0.6.0] - 2022-10-08
### Changed
- `similaritymeasures.pcm` now produces different values! This was done to better follow the original algorithm. To get the same results from previous versions, set `norm_seg_length=True`. What this option does is scale each segment length by the maximum values of the curve (borrowed from the `curve_length_measure`). This scaling should not be needed with the PCM method because both curves are always scaled initially.
- Fix docstring documentation for returns in `similaritymeasures.dtw` and `similaritymeasures.curve_length_measure`

## [0.5.0] - 2022-08-06
### Added
- Added mean absolute error as `similaritymeasures.mae` thanks to a contribution by [HarshRaoD](https://github.com/HarshRaoD)
- Added mean squared error as `similaritymeasures.mse` thanks to a contribution by [HarshRaoD](https://github.com/HarshRaoD)

## [0.4.4] - 2020-08-25
### Changed
- fix bug where similaritymeasures wouldn't install on certain systems due to Python's default locale based encodings
- new version.py to handling single source versioning
### Removed
- setuptools is no longer a runtime dependency

## [0.4.3] - 2020-02-06
### Changed
- Fix paper citation had the incorrect month and year.

## [0.4.2] - 2019-12-21
### Changed
- There was bug in testing for a complex quadrilateral that made me incorrectly change the is_simple_quad function. This bug has existed in the area function since August, and should be fixed now. Thanks to @aanchalMongia for the detailed report in https://github.com/cjekel/similarity_measures/issues/7 .

## [0.4.1] - 2019-12-20
### Changed
- Fix bug in simple quad check; simple quads occur with two or four positive cross products, or with two or four negative cross products.

## [0.4.0] - 2019-11-13
### Added
- setuptools is now a requirement
- online docs [here](https://jekel.me/similarity_measures/index.html)
### Changed
- Fréchet distance now uses an iterative dynamic programming algorithm (Thanks to Sen ZHANG https://github.com/SenZHANG-GitHub). The performance improvements were briefly studied in this [notebook](https://github.com/cjekel/similarity_measures/blob/master/frechet_distance_recursion_vs_dp.ipynb). 

## [0.3.4] - 2019-08-18
### Changed
- fixed bug in is_simple_quad(), which would sometimes return the incorrect value
- fixed bug in pcm() when a and b where swapped based on arc_length

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
