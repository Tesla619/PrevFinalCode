import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd
import zipfile
import shutil
import random

# Step 1: ADD images.zip and annotations.zip to customTF2
# Step 2: Enter Virtual Enviroemnt name
# Step 3: Enter the path for the python vm with tensorflow installed in anacondaPath
# Step 4: Run File

#user parameters
virtenv = "test"
anacondaPath  = "D:/anaconda3/envs/" + virtenv + "/python.exe"

def extract():  
  path_to_zip_file1 = "customTF2/images.zip"
  path_to_zip_file2 = "customTF2/annotations.zip"
  directory_to_extract_to = "customTF2/data"

  with zipfile.ZipFile(path_to_zip_file1, 'r') as zip_ref:
      zip_ref.extractall(directory_to_extract_to)
    
  with zipfile.ZipFile(path_to_zip_file2, 'r') as zip_ref:
      zip_ref.extractall(directory_to_extract_to)

def split():
    test_path = "customTF2/data/test_labels"
    train_path = "customTF2/data/train_labels"
  
    if not os.path.exists(test_path):    
        os.mkdir(test_path)
    
    if not os.path.exists(train_path):    
        os.mkdir(train_path)
    
    src_folder = r"customTF2/data/annotations"    
    dst_folder1 = r"customTF2/data/test_labels"
    dst_folder2 = r"customTF2/data/train_labels"

    pattern = "\*.xml"
    files = glob.glob(src_folder + pattern)
    
    totalDataSet = 0    
    for path in os.listdir(src_folder):
        if os.path.isfile(os.path.join(src_folder, path)):
            totalDataSet += 1
            
    randList =  random.sample(range(totalDataSet), totalDataSet)
  
    i = 0
    
    for file in files:
        
        if( i <= (totalDataSet * 0.2)):        
            file_name = os.path.basename(files[randList[i]])
            shutil.move(files[randList[i]], dst_folder1 + "/" + file_name)   
            print('Moved to test:', files[randList[i]])
            
        elif(i > (totalDataSet * 0.2)):
            file_name = os.path.basename(files[randList[i]])
            shutil.move(files[randList[i]], dst_folder2 + "/" + file_name)
            print('Moved to train:', files[randList[i]])
            
        i = i + 1

def xml_to_csv(path): #path -> customTF2/data/
  classes_names = []
  xml_list = []

  for xml_file in glob.glob(path + '/*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall('object'):
      classes_names.append(member[0].text)
      value = (root.find('filename').text  ,   
               int(root.find('size')[0].text),
               int(root.find('size')[1].text),
               member[0].text,
               int(member[4][0].text),
               int(member[4][1].text),
               int(member[4][2].text),
               int(member[4][3].text))
      xml_list.append(value)
      
  column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
  xml_df = pd.DataFrame(xml_list, columns=column_name) 
  classes_names = list(set(classes_names))
  classes_names.sort()
  return xml_df, classes_names

def main_xml_to_csv():
  for label_path in ['customTF2/data/train_labels', 'customTF2/data/test_labels']:
    image_path = os.path.join(os.getcwd(), label_path)
    xml_df, classes = xml_to_csv(label_path)
    xml_df.to_csv(f'{label_path}.csv', index=None)
    print(f'Successfully converted {label_path} xml to csv.')

  label_map_path = os.path.join("customTF2/data/label_map.pbtxt")
  pbtxt_content = ""

  for i, class_name in enumerate(classes):
      pbtxt_content = (
          pbtxt_content
          + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(i + 1, class_name)
      )
  pbtxt_content = pbtxt_content.strip()
  with open(label_map_path, "w") as f:
      f.write(pbtxt_content)
      print('Successfully created label_map.pbtxt ')

def genTF():    #not working with correct interpreter
    t1 = anacondaPath + " customTF2/tfrec.py customTF2/data/test_labels.csv  customTF2/data/label_map.pbtxt customTF2/data/images/ customTF2/data/test.record"
    t2 = anacondaPath + " customTF2/tfrec.py customTF2/data/train_labels.csv  customTF2/data/label_map.pbtxt customTF2/data/images/ customTF2/data/train.record"
    
    os.system(t1)
    os.system(t2)
    
def train():    
    training_dir = "customTF2/training"

    if not os.path.exists(training_dir):    
        os.mkdir(training_dir)
        
    train = anacondaPath + " models/research/object_detection/model_main_tf2.py --pipeline_config_path=customTF2/data/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.config --model_dir=customTF2/training --alsologtostderr"   
    os.system(train)
    
def test():
    test = anacondaPath + " models/research/object_detection/exporter_main_v2.py --trained_checkpoint_dir=customTF2/training --pipeline_config_path=customTF2/data/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.config --output_directory customTF2/data/inference_graph"    
    os.system(test)
    
def gen_files():
    extract()         
    split()
    main_xml_to_csv() 
    genTF()           
    
def model_and_export():
    train()
    test()
    print("\n\nDone.")
    
# gen_files()
model_and_export()
