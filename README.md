# NOVA Clippy

A simple web scraper and downloader for FCT-NOVA's internal e-learning platform, CLIP.

The program scrapes a user's courses for available downloads and syncs them with a local folder.

CLIP's files are organized in subcategories for each academic course like this:
Academic year >> Course documents >> Document subcategory >> Files list

Clippy successfully navigates the site in order to scrape it, and compares it to a local folder with a similar structure, keeping it in sync with the server.

```text
 __                 
/  \        _______________________ 
|  |       /                       \
@  @       | It looks like you     |
|| ||      | are downloading files |
|| ||   <--| from CLIP. Do you     |
|\_/|      | need assistance?      |
\___/      \_______________________/
```

## Usage

Usage: clippy [OPTIONS] [PATH]

### Arguments

[PATH]  The folder where CLIP files will be stored.

### Options

```text
--username        The user's username in CLIP.
--force-relogin   Ignores saved login credentials Ignora as credenciais guardadas em sistema. [default: no-force-relogin]                                                                        │
--auto            Automatically chooses the latest year available. [default: auto]                                                                            │
--help            Show this message and exit.
```