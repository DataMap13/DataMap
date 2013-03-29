
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
	ln -sf $(CURDIR)/daemons/datamap_daemon_control /etc/init.d/
	ln -sf $(CURDIR)/daemons/datamap_daemon_common.py /etc/init.d/
	ln -sf $(CURDIR)/daemons/datamap_$(type)_daemon /etc/init.d/
	ln -sf $(CURDIR)/daemons/.datamap_config /etc/init.d/
	update-rc.d datamap_daemon_control defaults 97

clean:
	make -C vermont clean
