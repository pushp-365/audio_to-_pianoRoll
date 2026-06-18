import json


with open(
    "outputs/tabs/lead_tabs.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)


tabs = data["tabs"]

string_changes = 0
same_note_changes = 0


for i in range(1, len(tabs)):

    prev = tabs[i-1]
    curr = tabs[i]

    if prev["string"] != curr["string"]:
        string_changes += 1


    if (
        prev["pitch"] == curr["pitch"]
        and prev["string"] != curr["string"]
    ):
        same_note_changes += 1


print("="*50)
print("🎸 LEAD TAB QUALITY REPORT")
print("="*50)

print(
    "Total notes:",
    len(tabs)
)

print(
    "Total string changes:",
    string_changes
)

print(
    "Same note string jumps:",
    same_note_changes
)


percentage = (
    same_note_changes /
    max(1, string_changes)
) * 100


print(
    f"Bad jumps percentage: {percentage:.2f}%"
)