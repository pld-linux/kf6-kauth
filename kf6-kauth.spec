#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - runtime Requires if any
%define		kdeframever	5.249.0
%define		qtver		5.15.2
%define		kfname		kauth

Summary:	Execute actions as privileged user
Name:		kf6-%{kfname}
Version:	5.249.0
Release:	0.1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	fde25c3b9c644325f7d5dc0d67cc0ec9
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
# TODO
#BuildRequires:	polkit-qt6-1-devel >= 0.99.0
#BuildRequires:	polkit-qt6-1-gui-devel >= 0.99.0
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kcoreaddons >= %{version}
#Requires:	polkit-qt6-1 >= 0.99.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KAuth provides a convenient, system-integrated way to offload actions
that need to be performed as a privileged user (root, for example) to
small (hopefully secure) helper utilities.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 3.16
Requires:	kf6-kcoreaddons-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKF6AuthCore.so.5.*.*
%ghost %{_libdir}/libKF6AuthCore.so.6
%dir %{_libdir}/qt6/plugins/kf6/kauth
%dir %{_libdir}/qt6/plugins/kf6/kauth/helper
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kauth/helper/kauth_helper_plugin.so
%{_datadir}/dbus-1/system.d/org.kde.kf6auth.conf
%dir %{_datadir}/kf6/kauth
%{_datadir}/kf6/kauth/dbus_policy.stub
%{_datadir}/kf6/kauth/dbus_service.stub
%{_datadir}/qlogging-categories6/kauth.categories
%{_datadir}/qlogging-categories6/kauth.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KAuth
%{_includedir}/KF6/KAuthCore
%{_libdir}/cmake/KF6Auth
%{_libdir}/libKF6AuthCore.so
