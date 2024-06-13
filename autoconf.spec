#specfile originally created for Fedora, modified for Moblin Linux
Summary:    A GNU tool for automatically configuring source code
Name:       autoconf
Version:    2.72
Release:    1
License:    GPLv2+ and GFDL
Source:     http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz
URL:        http://www.gnu.org/software/autoconf/
BuildRequires:      m4 >= 1.4.8
Requires:           m4 >= 1.4.8, coreutils, grep
Requires(post):     /sbin/install-info
Requires(preun):    /sbin/install-info
BuildArch: noarch

# filter out bogus perl(Autom4te*) dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Autom4te::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Autom4te::

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

%build
%configure
%make_build

#check
#make check VERBOSE=yes

%install
%make_install

# Disable gtkdocize after installation to prevent dependency to help2man
sed -i 's/uses_gtkdoc = 1/uses_gtkdoc = 0/g' $RPM_BUILD_ROOT%{_bindir}/autoreconf

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_datadir}/emacs

%post
[ -e %{_infodir}/autoconf.info ] && /sbin/install-info %{_infodir}/autoconf.info %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    [ -e %{_infodir}/autoconf.info ] && /sbin/install-info --del %{_infodir}/autoconf.info %{_infodir}/dir || :
fi

%files
%license COPYING
%{_bindir}/*
%doc %{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf/
%doc %{_mandir}/man1/*
%doc AUTHORS NEWS README THANKS TODO

