%define releasedate 20070927
%define sourcebasename tbb20_%{releasedate}oss_src
%define sourcefilename %{sourcebasename}.tar.gz

Summary: The Threading Building Blocks library abstracts low-level threading details
Name: tbb
Version: 2.0
Release: 4.%{releasedate}%{?dist}
License: GPLv2 with exceptions
Group: Development/Tools
URL: http://threadingbuildingblocks.org/
Source: http://threadingbuildingblocks.org/uploads/77/84/2.0/%{sourcefilename}
Source2: http://cache-www.intel.com/cd/00/00/30/11/301111_301111.pdf
Source3: http://cache-www.intel.com/cd/00/00/30/11/301114_301114.pdf
Source4: http://cache-www.intel.com/cd/00/00/30/11/301132_301132.pdf
Source5: http://cache-www.intel.com/cd/00/00/31/26/312687_312687.pdf
Patch0: tbb-2.0-20070927-soname.patch
Patch1: tbb-2.0-20070927-cxxflags.patch
Patch2: tbb-2.0-20070927-parallel-make.patch
Patch3: tbb-2.0-20070927-gcc43.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libstdc++-devel
# We need "arch" and "hostname" binaries:
BuildRequires: util-linux net-tools
ExclusiveArch: %{ix86} x86_64 ia64

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance.  It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models.  The applications you write are portable across
platforms.  Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.


%package devel
Summary: The Threading Building Blocks C++ headers and shared development libraries
Group: Development/Libraries
Requires: tbb = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.


%package doc
Summary: The Threading Building Blocks documentation
Group: Documentation

%description doc
PDF documentation for the user of the Threading Building Block (TBB)
C++ library.


%prep
%setup -q -n %{sourcebasename}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# Currently we build TBB in debug mode.  This overrides some of the
# CXXFLAGS passed in, namely turns off optimizations.  Either GCC 4.3
# or TBB have a bug that prevents TBB to compile correctly on anything
# above -O0.  As soon as upstream has this situation resolved, release
# builds can be reintroduced.
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS" DEBUG_SUFFIX= tbb_build_prefix=obj debug

cp -p %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} .
ln -s `basename %{SOURCE2}` getting_started_guide.pdf
ln -s `basename %{SOURCE3}` reference_manual.pdf
ln -s `basename %{SOURCE4}` tutorial.pdf
ln -s `basename %{SOURCE5}` release_notes.pdf

%install
rm -rf $RPM_BUILD_ROOT

pushd build/obj_debug
    for file in libtbb{,malloc}; do
        install -p -D -m 755 ${file}.so $RPM_BUILD_ROOT/%{_libdir}/$file.so.2.0
        ln -s $file.so.2.0 $RPM_BUILD_ROOT/%{_libdir}/$file.so.2
        ln -s $file.so.2.0 $RPM_BUILD_ROOT/%{_libdir}/$file.so
    done
popd

pushd include
    find tbb -type f -name \*.h -exec \
        install -p -D -m 644 {} $RPM_BUILD_ROOT/%{_includedir}/{} \
    \;
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.2.0
%{_libdir}/*.so.2

%files devel
%defattr(-,root,root,-)
%{_includedir}/tbb
%{_libdir}/*.so

%files doc
%defattr(-,root,root,-)
%doc 301111_301111.pdf getting_started_guide.pdf
%doc 301114_301114.pdf reference_manual.pdf
%doc 301132_301132.pdf tutorial.pdf
%doc 312687_312687.pdf release_notes.pdf

%changelog
* Wed Feb 13 2008 Petr Machata <pmachata@redhat.com> - 2.0-4.20070927
- Review fixes
  - Use updated URL
  - More timestamp preservation
- Initial import into Fedora CVS

* Mon Feb 11 2008 Petr Machata <pmachata@redhat.com> - 2.0-3.20070927
- Review fixes
  - Preserve timestamp of installed files
  - Fix soname not to contain "debug"

* Tue Feb  5 2008 Petr Machata <pmachata@redhat.com> - 2.0-2.20070927
- Review fixes
  - GCC 4.3 patchset
  - Add BR util-linux net-tools
  - Add full URL to Source0
  - Build in debug mode to work around problems with GCC 4.3

* Mon Dec 17 2007 Petr Machata <pmachata@redhat.com> - 2.0-1.20070927
- Initial package.
- Using SONAME patch from Debian.
