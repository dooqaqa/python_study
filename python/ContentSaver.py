import os;
from PIL import Image
import shutil

horizontal_dir_path = ".\\horizontal_pics"
vertical_dir_path = ".\\vertical_pics"

def GetSrcPath():
	home_path = os.path.expanduser('~')
	package_path = home_path + '\AppData\Local\Packages'
	src_path = ''
	
	filelist = os.listdir(package_path)
	for file in filelist:
		full_name = os.path.join(package_path,file);
		if os.path.isdir(full_name) and full_name.find("Microsoft.Windows.ContentDeliveryManager") >= 0:
			src_path = full_name + '\LocalState\Assets'
			break;
	return src_path

def GetFileNames(path):
	dict=[]
	filelist=os.listdir(path)
	for file in filelist:
		full_name=os.path.join(path,file);
		if not os.path.isdir(full_name):
			dict.append(file);
	return dict
	

def CheckAndCopyFiles(filelist, hdest_path, vdest_path):
	for file in filelist:
		img = Image.open(file[0])
		if img.size[0] >= img.size[1]:
			shutil.copyfile(file[0], hdest_path + '\\' + file[2] + '.' + img.format)
		else:
			shutil.copyfile(file[0], vdest_path + '\\' + file[2] + '.' + img.format)

def GetInitialFileList(path):
	ret = []
	filelist=os.listdir(path)
	for file in filelist:
		full_name=os.path.join(path,file);
		if os.path.isdir(full_name):
			continue
		ret.append([full_name, os.path.getsize(full_name), file])
	return ret

def LoseSmallOnes(file_list):
	if len(file_list)== 0:
		return []
	file_list.sort(key=lambda obj:obj[1], reverse=True)
	size_threshold = 0
	current_max_descend_ratio = 0
	prev = file_list[0]
	for file in file_list:
		if prev[1] / file[1] > current_max_descend_ratio:
			current_max_descend_ratio = prev[1] / file[1]
			size_threshold = file[1]
		prev = file
	file_list = filter(lambda obj: obj[1] > size_threshold, file_list)
	return file_list
	
def LoseDuplicatedOnes(file_list, old_file_list):
	if len(file_list)== 0:
		return 
	delete_list = []
	for file in file_list:
		for old_file in old_file_list:
			if file[2] in old_file:
				delete_list.append(file)
	file_list = filter(lambda obj: obj not in delete_list, file_list)
	return file_list



def main():
	if not os.path.exists(horizontal_dir_path):
		os.mkdir(horizontal_dir_path)
	if not os.path.exists(vertical_dir_path):
		os.mkdir(vertical_dir_path)
	old_files = GetFileNames(horizontal_dir_path)
	old_files.extend(GetFileNames(vertical_dir_path))
	src_path = GetSrcPath()
	src_files = GetInitialFileList(src_path)
	src_files = LoseSmallOnes(src_files)
	src_files = LoseDuplicatedOnes(src_files, old_files)
	CheckAndCopyFiles(src_files, horizontal_dir_path, vertical_dir_path)


if __name__ == '__main__':
	main();
