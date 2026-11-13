<div align="center">

<img src="assets/banner.svg" alt="changelogger" width="100%">

<p>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge">
  <img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-fbbf24?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Dependencies" src="https://img.shields.io/badge/dependencies-zero-38bdf8?style=for-the-badge">
</p>

**Write good commit messages once. Get release notes for free.**

</div>

---

## ✨ Features

- 🏷️ Picks the range automatically: **latest tag → HEAD** (or the whole history if there are no tags)
- 🗂️ Groups [Conventional Commits](https://www.conventionalcommits.org) into sections: features, fixes, performance, docs, and more
- 💥 Surfaces **breaking changes** (`feat!:` or a `BREAKING CHANGE:` footer) at the top
- 🔗 Links every commit to your GitHub/GitLab remote
- 🪶 One file, only needs `git`

## 🚀 Usage

```bash
git clone https://github.com/CyberLoop-dev/changelogger.git

# from inside any git repo:
python /path/to/changelogger.py                                    # since the latest tag
python /path/to/changelogger.py --from v1.0.0 --to v1.1.0 --version 1.1.0
python /path/to/changelogger.py -o CHANGELOG.md                    # write to a file
```

| Flag | Meaning |
|---|---|
| `--from REF` | Start of the range (default: latest tag) |
| `--to REF` | End of the range (default: `HEAD`) |
| `--version NAME` | Heading for this release |
| `--no-links` | Plain commit hashes, no links |
| `-o FILE` | Write to a file instead of stdout |

## 🧪 Example output

```markdown
## 1.1.0 (2026-11-13)

### 💥 Breaking changes

- **api:** drop the v1 endpoints ([`a1b2c3d`](https://github.com/you/app/commit/a1b2c3d))

### ✨ Features

- **auth:** add passkey login ([`e4f5a6b`](https://github.com/you/app/commit/e4f5a6b))

### 🐛 Bug fixes

- handle empty config files ([`c7d8e9f`](https://github.com/you/app/commit/c7d8e9f))
```

Commits that do not follow the convention land under **Other**. Merge commits are skipped.

## 📄 License

MIT
