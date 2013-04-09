
include .config

ifeq ($(type),node)
	BUILD_TARGET=build-node
	INSTALL_TARGET=install-node
else
	BUILD_TARGET=build-server
	INSTALL_TARGET=install-server
endif

build: $(BUILD_TARGET)

build-node:
	cd vermont; cmake -D SUPPORT_MYSQL=ON .
	make -C vermont
	
build-server:
	echo "Nothing to do"

install: $(INSTALL_TARGET)

install-node: install-both
	ln -sf $(CURDIR)/vermont/vermont /bin/
	ln -sf $(CURDIR)/vermont/db_config.xml /bin/vermont_config.xml
	ln -sf $(CURDIR)/scripts/start_vermont /bin/
	ln -sf $(CURDIR)/scripts/stop_vermont /bin/

install-server: install-both
	sed -i s/bind-address\\s*=.*/bind-address=$(server_addr)/ /etc/mysql/my.cnf
	sed -i s/port\\s*=.*/port=$(db_port)/ /etc/mysql/my.cnf
	mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$(db_user)'@'%' IDENTIFIED BY '$(db_password)' WITH GRANT OPTION;" -p
	sudo service mysql restart
	ln -sf $(CURDIR)/web $(web_folder)

install-both:
	ln -sf $(CURDIR)/daemons/datamap_daemon_control /etc/init.d/datamap
	ln -sf $(CURDIR)/daemons/datamap_daemon_common.py /bin/
	ln -sf $(CURDIR)/daemons/datamap_$(type)_daemon /bin/
	ln -sf $(CURDIR)/daemons/.datamap_config /bin/
	update-rc.d datamap defaults 97

clean:
	make -C vermont clean
