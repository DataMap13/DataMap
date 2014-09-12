
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
	@echo "Nothing to do"
	
build-server:
	echo "Nothing to do"

install: $(INSTALL_TARGET)
	install -m 0755 daemons/datamap_daemon_control /etc/init.d/datamap
	install -m 0755 daemons/datamap_daemon_common.py /bin
	install -m 0755 daemons/datamap_$(type)_daemon /bin
	install -m 0755 daemons/.datamap_config /bin
	update-rc.d datamap defaults 97

install-node:
	install -m 0755 scripts/start_capture /bin
	install -m 0755 scripts/stop_capture /bin
	install -m 0755 dragonfly3/df3_data_parser.py /bin

install-server:
	cp /etc/mysql/my.cnf /etc/mysql/my.cnf.orig
	sed -i s/bind-address\\s*=.*/bind-address=$(server_addr)/ /etc/mysql/my.cnf
	sed -i s/port\\s*=.*/port=$(db_port)/ /etc/mysql/my.cnf
	mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$(db_username)'@'%' IDENTIFIED BY '$(db_password)' WITH GRANT OPTION;" -p
	service mysql restart
	ln -sf $(CURDIR)/web $(web_folder)
	sed s/\$$USER/$(db_username)/ web/htaccess > web/.htaccess
	htpasswd -bc web/.htpasswd $(db_username) $(db_password)

clean: $(CLEAN_TARGET)

clean-node:
	@echo "Nothing to do"

clean-server:
	echo "Nothing to do"
	
uninstall: $(UNINSTALL_TARGET)
	rm -f /etc/init.d/datamap
	rm -f /bin/datamap_daemon_common.py
	rm -f /bin/datamap_$(type)_daemon
	rm -f /bin/.datamap_config
	update-rc.d -f datamap remove

uninstall-node:
	rm -f /bin/start_capture
	rm -f /bin/stop_capture
	rm -f /bin/df3_data_parser.py

uninstall-server:
	if [-e /etc/mysql/my.cnf.orig]; then mv /etc/mysql/my.cnf.orig /etc/mysql/my.cnf; fi;
	mysql -e "REVOKE ALL PRIVILEGES ON *.* FROM '$(db_username)'@'%'" -p
	service mysql restart
	rm -f $(web_folder)
