from lxml import etree
import re
import datetime
import os

tagmatch = r'<p>Tags:(.*)</p>'

def make_xml_tree(xmlstring: str):
    # because stupid bullshit, we have to chop off the xml declaration
    fixed_string = xmlstring.replace('<?xml version="1.0" encoding="utf-8"?>', '')
    root = etree.fromstring(fixed_string)
    return root

def get_components(xmltree):
    content = xmltree.find('params')[3] # always 3
    content_struct = content.getchildren()[0].getchildren()[0]
    members = content_struct.findall("member")
    post_title = ""
    post_body = ""
    for member in members:
        (n, v) = member.getchildren()
        if n.text == "title":
            post_title = v.getchildren()[0].text
        if n.text == "description":
            post_body = v.getchildren()[0].text
    return (post_title, post_body)


def get_tags(bodytext: str) -> str:
    """
    We can't have categories with micropub so!
    We'll look for the magic string:
    Tags:(.*)\n
    then we just chop off the Tags: bit and that's our tags.
    """
    found = re.findall(tagmatch, bodytext, re.I|re.M)
    if found:
        items = found[0].split(',')
        return ",".join([x.strip() for x in items])
    else:
        return ""
    
def fake_success() -> str:
    """
    I pretty much don't care about proper success. This is enough to fool MarsEdit.
    """
    return """
<?xml version="1.0"?>
<methodResponse>
   <params>
      <param>
         <value><string>POSTED</string></value>
      </param>
   </params>
</methodResponse>        
    """

def make_post(title, body, tags):
    body = re.sub(tagmatch, "", body, re.I|re.M)
    filename = title.replace(" ", "-") + ".md"
    now = datetime.datetime.now()
    post_date = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute)
    file_content = f"""Title: {title}
Date: {post_date}
Category: Recipes
Tags: {tags}
Slug: {title}
Authors: admin
Summary: {title}

{body}
    """
    if os.path.exists(os.path.join('content', filename)):
        print("That already exists. Try again.")
        exit()
    f = open(os.path.join('content', filename), 'w')
    f.write(file_content)
    f.close()
