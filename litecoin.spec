Summary:	Litecoin is a peer-to-peer currency
Name:		litecoin
Version:	0.13.2
Release:	3
License:	MIT/X11
Group:		X11/Applications
Source0:	https://github.com/litecoin-project/litecoin/archive/v%{version}//%{name}-%{version}.tar.gz
# Source0-md5:	c0944edfe7ef8612556d3bbf543b6974
URL:		http://www.litecoin.org/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Litecoin is a peer-to-peer currency. Peer-to-peer means that no
central authority issues new money or tracks transactions. These tasks
are managed collectively by the network.

%package qt
Summary:	Qt-based Litecoin Wallet
Group:		X11/Applications

%description qt
Qt-based Litecoin Wallet.

%prep
%setup -q

%build
./autogen.sh
%configure \
	--disable-shared \
	--disable-silent-rules \
	--with-miniupnpc \
	--with-qrencode \
	--with-incompatible-bdb \
	--with-boost \
	--with-gui=qt4 \
	--with-qtdbus
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_datadir}/kde4/services}

sed -e 's#bitcoin#litecoin#g' -e 's#Bitcoin#Litecoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/litecoin-qt.desktop
sed -e 's#bitcoin#litecoin#g' -e 's#Bitcoin#Litecoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/litecoin-qt.protocol

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p share/pixmaps/bitcoin32.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin32.png
cp -p share/pixmaps/bitcoin64.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin64.png
cp -p share/pixmaps/bitcoin128.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin128.png
cp -p share/pixmaps/bitcoin256.png $RPM_BUILD_ROOT%{_pixmapsdir}/litecoin256.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.txt contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/litecoind
%attr(755,root,root) %{_bindir}/litecoin-cli
%attr(755,root,root) %{_bindir}/litecoin-tx

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/litecoin-qt
%{_datadir}/kde4/services/litecoin-qt.protocol
%{_desktopdir}/litecoin-qt.desktop
%{_pixmapsdir}/litecoin*.png
