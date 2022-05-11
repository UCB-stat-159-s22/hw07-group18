help:
	@echo 'How to use our repository                                                 '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make clean                         clearing all figures/output folders        '
	@echo '                                                                          '
    
    
clean:
	rm -rf figures
	rm -rf models
	@echo ' Clearing Figures folder                                                                        '
	mkdir figures
	mkdir models
	touch figures/.gitkeep
	touch models/.gitkeep
    
all:
	conda activate hw7
	jupyter execute Analysis.ipynb
    
env:
	conda env create -f environment.yml
	conda activate hw7