# run.sh


configs=(


"./configs/config.yaml"


)
for config_path in  "${configs[@]}";do
	echo "config file:" $config_path

	python ./scripts_space/INIT.py  $config_path
	python ./scripts_space/SATs.py  $config_path
	python ./scripts_space/ISLs.py  $config_path

done







