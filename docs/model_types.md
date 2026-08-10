# Model Types and Prefixes

This is a reference to come back to, not a rulebook. It fixes the vocabulary
so that your diagram and our questions use the same words. Everything else
about how you model is yours to work out.

| Entity | Prefix | Rule |
|--------|--------|------|
| Hub | rv_hub_ | Business entity with hash key, business key, and audit columns. |
| Reference hub | rv_ref_hub_ | Small lookup keyed on its technical primary key, no hash key. |
| Link | rv_link_ | Relationship between hubs. Primary key built from contributor hub hash keys. |
| Non-historized link | rv_nhlink_ | Immutable relationship or event. |
| Hub satellite | rv_sat_ | Attributes for one hub. |
| Link satellite | rv_lsat_ | Attributes for one link. |
| Non-historized satellite | rv_nhsat_ | Attributes for one non-historized link. |
| Reference satellite | rv_ref_sat_ | Attributes for one reference hub. |
| Multi-active hub satellite | rv_msat_ | Repeating attributes for one hub. |
| Multi-active link satellite | rv_mlsat_ | Repeating attributes for one link. |

You do not have to use every type. Use the ones your design needs and say why.
