# MMexImporter
Python scripts to import CSVs of bank data into MMex (Money Manager EX)

This is a work in progress.  I am not actually a programmer, so please feel free to
contribute, but please don't judge. :)

##Usage:

1. Copy mmeximporter.cfg.sample to mmeximporter.cfg and fill it in
2. Call from commandline: ./mmeximporter.cfg \<account number\> \<file\_to\_import\>

## Configuration
"Schemas" is a little funny - the key is the account number you'd type in the command line above.  The value is a dictionary of the indices in the CSV for each necessary value for a transaction.  Currently the only supported key/values for transactions are:

  1. "payee" : \<index in CSV\>
  2. "date" : \<index in CSV\>
  3. "amount" : \<index in CSV\>, or...
    * 'debit\_amount' and 'credit_amount' (if there are separate columns for each)
    * "inverse\_amount" : Only valid when 'amount' is used.  The parser expects negative values for withdrawals and positive values for deposits.  If your CSV is opposite, set this to "True"
  4. "Transaction Number" : \<index in CSV\>
  5. "date_format" : A strpftime-compatible string of the format the date comes in the CSV for proper parsing
  6. "header" : If this is "True", then the parser skips the first row of the CSV.
  7. "notes" : \<index in CSV\> for arbitrary text that may be included

## Acknowledgements
This borrows heavily in spirit (but not in code) from kvidoo's [MMexUpdater](https://github.com/kvidoo/MMexUpdater)