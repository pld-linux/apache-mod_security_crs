%define		apxs		/usr/sbin/apxs
# Use the following command to verify gitver and githash when updating from master:
# wget --content-disposition https://github.com/SpiderLabs/owasp-modsecurity-crs/tarball/master
%define		gitver		2.2.7-21
%define		githash		d4f9c5a
Summary:	OWASP ModSecurity Core Rule Set (CRS)
Name:		apache-mod_security_crs
Version:	%(echo %{gitver} | tr - .)
Release:	2
License:	ASL 2.0
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/SpiderLabs/owasp-modsecurity-crs/tarball/%{githash}/SpiderLabs-owasp-modsecurity-crs-%{gitver}-%{githash}.tar.gz
# Source0-md5:	ae12b393c8c1af70a2c3d939aa4aafca
URL:		http://www.modsecurity.org/
BuildRequires:	apache-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache-mod_security >= 2.7.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
OWASP ModSecurity Core Rule Set provides generic protection from
unknown vulnerabilities often found in web applications, which are
in most cases custom coded. The Core Rules are heavily commented to
allow it to be used as a step-by-step deployment guide
for ModSecurity™.

%package extras
Summary:	Supplementary OWASP ModSecurity Core Rule Set (CRS)
Group:		Networking/Daemons/HTTP
Requires:       %{name} = %{version}-%{release}

%description    extras
This package provides supplementary rules for mod_security.

%prep
%setup -q -n SpiderLabs-owasp-modsecurity-crs-%{githash}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/activated_rules \
	$RPM_BUILD_ROOT%{_datadir}/modsecurity.d/base_rules \
	$RPM_BUILD_ROOT%{_datadir}/modsecurity.d/{optional,experimental,slr}_rules

install modsecurity_crs_10_setup.conf.example $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/modsecurity_crs_10_config.conf
install base_rules/* $RPM_BUILD_ROOT%{_datadir}/modsecurity.d/base_rules/

install optional_rules/* $RPM_BUILD_ROOT%{_datadir}/modsecurity.d/optional_rules/
install experimental_rules/* $RPM_BUILD_ROOT%{_datadir}/modsecurity.d/experimental_rules/
install slr_rules/* $RPM_BUILD_ROOT%{_datadir}/modsecurity.d/slr_rules

# activate base_rules
cd $RPM_BUILD_ROOT/%{_datadir}/modsecurity.d/base_rules
for f in * ; do
	ln -s %{_datadir}/modsecurity.d/base_rules/$f $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/activated_rules/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL LICENSE README.md util
%config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity.d/activated_rules/*
%config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity.d/modsecurity_crs_10_config.conf
%dir %{_datadir}/modsecurity.d
%{_datadir}/modsecurity.d/base_rules

%files extras
%defattr(644,root,root,755)
%{_datadir}/modsecurity.d/optional_rules
%{_datadir}/modsecurity.d/experimental_rules
%{_datadir}/modsecurity.d/slr_rules
