# https://www.kite.com/python/answers/how-to-traverse-a-directory-in-python
import os
import re

class WikilinkConverter:
  def __init__(self, start_path):
    #self.get_web_path = get_web_path
    self.start_path = start_path
    self.mapping = {} # Mapping of data to stuff
  
  def get_link_name(self, filename):
    if filename[-3:] == ".md":
      return filename[:-3]
    elif filename[-4:] == ".png":
      print(filename)
      return filename
    else:
      return None

  def get_web_path(self, directory,filename):
    linkname = self.get_link_name(filename)
    if linkname != None:
      return f"{directory[len(self.start_path):]}/{linkname}"
    else:
      return None
      
  def generate_mapping(self):
    self.mapping = {}
    
    path = os.walk(self.start_path)
    for root, directories, files in path:
      #print("###", root)
      for filename in files:
        #print(filename)
        linkname = self.get_link_name(filename)
        webpath = self.get_web_path(root,filename)
        if linkname != None:
          if self.mapping.get(linkname) == None:
            self.mapping[linkname] = []
          self.mapping[linkname].append(webpath)
          
          # Extra path
          other_path = f"{webpath}"
          if self.mapping.get(other_path) == None:
            self.mapping[other_path] = []
          self.mapping[other_path].append(webpath)  

  ### Replacing ########################################################
  def replace_wikilink(self, link):
    data = link[2:-2].split("|")
    link = name
    if len(data) == 1:
      link, name = data[0], data[0]
    elif len(data) >= 2:
      link, name = data
    
    #print(link, name, len(data))
    if self.mapping.get(link) == None or len(self.mapping[link]) == 0:
      return f"[{name}]({link})</a>"
      #return f"<a href='{link}'>{name}</a>"
    
    if len(self.mapping[link]) == 1:
      web_path = self.mapping[link][0]
      #return f"<a href='{web_path}'>{name}</a>"
      return f"[{name}]({web_path})</a>"
    
    ## Multiple wikilinks
    output = ""
    for i in range(len(self.mapping[link])):
      web_path = self.mapping[link][i]
      if i != 0: output += ","
      #output += f"<a href='{web_path}'>{i+1}</a>"
      output += f"[{i+1}]({web_path})</a>"
    return f"<span>[{name} - {output}]</span>"

  def replace_wikilink_image(self, link):
    data = link[3:-2].split("|")
    if len(data) == 1:
      link, name = data[0], data[0]
    elif len(data) == 2:
      link, name = data
    
    #print(link, name, len(data))
    if self.mapping.get(link) == None or len(self.mapping[link]) == 0:
      #return f"<img src=\"{link}\" alt=\"{name}\" >"
      return f"![{name}]({link})"
    ## Multiple wikilinks
    output = ""
    for i in range(len(self.mapping[link])):
      web_path = self.mapping[link][i]
      if i != 0: output += ","
      #output += f"<img src=\"{web_path}\" alt=\"{name}\" >"
      output += f"![{name}]({web_path})"
    print(link, output)
    return output
    
  def handle_images(self, text):
    wikilinks = re.findall("(!\[\[.+?\]\])",text)
    for wikilink in wikilinks:
      text = text.replace(wikilink, self.replace_wikilink_image(wikilink))
    return text
    
  def handle_text(self, text):
    wikilinks = re.findall("(\[\[.+?\]\])",text)
    for wikilink in wikilinks:
      text = text.replace(wikilink, self.replace_wikilink(wikilink))
    return text

def quick_handle_text(path, text):
  wkc = WikilinkConverter(path)
  wkc.generate_mapping()
  #print(wkc.mapping)
  return wkc.handle_text(wkc.handle_images(text))
  
if __name__ == "__main__":
  print(quick_handle_text("wiki", "README  [[README]] [[README|help]] [[TOD]] [[TODO]] ![[image.png]] ![[image-hslghgilu6we45v6nwrn5igc3mkn.png]]"))
