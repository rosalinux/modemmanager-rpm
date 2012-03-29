%define srcname ModemManager

Summary:	Mobile broadband modem management service
Name:		modemmanager
Version:	0.5.2.0
Release:	1
Source0:	http://ftp.gnome.org/pub/GNOME/sources/ModemManager/0.5/%{srcname}-%{version}.tar.xz
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		http://www.gnome.org/projects/NetworkManager/
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	ppp
BuildRequires:	xsltproc

%description
The ModemManager service provides a consistent API to operate many different
modems, including mobile broadband (3G) devices.

%prep
%setup -q -n %{srcname}-%{version}

%build
autoreconf -fi
pppver=`rpm -q --qf "%{VERSION}" ppp`
pppddir=%{_libdir}/pppd/$pppver
%configure2_5x \
	--enable-more-warnings=no \
	--with-udev-base-dir=/lib/udev \
	--with-tests=yes \
	--with-docs=yes \
	--disable-static \
	--with-pppd-plugin-dir="$pppddir"

%make

%check
%make check

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %{buildroot}%{_libdir}/%{srcname}/*.la

# only used by test suite
rm -f %{buildroot}%{_libdir}/%{name}/*.la
rm -f %{buildroot}%{_libdir}/pppd/2.*/*.la
rm -f %{buildroot}%{_libdir}/pppd/2.*/*.so

%clean
rm -rf %{buildroot}

%files
%defattr(0644, root, root, 0755)
%doc README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager.service
%{_datadir}/icons/hicolor/22x22/apps/modem-manager.png
%{_datadir}/polkit-1/actions/org.freedesktop.modem-manager.policy
%attr(0755,root,root) %{_sbindir}/modem-manager
%dir %{_libdir}/%{srcname}
%attr(0755,root,root) %{_libdir}/%{srcname}/*.so*
/lib/udev/rules.d/*
