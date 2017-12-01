import mosspy

userid = 223762299

m = mosspy.Moss(userid, "javascript")

# Submission Files
m.addFile("files/d3.js")
m.addFilesByWildcard("files/map.js")

url = m.send() # Submission Report URL

print ("Report Url: " + url)

# Save report file
m.saveWebPage(url, "report/report.html")

# Download whole report locally including code diff links
mosspy.download_report(url, "report/src/", connections=8)
