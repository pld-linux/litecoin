Summary:	Litecoin is a peer-to-peer currency
Name:		litecoin
Version:	0.6.9.2
Release:	3
License:	MIT/X11
Group:		X11/Applications
Source0:	https://github.com/litecoin-project/litecoin/archive/v%{version}.tar.gz
# Source0-md5:	8d28e0d4bfd4bc88b8d1c56637ee93cf
URL:		http://www.litecoin.org
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt4-qmake
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Litecoin is a peer-to-peer currency. Peer-to-peer means that no central
authority issues new money or tracks transactions. These tasks are
managed collectively by the network.

%package qt
Summary:	Qt-based Litecoin Wallet
Group:		X11/Applications

%description qt
Qt-based Litecoin Wallet.

%prep
%setup -q

%build
qmake-qt4 \
	USE_UPNP=1 \
	USE_DBUS=1 \
	USE_QRCODE=1

%{__make}

%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} %{rpmcxxflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man{1,5},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

install src/litecoind $RPM_BUILD_ROOT%{_libdir}/%{name}/litecoind
sed -e 's#/usr/lib/#%{_libdir}/#g' -e 's#bitcoin#litecoin#g' contrib/debian/bin/bitcoind > $RPM_BUILD_ROOT%{_bindir}/litecoind
chmod 755 $RPM_BUILD_ROOT%{_bindir}/litecoind

install litecoin-qt $RPM_BUILD_ROOT%{_bindir}
sed -e 's#bitcoin#litecoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/litecoin-qt.desktop
sed -e 's#bitcoin#litecoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/litecoin-qt.protocol

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.txt contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/litecoind
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/litecoind

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/litecoin-qt
%{_datadir}/kde4/services/litecoin-qt.protocol
%{_desktopdir}/litecoin-qt.desktop
