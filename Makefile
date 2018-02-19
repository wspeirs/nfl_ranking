# change this to whatever the names of the files are... blah.tex, blah.bib
DOC = paper

TEX = $(DOC).tex
BIB = $(DOC).bib

# just make the whole thing if either of these files have changed
create: $(TEX) $(BIB)
	latex $(DOC) && bibtex $(DOC); latex $(DOC) && latex $(DOC)

# makes the dvi if needed, and then starts up xdvi
dvi: create
	xdvi $(DOC).dvi

# makes the dvi if needed, and then creates a ps file
ps: create
	dvips $(DOC).dvi -o $(DOC).ps

# makes the dvi if needed, and then creates a pdf file
pdf: create
	dvipdf $(DOC).dvi

# makes the dvi if needed and then prints the file
print: create
	dvips $(DOC).dvi 

# removes all files except the .tex and .bib file
clean:
	rm $(DOC).aux $(DOC).bbl $(DOC).blg $(DOC).dvi $(DOC).log $(DOC).pdf $(DOC).ps
