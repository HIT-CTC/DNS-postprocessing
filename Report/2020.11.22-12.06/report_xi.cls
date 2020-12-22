%-------------------------------------------------------------------
% This is my first package aims at writing report in a easier way.
% My purpose is to just use one package to write report.
% Make my code clean and neat.
% Keep modest and keep updating.
% Author: Lingchu Xi
% Version: 0.3.0
% Date: 2020-11-23
%-------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{report_xi}[2020/11/23 v0.3.0 Add a color box for code.]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\LoadClass[
    fontset = fandol,
    a4paper
]{article}

%----------------------------------------%
%----------- Package Required -----------%
%----------------------------------------%
%------------- Math Formula -------------%
\RequirePackage{amsmath}
%-------- Draw Or Import Graphic --------%
\RequirePackage{graphicx}
\RequirePackage{subfigure}
\RequirePackage{caption}
\RequirePackage{tikz}
\RequirePackage{tikz-3dplot}
\RequirePackage{epstopdf}
\RequirePackage{xcolor}
%-------- Geometry And Sturcture --------%
\RequirePackage[margin=1in, headsep=.2in, headheight=2in]{geometry}
\RequirePackage{float}
\RequirePackage{fancyhdr}
\RequirePackage{indentfirst}
\RequirePackage{booktabs}
%------------- Fonts Setting -------------%
\RequirePackage{fontspec}
\setmainfont{Times New Roman}
%--------------- Citation ---------------%
\RequirePackage{natbib}
\bibliographystyle{unsrt}
\newcommand{\upcite}[1]{\textsuperscript{\textsuperscript{\cite{#1}}}}
%--------------- Colorboxs ---------------%
\RequirePackage{tcolorbox}
\tcbuselibrary{theorems, listings, skins, breakable}
%--------------- Hyperref ---------------%
\RequirePackage{hyperref}

%-----------------------------------------%
%----------- Define Page Style -----------%
%-----------------------------------------%
\pagestyle{fancy}
\renewcommand{\headrulewidth}{1pt}
\renewcommand{\footrulewidth}{0pt}
\renewcommand{\sectionmark}[1]{\markboth{#1}{}}
\fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[C]{\thepage}
    \fancyhead[L]{\@dtitle}
    \fancyhead[R]{\leftmark}
}

%----------------------------------------%
%------------ Set Title Info ------------%
%----------------------------------------%
\newcommand{\dauthor}[1]{\def\@dauthor{#1}}
\newcommand{\dtitle}[1]{\def\@dtitle{#1}}
\newcommand{\dinstitute}[1]{\def\@dinstitute{#1}}
\newcommand{\demail}[1]{\def\@demail{#1}}
\newcommand{\dtel}[1]{\def\@dtel{#1}}
\renewcommand{\maketitle}{
    \begin{center}
        \textbf{\huge{\@dtitle}}\\
        \vspace{\baselineskip}
        \textbf{\large{\@dauthor}}\\
        \today \\
        \vspace{0.5\baselineskip}
        \textbf{Email:}\@demail \qquad \textbf{Tel:}\@dtel
    \end{center}
}

%-----------------------------------------%
%----------- Hyperref Settings -----------%
%-----------------------------------------%
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=cyan,
    filecolor=magenta
}
\urlstyle{same}
%-----------------------------------------%
%----------- Geometry Settings -----------%
%-----------------------------------------%
\renewcommand{\baselinestretch}{1.2}
\setlength{\parindent}{1em}
%----------------------------------------%
%---------- Auto Title And Bib ----------%
%----------------------------------------%
\AtBeginDocument{
    \maketitle
    \pagestyle{plain}
}
% Bib
\AtEndDocument{
    \bibliography{docs/cite}
}
%----------------------------------------%
%-------------- Code Style --------------%
%----------------------------------------%
\newcounter{listings}
\definecolor{bg}{RGB}{232 232 232}
\definecolor{bf}{RGB}{156 156 156}
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}
\definecolor{pblue}{rgb}{0.13,0.13,1}
\newtcblisting{codebox}[3][default]{
    theorem={Listing}{listings}{#2}{#3},
    fonttitle=\scriptsize\bfseries,
    colback=bg,
    colframe=bf,
    enhanced,
    listing only,
    breakable,
    listing options={
        language=#1,
        keywordstyle=\bfseries\color{pblue},
        stringstyle=\bfseries\itshape\color{green!40!black},
        commentstyle=\bfseries\itshape\color{black!60},
        % commentstyle=\color{codegreen},
        % keywordstyle=\color{magenta},
        % numberstyle=\tiny\color{codegray},
        % stringstyle=\color{codepurple},
        basicstyle=\ttfamily\footnotesize,
        numbers=left,
        numbersep=2mm,
        showspaces=false,
        showtabs=false,
        breaklines=true,
        showstringspaces=false,
        tabsize=1
    },
        overlay={
        \begin{tcbclipinterior}
            \fill[gray!25] (frame.south west) rectangle ([xshift=4mm]frame.north west);
        \end{tcbclipinterior}}
}
