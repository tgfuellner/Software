\version "2.14.2"

\header {
  title = "Kletzmer"
  composer = "Franz Dartmann"
  tagline = \markup {
    \column {
      "B. & Co. 25 633"
    }
  }
}

dc = _\markup { \center-column { "D.C." \line  {"al " \musicglyph #"scripts.coda" \musicglyph #"scripts.tenuto" \musicglyph #"scripts.coda"}}}

ZweiteStimme = \relative c'' {
  \set Staff.instrumentName = #"Klarinette 2 "
  \clef treble
  \key f \major
  \time 4/4

  d4 f f f | f2 f4. f8 | g4 f g a | fis2. d4 | d4 f f f |
  g2 e4 d | cis4 bes a g | f1 \bar ":|" a'4 fis2 fis4 | g fis g2 |
  e2. e4 | f4 g a f | bes, d d c | bes2 bes4. d8 | \mark \markup { \musicglyph #"scripts.coda" }
  f4 e d e | f1 | a4 fis2 fis4 | g fis g2 | e2. e4 | f g a f | bes, d d c | bes2 bes4. d8 |
  \mark \markup { \musicglyph #"scripts.coda" }
  cis4 a a4. g8 | f2. \mark "Fine" r4 \bar "|:" f'4 e g fis | f2 f | f4 e g fis |
  f2 f | d4 cis g' f | g f e ees | d2 cis | d2 d,4 r\dc \bar ":|"
}

\score {
    \transpose c d {
        \new Staff \ZweiteStimme
    }

    \layout { }
    % \midi { }
}

