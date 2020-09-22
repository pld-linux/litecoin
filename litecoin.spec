Summary:	Litecoin is a peer-to-peer currency
Summary(pl.UTF-8):	Litecoin - waluta peer-to-peer
Name:		litecoin
Version:	0.18.1
Release:	2
License:	MIT
Group:		X11/Applications
#Sourrce0Download: https://github.com/litecoin-project/litecoin/releases
Source0:	https://download.litecoin.org/litecoin-%{version}/src/%{name}-%{version}.tar.gz
# Source0-md5:	67af5786635639536e78993b1fc082d0
Patch0:		qt-5.15.patch
Patch1:		%{name}-univalue.patch
URL:		http://www.litecoin.org/
BuildRequires:	Qt5Core-devel >= 5.4
BuildRequires:	Qt5DBus-devel >= 5.4
BuildRequires:	Qt5Gui-devel >= 5.4
BuildRequires:	Qt5Network-devel >= 5.4
BuildRequires:	Qt5Widgets-devel >= 5.4
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.49
BuildRequires:	db-cxx-devel >= 4.8
BuildRequires:	gettext-tools
BuildRequires:	libevent-devel >= 2
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	libunivalue-devel >= 1.0.4
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.4
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt5-linguist >= 5.4
BuildRequires:	qt5-qmake >= 5.4
BuildRequires:	zeromq-devel >= 4
Requires:	libunivalue >= 1.0.4
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
%patch0 -p1
%patch1 -p1

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
	--disable-bench \
	--disable-gui-tests \
	--disable-shared \
	--disable-silent-rules \
	--disable-tests \
	--with-boost \
	--with-incompatible-bdb \
	--with-miniupnpc \
	--with-qrencode \
	--with-qtdbus \
	--with-system-univalue
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_datadir}/kde4/services}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# shared disabled, development packages present in bitcoin.spec and feathercoin.spec
%{__rm} -r $RPM_BUILD_ROOT{%{_libdir}/libbitcoinconsensus.*,%{_includedir}/bitcoinconsensus.h,%{_pkgconfigdir}/libbitcoinconsensus.pc}

# see contrib/rpm/bitcoin.spec

cat <<EOF >$RPM_BUILD_ROOT%{_desktopdir}/litecoin-qt.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Litecoin
Comment=Litecoin P2P Cryptocurrency
Comment[fr]=Litecoin, monnaie virtuelle cryptographique pair à pair
Comment[pl]=Litecoin - kryptowaluta P2P
Comment[tr]=Litecoin, eşten eşe kriptografik sanal para birimi
Exec=litecoin-qt %u
Terminal=false
Type=Application
Icon=bitcoin
MimeType=x-scheme-handler/litecoin;
Categories=Office;Finance;
EOF

cat <<EOF >$RPM_BUILD_ROOT%{_datadir}/kde4/services/litecoin-qt.protocol
[Protocol]
exec=litecoin-qt '%u'
protocol=litecoin
input=none
output=none
helper=true
listing=
reading=false
writing=false
makedir=false
deleting=false
EOF

cp -p share/pixmaps/bitcoin.ico $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p share/pixmaps/nsis-*.bmp $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING doc/{README,REST-interface,assets-attribution,benchmarking,bips,dependencies,dnsseed-policy,reduce-traffic,release-notes*,shared-libraries,tor,zmq}.md doc/release-notes
%attr(755,root,root) %{_bindir}/litecoind
%attr(755,root,root) %{_bindir}/litecoin-cli
%attr(755,root,root) %{_bindir}/litecoin-wallet
%attr(755,root,root) %{_bindir}/litecoin-tx
%{_mandir}/man1/litecoin-cli.1*
%{_mandir}/man1/litecoin-wallet.1*
%{_mandir}/man1/litecoin-tx.1*
%{_mandir}/man1/litecoind.1*

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/litecoin-qt
%{_datadir}/kde4/services/litecoin-qt.protocol
%{_desktopdir}/litecoin-qt.desktop
%{_pixmapsdir}/bitcoin.ico
%{_pixmapsdir}/nsis-*.bmp
%{_mandir}/man1/litecoin-qt.1*
