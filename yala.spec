# TODO:
# - config file shouldn't be in %{_datadir}
Summary:	Yet Another LDAP Admin
Summary(pl):	Jeszcze jedno narzêdzie do administrowania LDAP
Name:		yala
Version:	0.30
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	f8810e588b3e3c3e1a8bad99d24e22fe
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
URL:		http://yala.sourceforge.net/
Requires:	apache
Requires:	php
Requires:	php-ldap
Requires(post,preun):	grep
Requires(preun):	fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		yaladir		%{_datadir}/%{name}

%description
YALA is a web-based LDAP administration GUI. The idea is to simplify
the directory administration with a graphical interface and neat
features, though to stay a general-purpose program (unlike some LDAP
browsers written specifically for managing users on the system). The
goal is to simplify the administration but not to make the YALA user
stupid: to achieve this, we try to show the user what YALA does behind
the scenes, what it sends to the server (unlike Microsoft Active
Directory, for example).

%description -l pl
YALA to oparty na WWW graficzny interfejs do administrowania LDAP.
Jego ide± jest uproszczenie administrowania katalogami przy u¿yciu
graficznego interfejsu i mi³ych cech, ale pozostanie programem
ogólnego przeznaczenia (w przeciwieñstwie do niektórych przegl±darek
LDAP napisanych specjalnie do zarz±dzania u¿ytkownikami w systemie).
Celem jest uproszczenie administracji, ale nie czynienie u¿ytkownika
YALA g³upim - aby to osi±gn±æ, program próbuje pokazaæ u¿ytkownikowi,
co YALA wykonuje pomiêdzy ekranami i co wysy³a do serwera (w
przeciwieñstwie do np. Microsoft Active Directory).

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd,%{yaladir}/{images/icons,include}}

install *.php *.html $RPM_BUILD_ROOT%{yaladir}
install images/*.png $RPM_BUILD_ROOT%{yaladir}/images
install images/icons/* $RPM_BUILD_ROOT%{yaladir}/images/icons
install include/* $RPM_BUILD_ROOT%{yaladir}/include

install config.inc.php.example $RPM_BUILD_ROOT/etc/yala.conf
ln -sf /etc/yala.conf $RPM_BUILD_ROOT%{yaladir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*yala.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/yala.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	grep -v "^Include.*yala.conf" /etc/httpd/httpd.conf > \
                /etc/httpd/httpd.conf.tmp
        mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHOR BUGS CREDITS ChangeLog README README.security TODO *.example
%dir %{yaladir}
%{yaladir}/images
%{yaladir}/include
%{yaladir}/*.php
%{yaladir}/*.html
%config(noreplace) %verify(not mtime size md5) /etc/yala.conf
%config(noreplace) %verify(not mtime size md5) /etc/httpd/%{name}.conf
