# FAQ

Expandable questions and answers. **On by default.**

## How to turn it on/off

Flag: `faq` in `site.config.json`. Questions use native `<details>`/`<summary>` elements: no JavaScript, works everywhere, accessible by default.

## Writing good FAQs

- Answer questions customers **actually ask**: parking, hours, dietary options, booking, prices, "do you do X?" If the owner has answered it twice in person, it belongs here.
- Short answers. Two to four sentences. Link to the relevant page for the long version.
- Write the question the way the customer phrases it ("Do you have gluten-free options?"), not the way the business phrases it ("Our allergen accommodation policy").
- 5 to 10 questions. More than that and it's a manual; split it into a page.

## SEO bonus

The build generates FAQ structured data from these questions, which can earn rich results in search. Keep the questions and answers in the HTML (not JS-rendered) so crawlers see them. See `rules/seo.md`.

## Maintenance

When the business changes something the FAQ answers (hours, policies, prices), the FAQ must change in the same commit. Make this a habit: "we changed X, does the FAQ still agree?"
