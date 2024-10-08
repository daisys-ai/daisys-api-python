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
