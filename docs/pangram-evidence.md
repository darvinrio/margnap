# All About Supporting Evidence | Pangram

Link to Original: https://www.pangram.com/supporting-evidence

How we measure the fingerprints AI leaves behind.

You probably know the giveaways. The word "delve". The scattered em dashes. The off-putting emojis, or advanced formatting where it shouldn't be. Or maybe, you can't put your finger on it, but a certain document just smells like AI.

You're likely to be right. [Research has shown](https://arxiv.org/abs/2501.15654) that individuals can train their personal intuition to detect AI writing by eye. But sometimes, it's laborious, confusing, and hard to communicate.

Supporting Evidence is a suite of tools to bring those AI tells to the surface. Using evidence-backed feature extraction across our corpus of millions of human and AI documents, we've identified nine patterns commonly found in AI outputs.

No single piece of supporting evidence is a giveaway. Just because a particular AI phrase or emoji appears in a text does not mean it was written by AI.

Pangram's flagship detection model takes a comprehensive view of a document and uses a deep-learning based detector that synthesizes millions of signals about a particular text. Extracted pieces of supporting evidence are not inputs to our model.

Given enough pieces of evidence, we hope to give you more understanding, more clarity, and more confidence in Pangram's AI prediction. Here's a breakdown of the nine patterns we track, ordered by how much more often they appear in AI text than human text.

Nine Pieces of Supporting Evidence
----------------------------------



* Signal: Markdown
  * Example: **amylase**Supporting EvidenceMarkdownMarkdown formatting inserted into plain text contexts
  * Humanper 10k words: 8
  * AIper 10k words: 90
  * Multiplier: 12×
* Signal: AI Phrases
  * Example: 45xdelve intoSupporting EvidenceAI PhraseWord patterns that appear far more often in AI-generated text
  * Humanper 10k words: 3
  * AIper 10k words: 30
  * Multiplier: 12×
* Signal: Em dashes
  * Example: Supporting EvidenceEm DashOveruse of em dashes where human writers typically would not
  * Humanper 10k words: 2
  * AIper 10k words: 17
  * Multiplier: 10×
* Signal: Bullet lists
  * Example: - Salivary glandsSupporting EvidenceBullet ListsStructured lists used to organize information systematically
  * Humanper 10k words: 3
  * AIper 10k words: 28
  * Multiplier: 9×
* Signal: Triads
  * Example: Triads1past, 2present and 3futureSupporting EvidenceTriadsGrouping ideas in threes, a common AI rhetorical pattern
  * Humanper 10k words: 5
  * AIper 10k words: 19
  * Multiplier: 4×
* Signal: "Not just X but Y"
  * Example: Anot just survive Bbut thriveSupporting EvidenceContrast Pattern'Not just A but B' constructions common in AI writing
  * Humanper 10k words: 1
  * AIper 10k words: 3
  * Multiplier: 3×
* Signal: Unusual Unicode
  * Example: ≈Supporting EvidenceUnicodeUnusual Unicode characters that may indicate humanization attempts
  * Humanper 10k words: 28
  * AIper 10k words: 71
  * Multiplier: 3×
* Signal: AI-style headers
  * Example: Certainly! Here'sSupporting EvidenceAI HeaderOverly helpful headers and introductions common in AI output
  * Humanper 10k words: 1
  * AIper 10k words: 2
  * Multiplier: 2×
* Signal: Emojis
  * Example: 🚀Supporting EvidenceEmojiEmoji inserted where human writers typically would not
  * Humanper 10k words: 0.1
  * AIper 10k words: 0.2
  * Multiplier: 2×


Markdown(12×)
-------------

Markdown is a way of encoding formatting as characters. It shows up as \*\*bold\*\*, ## Headers, \`\`\`inline code\`\`\`, or \*italics\*. Large Language Models often reach for fancy visualizations to emphasize items or draw attention to certain phrases. Humans typing into Google docs, email clients, or forum boxes rarely do.

Real-World Examples

One very important enzyme in your body is amylaseSupporting EvidenceMarkdownMarkdown formatting inserted into plain text contexts. Amylase helps break down starches (like bread, pasta, rice)…

Langer-Giedion syndrome (LGS)Supporting EvidenceMarkdownMarkdown formatting inserted into plain text contexts, also known as Trichorhinophalangeal Syndrome Type II…

#### Multiplier by markdown variant

Different markdown symbols are used at different rates by humans and AI.


|Variant        |Human / 10k|AI / 10k|Multiplier|
|---------------|-----------|--------|----------|
|Bold (**text**)|2          |65      |43×       |
|Headers (#)    |0.5        |11      |23×       |
|Inline code    |0.2        |0.8     |5×        |
|Italic         |5          |13      |2×        |


AI Phrases(12×)
---------------

AI Phrases were our original piece of supporting evidence. Sometimes it’s easy to notice that AI tends to overuse certain words and phrases. But when you look closer, you can find thousands of phrases that AI overuses to a statistically significant degree. Here, we highlight those phrases.

Real-World Examples

35xIn today's fast-paced worldSupporting EvidenceAI PhraseWord patterns that appear far more often in AI-generated text, it's 22xcrucial to note thatSupporting EvidenceAI PhraseWord patterns that appear far more often in AI-generated text we must 45xdelve intoSupporting EvidenceAI PhraseWord patterns that appear far more often in AI-generated text the ever-evolving landscape of information and 18xnavigate the tapestry ofSupporting EvidenceAI PhraseWord patterns that appear far more often in AI-generated text modern challenges.

#### A sampling of AI phrases

Each of these appears far more often in AI writing than in human writing. Different models have different favorites, so we maintain lists per model family.

*   “ability to adapt to”
*   “accessible even for those”
*   “anyone looking to elevate”
*   “become a focal point”
*   “become an essential part”
*   “blur the line between”
*   “can vary depending on the specific”
*   “casual night”
*   “complex tapestry”
*   “engaging narrative”
*   “fascinating and complex”
*   “feel repetitive”
*   “guessing until the final”
*   “he was known for”
*   “highly recommend for anyone”
*   “his ability to perform”
*   “i am writing to provide”
*   “i ordered their signature”
*   “is a compelling read”
*   “is a great question”
*   “its compact design”
*   “known for his ability”
*   “let me know if you'd”
*   “light on the complex”
*   “making it simple to”
*   “noticeable lag”
*   “offering profound”
*   “profound connection between”
*   “read for anyone interested”
*   “recently had the pleasure”
*   “reflection in the polished”
*   “steady despite the tremor”
*   “testament to human”
*   “to adapt to different”
*   “to detail and commitment”
*   “took a slow sip”
*   “weight of unspoken”
*   “you for your continued dedication”
*   “you or someone you know”
*   “you're touching on”

Em dashes(10×)
--------------

Em dashes are a legitimate type of punctuation that are used to indicate a break, add emphasis, or replace other punctuation for a more dramatic tone. For reasons not immediately obvious, AI uses em dashes at 10x the human rate.

Real-World Examples

I have a boring life Supporting EvidenceEm DashOveruse of em dashes where human writers typically would not had, I should say. Accountant by day, Netflix binge-watcher by night.

Michigan irrevocably changed. The "Big Three" automakers Supporting EvidenceEm DashOveruse of em dashes where human writers typically would not Ford, General Motors, and Chrysler Supporting EvidenceEm DashOveruse of em dashes where human writers typically would not made Michigan the automotive capital of the world.

#### Em dashes per 10,000 words, by model family

Humans average **5** em dashes per 10,000 words. Most model families exceed that by 7x-9x, while Gemini 3 Pro uses fewer em dashes than human writers.


|Model family         |Per 10k|Multiplier|
|---------------------|-------|----------|
|Human baseline       |5      |1×        |
|OpenAI               |45     |9×        |
|Open Source          |37     |8×        |
|Anthropic            |32     |7×        |
|Google (Gemini 3 Pro)|3      |0.7×      |


> One theory: AI em dash overuse surged in 2024, after the initial rise of LLMs, leading some to speculate that they stem from the document parsers foundation model companies use to scan and train on books and other long print documents.

Bullet lists(9×)
----------------

Where a human would write “apples, oranges, and bananas,” a model reaches for a line break and a dash, mostly to better organize text in quick conversational chat interfaces. This isn’t wrong, just more of a structural habit. Models produce them at roughly nine times the human rate, often in contexts where prose would read more naturally.

Real-World Examples

You make amylase in: \- Salivary glands – in your mouthSupporting EvidenceBullet ListsStructured lists used to organize information systematically \- Pancreas – secretes it into your small intestineSupporting EvidenceBullet ListsStructured lists used to organize information systematically

Whereas humans might write: Amylase is made in your salivary glands and pancreas, which release it into your small intestine to break down starches.

Triads(4×)
----------

The rule of three is a linguistic pattern that has existed for centuries. Many triads have entered our shared vocabulary: “blood, sweat, and tears.” “past, present, and future,” or even “reduce, reuse, recycle!” But AI takes it further than what often feels natural, using them about four times as often as humans.

Real-World Examples

I need to make sure it's concise, includes objectives, Triads1methods, 2results and 3conclusionsSupporting EvidenceTriadsGrouping ideas in threes, a common AI rhetorical pattern without extra fluff.

…threads that connect Triads1past, 2present and 3futureSupporting EvidenceTriadsGrouping ideas in threes, a common AI rhetorical pattern in this sacred place.

…a film that explores themes of Triads1love, 2loss and 3identitySupporting EvidenceTriadsGrouping ideas in threes, a common AI rhetorical pattern.

Not just X but Y(3×)
--------------------

One of the more inexplicable AI patterns, Not just X but Y refers to the extremely common template. AI loves to tell you that something isn’t just one thing, it’s an entirely separate thing altogether! AI uses phrases that fit this template three times as often as humans.

Real-World Examples

…a celestial compass that could navigate Anot only seas Bbut also the fabric of destiny itselfSupporting EvidenceContrast Pattern'Not just A but B' constructions common in AI writing.

…the baby symbolizes Anot only vulnerability Bbut also the possibility of renewal after catastropheSupporting EvidenceContrast Pattern'Not just A but B' constructions common in AI writing.

Unusual Unicode(3×)
-------------------

Unusual unicode characters are characters that aren’t on anyone’s keyboard: decorative dashes, math operators, arrow glyphs, box-drawing characters, or UI-style markers. These can show up in human text, but are rare. Furthermore, unusual unicode characters used in otherwise unrelated text can sometimes indicate humanization attempts.

Real-World Examples

Almost-equal glyph

The odds were ≈Supporting EvidenceUnicodeUnusual Unicode characters that may indicate humanization attempts 0.73 across all the experiments we ran.

Math operators

Any base ≥Supporting EvidenceUnicodeUnusual Unicode characters that may indicate humanization attempts 2 works mathematically. If we'd standardized on base-12, we'd…

Arrow glyphs

Before reacting with amylase: Starch + iodine →Supporting EvidenceUnicodeUnusual Unicode characters that may indicate humanization attempts dark blue or black color

#### Top unusual Unicode characters in AI text


|Char|Codepoint|Name                         |Multiplier|
|----|---------|-----------------------------|----------|
|─   |U+2500   |box drawings light horizontal|940×      |
|≈   |U+2248   |almost equal to              |241×      |
|⚠   |U+26A0   |warning sign                 |57×       |
|→   |U+2192   |rightwards arrow             |48×       |


Emojis(2×)
----------

Overall emoji use is barely elevated in AI text; humans use them about as often. But _which_ emojis differ wildly. Checkmarks, warning signs, and keycap numbers appear at rates hundreds of times above the human baseline, whereas humans use faces to express themselves far more often than AI.

Real-World Examples

Here's a quick framework to decide: ### ✅Supporting EvidenceEmojiEmoji inserted where human writers typically would not When it might make sense: 1. Lower interest rate…

\### ⚠️Supporting EvidenceEmojiEmoji inserted where human writers typically would not Key Risks to Avoid - Tax Evasion: Underreporting cash payments can lead to…

Space is amazing — thanks for asking! 🚀Supporting EvidenceEmojiEmoji inserted where human writers typically would not

#### Which emojis, not how many

Aggregate emoji use is barely elevated in AI text. But _which_ emojis differ wildly — UI-coded glyphs appear hundreds of times above the human baseline.


|Emoji|Name                  |Multiplier|
|-----|----------------------|----------|
|✅    |white heavy check mark|167×      |
|2️⃣  |keycap two            |129×      |
|4️⃣  |keycap four           |98×       |
|3️⃣  |keycap three          |86×       |
|✔️   |check mark            |64×       |
|1️⃣  |keycap one            |61×       |
|🚀   |rocket                |26×       |
|❌    |cross mark            |24×       |


#### The humans fight back

Everyday social emojis appear slightly more often on the human side:


|Emoji|Multiplier|
|-----|----------|
|😊   |0.6×      |
|❤️   |0.2×      |


The feature

### Supporting Evidence in Pangram

[Try it now](https://www.pangram.com/dashboard)
