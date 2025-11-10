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

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| appid                 | INTEGER   | PK                |
| name                  | TEXT      | NOT NULL          |
| controller_support    | INTEGER   |                   |
| has_achievements      | BOOLEAN   |                   |
| supports_windows      | BOOLEAN   |                   |
| supports_mac          | BOOLEAN   |                   |
| supports_linux        | BOOLEAN   |                   |
| price                 | REAL      |                   |
| release_date          | DATETIME  |                   |
| header_image          | TEXT      |                   |
| positive_reviews      | INTEGER   |                   |
| negative_reviews      | INTEGER   |                   |
| total_reviews         | INTEGER   |                   |

## categories
Information about Steam's official categories.

The id attribute matches the IDs provided by the Steam Store API. The IDs are
 NOT sequentially generated.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| id                    | INTEGER   | PK                |
| name                  | TEXT      | UNIQUE NOT NULL   |

## game_categories
A many-many relationship between games and categories.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| appid (games.appid)   | INTEGER   | NOT NULL, PK, FK  |
| cid (categories.id)   | INTEGER   | NOT NULL, PK, FK  |

## tags
Game tags gathered from user votes.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| id                    | INTEGER   | PK AUTOINCREMENT  |
| name                  | TEXT      | UNIQUE NOT NULL   |

## game_tags
A many-many relationship between games and tags.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| appid (games.appid)   | INTEGER   | NOT NULL, PK, FK  |
| tid (tags.id)         | INTEGER   | NOT NULL, PK, FK  |

## developers
Every game developer that has appeared on a Steam game page.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| id                    | INTEGER   | PK AUTOINCREMENT  |
| name                  | TEXT      | UNIQUE NOT NULL   |

## game_developers
A many-many relationship between games and developers.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| appid (games.appid)   | INTEGER   | NOT NULL, PK, FK  |
| did (developers.id)   | INTEGER   | NOT NULL, PK, FK  |

## publishers
Every game publisher that has appeared on a Steam game page.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| id                    | INTEGER   | PK AUTOINCREMENT  |
| name                  | TEXT      | UNIQUE NOT NULL   |

## game_publishers
A many-many relationship between games and publishers.

| Attribute             | Type      | Rules             |
|:----------------------|:---------:|------------------:|
| appid (games.appid)   | INTEGER   | NOT NULL, PK, FK  |
| pid (publishers.id)   | INTEGER   | NOT NULL, PK, FK  |

