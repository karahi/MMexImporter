# MMexImporter
Python scripts to import CSVs of bank data into MMex (Money Manager EX)

This is a work in progress.  

##Usage:

1. Copy mmeximporter.cfg.sample to mmeximporter.cfg and fill it in
2. Call from commandline: ./mmeximporter.cfg <account number> <file_to_import>

## Configuration
"Schemas" is a little funny - the key is the account number you'd type in the command line above.  The value is a dictionary of the indices in the CSV for each necessary value for a transaction.  Currently the only supported key/values for transactions are:

  1. "Payee" : \<index in CSV\>
  2. "Date" : \<index in CSV\>
  3. "Amount" : \<index in CSV\>
  4. "Transaction Number" : \<index in CSV\>
  5. "date_format" : A strpftime-compatible string of the format the date comes in the CSV for proper parsing
  6. "inverse_amount" : The parse expects negative values for withdrawals and positive values for deposits.  If your CSV is opposite, set this to "True"
  7. "header" : If this is "True", then the parser skips the first row of the CSV.

## Acknowledgements
This borrows heavily in spirit (but not in code) from kvidoo's [MMexUpdater](https://github.com/kvidoo/MMexUpdater)