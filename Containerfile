FROM texlive/texlive:latest

WORKDIR /workdir
ENTRYPOINT ["latexmk", "-pdf", "-outdir=build", "-interaction=nonstopmode"]
CMD ["main.tex"]
