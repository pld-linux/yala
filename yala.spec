Summary:	Yet Another LDAP Admin
Name:		yala
Version:	0.12
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	6a1fc88225f05edaa9c22a755ab6cc31
Source1:	%{name}.conf
URL:		http://yala.sourceforge.net/
Requires:	apache
Requires:	php-ldap
Requires(post,preun):	grep
Requires(preun):	fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	yaladir	%{_datadir}/%{name}

%description
YALA is a web-based LDAP administration GUI. The idea is to simplify
the directory administration with a graphical interface and neat
features, though to stay a general-purpose program (unlike some LDAP
browsers written specifically for managing users on the system). The
goal is to simplify the administration but not to make the YALA user
stupid: to achieve this, we try to show the user what YALA does behind
the scenes, what it sends to the server (unlike Micro$oft Active
Directory, for example).

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd,%{yaladir}/{images,include}}

install *.php *.html $RPM_BUILD_ROOT%{yaladir}/
install images/* $RPM_BUILD_ROOT%{yaladir}/images/
install include/* $RPM_BUILD_ROOT%{yaladir}/include/

install %SOURCE1 $RPM_BUILD_ROOT/etc/httpd/

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
%doc AUTHOR BUGS ChangeLog README TODO
%dir %{yaladir}
%{yaladir}/images
%{yaladir}/include
%{yaladir}/[^c]*.php
%{yaladir}/*.html
%config(noreplace) %verify(not mtime size md5) %{yaladir}/config.inc.php
%config(noreplace) %verify(not mtime size md5) /etc/httpd/%{name}.conf
