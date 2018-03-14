def sort_sentence(transcription_path):
	lines = open(transcription_path,'r').readlines()
	sorted_ids = [line[:line.find(' ')] for line in lines]
	return sorted_ids
if __name__ == '__main__':
	ids = sort_sentence('E:\\IEMOCAP_full_release\\Session1\\dialog\\transcriptions\\Ses01F_impro01.txt')
	print(ids)