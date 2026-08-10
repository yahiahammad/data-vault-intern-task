# Data Vault Design Task

Design a Raw Vault for three T24 core banking source tables: customer,
account, and statement entry.

This task is design only. You will not write SQL and you will not run dbt.
You will hand in a diagram and a profiling note.

## What you are given

| Path | Contents |
|------|----------|
| data/fbnk_customer.csv | 15 rows of customer data |
| data/fbnk_account.csv | 14 rows of account data |
| data/fbnk_stmt_entry.csv | 30 rows of statement entry data |
| docs/source_dictionary.md | Column by column meaning of all three tables |
| docs/reference_codes.md | Meaning of the code values used in the data |
| docs/model_types.md | The model types and prefixes, as a naming reference |
| docs/deliverables.md | Exactly what to hand in and how it is assessed |
| templates/erd.mmd | Starting file for the diagram |

The CSV files are dummy data. They are small on purpose. You are expected to
read every row.

## What you must produce

1. An entity relationship diagram of the Raw Vault you would build, with the
   reasoning for every model written next to it.
2. A short profiling note recording what you found in the data.

See docs/deliverables.md for the required format.

## How to work

There is no rulebook in this repo beyond docs/model_types.md, which fixes
the vocabulary so we are talking about the same things. How you apply Data
Vault is your call. Read around, decide, and be ready to defend it.

1. Read docs/source_dictionary.md alongside the CSV files. Open the CSVs in a
   spreadsheet and sort them. Most of the design decisions in this task are
   only visible once you look at the actual rows.
2. Profile before you model. Write down, for each table, which columns are
   always empty, which repeat per entity, which change often, and which change
   almost never. Your satellite design comes out of that.
3. Model the business, not the tables. Three source tables do not mean three
   hubs. Decide what the durable business entities are first.
4. Write down the reason for every split and every link. The reasoning is
   worth more marks than the diagram.
5. Pick a naming standard, state it in one or two lines at the top of your
   diagram, and hold to it. We care that it is consistent and readable, not
   that it matches a house style you were never shown.

## Questions you should be able to answer at review

- Why is your hub count what it is?
- What is the grain of each satellite, in one sentence each?
- What happens to your design when a customer changes their phone number?
- What happens when the same statement entry is loaded twice?
- Which of your models would break if the source started sending a null in a
  column that is currently always populated?

## Time

The design is expected to take two to three working days including reading.
Ask questions early rather than guessing for a day.
