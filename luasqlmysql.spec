%define name         luasqlmysql
%define srcname      luasql
%define soname       mysql
%define version 2.0b
%define major        2
%define release 2mdk
%define libname      %mklibname %{name} %{major}
%define libname_orig %mklibname %{name}
%define lua_version  5.0

Summary:        LuaMySQL is a simple interface from Lua to MySQL
Name:           %name
Version:        %version
Release:        %release
License:        MIT
Group:          Development/Other
URL:            http://www.keplerproject.org/luasql/
Source0:        %{srcname}-%{version}.tar.bz2
Patch0:         %{name}.patch.bz2
BuildRoot:      %_tmppath/%{name}-buildroot
Obsoletes:      %{libname} = %{version}
Obsoletes:      %{libname_orig}
Provides:       %{libname} = %{version}
Provides:       %{libname_orig}

%description
LuaMySQL is a simple interface from Lua to MySQL.

%package -n     %{libname}
Summary:        LuaMySQL is a simple interface from Lua to MySQL
Group:          Development/Other
Obsoletes:      %{libname} = %{version}
Obsoletes:      %{libname_orig}
Provides:       %{libname} = %{version}
Provides:       %{libname_orig}
Requires:       liblua5
BuildRequires:  liblua-devel

%description -n %{libname}
LuaMySQL is a simple interface from Lua to MySQL.

%package -n     %{libname}-devel
Summary:        Static library and header files for the luasqlmysql library
Group:          Development/Other
License:        MIT
Obsoletes:      %{libname}-devel = %{version}
Obsoletes:      %{libname_orig}-devel
Provides:       %{libname}-devel = %{version}
Provides:       %{libname_orig}-devel
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}-devel
LuaMySQL is a simple interface from Lua to MySQL.

This package contains the static libluamysql library needed to compile
applications that use luamysql.

%prep
%setup -q -n %{srcname}-%{version}
%patch -p1

%build
export CFLAGS="%{optflags} -fPIC"
%make mysqllinux

%install
strip %{soname}.so
%__rm -rf %{buildroot}
install -d %{buildroot}/%{_includedir}/lua/%{lua_version}
install -d %{buildroot}/%{_libdir}/lua/%{lua_version}
install -d %{buildroot}/%{_datadir}/lua/%{lua_version}
install -d %{buildroot}/%{_defaultdocdir}/lua/%{lua_version}/%{srcname}
install -m0755 %{soname}.so %{buildroot}%{_libdir}/lua/%{lua_version}
install -m0644 %{soname}.a %{buildroot}/%{_libdir}/lua/%{lua_version}
install -m0644 README %{buildroot}%{_defaultdocdir}/lua/%{lua_version}/%{srcname}
install -m0644 manual.html %{buildroot}%{_defaultdocdir}/lua/%{lua_version}/%{srcname}
install -m0644 index.html %{buildroot}%{_defaultdocdir}/lua/%{lua_version}/%{srcname}
install -m0644 license.html %{buildroot}%{_defaultdocdir}/lua/%{lua_version}/%{srcname}

%post -n %{libname}
cd %{_datadir}/lua/%{lua_version} && rm -f %{soname}.lua && ln default.lua %{soname}.lua

%postun -n %{libname}
if [ "$1" = "0" ]; then
  rm -f %{_datadir}/lua/%{lua_version}/%{soname}.lua
fi

%clean
%__rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lua/%{lua_version}/*.so
%{_defaultdocdir}/lua/%{lua_version}/%{srcname}/*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/lua/%{lua_version}/*.so
%{_libdir}/lua/%{lua_version}/*.a

