# 1Password for Fedora on ARM64 (aarch64)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

## About The Project

1Password currently only supplies official RPM packages for x86_64. This repository provides an RPM spec file to build 1Password for Fedora on ARM64 (aarch64) systems, such as Apple Silicon Macs running Fedora via Asahi Linux.

All development credits go to 1Password - this is their product and this repo simply repackages their official ARM64 tarball as an RPM.

See the [official 1Password Linux install guide](https://support.1password.com/install-linux/) for more information.

## Getting Started

### Prerequisites

Install the required build tools:

```sh
sudo dnf install rpmdevtools rpmbuild wget
```

### Building the RPM

1. Clone this repository:

   ```sh
   git clone https://github.com/spkane/1password-aarch64.git
   cd 1password-aarch64
   ```

2. Set up the RPM build environment:

   ```sh
   rpmdev-setuptree
   ```

3. Download the 1Password source tarball:

   ```sh
   wget -O ~/rpmbuild/SOURCES/1password-latest.tar.gz \
       https://downloads.1password.com/linux/tar/stable/aarch64/1password-latest.tar.gz
   ```

4. Build the RPM:

   ```sh
   rpmbuild -bb 1password.spec
   ```

5. Install the resulting RPM:

   ```sh
   sudo dnf install ~/rpmbuild/RPMS/aarch64/1password-*.rpm
   ```

### One-liner Build and Install

```sh
rpmdev-setuptree && \
wget -O ~/rpmbuild/SOURCES/1password-latest.tar.gz \
    https://downloads.1password.com/linux/tar/stable/aarch64/1password-latest.tar.gz && \
rpmbuild -bb 1password.spec && \
sudo dnf install ~/rpmbuild/RPMS/aarch64/1password-*.rpm
```

## Updating to a New Version

When a new version of 1Password is released:

1. Update the `Version:` field in `1password.spec`
2. Update the `%changelog` section
3. Download the new tarball and rebuild

## Usage

Just start 1Password as you would normally from your application menu or run:

```sh
1password
```

For more information, please refer to the [1Password Documentation](https://support.1password.com/).

## Uninstalling

```sh
sudo dnf remove 1password
```

## Acknowledgments

* [1Password](https://1password.com)
* This repo was directly inspired by the [original Arch Linux PKGBUILD approach by beeemT](https://github.com/beeemT/1password-aarch64).

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/spkane/1password-aarch64-rpm.svg?style=for-the-badge
[contributors-url]: https://github.com/spkane/1password-aarch64-rpm/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/spkane/1password-aarch64-rpm.svg?style=for-the-badge
[forks-url]: https://github.com/spkane/1password-aarch64-rpm/network/members
[stars-shield]: https://img.shields.io/github/stars/spkane/1password-aarch64-rpm.svg?style=for-the-badge
[stars-url]: https://github.com/spkane/1password-aarch64-rpm/stargazers
[issues-shield]: https://img.shields.io/github/issues/spkane/1password-aarch64-rpm.svg?style=for-the-badge
[issues-url]: https://github.com/spkane/1password-aarch64-rpm/issues
# 1password-aarch64-rpm

