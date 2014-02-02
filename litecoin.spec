Summary:	Litecoin is a peer-to-peer currency
Name:		litecoin
Version:	0.8.6.1
Release:	3
License:	MIT/X11
Group:		X11/Applications
Source0:	https://github.com/litecoin-project/litecoin/archive/v%{version}.tar.gz
# Source0-md5:	f818d06cad63cd5cf4ce7c2b8f04edef
URL:		http://www.litecoin.org/
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
qmake-qt4 \
	USE_UPNP=1 \
	USE_DBUS=1 \
	USE_QRCODE=1

%{__make} \
	CXX="%{__cxx}"

%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} %{rpmcxxflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{1,5},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

install -p src/litecoind $RPM_BUILD_ROOT%{_bindir}/litecoind
install -p litecoin-qt $RPM_BUILD_ROOT%{_bindir}

sed -e 's#bitcoin#litecoin#g' -e 's#Bitcoin#Litecoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/litecoin-qt.desktop
sed -e 's#bitcoin#litecoin#g' -e 's#Bitcoin#Litecoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/litecoin-qt.protocol

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

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/litecoin-qt
%{_datadir}/kde4/services/litecoin-qt.protocol
%{_desktopdir}/litecoin-qt.desktop
%{_pixmapsdir}/litecoin*.png
