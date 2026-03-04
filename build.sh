#!/bin/bash
# Build March 3 edition
cat parts/head.html parts/header.html parts/nav.html parts/main-start.html \
    parts/section-1.html parts/section-2.html parts/section-3.html \
    parts/section-4.html parts/section-5.html parts/section-6.html \
    parts/section-7.html parts/section-8.html \
    parts/closing-line.html parts/threads.html parts/jargon.html \
    parts/footer.html parts/mobile-nav.html parts/tooltip.html \
    parts/scripts.html > index.html
echo "Built index.html ($(wc -l < index.html) lines)"

# Build March 4 edition (shared: head.html, footer.html, tooltip.html)
cat parts/head.html parts-mar4/header.html parts-mar4/nav.html parts-mar4/main-start.html \
    parts-mar4/section-1.html parts-mar4/section-2.html parts-mar4/section-3.html \
    parts-mar4/section-4.html parts-mar4/section-5.html parts-mar4/section-6.html \
    parts-mar4/section-7.html parts-mar4/section-8.html \
    parts-mar4/closing-line.html parts-mar4/jargon.html \
    parts/footer.html parts-mar4/mobile-nav.html parts/tooltip.html \
    parts-mar4/scripts.html > march4.html
echo "Built march4.html ($(wc -l < march4.html) lines)"

# Build pitch page (shared: head.html, tooltip.html; uses mar4 scripts for standalone JS)
cat parts/head.html parts/pitch-body.html parts/tooltip.html \
    parts-mar4/scripts.html > pitch.html
echo "Built pitch.html ($(wc -l < pitch.html) lines)"

# Build soul page
cat parts/head.html parts/soul-body.html parts/tooltip.html \
    parts-mar4/scripts.html > soul.html
echo "Built soul.html ($(wc -l < soul.html) lines)"
