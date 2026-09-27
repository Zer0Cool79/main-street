# Booking link

"Book now" buttons that point at the owner's existing booking tool (Acuity, Calendly, Square Appointments, Vagaro, etc.). **Off by default.** This feature links out; it does not build a booking system.

## How to turn it on/off

Flag: `booking` in `site.config.json`. Set `integrations.bookingUrl` to the booking page URL. Buttons render wherever the booking call-to-action belongs (header, hero, services).

## Why link out instead of building it

Booking is a solved problem with real money and real calendars attached. Building it into the site means owning availability logic, reminders, cancellations, and payments. That's a product, not a feature. The booking tools do it well; the site's job is to send people there with one obvious button.

## Rules

- **Every booking CTA points to the real tool.** Never link a "book now" button to the contact form as a placeholder. A dead-end booking button silently eats customers.
- The URL lives in config, not in the markup, so it can change without touching pages.
- If the owner changes booking tools, update the URL the same day and check every button.

## Costs

The booking tool itself is the owner's existing subscription (or free tier). This feature adds $0.
