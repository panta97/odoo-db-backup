import re
import subprocess

bash_cmd = "fgrep -Ehn '^(COPY |SELECT )' dump.sql"
process = subprocess.Popen(bash_cmd, shell=True, stdout=subprocess.PIPE)
output, error = process.communicate()
if error:
    raise ("could'n run command")
output = output.decode("ascii")
lines = output.split("\n")
# remove last line element since its empty ''
lines = lines[:-1]
# data structure
ds_lines = []
tables_to_use = [
    "account_account_account_tag",
    "account_account",
    "account_invoice",
    "account_invoice_line",
    "account_journal",
    "res_partner",
    "wizard_multi_charts_accounts",
]
pattern = r"^(\d+):(COPY|SELECT)\s\w+\.(\w+)"
for line in lines:
    match = re.search(pattern, line)
    delete = True
    if match.group(2) == "COPY" and match.group(3) in tables_to_use:
        delete = False
    ds_lines.append(
        {
            "line_numb": int(match.group(1)),
            "ltype": match.group(2),
            "table": match.group(3),
            "delete": delete,
        }
    )

begin = 0
end = 0
del_ranges = []
for index, ds_line in enumerate(ds_lines):
    if ds_line["ltype"] == "COPY" and ds_line["delete"] and begin == 0:
        begin = ds_line["line_numb"]
    elif not ds_line["delete"]:
        end = ds_line["line_numb"] - 1
        del_ranges.append("{},{}d".format(begin, end))
        # reset begin
        begin = 0
    elif ds_lines[index - 1]["ltype"] == "COPY" and ds_line["ltype"] == "SELECT":
        end = ds_line["line_numb"] - 1
        # end = "$"
        del_ranges.append("{},{}d".format(begin, end))
        break
del_ranges = ";".join(del_ranges)

sed_cmd = "sed '{}' dump.sql > shrank-dump.sql".format(del_ranges)
process = subprocess.Popen(sed_cmd, shell=True, stdout=subprocess.PIPE)
output, error = process.communicate()

# print("D")
