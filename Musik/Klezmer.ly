\version "2.14.2"

#(set-default-paper-size "a4")

\paper {
  system-count = #6
}

\header {
  title = "Kletzmer"
  composer = "Franz Dartmann"
  tagline = \markup {
    \column {
      "B. & Co. 25 633"
    }
  }
}

% D.C. am Ende
dc = _\markup { \center-column { "D.C." \line  {"al " \musicglyph #"scripts.coda" \musicglyph #"scripts.tenuto" \musicglyph #"scripts.coda"}}}

coda = \mark \markup { \musicglyph #"scripts.coda" }

global = {
  \clef treble
  \key f \major
  \time 4/4
}

ErsteStimme = \relative c'' {
  \set Staff.instrumentName = #"Klarinette 1 "
  \global

  d4 a' a a| a2 a4. a8 | bes4 a bes c | a,2. d4 | d a' a a |
  bes2 g4 bes | a g f e | d1 \bar ":|" d'4 a d a | bes2 bes | 
  r4 g c bes | a1 | f4 bes bes a | g2 g4. bes8 | \coda a4 g f g | a1 |
  d4 a d c | bes2 bes | r4 g4 c bes | a1 | f4 bes bes a | g2 g4. bes8 | \coda
  a4 r f4. e8 | d2.\fermata r4 \bar "|:" d'4 cis c b | bes2 a | d4 cis c b |
  bes2 a | d4 cis bes a | bes a aes g | f2 e | d \acciaccatura cis'8 d4-> r \bar ":|"
}

ZweiteStimme = \relative c'' {
  \set Staff.instrumentName = #"Klarinette 2 "
  \global

  d4 f f f | f2 f4. f8 | g4 f g a | fis2. d4 | d4 f f f |
  g2 e4 d | cis4 bes a g | f1 \bar ":|" a'4 fis2 fis4 | g fis g2 |
  e2. e4 | f4 g a f | bes, d d c | bes2 bes4. d8 | \coda
  f4 e d e | f1 | a4 fis2 fis4 | g fis g2 | e2. e4 | f g a f | bes, d d c | bes2 bes4. d8 | \coda
  cis4 a a4. g8 | f2.\fermata \mark \markup {\bold Fine} r4 \bar "|:" f'4 e g fis | f2 f | f4 e g fis |
  f2 f | d4 cis g' f | g f e ees | d2 cis | d2 d,4 r\dc \bar ":|"
}

\score {
    \transpose c d {
      \new StaffGroup <<
        \new Staff \ErsteStimme
        \new Staff \ZweiteStimme
      >>
    }

    \layout {
    }

    % \midi { }
}

