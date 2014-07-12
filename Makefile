all: addons

design/saas_manager.xmi: design/saas_manager.zargo
	-echo "REBUILD saas_manager.xmi from saas_manager.zargo. I cant do it"

addons: saas_manager

saas_manager: design/saas_manager.uml
	xmi2oerp -r -i $< -t addons -v 2

clean:
	rm -rf addons/saas_manager/*
	sleep 1
	touch design/saas_manager.uml
