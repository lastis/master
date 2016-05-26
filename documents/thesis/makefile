# Using rubber version 1.4
.PHONY: clean

# The -c option passes arguments to the latex compiler. --unsafe is needed 
# because of this. Minted requires the --shell-escape option.
default: 
	rm -rf *.aux *.bbl *.blg *.log *.toc *.snm *.out *.bcf *.out *.gls \
	*.ptc *.toc *.nav *.run.xml *.glo *.glg *.ilg *.ist *.xdy *.ind *.pyg \
   	tags _minted*
	rubber -f --pdf -s --unsafe -c 'setlist arguments --shell-escape' thesis
	rm -rf *.aux *.bbl *.blg *.log *.toc *.snm *.out *.bcf *.out *.gls \
	*.ptc *.toc *.nav *.run.xml *.glo *.glg *.ilg *.ist *.xdy *.ind *.pyg \
   	tags _minted*

clean:
	rm -rf *.aux *.bbl *.blg *.log *.toc *.snm *.out *.bcf *.out *.gls \
	*.ptc *.toc *.nav *.run.xml *.glo *.glg *.ilg *.ist *.xdy *.ind *.pyg \
   	tags _minted*
