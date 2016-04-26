# Using rubber version 1.4
.PHONY: clean

default: presentation.tex $(DEPENDS)
		rubber -f --pdf -s $<
		# rubber-info --check $<
		rm -rf *.aux *.bbl *.blg *.log *.toc *.snm *.out *.bcf *.out *.ptc *.toc *.nav *.run.xml tags

clean:
		rm -rf *.aux *.bbl *.blg *.log *.toc *.snm *.out *.bcf *.out *.ptc *.toc *.nav *.run.xml tags
