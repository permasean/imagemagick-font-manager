from xml.etree import ElementTree
import os
import logging

class FontManager:
    def add_font(self, font_name, font_filepath, font_format='ttf') -> None:
        xml_paths = find_xml()

        if len(xml_paths) == 0:
           raise RuntimeError('There was an error adding font.')
        
        xml_path = xml_paths[0]
        etree = ElementTree.parse(xml_path)
        root = etree.getroot()
        typemap = etree.find('typemap') if root.tag != 'typemap' else root

        if typemap.tag != 'typemap':
           raise RuntimeError('Could not find typemap tag in XML')

        new_type = ElementTree.SubElement(typemap, 'type')
        new_type.set('format', font_format)
        new_type.set('name', font_name)
        new_type.set('glyphs', font_filepath)

        etree.write(xml_path)
        print("Successfully added font.")

def find_xml(xml_filename='type-ghostscript.xml', 
    top_directory='/opt/homebrew/Cellar/imagemagick') -> str:
    # currently only recognizes homebrew-installed imagemagick
    result = []
    for root, dir, files in os.walk(top_directory):
      if xml_filename in files:
         result.append(os.path.join(root, xml_filename))

    if len(result) == 0:
       msg = 'No font XML detected. Make sure that ImageMagick is installed'
    elif len(result) > 1:
       msg = 'Multiple XML files detected. Attempting with first result...'
    else:
       msg = 'XML successfully detected.'

    logging.debug(msg)
    return result

if __name__ == "__main__":
   font_manager = FontManager()
   font_manager.add_font('Montserrat ExtraBold', '/Users/seanphwang/Library/Fonts/Montserrat-ExtraBold.ttf')