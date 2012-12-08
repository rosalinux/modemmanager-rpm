%define srcname ModemManager

Summary:	Mobile broadband modem management service
Name:		modemmanager
Version:	0.6.0.0
Release:	1
Source0:	http://ftp.gnome.org/pub/GNOME/sources/ModemManager/0.6/%{srcname}-%{version}.tar.xz
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
autoreconf -fi

%build
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
%makeinstall_std

# only used by test suite
rm -f %{buildroot}%{_libdir}/pppd/2.*/*.so

%files
%defattr(0644, root, root, 0755)
%doc README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager.service
%dir %{_includedir}/mm
%{_includedir}/mm/ModemManager.h
%attr(0755,root,root) %{_sbindir}/modem-manager
%dir %{_libdir}/%{srcname}
%attr(0755,root,root) %{_libdir}/%{srcname}/*.so*
/lib/udev/rules.d/*


%changelog
* Thu Mar 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.5.2.0-1
+ Revision: 788069
- do autoreconf in %%prep
- clean out old junk
- use pkgconfig() deps for buildrequires
- new version

* Fri May 06 2011 Funda Wang <fwang@mandriva.org> 0.4-2
+ Revision: 669921
- disable werror

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Sun Jul 18 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 0.4-1mdv2011.0
+ Revision: 554818
- fix unpackaged files
- buildrequires intltool
- buildrequires gettext-devel
- new version

* Wed Jan 20 2010 Frederik Himpe <fhimpe@mandriva.org> 0.3-1mdv2010.1
+ Revision: 494267
- Fix BuildRequires
- Update to new version 0.3

* Wed Nov 11 2009 Frederik Himpe <fhimpe@mandriva.org> 0.2-0.20090826.1mdv2010.1
+ Revision: 464873
- Import package based on Fedora's package
- create modemmanager

