%define		apxs		/usr/sbin/apxs
Summary:	OWASP Core Rule Set activation for Apache mod_security
Summary(pl.UTF-8):	Aktywacja OWASP Core Rule Set dla modułu mod_security Apache'a
Name:		apache-mod_security_crs
# loader layout follows CRS 4 (plugins/*-{config,before,after}.conf), not a CRS release
Version:	4.0
Release:	2
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	%{name}.conf
Source1:	REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
Source2:	RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf
URL:		https://coreruleset.org/
# crs-setup.conf.example is copied at build time
BuildRequires:	modsecurity-crs >= 4
BuildRequires:	rpmbuild(macros) >= 1.268
# thin 90_mod_security.conf loader with IncludeOptional conf.d/modsecurity.d/*.conf
Requires:	apache-mod_security >= 2.9.14
Requires:	modsecurity-crs >= 4
Obsoletes:	apache-mod_security_crs-extras < 4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Loads the OWASP Core Rule Set (modsecurity-crs package) into Apache
mod_security: CRS setup, plugins and rules in the order CRS requires.
The CRS setup file for Apache lives in
/etc/httpd/modsecurity-crs/crs-setup.conf.

%description -l pl.UTF-8
Ładuje OWASP Core Rule Set (pakiet modsecurity-crs) do modułu
mod_security Apache'a: konfigurację CRS, wtyczki i reguły w kolejności
wymaganej przez CRS. Plik konfiguracyjny CRS dla Apache'a to
/etc/httpd/modsecurity-crs/crs-setup.conf.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{apacheconfdir}/{conf.d/modsecurity.d,modsecurity-crs}

cp -p %{SOURCE0} $RPM_BUILD_ROOT%{apacheconfdir}/conf.d/modsecurity.d/modsecurity_crs.conf
# rule 901001 rejects every request unless a setup file is loaded before rules/
cp -p %{_datadir}/modsecurity-crs/crs-setup.conf.example $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity-crs/crs-setup.conf
cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity-crs

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/conf.d/modsecurity.d/modsecurity_crs.conf
%dir %{apacheconfdir}/modsecurity-crs
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity-crs/crs-setup.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity-crs/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity-crs/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf
