# Cyrillic review, Krista, Jul 1, 2022 

*These are raw notes from a review meeting. If image links stop working, they can also be found in the accompanying PDF.*

Krista: overall, this texture looks really good.

`₴` should probably be connected in the middle, more like handwriting


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656684390974_image.png)


Krista: should this be more v-like? is this diagonal too long?

- Anya: I asked a Kazahk designer

Krista: Did you talk to Jovanna about Serbian?

- Anya: yes, she said the strokes above are optional in handwriting… there are no strong laws on it for “print” handwriting

![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656684596789_image.png)


Anya: Macedonian feature is having issues

- Krista: it can be useful to include serbian and macedonian as stylistic sets
- (note: it does seem to work in font goggles, `script cyrl lang MKD`


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656684719342_image.png)


Krista: I would avoid having this thing in the middle

- You could also make the top a triangle, optionally


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656684821195_image.png)


Krista: this could be more open, and less like a snowflake/asterisk



![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656684931921_image.png)

![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656684972119_image.png)

![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685059929_image.png)


Krista: not sure how we should handle this in the light

- In Bulgarian, it can be easy to confuse the “T” and the “M”
- So, we should probably make the “m” rounder on top / more typical 


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685177545_image.png)


Krista: this is getting a bit too asymmetrical… it could get a tiny bit more symmetrical

- it’s shifted too mcuh towards the right side
- and maybe a bit too sharp
![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685310178_image.png)

![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685445807_image.png)


Krista: “ш” gives too much whitespace in the lowercase in extrabold

- Light style is fine


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685329664_image.png)


Krista: this has a bit too small of a counter


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685573095_image.png)

![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685684617_image.png)


A bit more spacing here, in the four-dot version

- Anya: Ukrainians said they would still write four dots in their handwriting


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685715891_image.png)


Krista: lowercase and uppercase forms have a conflict…

- probably make the uppercase version “print” rather than cursive, to better match the lowercase and the overall vibe
- I’ve only seen the cursive version in a very classical italic … it seems strange to see it upright


![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656685953246_image.png)


Krista: this is a bit too angular (almost z-like?)

- in handwriting it gets more vertical and smooth, if anything


## Features

Krista: all the locl features seem to be there

- my only suggestion is to duplicate these as stylistic sets
- people are used to finding them there, and in some software, locl features don’t work

Krista: currently, the two *idieresis* is under the `liga` feature, but it might be better in the `calt` so it is on by default more of the time


## Questions

Stephen: How is the current font order?

- consensus: it doesn’t really matter that much

Anya: on localization, 

![](https://paper-attachments.dropbox.com/s_4BDD5400A038B7BB7C8096C7271985A7F6A162887DBC4A1B3F4D9CC75597D607_1656686344395_image.png)


Anya: on localization, the Google Fonts glyph set includes several glyphs where certain things are with cedilla vs basic descender

- these days, type designers tend to do it with just a straight stroke 
- I asked a couple of people whether it matters, and the two people were split
- Krista: in such an informal typeface, it probably doesn’t matter much…

Anya: what about the `Ghestroke-cy.loclBSH` that looks like an F?

## Next steps
- We will review interpolations next time
- Send an email when ready


## Tasks

Anya
- [ ] Various shaping corrections as mentioned above

Stephen
- [ ] duplicate locl features into stylistic sets
- [ ] We should probably make the “m” rounder on top (would be more typical for Bulgarian)
- [ ] make sure alt glyphs are getting removed from “normal” static fonts… these weren’t removed in the latest build
- [ ] shift the ïï ligature to a `calt` feature

