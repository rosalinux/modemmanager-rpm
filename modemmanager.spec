%define debug_package %{nil}
%define	_disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define pppver %(rpm -q --qf "%{VERSION}" ppp)
%define pppddir %{_libdir}/pppd/%{pppver}
%define srcname ModemManager

%define major 0
%define libname %mklibname mm-glib %{major}
%define devname %mklibname mm-glib -d

Summary:	Mobile broadband modem management service
Name:		modemmanager
Version:	1.7.991
Release:	1
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		http://www.freedesktop.org/software/ModemManager
Source0:	http://www.freedesktop.org/software/ModemManager/%{srcname}-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
BuildRequires:	intltool
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(qmi-glib)
BuildRequires:	pkgconfig(mbim-glib)
Requires:	mobile-broadband-provider-info
Requires:	usb_modeswitch

%description
The ModemManager service provides a consistent API to operate many different
modems, including mobile broadband (3G) devices.

%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
Shared libraries for %{name}.

%package -n %{devname}
Summary:	Development package for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Files for development with %{name}.

%prep
%setup -qn %{srcname}-%{version}

%build
# (tpg) fix clang issue
export CFLAGS="$CFLAGS -Wno-error=unused-const-variable -Wno-error=enum-conversion"
export CXXFLAGS="$CXXCLAGS -Wno-error=unused-const-variable -Wno-error=enum-conversion"

%configure \
	--with-systemdsystemunitdir=%{_systemunitdir}

%make

%check
make check

%install
%makeinstall_std

# only used by test suite
rm -f %{buildroot}%{pppddir}/mm-test-pppd-plugin.so

%find_lang %{srcname}

%triggerin -- %{name} < 1.0.0-1
/bin/systemctl enable %{srcname}.service
/bin/systemctl start %{srcname}.service

%files -f %{srcname}.lang
%doc README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager1.service
%{_datadir}/polkit-1/actions/org.freedesktop.ModemManager1.policy
%{_iconsdir}/hicolor/22x22/apps/ModemManager.png
%{_bindir}/mmcli
%{_datadir}/bash-completion/completions/mmcli
%{_sbindir}/ModemManager
%dir %{_libdir}/%{srcname}
%{_libdir}/%{srcname}/*.so
/lib/udev/rules.d/*
%{_systemunitdir}/ModemManager.service
%{_mandir}/man8/ModemManager.8*
%{_mandir}/man8/mmcli.8*

%files -n %{libname}
%{_libdir}/libmm-glib.so.%{major}*

%files -n %{devname}
%dir %{_includedir}/libmm-glib
%dir %{_includedir}/%{srcname}
%{_includedir}/libmm-glib/*.h
%{_includedir}/%{srcname}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/girepository-1.0/ModemManager-1.0.typelib
%{_datadir}/gir-1.0/ModemManager-1.0.gir
%{_datadir}/vala/vapi/libmm-glib.deps
%{_datadir}/vala/vapi/libmm-glib.vapi
