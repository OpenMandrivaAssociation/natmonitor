Summary:	This little utility monitor hosts bandwidth usage in your home lan
Name:		natmonitor
Version:	2.4
Release:	8
Group:		Monitoring
License:	GPL
URL:		https://natmonitor.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/natmonitor/%{name}-%{version}.tar.bz2
Source1:	natmonitord.service
Patch0:		natmonitor-datadir.patch.bz2
Patch1:		natmonitord-conf.patch.bz2
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	libpcap-devel >= 0.7.2
BuildRequires: systemd
Requires(pre): systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

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

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

%build
%make

%install
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_unitdir}
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
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/natmonitord.service

install -m644 natmonitor.conf %{buildroot}%{_sysconfdir}
install -m644 natmonitord.conf %{buildroot}%{_sysconfdir}

mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Name=Natmonitor 
Comment=Utility to monitor hosts bandwidth usage in your home lan
Icon=%{name}
Categories=System;Monitor;
EOF

%pre -n natmonitord
%systemd_pre natmonitord.service
%_pre_useradd natmonitor /var/lib/natmonitor /bin/false

%post -n natmonitord
%systemd_post natmonitord.service

%preun -n natmonitord
%systemd_preun natmonitord.service

%postun -n natmonitord
%systemd_postun_with_restart natmonitord.service
%_postun_userdel natmonitor


%files
%doc API BUGS CHANGELOG README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/natmonitor.conf
%attr(0755,root,root) %{_bindir}/natmonitor
%attr(0755,root,root) %{_bindir}/natmonitorconsole
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files -n natmonitord
%attr(0755,root,root) %{_unitdir}/natmonitord.service
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/natmonitord.conf
%attr(0755,root,root) %{_sbindir}/natmonitord
%attr(0755,natmonitor,natmonitor) %dir %{_localstatedir}/lib/natmonitor
