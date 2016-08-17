Filereader
==========

This is a very quick attempt at writing a tool that will read a text file
loud to you using an external tool, in this case Apple's ``say`` command
available in any console on Max OS X. Ironically, this was written after
reading Pieter Hintjens' book "Social Architecture" (much recommened) in
some inspired meta-state of trying to automate what had just happend (or
something like this).

This initial version maintains a bookmark per textfile to the last
paragraph read and will, when rerun on the same file, repeat this last
paragraph and continue reading from there.

The paragraph numbers are basically line numbers, not counting empty lines,
but including also those lines that will actually not be read, because the
are filtered, being comments or whatever.

You could record the audio by using ffmpeg or sox, which might be included
in a future version... But it is very questionable if a real human can
listen to larger amounts of text read by such a super-crude tool like this.

This code is not yet packaged or installable in any sense, being simply
a prototype, and was tested only on Python 3.5.

The self-test shown below does actually run on the online version of
Pieter's book mentioned above after fetching it first from github (this
will use the ``requests`` package which is the only external dependency).


Sample output (self-test)
-------------------------

.. code-block:: console

    $ python filereader.py -t
    socialarchitecture-master/ch00.txt
    (2) Preface

    (3) The Wisdom of Crowds

    (4) Niccolo Machiavelli observed, in "//Discourses on the First Decade of Titus Livius//" that:

    (5) "As for prudence and stability of purpose, I affirm that a people is more prudent, more stable, and of better judgment than a prince. Nor is it without reason that the voice of the people has been likened to the voice of God; for we see that wide-spread beliefs fulfill themselves, and bring about marvelous results."

    ^C
    Created/updated bookmark to para #5 for file "socialarchitecture-master/ch00.txt" in bookmarks.json.
    socialarchitecture-master/ch01.txt
