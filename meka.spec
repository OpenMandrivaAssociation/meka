# spec is based on Andrea Musuruane's work in Fedora

%define pkgdate 2010-05-30
%define pkgversion %(echo %version|sed s/\\\\\.//g)

Name:		meka
Version:	0.73
Release:	2
Summary:	Sega 8-bit machine emulator
Group:		Emulators
License:	MEKA and non-commercial
URL:		https://www.smspower.org/meka/
Source0:	http://www.smspower.org/meka/releases/%{name}-%{pkgdate}-srcs-v%{pkgversion}.zip
Source1:	%{name}.sh
Source2:	%{name}.desktop
Patch0:		meka-0.72-rpmopt.patch
Patch1:		meka-0.72-buffer_overflow.patch
# http://www.smspower.org/forums/viewtopic.php?t=12699
Patch2:		meka-0.73-execstack.patch
# http://www.smspower.org/forums/viewtopic.php?t=10848
# http://www.smspower.org/forums/viewtopic.php?t=12699
Patch3:		meka-0.73-noseal.patch
# http://www.smspower.org/forums/viewtopic.php?t=12699
Patch4:		meka-0.73-gcc45.patch

Patch5:		meka-0.73-sfmt.patch
Patch6:		meka-0.73-png15.patch

# This is package contains ix86 asm code
ExclusiveArch:	%{ix86}
BuildRequires:	allegro-devel
BuildRequires:	nasm
BuildRequires:	png-devel
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xxf86dga)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xext)
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils

%description
MEKA is a multi machine emulator, originally started as a Sega Master System
emulator, and generally very oriented toward Z80-based Sega 8-bit systems.
MEKA officially emulates the following systems:

 - Sega Game 1000        / SG-1000  / Japan, Oceania
 - Sega Computer 3000    / SC-3000  / Japan, Oceania, Europe
 - Super Control Station / SF-7000  / Japan, Oceania, Europe
 - Sega Mark III         / MK3      / Japan
    + FM Unit Extension  / MK3+FM   / Japan
 - Sega Master System    / SMS      / World Wide
 - Sega Game Gear        / GG       / World Wide
 - ColecoVision          / COLECO   / America, Europe
 - Othello Multivision   / OMV      / Japan

You can play other systems on it only if you are smart enough to figure how.
And if you are, I doubt you will want to play Nintendo games. So forget it.

%prep
%setup -q -c
# Fix CFLAGS in Makefilie
%patch0 -p1
# Fix buffer overflows
%patch1 -p1
# Patch not to require an executable stack
%patch2 -p1
# Patch not to require libseal (audio is severly broken)
%patch3 -p1
# Patch to compile with gcc 4.5
%patch4 -p1
# Fix string format error
%patch5 -p1
# Fix build with png15
%patch6 -p1
# Remove pre-built lib files
find -name '*.lib' -exec %__rm -f '{}' \;
# Fix end-of-line-encoding
%__sed -i 's/\r//' *.txt
# Fix char encondigs
for i in *.txt; do
  iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.utf8
  %__mv $i.utf8 $i
done


%build
cd srcs
# make doesn't compile with %%{?_smp_mflags}
%__make RPMFLAGS="%{optflags}"


%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}%{_bindir}
%__install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/meka
%__install -d %{buildroot}%{_libdir}/meka
%__install -m 755 meka %{buildroot}%{_libdir}/meka
%__install -d %{buildroot}%{_datadir}/meka
%__install -m 644 meka.{blt,dat,inp,msg,nam,pat,thm} %{buildroot}%{_datadir}/meka

# install desktop file
%__mkdir_p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

# install icons
%__mkdir_p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32}/apps
convert -delete 1 srcs/mekaw.ico \
  %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
convert -delete 0 srcs/mekaw.ico \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%clean
%__rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc changes.txt compat.txt debugger.txt history.txt mekanix.txt
%doc meka.txt multi.txt sources.txt tech.txt TODO.txt
%{_bindir}/meka
%{_libdir}/meka
%{_datadir}/meka
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png



%changelog
* Tue Mar 20 2012 Andrey Bondrov <abondrov@mandriva.org> 0.73-1
+ Revision: 785808
- imported package meka

