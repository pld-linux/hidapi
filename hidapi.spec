#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

%define		snap	20180121
%define		commit	a6a622ffb680c55da0de787ff93b80280498330f

Summary:	HID API for Windows, Linux and Mac OS X
Summary(pl.UTF-8):	API HID dla systemów Windows, Linux oraz Mac OS X
Name:		hidapi
Version:	0.8.0
Release:	0.%{snap}.1
License:	GPL v3 or BSD or HIDAPI
Group:		Libraries
Source0:	https://github.com/signal11/hidapi/archive/%{commit}/%{name}-%{version}.tar.gz
# Source0-md5:	dfbec50a01bf8c45cce003293648013e
Patch0:		%{name}-sh.patch
URL:		http://www.signal11.us/oss/hidapi/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0.9
# HIDRAW interface
BuildRequires:	linux-libc-headers >= 7:2.6.39
BuildRequires:	pkgconfig
BuildRequires:	udev-devel
Requires:	libusb >= 1.0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HIDAPI is a multi-platform library which allows an application to
interface with USB and Bluetooth HID-Class (Human Interface Device)
devices on Windows, Linux, and Mac OS X.

%description -l pl.UTF-8
HIDAPI to wieloplatformowa biblioteka pozwalająca aplikacjom
współpracować z urządzeniami USB i Bluetooth klasy HID (Human
Interface Device) w systemach Windows, Linux oraz Mac OS X.

%package devel
Summary:	Header file for HIDAPI library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki HIDAPI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel >= 1.0.9

%description devel
Header file for HIDAPI library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki HIDAPI.

%package static
Summary:	Static HIDAPI library
Summary(pl.UTF-8):	Statyczna biblioteka HIDAPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HIDAPI library.

%description static -l pl.UTF-8
Statyczna biblioteka HIDAPI.

%package apidocs
Summary:	HIDAPI API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki HIDAPI
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for HIDAPI library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki HIDAPI.

%prep
%setup -q -n %{name}-%{commit}
%patch0 -p1

cp -p linux/README.txt README-linux.txt

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%if %{with apidocs}
cd doxygen
doxygen Doxyfile
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/hidapi

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# included hid.rules as doc only - it uses e.g. MODE="0666", so requires some adjustments at least for stricter permissions
%doc AUTHORS.txt LICENSE.txt LICENSE-bsd.txt LICENSE-orig.txt README.txt README-linux.txt udev/99-hid.rules
%attr(755,root,root) %{_libdir}/libhidapi-hidraw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhidapi-hidraw.so.0
%attr(755,root,root) %{_libdir}/libhidapi-libusb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhidapi-libusb.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhidapi-hidraw.so
%attr(755,root,root) %{_libdir}/libhidapi-libusb.so
%{_libdir}/libhidapi-hidraw.la
%{_libdir}/libhidapi-libusb.la
%{_includedir}/hidapi
%{_pkgconfigdir}/hidapi-hidraw.pc
%{_pkgconfigdir}/hidapi-libusb.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhidapi-hidraw.a
%{_libdir}/libhidapi-libusb.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen/html/*
%endif
