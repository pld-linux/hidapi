#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	hidraw		# Linux 3 HIDRAW interface instead of libusb
#
Summary:	HID API for Windows, Linux and Mac OS X
Summary(pl.UTF-8):	API HID dla systemów Windows, Linux oraz Mac OS X
Name:		hidapi
Version:	0.7.0
Release:	1
License:	GPL v3 or BSD or HIDAPI
Group:		Libraries
Source0:	https://github.com/signal11/hidapi/archive/%{name}-%{version}.tar.gz
# Source0-md5:	5a0fa9e57960371942e6c3be2f988064
URL:		https://github.com/signal11/hidapi/
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool
%if %{with hidraw}
BuildRequires:	linux-libc-headers >= 7:2.6.39
%else
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	pkgconfig
%endif
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
%if %{without hidraw}
Requires:	libusb-devel >= 1.0
%endif

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

%description apidocs
API documentation for HIDAPI library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki HIDAPI.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp linux/README.txt README-linux.txt

%build
cd linux
%if %{with hidraw}
libtool --mode=compile --tag=CC %{__cc} %{rpmcflags} %{rpmcppflags} -c hid.c -o hid.lo -I../hidapi
OBJS=hid.lo
LIBS=
%else
libtool --mode=compile --tag=CC %{__cc} %{rpmcflags} %{rpmcppflags} -c hid-libusb.c -o hid-libusb.lo -I../hidapi $(pkg-config --cflags libusb-1.0)
OBJS=hid-libusb.lo
LIBS="$(pkg-config --libs libusb-1.0)"
%endif
libtool --mode=link --tag=CC %{__cc} %{rpmldflags} %{rpmcflags} -o libhidapi.la $OBJS $LIBS -rpath %{_libdir}
cd ..

%if %{with apidocs}
cd doxygen
doxygen Doxyfile
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

libtool --mode=install install linux/libhidapi.la $RPM_BUILD_ROOT%{_libdir}
cp -p hidapi/hidapi.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# included hid.rules as doc only - it uses e.g. MODE="0666", so requires some adjustments at least for stricter permissions
%doc AUTHORS.txt LICENSE.txt LICENSE-bsd.txt LICENSE-orig.txt README.txt README-linux.txt udev/99-hid.rules
%attr(755,root,root) %{_libdir}/libhidapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhidapi.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhidapi.so
%{_libdir}/libhidapi.la
%{_includedir}/hidapi.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libhidapi.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen/html/*
%endif
