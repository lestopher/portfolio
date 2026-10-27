# make           regenerate diagram.svg and splice it into index.html
# make check     all checks, including the shipping gate
# make check-build   checks without the shipping gate
# make preview   screenshots at desktop and phone widths into build/
PY := python3 -I
CHROME ?= /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
# The expected contact address lives outside the repository, next to the forbidden-names list.
EMAIL_FILE ?= $(HOME)/.config/portfolio/email

all:
	$(PY) tools/gen_diagram.py tools/icons.json diagram.svg
	$(PY) tools/splice.py diagram.svg index.html

check: all
	./check.sh
	# The email link is built by a script, so render the page and confirm the DOM carries the mailto.
	mkdir -p build
	"$(CHROME)" --headless --disable-gpu --no-first-run --no-default-browser-check \
	    --user-data-dir=build/chrome-profile --dump-dom "file://$(abspath index.html)" > build/dom.html 2>build/chrome-dom.log
	@test -s "$(EMAIL_FILE)" || { echo "FAIL: email: $(EMAIL_FILE) missing; the DOM check cannot run without it"; exit 1; }
	@addr=$$(head -n 1 "$(EMAIL_FILE)"); grep -q -F "href=\"mailto:$$addr\">$$addr</a>" build/dom.html \
	    || { echo "FAIL: email: rendered page has no assembled mailto link for the address in $(EMAIL_FILE)"; exit 1; }
	@echo "email link assembles in the browser"

check-build: all
	./check.sh build

preview: all
	mkdir -p build
	"$(CHROME)" --headless --disable-gpu --no-first-run --no-default-browser-check \
	    --user-data-dir=build/chrome-profile --hide-scrollbars --window-size=1440,1000 \
	    --screenshot=build/desktop.png "file://$(abspath index.html)" 2>build/chrome.log
	# Headless Chrome on macOS clamps windows to 500px wide, so the phone shot lays the page out in a 390px iframe.
	printf '%s' '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#888}</style></head><body><iframe src="../index.html" style="display:block;width:390px;height:1600px;border:0;background:#fff"></iframe></body></html>' > build/phone-frame.html
	"$(CHROME)" --headless --disable-gpu --no-first-run --no-default-browser-check \
	    --user-data-dir=build/chrome-profile --hide-scrollbars --window-size=600,1600 \
	    --screenshot=build/phone.png "file://$(abspath build/phone-frame.html)" 2>>build/chrome.log

clean:
	rm -rf build

.PHONY: all check check-build preview clean
