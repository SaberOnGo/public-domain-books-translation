# Step 07 Terminology Review
Check consistency of proper nouns, technical terms, industry terms.
Input: chapters/final/*.md + glossary/terms.csv
Output:
- qa/terminology/{same_filename}.md
- patch chapters/final/*.md in-place
Then set state.status=REVIEWED
