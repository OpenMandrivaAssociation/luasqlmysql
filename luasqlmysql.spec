%define debug_package %{nil}

%define srcname      luasql
%define soname       postgres
%define major        2
%define libname      %mklibname %{name}
%define develname    %mklibname %{name} -d
%define libname_orig %mklibname %{name}
%define lua_version  5.3

Summary:        Simple interface from Lua to MySQL
Name:           luasqlmysql
Version:        2.6.0
Release:        1
License:        MIT
Group:          Development/Other
URL:            https://github.com/lunarmodules/luasql
Source0:	https://github.com/lunarmodules/luasql/archive/refs/tags/%{version}.tar.gz
Obsoletes:      %{libname} = %{version}
Obsoletes:      %{libname_orig}
Provides:       %{libname} = %{version}
Provides:       %{libname_orig}
BuildRequires:	postgresql-devel	
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:  lua-devel
BuildRequires:  mysql-devel

%description
LuaMySQL is a simple interface from Lua to MySQL.

%package -n     %{libname}
Summary:        Simple interface from Lua to MySQL
Group:          Development/Other
Obsoletes:      %{libname} = %{version}
Obsoletes:      %{libname_orig}
Provides:       %{libname} = %{version}
Provides:       %{libname_orig}
Requires:       lua

%description -n %{libname}
LuaMySQL is a simple interface from Lua to MySQL.

%package -n     %{develname}
Summary:        Static library and header files for the luasqlmysql library
Group:          Development/Other
License:        MIT
Obsoletes:      %{libname_orig}-devel
Provides:       %{libname_orig}-devel
Requires:       %{libname} = %{version}-%{release}
Obsoletes:      %mklibname %{name} -d 2       

%description -n %{develname}
LuaMySQL is a simple interface from Lua to MySQL.

This package contains the static libluamysql library needed to compile
applications that use luamysql.

%prep
%setup -q -n %{srcname}-%{version}

%build
%make CFLAGS="%{optflags} -fPIC" mysql postgres sqlite3

%install
strip src/%{soname}.so
mkdir -p  %{buildroot}%{_libdir}/lua/%{lua_version}
make install LUA_LIBDIR=%{buildroot}%{_libdir}/lua/%{lua_version}

install -d %{buildroot}/%{_datadir}/lua/%{lua_version}
install -d %{buildroot}/%{_defaultdocdir}/lua/%{lua_version}/%{srcname}
cp -r doc/  %{buildroot}%{_defaultdocdir}/lua/%{lua_version}/%{srcname}

%post -n %{libname}
cd %{_datadir}/lua/%{lua_version} && rm -f %{soname}.lua && ln default.lua %{soname}.lua

%postun -n %{libname}
if [ "$1" = "0" ]; then
  rm -f %{_datadir}/lua/%{lua_version}/%{soname}.lua
fi

%files -n %{libname}
%{_libdir}/lua/%{lua_version}/%{srcname}/*.so
%{_defaultdocdir}/lua/%{lua_version}/%{srcname}/*

