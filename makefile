build:
	cd vermont; cmake -D SUPPORT_MYSQL=ON .
	make -C vermont

clean:
	make -C vermont clean
