%-------------------------------------------------------------------
% This is my first package aims at writing report in a easier way.
% My purpose is to just use one package to write report.
% Make my code clean and neat.
% Keep modest and keep updating.
% Author: Lingchu Xi
% Version: 0.2.0
% Date: 2020-10-27
%-------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{report_xi}[2020/10/27 v0.2.0 Help you write your report easier.]
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
%-------- Geometry And Sturcture --------%
\RequirePackage[margin=1in, headsep=.2in, headheight=2in]{geometry}
\RequirePackage{float}
\RequirePackage{fancyhdr}
\RequirePackage{indentfirst}
\RequirePackage{booktabs}
%------------- Fonts Setting -------------%
\RequirePackage{fontspec}
\setmainfont{Times New Roman}
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
