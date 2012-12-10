%define	name	natmonitor
%define	version	2.4
%define	release	%mkrel 6

Summary:	This little utility monitor hosts bandwidth usage in your home lan
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Monitoring
License:	GPL
URL:		http://natmonitor.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/natmonitor/%{name}-%{version}.tar.bz2
Source1:	natmonitord.init.bz2
Patch0:		natmonitor-datadir.patch.bz2
Patch1:		natmonitord-conf.patch.bz2
BuildRequires:	gtk+2-devel
BuildRequires:	libpcap-devel >= 0.7.2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
NAT Monitor is a tool to monitor hosts' bandwidth usage in a 
Linux-NAT network. A daemon collects data and clients display them
(currently a GTK app with graph and a text version). It detects 
new hosts, saves up to 12 hours of data, and has a nice summary 
statistic. 

%package -n	natmonitord
Summary:	The NAT Monitor daemon
Group:		System/Servers
Requires(post,preun): rpm-helper
Requires(pre,postun): rpm-helper

%description -n	natmonitord
The NAT Monitor daemon collects data for the natmonitor clients.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0 -b .datadir
%patch1 -p0 -b .natmonitord-conf

bzcat %{SOURCE1} > natmonitord.init

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

%build

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/lib/natmonitor

install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}

install -m644 icons/%{name}16x16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m644 icons/%{name}32x32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m644 icons/%{name}48x48.png %{buildroot}%{_liconsdir}/%{name}.png

install -m755 natmonitor %{buildroot}%{_bindir}/
install -m755 natmonitorconsole %{buildroot}%{_bindir}/
install -m755 natmonitord %{buildroot}%{_sbindir}/
install -m755 natmonitord.init %{buildroot}%{_initrddir}/natmonitord

install -m644 natmonitor.conf %{buildroot}%{_sysconfdir}
install -m644 natmonitord.conf %{buildroot}%{_sysconfdir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Name=Natmonitor 
Comment=Utility to monitor hosts bandwidth usage in your home lan
Icon=%{name}
Categories=System;Monitor;
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%pre -n natmonitord
%_pre_useradd natmonitor /var/lib/natmonitor /bin/false

%post -n natmonitord
%_post_service natmonitord

%preun -n natmonitord
%_preun_service natmonitord

%postun -n natmonitord
%_postun_userdel natmonitor

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc API BUGS CHANGELOG README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/natmonitor.conf
%attr(0755,root,root) %{_bindir}/natmonitor
%attr(0755,root,root) %{_bindir}/natmonitorconsole
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files -n natmonitord
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/natmonitord
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/natmonitord.conf
%attr(0755,root,root) %{_sbindir}/natmonitord
%attr(0755,natmonitor,natmonitor) %dir %{_localstatedir}/lib/natmonitor



%changelog
* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4-6mdv2009.1
+ Revision: 298288
- rebuilt against libpcap-1.0.0

* Tue Jul 29 2008 Thierry Vignaud <tvignaud@mandriva.com> 2.4-5mdv2009.0
+ Revision: 253570
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.4-3mdv2008.1
+ Revision: 133911
- auto-convert XDG menu entry
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- import natmonitor


* Wed Jul 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4-3mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Mon Jul 04 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4-2mdk
- rebuild
- misc spec file fixes

* Fri Jun 04 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4-1mdk
- 2.4
- fix deps
- fix menu entry

* Sun May 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.1-1mdk
- 2.1
- added P0, P1 & S1
- added the natmonitord sub package

* Tue Apr 22 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1-1mdk
- 1.1
- drop P0, this software doesn't seem to like cflags at all (i wonder why???)

* Tue Apr 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.9-1mdk
- 0.9
- fix P0
- install icons and menu stuff (i hope this is correct?)

* Tue Apr 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.7-1mdk
- initial cooker contrib
- added P0
