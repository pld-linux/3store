#
# Conditional build:
%bcond_with	glib2		# use glib2 (default is glib 1.x)
#
Summary:	3store RDF engine
Summary(pl.UTF-8):	Silnik RDF 3store
Name:		3store
Version:	2.2.22
Release:	15
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/threestore/%{name}-%{version}.tar.gz
# Source0-md5:	6fa70d2830c82eb030d8888f4da0c86c
Patch0:		%{name}-ac.patch
Patch1:		glib2.patch
Patch2:		format-security.patch
URL:		http://threestore.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
%{!?with_glib2:BuildRequires:	glib-devel}
%{?with_glib2:BuildRequires:	glib2-devel}
BuildRequires:	libraptor-devel >= 0.9.10
BuildRequires:	libtool
BuildRequires:	mysql-devel
%{?with_glib2:BuildRequires:	pkgconfig}
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
3store is a highly scalable RDF triplestore, made available under the
GNU General Public Licence and funded by the AKT Consortium
<http://www.aktors.org/>.

%description -l pl.UTF-8
3store to wysoce skalowalne triplestore RDF, udostępnione na
Powszechnej Licencji Publicznej GNU (GPL), sponsorowane przez AKT
Consortium <http://www.aktors.org/>.

%package devel
Summary:	Header files for 3store library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki 3store
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# for -lfl
Requires:	flex
%{!?with_glib2:Requires:	glib-devel}
%{?with_glib2:Requires:	glib2-devel}
Requires:	libraptor-devel >= 0.9.10
Requires:	mysql-devel

%description devel
Header files for 3store library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki 3store.

%package static
Summary:	Static 3store library
Summary(pl.UTF-8):	Statyczna biblioteka 3store
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static 3store library.

%description static -l pl.UTF-8
Statyczna biblioteka 3store.

%prep
%setup -q
%patch -P0 -p1
%{?with_glib2:%patch1 -p1}
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# librdfsql.la obsoleted by 3store.pc file
# libokbc.la is internal library (no header exported)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{okbc,rdfsql}.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/tstore_*
%attr(755,root,root) %{_libdir}/librdfsql.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librdfsql.so.0
%attr(755,root,root) %{_libdir}/libokbc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libokbc.so.0
%{_datadir}/3store

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/3store-config
%attr(755,root,root) %{_libdir}/librdfsql.so
%attr(755,root,root) %{_libdir}/libokbc.so
%{_includedir}/rdfsql
%{_pkgconfigdir}/3store.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/librdfsql.a
%{_libdir}/libokbc.a
