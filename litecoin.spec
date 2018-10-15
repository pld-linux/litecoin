Summary:	Litecoin is a peer-to-peer currency
Summary(pl.UTF-8):	Litecoin - waluta peer-to-peer
Name:		litecoin
Version:	0.13.2
Release:	7
License:	MIT
Group:		X11/Applications
Source0:	https://github.com/litecoin-project/litecoin/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c0944edfe7ef8612556d3bbf543b6974
URL:		http://www.litecoin.org/
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtDBus-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	automake >= 2.60
BuildRequires:	autoconf
BuildRequires:	boost-devel >= 1.49
BuildRequires:	db-cxx-devel >= 4.8
BuildRequires:	gettext-tools
BuildRequires:	libevent-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	libunivalue-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt4-linguist >= 4
BuildRequires:	qt4-qmake >= 4
BuildRequires:	zeromq-devel >= 4
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Litecoin is a peer-to-peer currency. Peer-to-peer means that no
central authority issues new money or tracks transactions. These tasks
are managed collectively by the network.

%description -l pl.UTF-8
Litecoin to waluta peer-to-peer. Oznacza to, że nie ma centralnej
instytucji emitującej nowe pieniądze czy śledzącej transakcje. Zadania
te są zarządzane kolektywnie przez sieć.

%package qt
Summary:	Qt-based Litecoin Wallet
Summary(pl.UTF-8):	Portfel na litecoiny oparty na Qt
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description qt
Qt-based Litecoin Wallet.

%description qt -l pl.UTF-8
Portfel na litecoiny oparty na Qt.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I build-aux/m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd src/secp256k1
%{__libtoolize}
%{__aclocal} -I build-aux/m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../..
%configure \
	--disable-shared \
	--disable-silent-rules \
	--with-boost \
	--with-gui=qt4 \
	--with-incompatible-bdb \
	--with-miniupnpc \
	--with-qrencode \
	--with-qtdbus \
	--with-system-univalue
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_datadir}/kde4/services}

sed -e 's#bitcoin#litecoin#g' -e 's#Bitcoin#Litecoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/litecoin-qt.desktop
sed -e 's#bitcoin#litecoin#g' -e 's#Bitcoin#Litecoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/litecoin-qt.protocol

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# shared disabled, development packages present in bitcoin.spec and feathercoin.spec
%{__rm} -r $RPM_BUILD_ROOT{%{_libdir}/libbitcoinconsensus.*,%{_includedir}/bitcoinconsensus.h,%{_pkgconfigdir}/libbitcoinconsensus.pc}

cp -p share/pixmaps/bitcoin32.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin32.png
cp -p share/pixmaps/bitcoin64.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin64.png
cp -p share/pixmaps/bitcoin128.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin128.png
cp -p share/pixmaps/bitcoin256.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin256.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.md doc/*.txt contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/litecoind
%attr(755,root,root) %{_bindir}/litecoin-cli
%attr(755,root,root) %{_bindir}/litecoin-tx

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/litecoin-qt
%{_datadir}/kde4/services/litecoin-qt.protocol
%{_desktopdir}/litecoin-qt.desktop
%{_pixmapsdir}/litecoin*.png
