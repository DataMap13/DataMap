
include .config

ifeq ($(type),node)
	BUILD_TARGET=build-node
else
	BUILD_TARGET=build-server
endif

build: $(BUILD_TARGET)

build-node:
	cd vermont; cmake -D SUPPORT_MYSQL=ON .
	make -C vermont
	
build-server:
	echo "Nothing to do"

install:
	ln -sf $(CURDIR)/daemons/datamap_daemon_control /etc/init.d/datamap
	ln -sf $(CURDIR)/daemons/datamap_daemon_common.py /bin/
	ln -sf $(CURDIR)/daemons/datamap_$(type)_daemon /bin/
	ln -sf $(CURDIR)/daemons/.datamap_config /bin/
	update-rc.d datamap defaults 97

clean:
	make -C vermont clean
