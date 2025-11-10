# DB Schema

## Games
The main table of the database, containing general data about every game.

The controller_support attribute uses the following values:
- 0: None
- 1: Partial
- 2: Full
- 3: Unknown

The header_image attribute is a string containing the URL of the game's header
image.

| Attribute             | Type      | Rules     |
|:----------------------|:---------:|----------:|
| appid                 | INTEGER   | PK        |
| name                  | TEXT      | NOT NULL  |
| controller_support    | INTEGER   |           |
| has_achievements      | BOOLEAN   |           |
| supports_windows      | BOOLEAN   |           |
| supports_mac          | BOOLEAN   |           |
| supports_linux        | BOOLEAN   |           |
| price                 | REAL      |           |
| release_date          | DATETIME  |           |
| header_image          | TEXT      |           |
| positive_reviews      | INTEGER   |           |
| negative_reviews      | INTEGER   |           |
| total_reviews         | INTEGER   |           |
