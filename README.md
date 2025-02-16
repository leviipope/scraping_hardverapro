# scraping_hardverapro
This is a simple web scraping program that uses hardverapro as its source.
It was a fun way of learning web scraping basics.

## Versions

### V? (planned)
Graphs

### V1.2.5 (planned)
3080tis separated

### V2.0.1 *Current*
The database has been added to the GitHub Actions automation.

### V2.0.0
Created an SQLite database that is migrated from the csv.

### V1.2.4
Ti value changed from string to boolean.
"eloresorolt"; time without hh:mm; "ma" "tegnap" -> fixed to a yyyy-MM-dd hh:mm format

### V1.2.3 
if id not found in the current list -> archived to true

### V1.2.2
Send an email if a 3080 is listed below 160k

### V1.2.1
If gpu is in the csv but ice status has changed, it changes the ice status. In addition,
'ma' and 'tegnap' -> today's date and yesterday's date.

### V1.2.0
Added automation via GitHub actions.

### V1.1.0
Storing data on a csv and maintaining a "database" on it

### V1.0.1
Bug fixes (iced, promoted listings)

### V1.0.0
The basic program functions. The program is not dynamic at all. 
It can't be changed to other graphics cards or any other products on hardverapro.

## Planned for later
<li>more cards </li>
<li>SQL database</li>
