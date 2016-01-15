\NeedsTeXFormat{LaTeX2e}[1995/06/01]
\RequirePackage{ifthen}
\ProvidesClass{uiophd}[2008/04/15 v 1.03 UiO document class]
\DeclareOption{10pt}{\ClassWarningNoLine{uiophd}{Do not
        use type size `10pt'}}
\DeclareOption{11pt}{\ClassWarningNoLine{uiophd}{Do not
        use type size `11pt'}}
\DeclareOption{12pt}{}
\DeclareOption{american}{\renewcommand{\uiophd@lang}{american}}
\DeclareOption{english}{\renewcommand{\uiophd@lang}{english}}
\newcommand{\uiophd@lang}{american}
\DeclareOption{altfont}{\setboolean{uiophd@altfont}{true}}
\newboolean{uiophd@altfont}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions \relax
\RequirePackage[\uiophd@lang]{babel}
\RequirePackage[T1]{fontenc}
\RequirePackage[a4paper]{geometry}
\RequirePackage{setspace}
\AtBeginDocument{\setstretch{1.1}}
\RequirePackage{textcomp}
\LoadClass[openright,12pt]{report}
\geometry{twoside,margin=2.5cm}
\ifthenelse{\boolean{uiophd@altfont}}
  {\renewcommand{\rmdefault}{ptm}}
  {\renewcommand{\rmdefault}{padx}}
\ifthenelse{\boolean{uiophd@altfont}}
  {\renewcommand{\sfdefault}{phv}}
  {\renewcommand{\sfdefault}{iofs}}
\ifthenelse{\boolean{uiophd@altfont}}
  {\renewcommand{\ttdefault}{pcr}}
  {\renewcommand{\ttdefault}{hlct}}
\newcommand{\frontmatter}{\cleardoublepage
  \pagenumbering{roman}}
\newcommand{\mainmatter}{\cleardoublepage
  \pagenumbering{arabic}}
\newcommand{\backmatter}{\cleardoublepage}

