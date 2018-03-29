(TeX-add-style-hook
 "relatorio"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "12pt" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("babel" "brazilian") ("geometry" "left=3.00cm" "right=2.00cm" "top=3.00cm" "bottom=2.00cm") ("hyperref" "breaklinks")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art12"
    "inputenc"
    "babel"
    "geometry"
    "enumitem"
    "longtable"
    "tabu"
    "zi4"
    "listings"
    "lstautogobble"
    "color"
    "mathpazo"
    "parskip"
    "graphicx"
    "verbatim"
    "booktabs"
    "amsmath"
    "hyperref")
   (TeX-add-symbols
    '("code" 1)))
 :latex)

