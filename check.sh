#!/bin/sh
# Checks for the portfolio page.
# Usage: ./check.sh         build checks plus the shipping gate (no draft markers, no placeholders)
#        ./check.sh build   build checks only
set -u
failed=0
fail() { echo "FAIL: $1: $2"; failed=1; }

EMDASH=$(printf '\342\200\224')
FORBIDDEN_FILE=${FORBIDDEN_FILE:-$HOME/.config/portfolio/forbidden}
LLM="not (just|only) [^.]* but|it'?s not [^.]*, it'?s|isn'?t [^.]*, it'?s|less about [^.]* than|delve|robust|seamless|leverag|passionate|cutting-edge|spearhead|synergy"

build_checks() {
  [ -f index.html ] || fail "index missing" "index.html not found"
  [ -f diagram.svg ] || fail "svg missing" "diagram.svg not found"
  { [ -f index.html ] && [ -f diagram.svg ]; } || return 0
  mkdir -p build

  grep -q -F '<title>Christopher Nguyen: selected work</title>' index.html || fail "title" "page title missing or changed"
  grep -q -F '<meta name="viewport"' index.html || fail "viewport" "viewport meta missing"

  grep -q -F 'href="diagram.svg"' index.html || fail "diagram link" "no relative link to diagram.svg"
  grep -q 'class="phone-note">[^<]*<a href="diagram.svg">' index.html || fail "phone note link" "the phone note must link to diagram.svg"
  grep -n -F 'href="/' index.html && fail "diagram link" "absolute link breaks under /portfolio/ (see above)"

  grep -q -F '<!-- diagram:start -->' index.html || fail "svg inline" "start marker missing"
  grep -q -F '<!-- diagram:end -->' index.html || fail "svg inline" "end marker missing"
  sed -n '/<!-- diagram:start -->/,/<!-- diagram:end -->/p' index.html | grep -q 'aria-label=' || fail "svg inline" "no aria-label on the inline svg"
  sed -n '/<!-- diagram:start -->/,/<!-- diagram:end -->/{//!p;}' index.html > build/inline.svg
  cmp -s build/inline.svg diagram.svg || fail "svg match" "inline svg differs from diagram.svg (run make)"

  for s in "DNS lookup" "HTTPS 443" "5432, app security group only" "uploads, credentials from the role over IMDSv2" \
           "signed webhook /webhooks/stripe" "SMS out; inbound webhook /webhooks/twilio" "SMTP 587" \
           "serve_from = aws" "serve_from = hetzner" "GET /up"; do
    grep -q -F -- "$s" diagram.svg || fail "flow labels" "'$s' missing from diagram.svg"
  done

  grep -n -E "github\.com/|Drawn from" index.html diagram.svg README.md \
    && fail "forbidden" "forbidden phrase (see above)"
  # Names that must never appear are listed one pattern per line in a file kept outside this repository.
  if [ -f "$FORBIDDEN_FILE" ]; then
    grep -n -f "$FORBIDDEN_FILE" index.html diagram.svg README.md \
      && fail "forbidden" "a name from $FORBIDDEN_FILE appears (see above)"
  else
    fail "forbidden" "list file $FORBIDDEN_FILE missing; the gate cannot run without it"
  fi
  # IP addresses: checked in prose and in the drawing's text labels, not in icon path data.
  grep -o '<text[^>]*>[^<]*' diagram.svg > build/svg-text.txt
  grep -n -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" build/svg-text.txt \
    && fail "forbidden" "looks like an IP address in a diagram label (see above)"

  grep -n -- "$EMDASH" index.html README.md tools/gen_diagram.py tools/splice.py check.sh Makefile 2>/dev/null \
    && fail "em dash" "em dash found (see above)"

  sed '/<!-- diagram:start -->/,/<!-- diagram:end -->/d' index.html | sed -e 's/<[^>]*>//g' > build/page.txt
  grep -n -iE "$LLM" build/page.txt && fail "llm-ism" "LLM-ism pattern or word in page text (see above)"
  grep -n -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" build/page.txt \
    && fail "forbidden" "looks like an IP address in page text (see above)"

  for id in 'id="si:claude"' 'id="si:anthropic"' 'id="si:openai"'; do
    grep -q -F "$id" index.html && fail "icons" "unrelated logo $id shipped in the page"
  done

  [ "$(wc -c < index.html)" -lt 400000 ] || fail "size" "index.html is $(wc -c < index.html) bytes, limit 400000"
  grep -q -F 'href="https://three-ring-binder.com/"' index.html || fail "three ring binder" "link to three-ring-binder.com missing"
  # The email address is assembled by a script at load time so it never sits in the HTML as one string.
  grep -n -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' index.html README.md check.sh Makefile tools/*.py \
    && fail "email" "an email address appears in the repository (see above)"
  grep -q -F 'id="email"' index.html || fail "email" "no element with id=\"email\" for the script to fill"
  grep -q -F "getElementById('email')" index.html || fail "email" "no script filling the email link"
  grep -q -F "'mailto:'" index.html || fail "email" "the script does not build a mailto link"
  grep -q -F '<noscript>' index.html || fail "email" "no noscript fallback for the address"
  grep -q -F 'href="https://www.linkedin.com/in/christopher-nguyen-96b0bb9"' index.html || fail "footer links" "LinkedIn is not a link"
  [ "$(grep -c -F 'More information available upon request.' index.html)" -eq 2 ] \
    || fail "request lines" "expected the 'more information' line under devbox and the agent, found $(grep -c -F 'More information available upon request.' index.html)"
  return 0
}

ship_checks() {
  [ -f index.html ] || return 0
  n=$(grep -c 'class="draft"' index.html)
  [ "$n" -eq 0 ] || fail "draft" "$n draft marker(s) remain"
  [ "$(grep -c -F '[URL]' index.html)" -eq 0 ] || fail "placeholder" "[URL] placeholder remains"
  return 0
}

case "${1:-}" in
  build) build_checks ;;
  "")    build_checks; ship_checks ;;
  *) echo "usage: $0 [build]" >&2; exit 2 ;;
esac
[ "$failed" -eq 0 ] && echo OK
exit "$failed"
