venv\Scripts\activate
cd .\website
..\venv\Scripts\python copy_notebooks.py
..\venv\Scripts\pelican content -o output -s pelicanconf.py
xcopy output\pages\* output\ /Y
..\venv\Scripts\ghp-import output
git push origin gh-pages
cd ..
cd .\book
..\venv\Scripts\python copy_notebooks.py
cd .\content\notebooks
pdflatex -synctex=1 -interaction=nonstopmode --shell-escape book.tex
cd ..\..\..