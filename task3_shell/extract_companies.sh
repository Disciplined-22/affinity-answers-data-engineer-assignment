
# Block first : Block 1 starts the script with Bash, enables safer Bash behavior, 
# checks that exactly one argument was provided, stops with a usage message if not, 
# and stores the provided CSV URL in CSV_URL if everything is valid.

# Run this script using Bash.

#!/usr/bin/env bash

# set -euo pipefail
# -e       → stop when a command fails
# -u       → don't silently use undefined variables
# pipefail → detect failures inside pipelines

set -euo pipefail

# The number of command-line arguments supplied to the script.
# "Is the number of arguments NOT equal to 1?"
# the script requires exactly one argument.
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <CSV_URL>"
    exit 1 # Stop executing the script and return exit status 1.
fi

# Store the URL
CSV_URL="$1"

# ------------------------------------------------------------
# BLOCK 2: Download and process the CSV
# ------------------------------------------------------------

# curl downloads the CSV from the URL stored in CSV_URL.
#
# -s : silent mode
# -S : show errors even when silent mode is enabled
# -L : follow redirects
#
# The "|" sends the downloaded CSV directly to AWK
# instead of saving it to a temporary file.



# curl is being used to download the CSV data from the URL.
curl -sSL "$CSV_URL" | awk '

#  ------------------------------------------------------------
# AWK BLOCK 2A: Configure CSV field parsing
# ------------------------------------------------------------

BEGIN {

    # FPAT tells GNU AWK what a complete field looks like.
    #
    # It allows:
    # 1. A field containing characters other than commas
    # 2. A field enclosed in double quotes
    #
    # This allows commas inside quoted CSV fields to stay
    # inside the same field.

    FPAT = "([^,]+)|(\"[^\"]+\")"
}


NR > 1 {

    # For this CSV:
    # $2 = Company Name
    # $5 = Location
    # $8 = Founded

    name = $2
    location = $5
    founded_col = $8

    # Remove surrounding double quotes from the
    # company name and location.
    
    gsub(/^"|"$/, "", name)
    gsub(/^"|"$/, "", location)

    # Extract the first 4-digit year specifically from the Founded column ($8)
    # Start with an empty year.
    year = ""

    # Search the Founded column for the first
    # four-digit year beginning with 17, 18, 19, or 20.
    
    if (match(founded_col, /(17|18|19|20)[0-9]{2}/)) {
        year = substr(founded_col, RSTART, RLENGTH)
    }

    # Output the record only when:
    # 1. A valid year was found
    # 2. The company name is not empty

    if (year != "" && length(name) > 0) {
        
        # Output:
        # year + TAB + company name + TAB + location
        printf "%s\t%s\t%s\n", year, name, location
    }
}' | sort -n -k1,1 | awk -F'\t' '



# ------------------------------------------------------------
# BLOCK 4: Format the final output
# ------------------------------------------------------------

BEGIN {
    # BEGIN runs once before processing the input records.
    #
    # Print the table header.
    # %-15s = left-align a string in a 15-character space
    # %-35s = left-align a string in a 35-character space
    # %-30s = left-align a string in a 30-character space

    printf "%-15s | %-35s | %-30s\n", "FOUNDING YEAR", "COMPANY NAME", "LOCATION"

    # Print a separator line below the header.
    print "--------------------------------------------------------------------------------"
}


{

    # $1 = founding year
    # $2 = company name
    # $3 = location
    #
    # substr($2, 1, 35) = keep at most 35 characters of company name
    # substr($3, 1, 30) = keep at most 30 characters of location

    printf "%-15s | %-35s | %-30s\n", $1, substr($2, 1, 35), substr($3, 1, 30)
}'