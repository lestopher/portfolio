# Christopher Nguyen: selected work

Source of https://lestopher.github.io/portfolio/.

`make` rebuilds the diagram and the page, `make check` runs the checks, and `make preview` renders screenshots into `build/`.

`check.sh` reads a list of names that must never appear on the page from `~/.config/portfolio/forbidden`, one pattern per line, and refuses to pass without it. `make check` also reads the contact address from `~/.config/portfolio/email` to confirm the footer link assembles in a browser render; the address itself is never committed.
