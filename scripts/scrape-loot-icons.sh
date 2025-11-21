#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <output_directory>"
    exit 1
fi

OUTDIR="$1"
mkdir -p "$OUTDIR"

BASE_URL="https://arcraiders.wiki"
LOOT_URL="$BASE_URL/wiki/Loot"

echo "[DEBUG] Fetching page..."
HTML=$(curl -s "$LOOT_URL")

echo "[DEBUG] Page length: ${#HTML}"

###############################################################################
# 1. Navigate to /html/body/div[1]/main/div[2]/div/div[2]/div[1]/section/div/div[2]
###############################################################################

# Extract first <div> inside <body>
BODY_DIV1=$(echo "$HTML" | sed -n '/<body/,/<\/body>/p' \
    | sed -n '/<div/,/<\/div>/p')

# Extract <main> inside that <div>
MAIN=$(echo "$BODY_DIV1" | sed -n '/<main/,/<\/main>/p')

# Extract main/div[2]/div/div[2]/div[1]/section/div/div[2]
CONTAINER=$(echo "$MAIN" \
    | sed -n '/<main/,/<\/main>/p' \
    | sed -n '/<div[^>]*>/,/<\/div>/p' \
    | sed -n '1,/./p' ) # first container div

# We now need the specific path: main > div[2] > div > div[2] > div[1] > section > div > div[2]

# Practically: Extract section and then the inner div[2]
SECTION=$(echo "$MAIN" | sed -n '/<section/,/<\/section>/p')

INNER=$(echo "$SECTION" | sed -n '/<div[^>]*>/,/<\/div>/p' | sed -n '2,/./p')

###############################################################################
# 2. Inside that container: select table[2]
###############################################################################

# Extract ALL tables inside this container
TABLES=$(echo "$HTML" \
    | sed -n '/<table/,/<\/table>/p')

# Now select table[2] only
TABLE2=$(echo "$TABLES" \
    | awk '
        /<table/ { tbl_count++ }
        tbl_count == 2
        /<\/table>/ && tbl_count == 2 { exit }
    ')

echo "[DEBUG] Selected table[2] length: ${#TABLE2}"

###############################################################################
# 3. Extract its <tbody>
###############################################################################

TBODY=$(echo "$TABLE2" | sed -n '/<tbody/,/<\/tbody>/p')

echo "[DEBUG] TBODY length: ${#TBODY}"

if [ -z "$TBODY" ]; then
    echo "[ERROR] table[2] has no <tbody>. Dumping table:"
    echo "$TABLE2"
    exit 1
fi

###############################################################################
# 4. Extract links ONLY from first <td> of each <tr>
###############################################################################

LINKS=$(echo "$TBODY" \
    | awk '
        /<tr/ { in_tr=1; td_count=0 }
        /<\/tr/ { in_tr=0 }
        in_tr {
            if ($0 ~ /<td/) td_count++
            if (td_count==1 && $0 ~ /<a /) {
                match($0, /href="[^"]+"/)
                if (RSTART > 0) {
                    href=substr($0, RSTART+6, RLENGTH-7)
                    print href
                }
            }
        }
    ')

echo "[DEBUG] LINKS found:"
echo "$LINKS"

if [ -z "$LINKS" ]; then
    echo "[ERROR] No links extracted. Dumping TBODY:"
    echo "$TBODY"
    exit 1
fi

###############################################################################
# 5. Download mv-file-element images for each page
###############################################################################

for LINK in $LINKS; do
    FULL_URL="$BASE_URL$LINK"
    echo "[DEBUG] Visiting $FULL_URL"

    PAGE=$(curl -s "$FULL_URL")

    IMG_SRC=$(echo "$PAGE" \
        | grep -o '<img[^>]*class="[^"]*mv-file-element[^"]*"[^>]*>' \
        | sed -n 's/.*src="\([^"]*\)".*/\1/p' | head -n 1)

    echo "[DEBUG] IMG_SRC: $IMG_SRC"

    if [ -z "$IMG_SRC" ]; then
        echo "[WARN] No image on $FULL_URL"
        continue
    fi

    case "$IMG_SRC" in
        http*) IMG_URL="$IMG_SRC" ;;
        *) IMG_URL="$BASE_URL$IMG_SRC" ;;
    esac

    FILE=$(basename "$IMG_URL")

    echo "[DEBUG] Downloading to $OUTDIR/$FILE"
    curl -s -L "$IMG_URL" -o "$OUTDIR/$FILE"
done

echo "Done."