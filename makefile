
include .config

ifeq ($(type),node)
	BUILD_TARGET=build-node
	INSTALL_TARGET=install-node
	CLEAN_TARGET=clean-node
	UNINSTALL_TARGET=uninstall-node
else
	BUILD_TARGET=build-server
	INSTALL_TARGET=install-server
	CLEAN_TARGET=clean-server
	UNINSTALL_TARGET=uninstall-server
endif

build: $(BUILD_TARGET)

build-node:
	git submodule init
	git submodule update
	tar xvf vermont_patch.tar
	cd vermont; cmake -D SUPPORT_MYSQL=ON .
	make -C vermont
	svn co http://trac.aircrack-ng.org/svn/trunk aircrack-ng
	make -C aircrack-ng
	
build-server:
	echo "Nothing to do"

install: $(INSTALL_TARGET)
	ln -sf $(CURDIR)/daemons/datamap_daemon_control /etc/init.d/datamap
	ln -sf $(CURDIR)/daemons/datamap_daemon_common.py /bin/
	ln -sf $(CURDIR)/daemons/datamap_$(type)_daemon /bin/
	ln -sf $(CURDIR)/daemons/.datamap_config /bin/
	update-rc.d datamap defaults 97

install-node:
	ln -sf $(CURDIR)/vermont/vermont /bin/
	ln -sf $(CURDIR)/vermont/db_config.xml /bin/vermont_config.xml
	ln -sf $(CURDIR)/scripts/start_capture /bin/
	ln -sf $(CURDIR)/scripts/stop_capture /bin/
	make -C aircrack-ng install

install-server:
	cp /etc/mysql/my.cnf /etc/mysql/my.cnf.orig
	sed -i s/bind-address\\s*=.*/bind-address=$(server_addr)/ /etc/mysql/my.cnf
	sed -i s/port\\s*=.*/port=$(db_port)/ /etc/mysql/my.cnf
	mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$(db_username)'@'%' IDENTIFIED BY '$(db_password)' WITH GRANT OPTION;" -p
	service mysql restart
	ln -sf $(CURDIR)/web $(web_folder)

clean: $(CLEAN_TARGET)

clean-node:
	rm -fr vermont
	mkdir vermont
	
clean-server:
	echo "Nothing to do"
	
uninstall: $(UNINSTALL_TARGET)
	rm -f /etc/init.d/datamap
	rm -f /bin/datamap_daemon_common.py
	rm -f /bin/datamap_$(type)_daemon
	rm -f /bin/.datamap_config
	update-rc.d -f datamap remove

uninstall-node:
	rm -f /bin/vermont
	rm -f /bin/vermont_config.xml
	rm -f /bin/start_capture
	rm -f /bin/stop_capture
	rm -f /bin/vermont_config.xml.tmp

uninstall-server:
	if [-e /etc/mysql/my.cnf.orig]; then mv /etc/mysql/my.cnf.orig /etc/mysql/my.cnf; fi;
	mysql -e "REVOKE ALL PRIVILEGES ON *.* FROM '$(db_username)'@'%'" -p
	service mysql restart
	rm -f $(web_folder)
