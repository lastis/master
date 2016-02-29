# Using rubber version 1.4
.PHONY: clean

default: 
	touch thesis.glo
	rubber -m glossaries -f --pdf -s thesis
	rm -rf *.aux *.bbl *.blg *.log *.toc *.snm *.out *.bcf *.out *.gls \
	*.ptc *.toc *.nav *.run.xml *.glo *.glg *.ilg *.ist *.xdy *.ind tags

clean:
	rm -rf *.aux *.bbl *.blg *.log *.toc *.snm *.out *.bcf *.out *.gls \
	*.ptc *.toc *.nav *.run.xml *.glo *.glg *.ilg *.ist *.xdy *.ind tags
