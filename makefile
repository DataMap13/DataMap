build:
	cd vermont; cmake -D SUPPORT_MYSQL=ON .
	make -C vermont

install:
	ln -sf $(CURDIR)/scripts/frequency_select.py /etc/init.d
	ln -sf $(CURDIR)/scripts/get_ipaddr.py /etc/init.d
	update-rc.d frequency_select.py defaults 98
	update-rc.d get_ipaddr.py defaults 97

clean:
	make -C vermont clean
