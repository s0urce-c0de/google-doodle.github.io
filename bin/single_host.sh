#/bin/bash
# this is for testing if you don't have a fancy server that can handle
# multiple paths. These files are excluded in .gitignore
# you need git subtree
cd "$(dirname "$(dirname "$0")")"

for doodle in $(jq -r '.[]' doodles/doodles.json); do
  bin/subtree/add_subtree "$doodle" "https://github.com/Google-Doodle/${doodle}.git" "$doodle" "main" # we always use main
done

ALREADY_WRITTEN_FILE=".testing_without_fancy_server"

if [ ! -e "$ALREADY_WRITTEN_FILE" ]; then
  echo "
$(jq -r '.[]' doodles/doodles.json)
$ALREADY_WRITTEN_FILE
" >> .git/info/exclude
  touch "$ALREADY_WRITTEN_FILE"
fi