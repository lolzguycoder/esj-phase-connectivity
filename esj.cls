%% ================================================================
%%  esj.cls  --  ENOSH Science Journal manuscript class
%%  Version 1.0.1 (2026/10/03)
%% ================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{esj}[2026/10/03 v1.0.1 ENOSH Science Journal manuscript class]

\newif\if@final        \@finalfalse
\newif\if@anon         \@anonfalse
\newif\if@lineno       \@linenotrue

\DeclareOption{submission}{\@finalfalse}
\DeclareOption{final}{\@finaltrue}
\DeclareOption{anonymous}{\@anontrue}
\DeclareOption{nolinenumbers}{\@linenofalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\if@final
  \LoadClass[10pt,twocolumn,a4paper]{article}
\else
  \LoadClass[12pt,onecolumn,a4paper]{article}
\fi

%% ---------------- Journal identity ----------------
\newcommand\journalname{ENOSH Science Journal}
\newcommand\journalabbrev{ESJ}
\newcommand\journalurl{enoshscience.org/journal/index.php/esj}
\newcommand\journalissn{ISSN 0000-0000 (Online)}
\newcommand\journalpublisher{ENOSH Science Center}
\newcommand\journallogo{esj-logo}
\newcommand\journallicense{This article is published under the Creative
  Commons Attribution 4.0 International License (CC BY 4.0).}
\RequirePackage{xcolor}
\definecolor{jmain}{HTML}{14112C}
\definecolor{jaccent}{HTML}{E60000}
\definecolor{jlight}{HTML}{F2F1F6}

%% ---------------- Packages ----------------
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{mathptmx}
\RequirePackage[scaled=0.92]{helvet}
\RequirePackage{courier}
\RequirePackage{amsmath,amssymb,amsthm}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{etoolbox}
\RequirePackage{setspace}
\RequirePackage{microtype}
\RequirePackage{enumitem}
\RequirePackage{authblk}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{titlesec}
\RequirePackage[font=small,labelfont={bf,sf,color=jmain},labelsep=period]{caption}
\RequirePackage{url}
\urlstyle{same}
\RequirePackage[round,authoryear]{natbib}
\RequirePackage[colorlinks=true,linkcolor=jmain,citecolor=jmain,
                urlcolor=jmain]{hyperref}

\if@final
  \RequirePackage[a4paper,top=22mm,bottom=22mm,left=16mm,right=16mm,
                  columnsep=7mm,headsep=5mm,footskip=9mm]{geometry}
\else
  \RequirePackage[a4paper,margin=25mm,headheight=30pt]{geometry}
\fi

%% ---------------- Citation style ----------------
\bibpunct{(}{)}{;}{a}{}{,}
\bibliographystyle{plainnat}
\setlength{\bibsep}{2pt plus 1pt}
\renewcommand{\bibfont}{\small}
\setlength{\bibhang}{1.5em}

%% ---------------- Metadata ----------------
\newcommand\@articletype{Research Article}
\newcommand\articletype[1]{\renewcommand\@articletype{#1}}
\newcommand\@volume{00}    \newcommand\volume[1]{\renewcommand\@volume{#1}}
\newcommand\@issue{0}      \newcommand\issue[1]{\renewcommand\@issue{#1}}
\newcommand\@pubyear{\the\year}
\newcommand\pubyear[1]{\renewcommand\@pubyear{#1}}
\newcommand\@firstpage{1}  \newcommand\firstpage[1]{\renewcommand\@firstpage{#1}\setcounter{page}{#1}}
\newcommand\@articledoi{10.0000/xxxx.0000}
\newcommand\articledoi[1]{\renewcommand\@articledoi{#1}}
\newcommand\@received{DD Month YYYY}  \newcommand\received[1]{\renewcommand\@received{#1}}
\newcommand\@revised{DD Month YYYY}   \newcommand\revised[1]{\renewcommand\@revised{#1}}
\newcommand\@accepted{DD Month YYYY}  \newcommand\accepted[1]{\renewcommand\@accepted{#1}}
\newcommand\@published{DD Month YYYY} \newcommand\published[1]{\renewcommand\@published{#1}}
\newcommand\@shorttitle{Short title}  \newcommand\shorttitle[1]{\renewcommand\@shorttitle{#1}}
\newcommand\@shortauthors{Author et al.}
\newcommand\shortauthors[1]{\renewcommand\@shortauthors{#1}}
\def\@corresp{}     \newcommand\corresp[1]{\def\@corresp{#1}}
\def\@keywords{}    \newcommand\keywords[1]{\def\@keywords{#1}}
\def\@msc{}         \newcommand\msc[1]{\def\@msc{#1}}

\renewcommand\Authfont{\normalsize\sffamily\bfseries}
\renewcommand\Affilfont{\footnotesize\normalfont\itshape}
\renewcommand\Authsep{, }
\renewcommand\Authand{ and }
\renewcommand\Authands{, and }
\setlength{\affilsep}{0.6em}

\RequirePackage{environ}
\newcommand\@abstracttext{}
\let\abstract\relax\let\endabstract\relax
\NewEnviron{abstract}{\global\let\@abstracttext\BODY}

%% ---------------- Headings ----------------
\setcounter{secnumdepth}{3}
\titleformat{\section}{\normalfont\sffamily\large\bfseries\color{jmain}}
  {\textcolor{jaccent}{\thesection}}{0.6em}{}
\titleformat{\subsection}{\normalfont\sffamily\normalsize\bfseries}
  {\thesubsection}{0.6em}{}
\titleformat{\subsubsection}{\normalfont\normalsize\itshape}
  {\thesubsubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{1.4ex plus .5ex}{0.8ex}
\titlespacing*{\subsection}{0pt}{1.2ex plus .4ex}{0.5ex}
\titlespacing*{\subsubsection}{0pt}{1ex plus .3ex}{0.4ex}

%% ---------------- Theorem environments ----------------
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{hypothesis}{Hypothesis}
\newtheorem{example}{Example}
\theoremstyle{remark}
\newtheorem{remark}{Remark}

%% ---------------- End-matter ----------------
\newcommand\@endsection[2]{%
  \par\medskip\noindent{\sffamily\bfseries\color{jmain}#1.}\enspace #2\par}
\newcommand\acknowledgments[1]{\if@anon
  \@endsection{Acknowledgments}{Removed for blind review.}\else
  \@endsection{Acknowledgments}{#1}\fi}
\newcommand\funding[1]{\@endsection{Funding}{#1}}
\newcommand\conflicts[1]{\@endsection{Conflict of Interest}{#1}}
\newcommand\dataavailability[1]{\@endsection{Data Availability}{#1}}
\newcommand\codeavailability[1]{\@endsection{Code Availability}{#1}}
\newcommand\ethics[1]{\@endsection{Ethics Statement}{#1}}
\newcommand\authorcontributions[1]{\if@anon\else
  \@endsection{Author Contributions}{#1}\fi}
\newcommand\aiuse[1]{\@endsection{Use of AI Tools}{#1}}

%% ---------------- Title block ----------------
\newcommand\@keywordline{%
  \ifx\@keywords\@empty\else
    \par\smallskip\noindent{\sffamily\bfseries\color{jmain}Keywords:}\enspace\@keywords
  \fi
  \ifx\@msc\@empty\else
    \par\noindent{\sffamily\bfseries\color{jmain}MSC 2020:}\enspace\@msc
  \fi}

\newcommand\@authorblock{%
  \if@anon
    {\sffamily\bfseries Anonymous Author(s)}\par
    {\footnotesize\itshape Affiliations removed for blind review}\par
  \else
    {\@author\par}%
    \ifx\@corresp\@empty\else
      \smallskip{\footnotesize\textbf{Correspondence:} \textsuperscript{*}\@corresp}\par
    \fi
  \fi}

\newcommand\@maketitle@submission{%
  \thispagestyle{jfirstsub}%
  \begin{singlespace}
  \begin{center}
    {\sffamily\small\color{jmain}\MakeUppercase{\@articletype}}\par\medskip
    {\sffamily\LARGE\bfseries\@title\par}\bigskip
    \@authorblock
  \end{center}
  \vspace{1em}
  \noindent{\sffamily\bfseries\color{jmain}Abstract}\par
  \noindent\@abstracttext\par
  \@keywordline\par
  \end{singlespace}
  \vspace{1.2em}}

\newcommand\@maketitle@final{%
  \twocolumn[{%
    \thispagestyle{jfirstfinal}%
    \noindent\begin{minipage}[c]{0.34\textwidth}
      \includegraphics[height=15mm]{\journallogo}\end{minipage}\hfill
    \begin{minipage}[c]{0.64\textwidth}\raggedleft
      {\sffamily\bfseries\LARGE\color{jmain}\journalname}\par\vspace{2pt}
      {\sffamily\scriptsize\color{jmain}\journalpublisher\enspace$\cdot$\enspace\journalissn}\par
      {\sffamily\scriptsize\color{jmain}Vol.~\@volume, No.~\@issue\ (\@pubyear)\enspace$\cdot$\enspace
        \url{https://doi.org/\@articledoi}}\par
    \end{minipage}\par
    \vspace{4pt}{\color{jaccent}\rule{\textwidth}{1.2pt}}\par
    \vspace{10pt}
    \noindent{\sffamily\small\bfseries\color{jaccent}\MakeUppercase{\@articletype}}\par
    \vspace{4pt}
    \noindent\begin{minipage}{\textwidth}\raggedright
      {\sffamily\huge\bfseries\color{black}\@title\par}\vspace{8pt}
      \@authorblock
    \end{minipage}\par
    \vspace{8pt}
    \noindent\colorbox{jlight}{\parbox{\dimexpr\textwidth-2\fboxsep}{%
      \vspace{4pt}\small
      \noindent{\sffamily\bfseries\color{jmain}Abstract}\par\smallskip
      \noindent\@abstracttext\par
      \@keywordline\par
      \vspace{4pt}{\scriptsize\sffamily\color{jmain}
        Received: \@received\enspace$\cdot$\enspace Revised: \@revised
        \enspace$\cdot$\enspace Accepted: \@accepted
        \enspace$\cdot$\enspace Published: \@published}\vspace{3pt}}}\par
    \vspace{14pt}
  }]%
  \saythanks}

\renewcommand\maketitle{%
  \if@final\@maketitle@final\else\@maketitle@submission\fi
  \if@final\else\if@lineno\linenumbers\fi\fi}

\newcommand\saythanks{%
  \begingroup
  \renewcommand\thefootnote{}%
  \footnotetext{\scriptsize\copyright\ \@pubyear\ The Author(s).
    \journallicense}%
  \endgroup}

%% ---------------- Page styles ----------------
\fancypagestyle{jfirstsub}{%
  \fancyhf{}\renewcommand\headrulewidth{0pt}
  \fancyhead[L]{\raisebox{-0.3\height}{\includegraphics[height=9mm]{\journallogo}}}
  \fancyhead[R]{\sffamily\scriptsize\color{jmain}Manuscript submitted to \journalname}
  \fancyfoot[C]{\sffamily\footnotesize\thepage}}
\fancypagestyle{jsub}{%
  \fancyhf{}\renewcommand\headrulewidth{0pt}
  \fancyhead[L]{\sffamily\scriptsize\color{jmain}\journalname\ -- manuscript under review}
  \fancyfoot[C]{\sffamily\footnotesize\thepage}}
\fancypagestyle{jfirstfinal}{%
  \fancyhf{}\renewcommand\headrulewidth{0pt}
  \fancyfoot[L]{\sffamily\scriptsize\color{jmain}\journalurl}
  \fancyfoot[R]{\sffamily\scriptsize\thepage}}
\fancypagestyle{jfinal}{%
  \fancyhf{}
  \renewcommand\headrulewidth{0.4pt}
  \renewcommand\headrule{{\color{jmain}\hrule height\headrulewidth width\headwidth}}
  \fancyhead[LE]{\sffamily\scriptsize\thepage\quad\color{jmain}\journalname}
  \fancyhead[RE]{\sffamily\scriptsize\itshape\@shortauthors}
  \fancyhead[LO]{\sffamily\scriptsize\itshape\@shorttitle}
  \fancyhead[RO]{\sffamily\scriptsize\color{jmain}\journalabbrev\
      \@volume(\@issue)\quad\color{black}\thepage}
  \fancyfoot[C]{\sffamily\scriptsize\color{jmain}https://doi.org/\@articledoi}}

\newlength\figwidth
\if@final\setlength\figwidth{\columnwidth}\else\setlength\figwidth{0.65\textwidth}\fi

\if@final
  \pagestyle{jfinal}
  \setlength{\parindent}{1em}
  \AtBeginDocument{\setlength{\abovedisplayskip}{6pt plus 2pt minus 2pt}%
    \setlength{\belowdisplayskip}{6pt plus 2pt minus 2pt}}
\else
  \pagestyle{jsub}
  \doublespacing
  \setlength{\parindent}{1.5em}
  \RequirePackage[running]{lineno}
  \renewcommand\linenumberfont{\normalfont\scriptsize\sffamily\color{gray}}
  \newcommand*\patchAmsMathEnvironmentForLineno[1]{%
    \expandafter\let\csname old#1\expandafter\endcsname\csname #1\endcsname
    \expandafter\let\csname oldend#1\expandafter\endcsname\csname end#1\endcsname
    \renewenvironment{#1}%
      {\linenomath\csname old#1\endcsname}%
      {\csname oldend#1\endcsname\endlinenomath}}%
  \newcommand*\patchBothAmsMathEnvironmentsForLineno[1]{%
    \patchAmsMathEnvironmentForLineno{#1}%
    \patchAmsMathEnvironmentForLineno{#1*}}%
  \AtBeginDocument{%
    \patchBothAmsMathEnvironmentsForLineno{equation}%
    \patchBothAmsMathEnvironmentsForLineno{align}%
    \patchBothAmsMathEnvironmentsForLineno{gather}}
\fi

\if@final\else
  \AtBeginEnvironment{table}{\singlespacing}
  \AtBeginEnvironment{figure}{\singlespacing}
  \AtBeginEnvironment{thebibliography}{\onehalfspacing}
\fi

\setlist{itemsep=2pt,topsep=4pt}
\endinput