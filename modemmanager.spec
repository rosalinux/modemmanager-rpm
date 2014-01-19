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
Version:	1.0.0
Release:	1
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		http://www.freedesktop.org/software/ModemManager/%{srcname}-%{version}.tar.xz
Source0:	http://www.freedesktop.org/software/ModemManager/%{srcname}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	gtk-doc
BuildRequires:	ppp
BuildRequires:	xsltproc
BuildRequires:	gettext-devel
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(qmi-glib)
BuildRequires:	systemd

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
%configure2_5x \
	--enable-more-warnings=error \
	--with-udev-base-dir=/lib/udev \
	--enable-gtk-doc=yes \
	--with-polkit=yes \
	--with-systemdsystemunitdir=%{_unitdir} \
	--disable-static \
	--with-qmi=yes \
	--without-mbim \
    --with-pppd-plugin-dir="%{pppddir}"

%make 

%check
make check

%install
%makeinstall_std

# only used by test suite
rm -f %{buildroot}%{pppddir}/mm-test-pppd-plugin.so

%triggerin -- %{name} < 1.0.0-1
/bin/systemctl enable %{srcname}.service
/bin/systemctl start %{srcname}.service

%post
%systemd_post %{srcname}.service

%preun
%systemd_preun %{srcname}.service

%postun
%systemd_postun


%files
%doc README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager1.service
%{_datadir}/polkit-1/actions/org.freedesktop.ModemManager1.policy
%{_iconsdir}/hicolor/22x22/apps/ModemManager.png
%{_bindir}/mmcli
%{_sbindir}/ModemManager
%dir %{_libdir}/%{srcname}
%{_libdir}/%{srcname}/*.so
/lib/udev/rules.d/*
%{_mandir}/man8/ModemManager.8*
%{_mandir}/man8/mmcli.8*

%files -n %{libname}
%{_libdir}/libmm-glib.so.%{major}*

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/libmm-glib
%doc %{_datadir}/gtk-doc/html/%{srcname}
%dir %{_includedir}/libmm-glib
%dir %{_includedir}/%{srcname}
%{_includedir}/libmm-glib/*.h
%{_includedir}/%{srcname}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

