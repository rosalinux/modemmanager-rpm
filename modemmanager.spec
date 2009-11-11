%define snapshot 20090826
%define srcname ModemManager

Summary:	Mobile broadband modem management service
Name:		modemmanager
Version:	0.2
Release:	%mkrel 0.%{snapshot}.1
#
# Source from git://anongit.freedesktop.org/ModemManager/ModemManager
# tarball built with:
#    ./autogen.sh --prefix=/usr --sysconfdir=/etc --localstatedir=/var
#    make distcheck
#
Source:		%{srcname}-%{version}-%{snapshot}.tar.bz2
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		http://www.gnome.org/projects/NetworkManager/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	glib2-devel
BuildRequires:	dbus-glib-devel >= 0.75
BuildRequires:	libgudev-devel >= 143

%description
The ModemManager service provides a consistent API to operate many different
modems, including mobile broadband (3G) devices.

%prep
%setup -q -n %{srcname}-%{version}

%build
%configure2_5x \
	--enable-more-warnings=yes \
	--with-udev-base-dir=/lib/udev \
	--disable-static
%make

%check
%make check

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %{buildroot}%{_libdir}/%{srcname}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(0644, root, root, 0755)
%doc README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager.service
%attr(0755,root,root) %{_sbindir}/modem-manager
%dir %{_libdir}/%{srcname}
%attr(0755,root,root) %{_libdir}/%{srcname}/*.so*
/lib/udev/rules.d/*
