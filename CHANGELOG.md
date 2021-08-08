# Changelog

All notable changes to this project will be documented in this file.
## [0.4.0](https://github.com/nkomiya/create-github-project/compare/v0.3.2...v0.4.0) (2021-08-08)


### Features

* add cloud build template files ([#94](https://github.com/nkomiya/create-github-project/issues/94)) ([2f4f9bc](https://github.com/nkomiya/create-github-project/commit/2f4f9bc1e764bebef71174be85eb68313ff7816e))
* add follow up message for cloud build ([#95](https://github.com/nkomiya/create-github-project/issues/95)) ([d125408](https://github.com/nkomiya/create-github-project/commit/d12540876c871f40889e3863195d6b4483629eb8))
* add link style support for google source repository ([#96](https://github.com/nkomiya/create-github-project/issues/96)) ([adf72c2](https://github.com/nkomiya/create-github-project/commit/adf72c20c46d47c5b8b6887004d7cbd7242bdbef))


### Bug Fixes

* `init` command fail on selecting reviewers ([#91](https://github.com/nkomiya/create-github-project/issues/91)) ([7d9a29d](https://github.com/nkomiya/create-github-project/commit/7d9a29d7d7bd62b34bc7a9d3a7730c635c2141a1))

### [0.3.2](https://github.com/nkomiya/create-github-project/compare/v0.3.1...v0.3.2) (2021-07-28)


### Bug Fixes

* process not aborted on press ctrl-c ([#80](https://github.com/nkomiya/create-github-project/issues/80)) ([0ddce86](https://github.com/nkomiya/create-github-project/commit/0ddce86c8de0faf3eeb66fdf203d4a029a68003a))

### [0.3.1](https://github.com/nkomiya/create-github-project/compare/v0.3.0...v0.3.1) (2021-07-28)


### Bug Fixes

* modify case for github templates ([#69](https://github.com/nkomiya/create-github-project/issues/69)) ([105eb4d](https://github.com/nkomiya/create-github-project/commit/105eb4d73591ebb5b12ffbc880e9da27a3c5bf9c))
* release request workflows fail if production branch is main ([#70](https://github.com/nkomiya/create-github-project/issues/70)) ([3472fa6](https://github.com/nkomiya/create-github-project/commit/3472fa660f62a7cd386f447f74a8287a989fda28))

## [0.3.0](https://github.com/nkomiya/create-github-project/compare/v0.2.0...v0.3.0) (2021-07-24)


### Features

* add `update` command ([#47](https://github.com/nkomiya/create-github-project/issues/47)) ([4d7d3cb](https://github.com/nkomiya/create-github-project/commit/4d7d3cb902fce9471d8d403254b45e7915e4ff82))
* add `version` command ([#49](https://github.com/nkomiya/create-github-project/issues/49)) ([52e19d2](https://github.com/nkomiya/create-github-project/commit/52e19d240a1e2369a21a57e279a92b4448adb625))


### Bug Fixes

* wrong git command in follow up message ([#53](https://github.com/nkomiya/create-github-project/issues/53)) ([9376cea](https://github.com/nkomiya/create-github-project/commit/9376cea5267a45670b70c5107bb82607c40f90ff))

## [0.2.0](https://github.com/nkomiya/create-github-project/compare/v0.1.0...v0.2.0) (2021-07-24)


### Features

* allow empty string for list option ([#42](https://github.com/nkomiya/create-github-project/issues/42)) ([cfd6ef2](https://github.com/nkomiya/create-github-project/commit/cfd6ef286f26d42bef459857dd2d5ed3afed5e11))


### Bug Fixes

* `init` command fail if no github accounts are added ([#40](https://github.com/nkomiya/create-github-project/issues/40)) ([f5dca02](https://github.com/nkomiya/create-github-project/commit/f5dca02f13d14f6c5766a8cb761864933097cfd9))
* modify package version ([#38](https://github.com/nkomiya/create-github-project/issues/38)) ([0fca632](https://github.com/nkomiya/create-github-project/commit/0fca63221afa63677e2eef080a81b88660a1dc80))

## 0.1.0 (2021-07-24)


### Features

* add command line interface ([#6](https://github.com/nkomiya/create-github-project/issues/6)) ([5b0855e](https://github.com/nkomiya/create-github-project/commit/5b0855e92410a692e6aecaa73914aaf043a7eb87))
* add description on development in generated readme ([#15](https://github.com/nkomiya/create-github-project/issues/15)) ([f9ba1fa](https://github.com/nkomiya/create-github-project/commit/f9ba1fac7251c5f2b91a3a937e77796ea25d6b69))
* add feature for github account management ([#34](https://github.com/nkomiya/create-github-project/issues/34)) ([72227b5](https://github.com/nkomiya/create-github-project/commit/72227b5f37af989eba8dfacaf0cb4c908c052e1d))
* add issue and pr template ([#18](https://github.com/nkomiya/create-github-project/issues/18)) ([f3e8c05](https://github.com/nkomiya/create-github-project/commit/f3e8c055365ab3c2b7d28fd7eb81513114407792))
* add manage releases with standard-version ([#11](https://github.com/nkomiya/create-github-project/issues/11)) ([8c39b3b](https://github.com/nkomiya/create-github-project/commit/8c39b3bebb10ba75198a315512667d92fd348b35))
* add prompt for production branch ([#7](https://github.com/nkomiya/create-github-project/issues/7)) ([00cd2c4](https://github.com/nkomiya/create-github-project/commit/00cd2c475ef9e0d79b96f4d7ad7e8d98d0fb09c4))
* add readme template ([#9](https://github.com/nkomiya/create-github-project/issues/9)) ([affd2b2](https://github.com/nkomiya/create-github-project/commit/affd2b2357ef12b77b5766e48d433ac478795455))
* add reviewers via command line ([#35](https://github.com/nkomiya/create-github-project/issues/35)) ([fc2b3f7](https://github.com/nkomiya/create-github-project/commit/fc2b3f7c8c9c967fd7427c8c5a6293acd4086d18))
* add selector for commit types to be included in changelog ([#13](https://github.com/nkomiya/create-github-project/issues/13)) ([1037391](https://github.com/nkomiya/create-github-project/commit/103739101ad62484da0124448d14fb2213dee289))
* add support for initializing git repository ([#4](https://github.com/nkomiya/create-github-project/issues/4)) ([c4f15ab](https://github.com/nkomiya/create-github-project/commit/c4f15ab588993d066d982714e32c2697645b9810))
* add workflow for release ([#22](https://github.com/nkomiya/create-github-project/issues/22)) ([6ba2729](https://github.com/nkomiya/create-github-project/commit/6ba27292ebaa7ae5552e060fb265f6b555c4d9d4))
* add workflow template for create release pull request ([#21](https://github.com/nkomiya/create-github-project/issues/21)) ([3a7d969](https://github.com/nkomiya/create-github-project/commit/3a7d969558595129beb30fed7432fff80e112aac))


### Bug Fixes

* enable pip install via github ([#25](https://github.com/nkomiya/create-github-project/issues/25)) ([ad57696](https://github.com/nkomiya/create-github-project/commit/ad576966ce2c9b2c6ba1c87d0ce59ffbc7e1d781))
* modify pathes in workflows ([#32](https://github.com/nkomiya/create-github-project/issues/32)) ([bd031fb](https://github.com/nkomiya/create-github-project/commit/bd031fb59c6693bf02eb024cfcc42885ae99cc45))
