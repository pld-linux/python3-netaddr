#
# Conditional build:
%bcond_without	doc		# Sphinx based documentation
%bcond_without	tests		# unit tests

%define		module	netaddr
Summary:	A pure Python network address representation and manipulation library
Summary(pl.UTF-8):	Czysto pythonowa biblioteka do reprezentacji i operacji na adresach sieciowych
Name:		python3-netaddr
Version:	1.3.0
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/n/netaddr/%{module}-%{version}.tar.gz
# Source0-md5:	b0307617f8f3aa73bbcfadac52d91df7
URL:		https://github.com/drkjam/netaddr/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-packaging
BuildRequires:	python3-pytest >= 2.4.2
%endif
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	rpm-pythonprov
%if %{with doc}
BuildRequires:	python3-furo >= 2023.9.10
BuildRequires:	python3-sphinx_issues >= 4.0.0
BuildRequires:	sphinx-pdg-3 >= 7.2.6
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A pure Python network address representation and manipulation library.

netaddr provides a Pythonic way to work with:
- IPv4 and IPv6 addresses and subnets (including CIDR notation)
- MAC (Media Access Control) addresses in multiple presentation
  formats
- IEEE EUI-64, OUI and IAB identifiers
- nmap-style IP address ranges
- a user friendly IP glob-style format

Included are routines for:
- generating, sorting and summarizing IP addresses
- converting IP addresses and ranges between various different formats
- performing set based operations on groups of IP addresses and
  subnets
- arbitrary IP address range calculations and conversions
- querying IEEE OUI and IAB organisational information
- querying of IP standards related data from key IANA data sources

%description -l pl.UTF-8
Czysto pythonowa biblioteka do reprezentacji i operacji na adresach
sieciowych.

Zapewnia pythonowe sposoby pracy z:
- adresami i podsieciami IPv4 i IPv6 (wraz z notacją CIDR)
- adresami MAC (Media Access Control) w wielu formatach
- identyfikatorami IEEE EUI-64, OUI i IAB
- przedziałami adresów IP w stylu nmapa
- przyjaznym dla użytkownika formacie IP w stylu globów

Zawiera funkcje do:
- generowania, sortowania i skracania adresów IP
- konwersji adresów i przedziałów IP między różnymi formatami
- operacji teoriomnogościowych na grupach adresów i podsieciach IP
- dowolnych obliczeń i konwersji przedziałów adresów IP
- zapytań o informacje organizacyjne dotyczące IEEE OUI i IAB
- zapytań o dane związane ze standardami IP z kluczowych źródeł IANA

%package -n netaddr
Summary:	An interactive shell for the Python netaddr library
Summary(pl.UTF-8):	Interaktywna powłoka do biblioteki Pythona netaddr
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n netaddr
Interactive shell for the python-netaddr library.

%description -n netaddr -l pl.UTF-8
Interaktywna powłoka do biblioteki Pythona netaddr.

%package apidocs
Summary:	API documentation for Python netaddr module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona netaddr
Group:		Documentation

%description apidocs
API documentation for Python netaddr module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona netaddr.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest netaddr/tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs/source docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst COPYRIGHT.rst LICENSE.rst README.rst THANKS.rst
%{py3_sitescriptdir}/netaddr
%{py3_sitescriptdir}/netaddr-%{version}.dist-info

%files -n netaddr
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/netaddr

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,dev-how-to,reference,*.html,*.js}
%endif
