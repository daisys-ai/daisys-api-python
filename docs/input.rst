Daisys API input
================

The following examples can be used to see how the Daisys API client library for Python can
be used.

For generating speech audio, the Daisys API supports input text that can include certain directives.

Input Text Customization
------------------------

Our models employ a powerful ``Normalizer`` (Advanced Text and SSML Tag Processing tool)
designed to process and normalize text, making it more readable and coherent. It is
equipped with a default pipeline of operations to apply on the input text, but it also
allows for customizing the normalization process according to specific needs.

The Normalizer applies a series of pre-defined steps by default to transform the text:

Default pipeline:

1. **Abbreviations:** Converts common abbreviations like "Mr." to their full spoken
   versions (e.g., "Mister").
2. **Acronyms:** Acronyms will be processed and insert small pause between letter for
   better pronunciation (e.g., "10 AM" to "10 A M").
3. **Road numbers:** Converts road numbers by inserting a space, similar to acronyms (e.g. "A263" becomes "A 263").
4. **URLs:** Replaces URLs with a more human-readable description. (e.g. "As an example of
   https://google.com" to "As an example of google dot com.")
5. **Numbers:** Converts numerical expressions to their spoken form (e.g., "10" to "ten",
   "$40" to "forty dollars").
6. **Punctuation Repeats:** Simplifies repeated punctuation (e.g., "Hey!!!!" to "Hey!").
7. **Units:** Converts units such as "km/h" to their spoken form ("kilometer(s) per hour").

Advanced Capabilities:
----------------------

The Normalizer also provides advanced functionalities to handle `SSML`_ tags. It follows
SSML is based on the World Wide Web Consortium's "Speech Synthesis Markup Language Version
1.0".  Partially supports `voice` , `phoneme` and `say-as` tags.

.. _SSML: https://www.w3.org/TR/2004/REC-speech-synthesis-20040907/

Voice Tag
^^^^^^^^^

The voice tag is used when a specific text segment comes from a different language than
the base language of that model. Our advanced automatic language prediction algorithm captures these parts
and inserts a voice tag with the proper language attribute.
This allows the model to apply required language change for that section.
This tag can be manually added to input text. Normalization will be applied based
on the defined language for voice tag section.

Example usage:

.. code-block:: html

    Input:
      The parking season ticket was valid <voice language="nl">t/m 09-01-2010</voice>.
    Normalizer output:
      The parking season ticket was valid tot en met negen januari tweeduizend tien.


Phoneme Tag
^^^^^^^^^^^

The phoneme tag provides control over the phonemization for the model. The model will
use this pronunciation.

Example usage:

.. code-block:: html

      De <phoneme ph="ɣ ə k l øː r d ə">gekleurde</phoneme> vlag van een land.


..

    📌 Note: Phonemes need to be separated by a space. In case of multiple words, they should be separated by the `@` symbol (e.g. `De ernstige kapitein` → `d ə @ ɛ r n s t ə ɣ ə @ k ɑ p i t ɛɪ n`)

Say-as Tag
^^^^^^^^^^

The say-as tags allow users to interpret some specific types of text in a certain way.

Supported attributes:
1. spell-out
2. year
3. date
4. time


Example usage:

.. code-block:: html

    Input:
      Mijn naam spel je als <say-as interpret-as="spell-out">Fred</say-as>.
      Het was <say-as interpret-as="year">1944</say-as>.
      Ik vertrek om <say-as interpret-as="time">13.10</say-as>.
      Ik ben geboren op <say-as interpret-as="date">11.4.1984</say-as>.

    Output:
      Mijn naam spel je als F r e d.
      Het was negentien vierenveertig.
      Ik vertrek om tien over één.
      Ik ben geboren op elf april negentien vierentachtig.

w Tag
^^^^^

The ``<w>`` tag allows the user to select the correct pronunciation for a word based on the part of speech and meaning.
The part-of-speech tags from the [Penn Treebank](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) are used.

Example options:

- ``<w role="daisys:VB">read</w>`` : verb, present tense
- ``<w role="daisys:VBD">read</w>`` : verb, past tense
- ``<w role="daisys:NN">wind</w>`` : noun
- ``<w role="daisys:JJ">live</w>`` : adjective
- ``<w role="daisys:RB">live</w>`` : adverb
- ``<w role="daisys:NN" sense="daisys:DEFAULT">bass</w>`` : default meaning/pronunciation (in the example: the music-related sense)
- ``<w role="daisys:NN" sense="daisys:SENSE_1">bass</w>`` : first non-default meaning/pronunciation (in the example: the fish)

Emphasis Tag
^^^^^^^^^^^^

The ``<emphasis>`` tag allows to select a word for emphasis. Intonation and
duration behaviour of the model will be modified in the text between the tags.

The strength of the emphasis can be modulated by the ``level`` attribute, which
by default is ``moderate`` but can take the following values:

- ``<emphasis level="moderate">some text</emphasis>``: somewhat emphasize the text
- ``<emphasis level="strong">some text</emphasis>``: more strongly emphasize the text
- ``<emphasis level="down">some text</emphasis>``: emphasize the text by going down in pitch
- ``<emphasis level="none">some text</emphasis>``: avoid that the model automatically emphasizes this text

Note that the model will often choose which parts of a sentence to emphasize
depending on context if no hints are provided, so this level of control is
critical if you want to avoid that the wrong word is selected or the ensure the
right word is selected for emphasis.

The ``pause`` attribute may also be added to insert a pause after the word which
can enhance emphasis, it takes the same values as the ``strength`` attribute of
the ``<break>`` tag:

- ``<emphasis level="moderate" pause="weak">some text</emphasis>``: somewhat emphasize the text, including a short pause
- ``<emphasis level="strong" pause="weak">some text</emphasis>``: strongly emphasize the text, including a medium pause
- ``<emphasis pause="weak">some text</emphasis>``: somewhat emphasize the text, including a long pause

Break Tag
^^^^^^^^^

The ``<break>`` tag inserts a pause at a given place in the text.  The duration
of the pause can be controlled by the ``strength`` attribute:

- ``<break strength="weak"/>``: a short pause, such as after a comma
- ``<break strength="medium"/>``: a medium-length pause, such as between sentences
- ``<break strength="strong"/>``: a longer pause, such as between paragraphs

Prosody Tag
^^^^^^^^^^^

The ``<prosody>`` tag allows the user to change the pitch, pace and expression
of a sentence.  The range of values for each attribute is -10 to 10.

- ``<prosody pitch="8">Hi there, friend!</prosody>``: Relatively high pitched text
- ``<prosody pitch="-4">Hi there, friend.</prosody>``: Moderately low pitched text
- ``<prosody pace="-10">Hi there... friend...</prosody>``: Very slow paced text
- ``<prosody pace="7">Hi there, friend!</prosody>``: Somewhat high paced text
- ``<prosody expression="-5">Hi there, friend.</prosody>``: Moderately flat/monotonous text
- ``<prosody expression="10">Hi there, friend!</prosody>``: Highly expressive and modulated text

Style Tag
^^^^^^^^^

The ``<daisys:style>`` tag allows the user to switch to a different style of
speaking for a sentence, supported by the model.  E.g., for the `english-v3.0`
model, the model supports the *english* and *american* styles.

- ``<daisys:style name"english">The tube's a bit dodgy today, staying home.</daisys:style>``: Uses a British accent for the text
- ``<daisys:style name"american">I'll hop on the subway and be right over!</daisys:style>``: Uses an American accent for the text
