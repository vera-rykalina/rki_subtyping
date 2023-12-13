import requests, time
import pandas as pd
import sys

# First request to get cookies
r = requests.get("https://comet.lih.lu/")
cookies = r.cookies

# Second request to upload the data and get the job ID
# First send the form data (which button was clicked, which checkboxes have been checked)

"""
 Postdata can be gotten by using print(r.text)
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
Get the url (https://comet.lih.lu/index.php?cat=hiv1) after manual upload of a fasta file. 
"""
# Then, post the request with postdata, file and cookies

infilename = sys.argv[1]
outfilename = sys.argv[2]

f = open(infilename, "r")
data=f.read()
f.close()

name1 = infilename.rsplit("/")[-1] # gives a file name.fasta
name2 = name1.split("_")[1] # gives a middle part after splitting by "_"
name3 = name1.rsplit(".")[-2] # gives a file name (cuts .fasta)
    
   
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


with open("comet_" + name3 + ".csv", "w") as f:
    f.write(r.text)

# Read .csv (it is separated by tab)
df = pd.read_csv("comet_" + name3 + ".csv", sep="\t")

# Rename some columns (as done for stanford df)
df. rename(columns = {"name":"SequenceName", "subtype": "Comet_" + name2 + "_Subtype"}, inplace = True)

 # Add to the "Comment" column bootstrap support info
df["Comet_" + name2 + "_Comment"] = df["bootstrap support"].astype(str)

# Delete undesired columns
df.drop(columns=["virus", "bootstrap support"], axis = 1,  inplace = True)

# Replace some patterns so they look Stanford-like (add CRF)
df["Comet_" + name2 + "_Subtype"] = df["Comet_" + name2 + "_Subtype"].replace(r"^(\w{2})_(\D)(\d?)(\w)(\w{0,1}?)(\d?)$", r"CRF\1_\2\4\5", regex=True)

df["Comet_" + name2 + "_Subtype"] = df["Comet_" + name2 + "_Subtype"].replace(r"^(\d{2,3})_(\w{2,4})$", r"CRF\1_\2", regex=True)

df["Comet_" + name2 + "_Subtype"] = df["Comet_" + name2 + "_Subtype"].replace(r"^(\d{2,3}_\w{2,4})(\s\(check for\s)(\d{2,4}_\w{2,4}\))$", r"CRF\1\2CRF\3", regex=True)

# Replace "unassigned_" group with "Unassigned"
df.loc[df["Comet_" + name2 + "_Subtype"].str.contains("unassigned"), "Comet_" + name2 + "_Subtype"] = "Unassigned"

# Replace "nan" with "0"
df["Comet_" + name2 + "_Comment"] = df["Comet_" + name2 + "_Comment"].replace("nan", "0")

# Sort df by SequenceName
df = df.sort_values(by=["SequenceName"])

# Prepare a clean .csv file
df.to_csv("comet_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")