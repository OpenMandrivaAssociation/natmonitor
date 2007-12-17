%define	name	natmonitor
%define	version	2.4
%define	release	%mkrel 3

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
install -d %{buildroot}%{_localstatedir}/natmonitor

install -d %{buildroot}%{_menudir}
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

cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{name}" \
title="Natmonitor " \
longtitle="This little utility monitor hosts bandwidth usage in your home lan." \
needs="x11" \
icon="%{name}.png" \
section="System/Monitoring"
EOF

%post
%update_menus

%postun
%clean_menus

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
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files -n natmonitord
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/natmonitord
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/natmonitord.conf
%attr(0755,root,root) %{_sbindir}/natmonitord
%attr(0755,natmonitor,natmonitor) %dir %{_localstatedir}/natmonitor

