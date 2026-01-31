%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links none

Name:           1password
Version:        8.12.0
Release:        1%{?dist}
Summary:        Password manager and secure wallet

License:        Proprietary
URL:            https://1password.com
ExclusiveArch:  aarch64

# Download from: https://downloads.1password.com/linux/tar/stable/aarch64/1password-latest.tar.gz
Source0:        1password-latest.tar.gz

BuildRequires:  coreutils

Requires:       hicolor-icon-theme
Requires:       gtk3
Requires:       nss
Requires:       xdg-utils
Requires:       polkit

%description
1Password is a password manager developed by AgileBits Inc. It provides
a place for users to store various passwords, software licenses, and
other sensitive information in a virtual vault that is locked with a
PBKDF2-guarded master password.

%prep
%setup -q -n 1password-%{version}.arm64

%build
# Nothing to build - precompiled binary

%install
# Install icons
for resolution in 32x32 64x64 256x256 512x512; do
    install -Dm0644 "resources/icons/hicolor/${resolution}/apps/1password.png" \
        "%{buildroot}%{_datadir}/icons/hicolor/${resolution}/apps/1password.png"
done

# Install desktop file
install -Dm0644 resources/1password.desktop %{buildroot}%{_datadir}/applications/1password.desktop

# Create policy file from template
# The policy owners will be populated at install time via post script
cat ./com.1password.1Password.policy.tpl | sed 's/\${POLICY_OWNERS}//g' > ./com.1password.1Password.policy

# Install system unlock PolKit policy file
install -Dm0644 com.1password.1Password.policy %{buildroot}%{_datadir}/polkit-1/actions/com.1password.1Password.policy

# Install examples
install -Dm0644 resources/custom_allowed_browsers %{buildroot}%{_docdir}/%{name}/examples/custom_allowed_browsers

# Create opt directory and copy application files
install -dm0755 %{buildroot}/opt/1Password

# Copy all files from source to destination
cp -a * %{buildroot}/opt/1Password/

# Cleanup un-needed files from /opt/1Password
rm -f %{buildroot}/opt/1Password/com.1password.1Password.policy
rm -f %{buildroot}/opt/1Password/com.1password.1Password.policy.tpl
rm -f %{buildroot}/opt/1Password/install_biometrics_policy.sh
rm -rf %{buildroot}/opt/1Password/resources/icons/
rm -f %{buildroot}/opt/1Password/resources/1password.desktop
rm -f %{buildroot}/opt/1Password/resources/custom_allowed_browsers

# Move license files to standard location to avoid duplicates
install -dm0755 %{buildroot}%{_licensedir}/%{name}
mv %{buildroot}/opt/1Password/LICENSE.electron.txt %{buildroot}%{_licensedir}/%{name}/
mv %{buildroot}/opt/1Password/LICENSES.chromium.html %{buildroot}%{_licensedir}/%{name}/

# Create symlink to /usr/bin
install -dm0755 %{buildroot}%{_bindir}
ln -sr %{buildroot}/opt/1Password/1password %{buildroot}%{_bindir}/1password

%pre
# Create the onepassword group if it doesn't exist
getent group onepassword >/dev/null || groupadd -r onepassword

%post
# Setup the Core App Integration helper binary with the correct permissions and group
BROWSER_SUPPORT_PATH="/opt/1Password/1Password-BrowserSupport"
if [ -f "$BROWSER_SUPPORT_PATH" ]; then
    chgrp onepassword "$BROWSER_SUPPORT_PATH"
    chmod g+s "$BROWSER_SUPPORT_PATH"
fi

# chrome-sandbox requires the setuid bit to be specifically set
# See https://github.com/electron/electron/issues/17972
CHROME_SANDBOX="/opt/1Password/chrome-sandbox"
if [ -f "$CHROME_SANDBOX" ]; then
    chmod 4755 "$CHROME_SANDBOX"
fi

# Update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

# Update desktop database
update-desktop-database %{_datadir}/applications &>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
    # Remove the onepassword group
    getent group onepassword >/dev/null && groupdel onepassword || :

    # Update icon cache
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

    # Update desktop database
    update-desktop-database %{_datadir}/applications &>/dev/null || :
fi

%files
%license %{_licensedir}/%{name}/LICENSE.electron.txt
%license %{_licensedir}/%{name}/LICENSES.chromium.html
%doc %{_docdir}/%{name}/examples/custom_allowed_browsers
%{_bindir}/1password
%{_datadir}/applications/1password.desktop
%{_datadir}/icons/hicolor/*/apps/1password.png
%{_datadir}/polkit-1/actions/com.1password.1Password.policy
%dir /opt/1Password/
/opt/1Password/*

%changelog
* Fri Jan 31 2025 Package Maintainer <spkane00+linux@gmail.com> - 8.12.0-1
- Convert from Arch Linux PKGBUILD to Fedora RPM spec
- Initial RPM package for Fedora 42 on aarch64
