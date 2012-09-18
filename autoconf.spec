#specfile originally created for Fedora, modified for Moblin Linux
Summary:    A GNU tool for automatically configuring source code
Name:       autoconf
Version:    2.69
Release:    1
License:    GPLv2+ and GFDL
Group:      Development/Tools
Source:     http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz
Source1:    filter-provides-automake.sh
Source2:    filter-requires-automake.sh
URL:        http://www.gnu.org/software/autoconf/
BuildRequires:      m4 >= 1.4.7
Requires:           m4 >= 1.4.7, coreutils, grep
Requires(post):     /sbin/install-info
Requires(preun):    /sbin/install-info
BuildArch: noarch

# filter out bogus perl(Autom4te*) dependencies
%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%define __find_requires %{SOURCE2}

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q
chmod +x %{SOURCE1}
chmod +x %{SOURCE2}

%build
# use ./configure here to avoid copying config.{sub,guess} with those from the
# rpm package
./configure --prefix=%{_prefix} 
make #  %{?_smp_mflags}  Makefile not smp save

#check
#make check VERBOSE=yes

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_datadir}/emacs

%post
[ -e %{_infodir}/autoconf.info ] && /sbin/install-info %{_infodir}/autoconf.info %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    [ -e %{_infodir}/autoconf.info ] && /sbin/install-info --del %{_infodir}/autoconf.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%{_bindir}/*
%doc %{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf/
%doc %{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO

