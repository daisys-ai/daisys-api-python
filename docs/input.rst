Daisys API input
================

The following examples can be used to see how the Daisys API client library for Python can
be used.

For generating speech audio, the Daisys API supports input text that can include certain directives.

Input Text Customization
------------------------

Our models employ a powerful ``Normalizer`` (Advanced Text and SSML Tag Processor tool)
designed to process and normalize text, making it more readable and coherent. It is
equipped with a default pipeline of operations to apply on the input text, but it also
allows for customizing the normalization process according to specific needs.

Processor applies a series of pre-defined steps by default to transform your text:

Default pipeline:

1. **Abbreviations:** Converts common abbreviations like "Mr." to their full spoken
   versions (e.g., "Mister").
2. **Acronyms:** Acronyms will be processed and insert small pause between letter for
   better pronunciation (e.g., "10 AM" to "10 A M").
3. **URLs:** Replaces URLs with a more human-readable description. (e.g. "As an example of
   https://google.com" to "As an example of google dot com.")
4. **Numbers:** Converts numerical expressions to their spoken form (e.g., "10" to "ten",
   "$40" to "forty dollars").
5. **Punctuation Repeats:** Simplifies repeated punctuation (e.g., "Hey!!!!" to "Hey!").

Advanced Capabilities:
----------------------

The Normalizer also provides advanced functionalities to handle `SSML`_ tags. It follows
SSML is based on the World Wide Web Consortium's "Speech Synthesis Markup Language Version
1.0".  Partially supports `voice` , `phoneme` and `say-as` tags.

.. _SSML: https://www.w3.org/TR/2004/REC-speech-synthesis-20040907/

Voice Tag
^^^^^^^^^

The voice tag is used when the specific part of text that requests a change in speaking
voice (e.g. language). Input text might include excerpt in other languages. Our advanced
automatic language prediction algorithm captures these parts and inserts a voice tag with
proper language attribute. This allows model to apply required language change for that
section. This tag can be manually added to input text. Normalization will be applied based
on defined language for voice tag section.

Example usage:

.. code-block:: html

    Input: 
      The parking season ticket was valid <voice language="en"> t/m 09-01-2010</voice>.
    Normalizer output:
      The parking season ticket was valid tot en met negen januari tweeduizend tien.


Phoneme Tag
^^^^^^^^^^^

The phoneme tag provides specific pronunciation phonemization for model. The model will
use this pronunciation.

Example usage:

.. code-block:: html

      De <phoneme ph="ɣ ə k l øː r d ə"> gekleurde </phoneme> bevolking van een land.


..

    📌 Note: Phonemes need to be separated by space. In case of multiple words, they should be separated by `@` symbol (e.g. `De ernstige kapitein` → `d ə @ ɛ r n s t ə ɣ ə @ k ɑ p i t ɛɪ n`)

Say-as Tag
^^^^^^^^^^

The say-as tags allow users to specify the type of text to be normalized. Say-as tag has
two attributes ``interpret_as`` and ``format``. Main attribute is ``interpret_as``,
``format`` follows ``interpet_as`` attribute.

Supported attributes:

``interpret_as``

1. spell-out
2. number
3. date
4. time
5. currency

format
""""""

``interpret_as=number``

1. cardinal
2. ordinal
3. year

Example usage:

.. code-block:: html

    Input: 
      Vandaag is <say-as interpret-as="number" format="ordinal"> 3. </say-as> dag van de week.
      Vandaag is <say-as interpret-as="number" format="cardinal"> 3. </say-as> dag van de week.
      Het was <say-as interpret-as="number" format="year"> 1800 </say-as>.
      Horen om <say-as interpret-as="time">13.10</say-as>.
      Ik ben geboren op <say-as interpret-as="date"> 11.4.1984 </say-as>.

    Output:
      Vandaag is derde dag van de week.
      Vandaag is drie dag van de week.
      Het was achttienhonderd. 
      Horen om tien over één.
      Ik ben geboren op elf april negentien vierentachtig.
