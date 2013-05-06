%define		apxs		/usr/sbin/apxs
Summary:	OWASP ModSecurity Core Rule Set (CRS)
Name:		apache-mod_security_crs
Version:	-
Release:	0.1
License:	ASL 2.0
Group:		Networking/Daemons/HTTP
# Use the following command to generate the tarball:
# wget https://github.com/SpiderLabs/owasp-modsecurity-crs/tarball/%{version}
#Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	4a220bf4b954ed1760462e5956f65b21
URL:		http://www.modsecurity.org/
BuildRequires:	apache-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache-mod_security >= 2.7.0
BuildArch:	moarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
OWASP ModSecurity Core Rule Set provides generic protection from
unknown vulnerabilities often found in web applications, which are
in most cases custom coded. The Core Rules are heavily commented to
allow it to be used as a step-by-step deployment guide
for ModSecurity™.

%prep
%setup -q -n modsecurity-apache_%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir}}

install -d $RPM_BUILD_ROOT%{apacheconfdir}/modsecurity.d/blocking

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README.* modsecurity* doc/* tools
%dir %{apacheconfdir}/modsecurity.d
%dir %{apacheconfdir}/modsecurity.d/blocking
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/modsecurity.d/*.*
