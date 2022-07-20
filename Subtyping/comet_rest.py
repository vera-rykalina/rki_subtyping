import requests, time, glob2
import pandas as pd
import csv

# First request to get cookies
r = requests.get("https://comet.lih.lu/")
cookies = r.cookies

# Second request to upload the data and get the job ID
# First send the form data (which button was clicked, which checkboxes have been checked)

"""
You can get this postdata by using print(r.text)
<form action="index.php?cat=hiv1" method="post" enctype="multipart/form-data" style = "margin-left:20px;">
        <input name="fastafile" type="file" size="40"><p><input type="checkbox" name="non_commercial" value="confirmed">
        I confirm to use COMET only for non-commercial research purpose (*)</p><input style="color:#5d0524;font-weight:bolder"
        type="submit" name="submit" value="submit fasta file">
    </form>
"""

postdata = {
    "non_commercial": "confirmed",
    "submit": "submit fasta file"
}


"""
You can get this url (https://comet.lih.lu/index.php?cat=hiv1) after manual upload of 
a fasta file. 
"""
# Then, post the request with postdata, file and cookies

for file in glob2.glob("/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/*_PRRT_*.fasta"):
    with open(file, "r") as f:
        data = f.read()

print("Uploading FASTA file")
r = requests.post("https://comet.lih.lu/index.php?cat=hiv1",
                  data=postdata,
                  files={"fastafile": data},
                  cookies=cookies)

# Finally, parse the job ID out of the response
jobid = r.text.split("job=")[1].split("'")[0]
print("Successfully uploaded FASTA file, job ID:" + jobid)

# If the server does not manage to calculate the results within ~5 minuets, give up
waittime = 5
for i in range(0, 10):
    print("Trying to get results (attempt " + str(i+1) + "/10)")
    r = requests.get("https://comet.lih.lu/index.php?job=" + jobid + "&cat=hiv1")
    # Very important! Include a delay between every two requests, otherwise the server will be overloaded!
    # Also, every time increase the delay to give the server more time.
    if "csv.php?job=" in r.text:
        break
    waittime += 5*i
    print("...no results yet, waiting for " + str(waittime) + " seconds before next attempt")

r = requests.get("https://comet.lih.lu/csv.php?job=" + jobid, cookies=cookies)


with open("comet_prrt_raw.csv", "w") as f:
    f.write(r.text)

# Read raw .csv (it is separated by tab)
df = pd.read_csv("comet_prrt_raw.csv", sep="\t")

# Rename some columns (as done for stanford df)
df. rename(columns = {"name":"SequenceName", "subtype": "Subtype"}, inplace = True)

# Add to the "Comnent" column unnecessary info
df["Comment"] = df["virus"].astype(str) + " " + df["bootstrap support"].astype(str)
#df["Comment"] = df["Comment"].str.replace(" ", ",")

# Delete undesired columns
df.drop(columns=["virus", "bootstrap support"], axis = 1,  inplace = True)



# Prepare a clean .csv file
df.to_csv("comet_prrt.csv", sep=",", index=False, encoding="utf-8")



